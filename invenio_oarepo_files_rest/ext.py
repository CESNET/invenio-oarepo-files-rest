# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# OArepo Files REST is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for OArepo Files REST."""

from __future__ import absolute_import, print_function

import sys

from os.path import join

from invenio_files_rest.models import Location
from werkzeug.utils import cached_property

from invenio_oarepo_files_rest.buckets import create_bucket, get_bucket
from . import config


class _OarepoFilesState(object):
    """OArepo Files state."""

    def __init__(self, app):
        """Initialize state."""
        self.app = app

    @cached_property
    def default_location_uri(self):
        """ Default files location URI"""
        return self.app.config.get(
            'INVENIO_OAREPO_FILES_DEFAULT_LOCATION', join(sys.prefix, 'var/instance/data')
        )

    @cached_property
    def archive_location_uri(self):
        """ Archive files Location URI """
        return self.app.config.get(
            'INVENIO_OAREPO_FILES_ARCHIVE_LOCATION', join(sys.prefix, 'var/instance/archive')
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


class InvenioOArepoFilesREST(object):
    """OArepo Files REST extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['invenio-oarepo-files-rest'] = _OarepoFilesState(app)

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        for k in dir(config):
            if k.startswith('INVENIO_OAREPO_FILES_'):
                app.config.setdefault(k, getattr(config, k))
