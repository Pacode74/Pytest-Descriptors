# # test_performance.py
# import pytest
# from descriptor_application_part_1.apps.resources import Resources
# from time import sleep
#
# from descriptor_application_part_1.apps.track_performance_decorator import (
#     track_performance_decorator,
# )
#
#
# @pytest.mark.performance
# @track_performance_decorator
# def test_performance():
#     """1) mark it with performance marker that is registered in pytest.ini.
#     2) decorate it track_performance_decorator"""
#     # sleep(3)
#     Resources("Intel-core", "Intel")
