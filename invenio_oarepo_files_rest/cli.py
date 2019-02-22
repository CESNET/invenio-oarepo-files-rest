# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

""" OArepo files CLI commands """
import os

import click
from flask.cli import with_appcontext

from invenio_oarepo_files_rest.proxies import current_oarepo_files
from invenio_oarepo_files_rest.locations import init_locations
from invenio_db import db


@click.group()
def files():
    """OARepo File management commands."""


@files.command('createbucket')
@with_appcontext
@click.option('--location', '-l', type=click.STRING, default='default')
@click.option('--storage', '-s', type=click.STRING)
@click.option('--quota', '-q', type=click.INT)
@click.option('--filesize', '-f', type=click.INT)
@click.option('--locked', '-x', is_flag=True, default=False)
def create_bucket_cli(location, storage, quota, filesize, locked):
    kwargs = {
        'quota_size': quota,
        'max_file_size': filesize,
        'locked': locked
    }

    bucket_id = current_oarepo_files.get_or_create_bucket(location, **kwargs, storage_class=storage)
    click.secho('Created bucket: {0}'.format(bucket_id), fg='green')


@files.command('initlocations')
@with_appcontext
def init_locations_cli():
    """ Initialize invenio-files-rest bucket locations."""
    init_locations()


@files.command('relocate')
@with_appcontext
@click.option('--old_location')
@click.argument('new_location')
def relocate(old_location, new_location):
    if new_location[-1] != '/':
        new_location += '/'
    if new_location[0] != '/':
        raise AttributeError('Please use absolute file path in new_location')

    if not old_location:
        result = db.session.execute(r"""
            select uri from files_location
        """)
        locations = [x[0] for x in result.fetchall()]
        old_location = os.path.commonprefix(locations)
        click.secho('Using the following prefix for old data: ', nl=False)
        click.secho(old_location, fg='green')
        if click.prompt('Is it correct (y/N)') != 'y':
            click.secho('Cancelled.')
            return

    if old_location[-1] != '/':
        old_location += '/'
    if old_location[0] != '/':
        raise AttributeError('Please use absolute file path in old location')

    click.echo('Replacements:')
    result = db.session.execute(r"""
        select uri, regexp_replace(uri, '^' || :old_location, :new_location) from files_location
        where uri like (:old_location || '%')
    """, dict(old_location=old_location, new_location=new_location))
    for r in result.fetchall():
        click.secho('    ' + r[0], fg='green', nl=False)
        click.secho(' -> ', nl=False)
        click.secho(r[1], fg='yellow')

    if click.prompt('Proceed? (y/N)') != 'y':
        click.secho('Cancelled.')
        return

    db.session.execute(r"""
        update files_location set uri=regexp_replace(uri, '^' || :old_location, :new_location)
        where uri like (:old_location || '%')
    """, dict(old_location=old_location, new_location=new_location))

    db.session.execute(r"""
        update files_files set uri=regexp_replace(uri, '^' || :old_location, :new_location)
        where uri like (:old_location || '%')
    """, dict(old_location=old_location, new_location=new_location))

    click.echo('\n\nNew locations:')
    result = db.session.execute(r"""
        select uri from files_location
    """)
    for r in result.fetchall():
        click.secho('    ' + r[0], fg='green')

    db.session.commit()
