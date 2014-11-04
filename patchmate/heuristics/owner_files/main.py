#!/usr/bin/env python
# -*- coding: utf-8 -*-
from patchmate.common.git_adapter.git_adapter import GitAdapter
from patchmate.heuristics.interface import HeuristicInterface
from patchmate.common.logger import logger
from metadata_processor.metadata_processor import MetadataProcessor


class OwnerFilesHeuristic(HeuristicInterface):
    def __init__(self, repo_path, youngest_commit, oldest_commit):
        self.git_adapter = GitAdapter(repo_path)
        self.youngest_commit = youngest_commit
        self.oldest_commit = oldest_commit
        self.repo_path = repo_path
        logger.debug("OwnerFilesHeuristic object was created with: \n"
                     " -youngest_commit: {}\n"
                     " -oldest_commit: {}\n"
                     " -repo_path:{}".format(youngest_commit, oldest_commit, repo_path))

    def get_reviewers(self):
        commits_list = self.git_adapter.get_commits_from_range(self.youngest_commit, self.oldest_commit)
        logger.debug("Commits amount: {}".format(len(commits_list)))
        changed_files = set([])
        for index, commit_hash in enumerate(commits_list):
            changed_files = changed_files.union(set(self.git_adapter.get_changed_files_in_commit(commit_hash)))

        logger.debug("Found changed files: {}".format(commits_list))
        return MetadataProcessor(self.repo_path, changed_files).process()
