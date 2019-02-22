## -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxy definitions."""

from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.local import LocalProxy

from invenio_oarepo_files_rest.ext import _OarepoFilesState

current_oarepo_files: _OarepoFilesState = LocalProxy(
    lambda: current_app.extensions['invenio-oarepo-files-rest'])
"""Helper proxy to access oarepo files state object."""

__all__ = ('current_oarepo_files',)
