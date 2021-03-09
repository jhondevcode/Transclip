"""Custom exceptions for every situation"""
# -*- coding: utf-8 -*-


class LangConfigurationsError(Exception):
    """This exception is shown when there are problems with the languages"""

    def __init__(self, *args, **kwargs):
        """Default constructor"""
        super(LangConfigurationsError, self).__init__(args, kwargs)
