#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from abc import ABCMeta, abstractmethod
from results_container import ResultsContainer
from line_wrapper import MetadataLineWrapper


class AbstractMetaDataProcessor(object):
    __metaclass__ = ABCMeta

    def __init__(self, begin_header="@REVIEW-METADATA-BEGIN", end_header="@REVIEW-METADATA-END"):
        self.begin_header = begin_header
        self.end_header = end_header

    def _get_empty_results_dict(self):
        return ResultsContainer()

    def _parse_metadata(self, metadata):
        results = self._get_empty_results_dict()
        for line in filter(None, metadata.splitlines()):
            metadata_line_object = MetadataLineWrapper(line)
            metadata_line_object.add_content(results)
        return results

    @abstractmethod
    def parse_metadata(self):
        return


class FileMetadataProcessor(AbstractMetaDataProcessor):
    def __init__(self, changed_file_path):
        super(FileMetadataProcessor, self).__init__()
        self.path = changed_file_path

    def parse_metadata(self):
        if not os.path.exists(self.path):
            metadata = None
        else:
            with open(self.path) as metadata_file:
                metadata_search_object = re.search('{begin}(.*){end}'.format(begin=self.begin_header, end=self.end_header),
                                                   metadata_file.read(),
                                                   re.DOTALL | re.MULTILINE)
                metadata = metadata_search_object.group(1) if metadata_search_object else None
        results = self._parse_metadata(metadata) if metadata else self._parse_metadata('')
        if results.recursive:
            results += DirectoryMetadataProcessor(os.path.dirname(self.path)).parse_metadata()
        return results


class DirectoryMetadataProcessor(AbstractMetaDataProcessor):
    def __init__(self, directory_path):
        super(DirectoryMetadataProcessor, self).__init__()
        self.directory_path = directory_path

    def parse_metadata(self, metadata_file_name="review.metadata"):
        review_metadata = os.path.join(self.directory_path, metadata_file_name)

        if os.path.exists(review_metadata):
            with open(review_metadata) as metadata_file:
                metadata = re.search('{begin}(.*){end}'.format(begin=self.begin_header, end=self.end_header),
                                     metadata_file.read(),
                                     re.DOTALL | re.MULTILINE)
                metadata = metadata.group(1) if metadata else None
        else:
            metadata = None
        results = self._parse_metadata(metadata) if metadata else self._parse_metadata('')
        if results.recursive:
            results += DirectoryMetadataProcessor(os.path.dirname(self.directory_path)).parse_metadata()
        return results
