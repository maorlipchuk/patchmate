#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from receivers import GroupOfPotentialReceivers, PotentialReceiver
from results_container import ResultsContainer
from concrete_metadata_processor import FileMetadataProcessor


class MetadataProcessor(object):
    def __init__(self, project_root, changed_files_list):
        self.project_root = project_root
        self.changed_files_list = changed_files_list

    def _convert_results(self, results):
        results.maintainers.receivers = [PotentialReceiver(name, email) for name, email in results.maintainers.receivers]
        for group in results.maintainers.groups:
            results.maintainers.receivers += GroupOfPotentialReceivers(group).get_emails(self.project_root)

        results.cc.receivers = [PotentialReceiver(name, email) for name, email in results.cc.receivers]

        for group in results.cc.groups:
            results.cc.receivers += GroupOfPotentialReceivers(group).get_emails(self.project_root)

        return results

    def process(self):
        results = ResultsContainer()
        for path in self.changed_files_list:
            results += FileMetadataProcessor(os.path.join(self.project_root, os.path.normpath(path))).parse_metadata()
        return self._convert_results(results)
