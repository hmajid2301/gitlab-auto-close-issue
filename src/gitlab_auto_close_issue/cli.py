# -*- coding: utf-8 -*-
r"""This script uses the GitLab API to automatically close issues on GitLab on your behalf. The script can also
remove labels from the issues (such as "doing" or "to do"). The script also removes the due date and assignee
from it.

Example:
    ::

        $ pip install -e .
        $ gitlab_auto_close_issue --private-token xxx  --project-url https://gitlab.com/hmajid2301/test --project-id 14416075 --issue 1 --remove-label bug

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""

import os
import re
import sys

import click
import gitlab


@click.command()
@click.option(
    "--private-token",
    envvar="GITLAB_PRIVATE_TOKEN",
    required=True,
    help="Private GITLAB token, used to authenticate when calling the auto close API.",
)
@click.option(
    "--project-id",
    envvar="CI_PROJECT_ID",
    required=True,
    type=int,
    help="The project ID on GitLab to create the auto close for.",
)
@click.option("--gitlab-url", envvar="CI_PROJECT_URL", required=True, help="The GitLab URL.")
@click.option("--issue", "-i", multiple=True, required=True, help="The ID of the issue to close.")
@click.option(
    "--remove-label", "-r", multiple=True, help="The labels to remove from (all) the issue(s) before closing it."
)
def cli(private_token, project_id, gitlab_url, issue, remove_label):
    """Gitlab Auto Close Issue"""
    if "CI_PROJECT_URL" in os.environ and gitlab_url == os.environ["CI_PROJECT_URL"]:
        gitlab_url = re.search("^https?://[^/]+", gitlab_url).group(0)

    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
    try:
        project = gl.projects.get(project_id)
    except gitlab.exceptions.GitlabAuthenticationError:
        print(f"Unable to get project {project_id}. Unauthorised access, check your access token is valid.")
        sys.exit(1)
    except gitlab.exceptions.GitlabGetError:
        print(f"Unable to get project {project_id}.")
        sys.exit(1)

    for issue_id in issue:
        try:
            issue = project.issues.get(issue_id)
        except gitlab.exceptions.GitlabGetError:
            print(f"The issue with id {issue_id} doesn't exist.")
            continue

        issue.labels = list(set(issue.labels) - set(remove_label))
        issue.state_event = "close"
        issue.assignee_ids = 0
        issue.due_date = None
        issue.save()
        print(f"Issue with id {issue_id} has been closed.")
