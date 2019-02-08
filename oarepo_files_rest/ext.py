# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# OArepo Files REST is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for OArepo Files REST."""

from __future__ import absolute_import, print_function

from flask import current_app
from invenio_db import db
from invenio_files_rest.errors import FileSizeError
from invenio_files_rest.models import Location
from invenio_files_rest.utils import load_or_import_from_config
from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets
from werkzeug.utils import cached_property

from oarepo_files_rest.buckets import create_bucket, get_bucket
from oarepo_files_rest.objects import create_object_version
from . import config


class _OarepoFilesState(object):
    """OArepo Files state."""

    def __init__(self, app):
        """Initialize state."""
        self.app = app

    @cached_property
    def default_location_uri(self):
        """ Default files location URI"""
        return load_or_import_from_config(
            'OAREPO_FILES_DEFAULT_LOCATION', app=self.app
        )

    @cached_property
    def archive_location_uri(self):
        """ Archive files Location URI """
        return load_or_import_from_config(
            'OAREPO_FILES_ARCHIVE_LOCATION', app=self.app
        )

    @cached_property
    def locations(self):
        """ Available files locations """
        return Location.all()

    def get_or_create_bucket(self, location='', storage_class='S', **kwargs):
        """ Get Bucket by UUID or create a new one in a given location """
        if 'id' not in kwargs:
            if location == '':
                location = Location.query.filter_by(default=True).one()
            else:
                location = Location.query.filter_by(name=location).one()

            bucket_id = create_bucket(location, storage_class, **kwargs)
        else:
            bucket_id = kwargs['id']

        return get_bucket(bucket_id)

    def create_file(self, bucket_id, key, content_stream, content_length):
        """ Creates a File Object in a Bucket

            :raises FileSizeError
        """
        bucket = self.get_or_create_bucket(id=bucket_id)
        size_limit = bucket.size_limit
        if size_limit:
            if content_length > size_limit:
                desc = 'File size limit exceeded.' \
                    if isinstance(size_limit, int) else size_limit.reason
                raise FileSizeError(description=desc)

        bucket.locked = False

        create_object_version(bucket, key, content_stream, content_length)

        record = Record.create({})

        RecordsBuckets.create(record=record.model, bucket=bucket)

        record.files[key] = content_stream
        bucket.locked = True
        record.commit()
        db.session.commit()

        return record.id


class OArepoFilesREST(object):
    """OArepo Files REST extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['oarepo-files-rest'] = _OarepoFilesState(app)

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        for k in dir(config):
            if k.startswith('OAREPO_FILES_'):
                app.config.setdefault(k, getattr(config, k))
