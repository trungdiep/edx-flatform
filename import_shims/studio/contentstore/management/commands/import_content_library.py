"""Deprecated import support. Auto-generated by import_shims/generate_shims.sh."""
# pylint: disable=redefined-builtin,wrong-import-position,wildcard-import,useless-suppression,line-too-long

from import_shims.warn import warn_deprecated_import

warn_deprecated_import('contentstore.management.commands.import_content_library', 'cms.djangoapps.contentstore.management.commands.import_content_library')

from cms.djangoapps.contentstore.management.commands.import_content_library import *