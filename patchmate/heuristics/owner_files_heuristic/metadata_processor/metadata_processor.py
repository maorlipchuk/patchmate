#!/usr/bin/env python
# -*- coding: utf-8 -*-
from results_container import ResultsContainer
from concrete_metadata_processor import FileMetadataProcessor


class MetadataProcessor(object):
    def __init__(self, changed_files_list):
        self.changed_files_list = changed_files_list

    def process(self):
        results = ResultsContainer()
        for changed_file in self.changed_files_list:
            results += FileMetadataProcessor(changed_file).parse_metadata()
        return results
