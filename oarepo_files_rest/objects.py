# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

""" OArepo files module Object methods """

from flask.cli import with_appcontext
from invenio_db import db
from invenio_files_rest.models import Bucket, ObjectVersion

@with_appcontext
def create_object_version(bucket: Bucket, key, content_stream, content_length) -> ObjectVersion:
    with db.session.begin_nested():
        obj = ObjectVersion.create(bucket, key)
        obj.set_contents(stream=content_stream, size=content_length, size_limit=bucket.size_limit)

    db.session.commit()
    return obj
