"""
CourseSettingsEncoder
"""


import datetime
import json
from json.encoder import JSONEncoder

from opaque_keys.edx.locations import Location

from openedx.core.djangoapps.models.course_details import CourseDetails
from xmodule.fields import Date, Timedelta

from .course_grading import CourseGradingModel


class CourseSettingsEncoder(json.JSONEncoder):
    """
    Serialize CourseDetails, CourseGradingModel, datetime, and old
    Locations
    """
    def default(self, obj):  # pylint: disable=method-hidden
        if isinstance(obj, (CourseDetails, CourseGradingModel)):
            return obj.__dict__
        elif isinstance(obj, Location):
            return obj.dict()
        elif isinstance(obj, datetime.datetime):
            return Date().to_json(obj)
        elif isinstance(obj, datetime.timedelta):
            return Timedelta().to_json(obj).split()[0]
        else:
            return JSONEncoder.default(self, obj)
