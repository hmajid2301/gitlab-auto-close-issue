.. image:: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/badges/master/pipeline.svg
   :target: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue
   :alt: Pipeline Status

.. image:: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/badges/master/coverage.svg
   :target: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue
   :alt: Coverage

.. image:: https://img.shields.io/pypi/l/gitlab-auto-close-issue.svg
   :target: https://pypi.org/project/gitlab-auto-close-issue/
   :alt: PyPI Project License

.. image:: https://img.shields.io/pypi/v/gitlab-auto-close-issue.svg
   :target: https://pypi.org/project/gitlab-auto-close-issue/
   :alt: PyPI Project Version

gitlab-auto-close-issue
=======================

This is a simple Python cli script that allows you close issues on GitLab automatically. It is intended to be
used during your CI/CD. However you can chose to use it however you wish.

Usage
-----

First you need to create a personal access token, `more information here
<https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_. With the scope ``api``, so it can close the issue for you.

.. code-block:: bash

  pip install gitlab-auto-close-issue
  gitlab_auto_close_issue --help

  Usage: gitlab_auto_close_issue [OPTIONS]

    GitLab Auto Close Issue

  Options:
    --private-token TEXT     Private GITLAB token, used to authenticate when
                            calling the auto issue close API.  [required]
    --project-id INTEGER     The project ID on GitLab to create the auto close API for.
                            [required]
    --gitlab-url TEXT       The GitLab URL.
                            [required]
    -i, --issue TEXT         The Issue ID to close.  [required]
    -r, --remove-label TEXT  The labels to remove from (all) the issue(s) before
                            closing it.
    --help                   Show this message and exit.

.. code-block:: bash

    $ gitlab_auto_close_issue --private-token xxx  --project-url https://gitlab.com/hmajid2301/test \
      --project-id 14416075 --issue 1 --remove-label bug

GitLab CI
*********

Set a secret variable in your GitLab project with your private token. Name it ``GITLAB_PRIVATE_TOKEN`` (``CI/CD > Environment Variables``).
This is necessary to close the issue on your behalf.
More information `click here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
This access token is passed to the script with the ``--private-token`` argument.
An example CI using this can be found
`here <https://gitlab.com/hmajid2301/stegappasaurus/blob/a22b7dc80f86b471d8a2eaa7b7eadb7b492c53c7/.gitlab-ci.yml>`_,
look for the ``close:issue`` job.

Add the following to your ``.gitlab-ci.yml`` file:

.. code-block:: yaml

  stages:
    - post

  close:issue:
    image: registry.gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue
    stage: post
    before_script: []
    script:
      - gitlab_auto_close_issue --issue 1 --remove-label "Doing" --remove-label "To Do"

Predefined Variables
^^^^^^^^^^^^^^^^^^^^

Please note some of the arguments can be filled in using environment variables defined during GitLab CI.
For more information `click here <https://docs.gitlab.com/ee/ci/variables/predefined_variables.html>_`.

* If ``--private-token`` is not set the script will look for the ENV variable ``GITLAB_PRIVATE_TOKEN``
* If ``--project-id`` is not set it will look for for the ENV variable ``CI_PROJECT_ID``
* If ``--gitlab-url`` is not set it will look for for the ENV variable ``CI_PROJECT_URL``


Setup Development Environment
==============================

.. code-block:: bash

  git clone git@gitlab.com:gitlab-automation-toolkit/gitlab-auto-close-issue.git
  cd gitlab-auto-close-issue
  pip install tox
  make install-venv
  source .venv/bin/activate
  make install-dev


Changelog
=========

You can find the `changelog here <https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/blob/master/CHANGELOG.md>`_.