# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# OArepo Files REST is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""REST API for uploading/downloading files for OArepo."""

from __future__ import absolute_import, print_function

from .ext import InvenioOArepoFilesREST
from .version import __version__
from .proxies import current_oarepo_files

__all__ = ('__version__', 'InvenioOArepoFilesREST', 'current_oarepo_files')
