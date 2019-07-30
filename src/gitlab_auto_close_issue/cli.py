# -*- coding: utf-8 -*-
r"""

Example:
    ::

        $ pip install -e .

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""

import click


@click.command()
def cli():
    """Python script which will automatically close issues on GitLab for you.."""
    pass
