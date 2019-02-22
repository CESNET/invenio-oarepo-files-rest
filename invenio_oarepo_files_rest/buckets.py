# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

""" OArepo files module Bucket methods """

from flask.cli import with_appcontext
from invenio_db import db
from invenio_files_rest.models import Bucket, Location
from uuid import UUID


@with_appcontext
def get_bucket(bucket_id: UUID) -> Bucket:
    """ Returns a bucket of a given UUID """
    return Bucket.query.get(bucket_id)


@with_appcontext
def create_bucket(location: Location, storage_class=None, **kwargs) -> Bucket:
    """ Creates a Bucket in a given Storage and Location """
    bucket = Bucket.create(location, storage_class, **kwargs)
    db.session.commit()
    return bucket.id
