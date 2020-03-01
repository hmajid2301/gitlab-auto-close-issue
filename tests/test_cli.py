import os

import gitlab
import pytest

from gitlab_auto_close_issue.cli import cli


@pytest.mark.parametrize(
    "args, exit_code",
    [
        ([], 2),
        (["--private-token", "ATOKEN1234", "--project-id", 213145], 2),
        (
            [
                "--private-token",
                "ATOKEN1234",
                "--project-id",
                213145,
                "--gitlab-url",
                "gitlab.com/hmajid2301/gitlab-auto-mr",
            ],
            2,
        ),
        (
            [
                "--private-token",
                "ATOKEN1234",
                "--project-id",
                213145,
                "--gitlab-url",
                "gitlab.com/hmajid2301/gitlab-auto-mr",
                "--remove-label",
                "Doing",
            ],
            2,
        ),
        (
            [
                "--private-token",
                "ATOKEN1234",
                "--project-id",
                213145,
                "--gitlab-url",
                "gitlab.com/hmajid2301/gitlab-auto-mr",
                "--issue",
                "83",
                "--remove-label",
                "Doing",
            ],
            1,
        ),
    ],
)
def test_fail_args(runner, args, exit_code):
    result = runner.invoke(cli, args)
    assert result.exit_code == exit_code


def test_fail_invalid_project(mocker, runner):
    args = [
        "--private-token",
        "ATOKEN1234",
        "--project-id",
        213145,
        "--gitlab-url",
        "https://gitlab.com/hmajid2301/gitlab-auto-mr",
        "--issue",
        "83",
        "--remove-label",
        "Doing",
    ]
    mocker.patch("gitlab.v4.objects.ProjectManager.get", side_effect=gitlab.exceptions.GitlabGetError)
    result = runner.invoke(cli, args)
    assert result.exit_code == 1


def test_fail_invalid_private_token(runner):
    args = [
        "--private-token",
        "ATOKEN1234",
        "--project-id",
        213145,
        "--gitlab-url",
        "https://gitlab.com",
        "--issue",
        "83",
        "--remove-label",
        "Doing",
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 1


def test_pass_invalid_issue_number(mocker, runner):
    args = [
        "--private-token",
        "_hrEy",
        "--project-id",
        8593636,
        "--gitlab-url",
        "https://gitlab.com",
        "--issue",
        "8593636",
        "--remove-label",
        "Doing",
    ]
    mock = mocker.patch("gitlab.v4.objects.ProjectManager.get")
    mock.return_value.issues.get.side_effect = gitlab.exceptions.GitlabGetError
    result = runner.invoke(cli, args)
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "args",
    [
        (
            [
                "--private-token",
                "ATOKEN1234",
                "--project-id",
                213145,
                "--gitlab-url",
                "gitlab.com/hmajid2301/gitlab-auto-mr",
                "--issue",
                "83",
                "--remove-label",
                "Doing",
            ]
        ),
        (
            [
                "--private-token",
                "ATOKEN1234",
                "--project-id",
                213145,
                "--gitlab-url",
                "gitlab.com/hmajid2301/gitlab-auto-mr",
                "--issue",
                "830",
                "--issue",
                "831",
            ]
        ),
        (
            [
                "--private-token",
                "ATOKEN1234",
                "--project-id",
                213145,
                "--gitlab-url",
                "gitlab.com/hmajid2301/gitlab-auto-mr",
                "-i",
                "830",
                "-i",
                "831",
                "-r",
                "Doing",
            ]
        ),
    ],
)
def test_success(mocker, runner, args):
    mocker.patch("gitlab.Gitlab")
    mocker.patch("gitlab.Gitlab.projects.get")
    result = runner.invoke(cli, args)
    assert result.exit_code == 0


def test_envvars(mocker, runner):
    args = ["--issue", "830", "--issue", "831", "--remove-label", "doing"]
    os.environ["GITLAB_PRIVATE_TOKEN"] = "NOTATOKEN"
    os.environ["CI_PROJECT_ID"] = "81236"
    os.environ["CI_PROJECT_URL"] = "https://gitlab.com/hmajid2301/gitlab-auto-mr"

    mocker.patch("gitlab.Gitlab")
    mocker.patch("gitlab.Gitlab.projects.get")
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
