#!/usr/bin/env python
# -*- coding: utf-8 -*-


from add_potential_reviewers.interface import HeuristicInterface


class BlameHeuristic(HeuristicInterface):
    def get_reviewers(self):
        return ("blame_reviewer1@gmail.com", "blame_reviewer2@gmail.com")
