# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- unit tests with 100% code coverage.
- `dev-requirements.txt` for development requirements such as black.
- `isort` to sort imports.
- `coverage` to detect code coverage from unit tests.
- `coverage` job in `.gitlab-ci.yml`.

### Changed
- `makefile` to `Makefile`.
- `MANIFEST.in` with recommended changes from `check-manifest`.
- `README.rst` added a coverage badge.
- `code-formatter` name in `tox.ini` to.
- `docker` publish job to pre-publish only on release tags.

### Removed
- `docs` folder.

## [1.0.0] - 2019-10-21
### Changed
- Removed all references of MRs/Release from the docs and replaced with auto close.

## [0.1.0] - 2019-09-20
### Added
- Initial Release

[Unreleased]: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/-/compare/release%2F1.0.0...master
[1.0.0]: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/-/compare/release%2F0.1.0...release%2F1.0.0
[0.1.0]: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/-/tags/release%2F0.1.0