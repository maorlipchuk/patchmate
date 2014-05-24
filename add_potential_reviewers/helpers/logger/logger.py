#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger("Add Potential Reviewers Logger")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
