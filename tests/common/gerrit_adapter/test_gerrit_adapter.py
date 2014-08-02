#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
import requests
from mock import patch, MagicMock
from patchmate.common.gerrit_adapter import GerritAdapter


@patch("patchmate.common.gerrit_adapter.gerrit_adapter.logger")
class TestGerritAdapter(unittest.TestCase):
    def setUp(self):
        self.login = "login"
        self.password = "password"
        self.url = "http://url_to_gerrit.com/"
        self.headers = {'content-type': 'application/json'}
        self.gerrit_adapter = GerritAdapter(self.url, self.login, self.password)

    def _make_url_schema(self, type):
        switch = {"review": "/a/changes/{}/reviewers/"}
        return switch.get(type)

    def test_if_all_parameters_were_set_correctly(self, logger_mock):
        self.assertEqual(self.gerrit_adapter.username, self.login)
        self.assertEqual(self.gerrit_adapter.password, self.password)
        self.assertEqual(self.gerrit_adapter.url, self.url[:-1])
        self.assertIsInstance(self.gerrit_adapter.auth, requests.auth.AuthBase)
        self.assertIsInstance(self.gerrit_adapter.session, requests.Session)

    def test_if_user_can_inject_own_authentication_class(self, logger_mock):
        auth = MagicMock()
        self.gerrit_adapter = GerritAdapter(self.url, self.login, self.password, auth)
        self.assertIsInstance(self.gerrit_adapter.auth, MagicMock)

    def test_if_add_reviewer_doesnt_log_warning_message_when_method_add_reviewer_adds_reviewer_to_gerrit_with_200_status_code(self, logger_mock):
        reviewer = "reviewer@review.com"
        reviewer_json = json.dumps({"reviewer": reviewer})
        change_id = "change_id_#"
        url = "{}{}".format(self.url[:-1], self._make_url_schema("review").format(change_id))
        response_mock = MagicMock(status_code=200)
        self.gerrit_adapter.session.post = MagicMock(return_value=response_mock)
        self.gerrit_adapter.add_reviewer(change_id, reviewer)
        self.gerrit_adapter.session.post.assert_called_once_with(url, data=reviewer_json, auth=self.gerrit_adapter.auth, headers=self.headers)
        self.assertFalse(logger_mock.warning.called)
        self.assertTrue(logger_mock.info.called)

    def test_add_reviewer_logs_warning_message_when_method_add_reviewer_doesnt_add_reviewer_to_gerrit_with_recognized_status_code(self, logger_mock):
        reviewer = "reviewer@review.com"
        reviewer_json = json.dumps({"reviewer": reviewer})
        change_id = "change_id_#"
        url = "{}{}".format(self.url[:-1], self._make_url_schema("review").format(change_id))
        response_mock = MagicMock(status_code=422)
        self.gerrit_adapter.session.post = MagicMock(return_value=response_mock)
        self.gerrit_adapter.add_reviewer(change_id, reviewer)
        self.gerrit_adapter.session.post.assert_called_once_with(url, data=reviewer_json, auth=self.gerrit_adapter.auth, headers=self.headers)
        self.assertFalse(logger_mock.info.called)

    def test_add_reviewer_logs_error_message_when_add_reviewer_doesnt_add_reviewer_to_gerrit_and_returns_unrecognized_status_code(self, logger_mock):
        reviewer = "reviewer@review.com"
        reviewer_json = json.dumps({"reviewer": reviewer})
        change_id = "change_id_#"
        url = "{}{}".format(self.url[:-1], self._make_url_schema("review").format(change_id))
        response_mock = MagicMock(status_code=100000)
        self.gerrit_adapter.session.post = MagicMock(return_value=response_mock)
        self.gerrit_adapter.add_reviewer(change_id, reviewer)
        self.gerrit_adapter.session.post.assert_called_once_with(url, data=reviewer_json, auth=self.gerrit_adapter.auth, headers=self.headers)
        self.assertFalse(logger_mock.info.called)


if __name__ == "__main__":
    unittest.main()