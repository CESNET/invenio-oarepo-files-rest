# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

""" OArepo files module for invenio-files-rest """

from flask.cli import with_appcontext
from os.path import exists

from os import makedirs

from invenio_db import db
from invenio_files_rest.models import Location

from invenio_oarepo_files_rest import current_oarepo_files


@with_appcontext
def init_locations():
    """ Create invenio-files-rest Bucket Locations."""
    try:
        locations = [
            ('default', True, current_oarepo_files.default_location_uri),
            ('archive', False, current_oarepo_files.archive_location_uri)
        ]
        created = []
        session = db.session
        for name, default, uri in locations:
            if uri.startswith('/') and not exists(uri):
                makedirs(uri)
            if not Location.query.filter_by(name=name).count():
                loc = Location(name=name, uri=uri, default=default)
                session.add(loc)
                created.append(loc)
        session.commit()
        return created
    except Exception:
        db.session.rollback()
        raise
