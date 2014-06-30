#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from line_wrapper import MetadataLineWrapper


class FileMetadataProcessor(object):
    def __init__(self, changed_file_path):
        self.path = changed_file_path
        self.begin_header = "@REVIEW-METADATA-BEGIN"
        self.end_header = "@REVIEW-METADATA-END"

    def _get_empty_results_dict(self):
        return {"maintainer": {'receivers': [], "groups": []}, 'cc': {'receivers': [], "groups": []}, 'recursive': 0}

    def _parse_metadata(self, metadata):
        results = self._get_empty_results_dict()
        for line in filter(None, metadata.splitlines()):
            metadata_line_object = MetadataLineWrapper(line)
            metadata_line_object.add_content(results)
        return results

    def _parse_file_metadata(self, path):
        with open(path) as f:
            content = f.read()
            metadata = re.search('{begin}(.*){end}'.format(begin=self.begin_header, end=self.end_header), content, re.DOTALL | re.MULTILINE).group(1)
            return self._parse_metadata(metadata) if metadata else self._parse_metadata('')
