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

    def _parse_metadata(self, metadata, file_relative_path):
        results = self._get_empty_results_dict()
        for line in filter(None, metadata.splitlines()):
            metadata_line_object = MetadataLineWrapper(line, file_relative_path)
            metadata_line_object.add_content(results)
        return results

    @abstractmethod
    def parse_metadata(self):
        return


class FileMetadataProcessor(AbstractMetaDataProcessor):
    def __init__(self, changed_file_path, changed_file_relative_path):
        super(FileMetadataProcessor, self).__init__()
        self.path = changed_file_path
        self.changed_file_relative_path = changed_file_relative_path

    def parse_metadata(self):
        if not os.path.exists(self.path):
            metadata = None
        else:
            with open(self.path) as metadata_file:
                metadata_search_object = re.search('{begin}(.*){end}'.format(begin=self.begin_header, end=self.end_header),
                                                   metadata_file.read(),
                                                   re.DOTALL | re.MULTILINE)
                metadata = metadata_search_object.group(1) if metadata_search_object else None

        if metadata:
            results = self._parse_metadata(metadata, self.changed_file_relative_path)
        else:
            results = self._parse_metadata('', self.changed_file_relative_path)

        if results.recursive:
            results += DirectoryMetadataProcessor(os.path.dirname(self.path), os.path.dirname(self.changed_file_relative_path)).parse_metadata()
        return results


class DirectoryMetadataProcessor(AbstractMetaDataProcessor):
    def __init__(self, directory_path, directory_relative_path):
        super(DirectoryMetadataProcessor, self).__init__()
        self.directory_path = directory_path
        self.directory_relative_path = directory_relative_path

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
        results = self._parse_metadata(metadata, self.directory_relative_path) if metadata else self._parse_metadata('', self.directory_relative_path)
        if results.recursive:
            directory_path_dirname = os.path.dirname(self.directory_path)
            directory_relative_path_dirname = os.path.dirname(self.directory_relative_path)
            results += DirectoryMetadataProcessor(directory_path_dirname, directory_relative_path_dirname).parse_metadata()
        return results
