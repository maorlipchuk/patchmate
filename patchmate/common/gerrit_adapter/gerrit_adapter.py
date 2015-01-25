#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from patchmate.common.logger import logger


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
        return GerritAdapter._check_status_code(response)

    def get_reviewers_from_change_by_info(self, change_id, code_review_grade=None):
        """
        Gets reviewers from change
        :param change_id: Change in gerrit
        :param code_review_grade: Minimum acceptance criteria of code review grade
        :return: List of reviewers who meet conditions
        """
        url = self._make_url("/a/changes/{}/reviewers/".format(change_id))
        response = self.session.get(url, auth=self.auth, headers={'content-type': 'application/json'})
        GerritAdapter._check_status_code(response)
        response_json = GerritAdapter._get_json(response)
        reviewers_meet_conditions = GerritAdapter._get_reviewers_meet_conditions(response_json, code_review_grade)
        return reviewers_meet_conditions

    def _make_url(self, endpoint):
        return "{}{}".format(self.url, endpoint)

    @staticmethod
    def _get_reviewers_meet_conditions(reviewers_json_list, code_review):
        return [reviewer_dict for reviewer_dict in reviewers_json_list if GerritAdapter._meet_reviewer_conditions(reviewer_dict, code_review)]

    @staticmethod
    def _meet_reviewer_conditions(reviewer_dict, code_review_grade):
        return code_review_grade is None or int(reviewer_dict['approvals']['Code-Review']) >= int(code_review_grade)

    @staticmethod
    def _get_json(response, json_prefix=")]}'"):
        text = response.text[len(json_prefix):] if response.text.startswith(json_prefix) else response.text
        return json.loads(text) if isinstance(text, (unicode, str)) else json.load(text)

    @staticmethod
    def _check_status_code(response):
        if response.status_code == 200:
            logger.info("{}: {}".format(response.status_code, response.text))
            return True
        elif response.status_code == 422:
            logger.warning("{}: {}".format(response.status_code, response.text))
        else:
            logger.warning("{}: {}".format(response.status_code, response.text))
        return False
