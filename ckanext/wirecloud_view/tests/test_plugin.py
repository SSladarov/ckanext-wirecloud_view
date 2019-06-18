# -*- coding: utf-8 -*-

# Copyright (c) 2017 Future Internet Consulting and Development Solutions S.L.

# This file is part of CKAN WireCloud View Extension.

# CKAN WireCloud View Extension is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CKAN WireCloud View Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with CKAN WireCloud View Extension. If not, see <http://www.gnu.org/licenses/>.
# This file is part of CKAN Data Requests Extension.

import unittest

from ckan.plugins import toolkit as tk
from mock import MagicMock, patch
from parameterized import parameterized
import six

from ckanext.wirecloud_view import plugin


class WirecloudViewPluginTest(unittest.TestCase):

    def setUp(self):
        self.WirecloudView = plugin.WirecloudView()

    def test_process_dashboardid_resource_should_strip(self):

        self.assertEqual(plugin.process_dashboardid_resource("  owner/name ", {}), "owner/name")

    def test_process_dashboardid_resource_should_leave_untouched_valid_dashboard_ids(self):

        self.assertEqual(plugin.process_dashboardid_resource("owner/name", {}), "owner/name")

    def test_process_dashboardid_resource_should_raise_invalid_exception(self):

        with self.assertRaises(tk.Invalid):
            plugin.process_dashboardid_resource("a/b/c", {})

    def test_process_dashboardid_dataset_should_strip(self):

        self.assertEqual(plugin.process_dashboardid_dataset("  owner/name ", {}), "owner/name")

    def test_process_dashboardid_dataset_should_leave_untouched_valid_dashboard_ids(self):

        self.assertEqual(plugin.process_dashboardid_dataset("owner/name", {}), "owner/name")

    def test_process_dashboardid_dataset_should_raise_invalid_exception(self):

        with self.assertRaises(tk.Invalid):
            plugin.process_dashboardid_dataset("a/b/c", {})

    def test_can_view_returns_false(self):
        instance = plugin.WirecloudView()
        self.assertFalse(instance.can_view({}))

    def test_get_helpers(self):
        instance = plugin.WirecloudView()
        helpers = instance.get_helpers()

        for key, helper in six.iteritems(helpers):
            self.assertTrue(callable(helper))

    def test_info_returns_dict(self):
        instance = plugin.WirecloudView()
        self.assertTrue(isinstance(instance.info(), dict))

    def test_form_template(self):
        instance = plugin.WirecloudView()
        self.assertEqual(instance.form_template(None, None), "wirecloud_form.html")

    def test_view_template(self):
        instance = plugin.WirecloudView()
        self.assertEqual(instance.view_template(None, None), "wirecloud_view.html")

    #Schemas Dataset

    def _check_fields(self, schema, fields):
        for field in fields:
            for checker_validator in fields[field]:
                self.assertTrue(checker_validator in schema[field])
            self.assertEquals(len(fields[field]), len(schema[field]))

    @parameterized.expand([
        ('create_package_schema'),
        ('update_package_schema'),
    ])
    def test_schema_create_update(self, function_name):

        function = getattr(self.WirecloudView, function_name)
        returned_schema = function()

        fields = {
            'dashboard': [plugin.process_dashboardid_dataset,
                          tk.get_validator('ignore_missing'),
                          tk.get_converter('convert_to_extras')]
        }

        self._check_fields(returned_schema, fields)

    def test_schema_show(self):

        returned_schema = self.WirecloudView.show_package_schema()

        fields = {
            'dashboard': [tk.get_converter('convert_from_extras'),
                          tk.get_validator('ignore_missing')]
        }

        self._check_fields(returned_schema, fields)

    def test_fallback(self):
        self.assertEquals(True, self.WirecloudView.is_fallback())

    def test_package_types(self):
        self.assertEquals([], self.WirecloudView.package_types())
