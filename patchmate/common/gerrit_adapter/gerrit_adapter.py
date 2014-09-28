#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from ..logger import logger


class GerritAdapter(object):
    """
    Class for executing unnecessary gerrit operations via Rest API
    """
    def __init__(self, url, username, password, requests_auth=requests.auth.HTTPDigestAuth):
        """
        Constructor

        :param url: Gerrit url
        :type url: str

        :param username: Gerrit login
        :type username: str

        :param password: Gerrit password
        :type password: str

        :param requests_auth: One of possible requests http authentication class (default: requests.auth.HTTPDigestAuth)
        :type requests_auth: requests.auth.AuthBase
        """
        self.username = username
        self.password = password
        self.auth = requests_auth(username, password)
        self.url = url.rstrip('/')
        self.session = requests.session()

    def add_reviewer(self, change_id, user_unique_name):
        """
        Adds given reviewer to gerrit change determining by given change_id and logs information about request.

        :param change_id: Gerrit change hash
        :type change_id: str

        :param user_unique_name: String identifying gerrit user (e.g username or email address)
        :type user_unique_name: str
        """
        add_reviewer_json = json.dumps({"reviewer": user_unique_name})
        url = self._make_url("/a/changes/{}/reviewers/".format(change_id))
        response = self.session.post(url, data=add_reviewer_json, auth=self.auth, headers={'content-type': 'application/json'})
        self._check_status_code(response)

    def get_reviewers_from_change_by_info(self, change_id, code_review=None):
        url = self._make_url("/a/changes/{}/reviewers/".format(change_id))
        response = self.session.get(url, auth=self.auth, headers={'content-type': 'application/json'})
        self._check_status_code(response)
        response_json = self._get_json(response)
        reviewers_meet_conditions = self._get_reviewers_meet_conditions(response_json, code_review)
        return reviewers_meet_conditions

    def _get_reviewers_meet_conditions(self, reviewers_json_list, code_review):
        return [reviewer_dict for reviewer_dict in reviewers_json_list if self._meet_reviewer_conditions(reviewer_dict, code_review)]

    def _meet_reviewer_conditions(self, reviewer_dict, code_review):
        return code_review is None or int(reviewer_dict['approvals']['Code-Review']) >= int(code_review)

    def _get_json(self, response, json_prefix=")]}'"):
        text = response.text[len(json_prefix):] if response.text.startswith(json_prefix) else response.text
        return json.loads(text) if isinstance(text, (unicode, str)) else json.load(text)

    def _make_url(self, endpoint):
        return "{}{}".format(self.url, endpoint)

    def _check_status_code(self, response):
        if response.status_code == 200:
            logger.info("{}: {}".format(response.status_code, response.text))
        elif response.status_code == 422:
            logger.warning("{}: {}".format(response.status_code, response.text))
        else:
            logger.warning("{}: {}".format(response.status_code, response.text))
