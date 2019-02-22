# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# OArepo Files REST is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""
import sys

from os.path import join

INVENIO_OAREPO_FILES_DEFAULT_LOCATION = join(sys.prefix, 'var/instance/data')
""" Where Invenio should store its file data by default """

INVENIO_OAREPO_FILES_ARCHIVE_LOCATION = join(sys.prefix, 'var/instance/archive')
""" Where Invenio should store archived file data """
