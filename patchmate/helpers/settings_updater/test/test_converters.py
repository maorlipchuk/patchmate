#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from patchmate.helpers.settings_updater.converters import StrToStrConverter, StrToIntConverter,\
    StrToListConverter, StrToBoolConverter, StrToFloatConverter, ConverterException


class TestStrToStrConverter(unittest.TestCase):
    def setUp(self):
        self.converter = StrToStrConverter()

    def test_convert_str_to_str(self):
        data = "test"
        self.assertEquals(self.converter.convert(data), data)


class TestStrToIntConverter(unittest.TestCase):
    def setUp(self):
        self.converter = StrToIntConverter()

    def test_convert_number_str_to_int(self):
        data = "11"
        self.assertEquals(self.converter.convert(data), 11)

    def test_convert_float_str_to_int_should_raise_exception(self):
        data = "11.0"
        with self.assertRaises(ConverterException):
            self.converter.convert(data)


class TestStrToBoolConverter(unittest.TestCase):
    def setUp(self):
        self.converter = StrToBoolConverter()

    def test_convert_true_str_to_bool(self):
        data_set = ["true", "True", "TRUE"]
        for data in data_set:
            self.assertTrue(self.converter.convert(data))

    def test_convert_false_str_to_bool(self):
        data_set = ["false", "False", "False"]
        for data in data_set:
            self.assertFalse(self.converter.convert(data))

    def test_convert_number_str_to_bool_should_raise_exception(self):
        data = "11.0"
        with self.assertRaises(ConverterException):
            self.converter.convert(data)


class TestStrToFloatConverter(unittest.TestCase):
    def setUp(self):
        self.converter = StrToFloatConverter()

    def test_convert_int_str_to_float(self):
        data = "11"
        self.assertEquals(self.converter.convert(data), 11.0)

    def test_convert_float_str_to_float(self):
        data = "11.0"
        self.assertEquals(self.converter.convert(data), 11.0)

    def test_convert_str_to_float_should_raise_exception(self):
        data = "test"
        with self.assertRaises(ConverterException):
            self.converter.convert(data)


class TestStrToListConverter(unittest.TestCase):
    def setUp(self):
        self.converter = StrToListConverter()

    def test_convert_list_str_without_spaces_after_commas_to_list(self):
        data = "[1,2,3]"
        self.assertEquals(self.converter.convert(data), ["1", "2", "3"])

    def test_convert_list_str_with_spaces_after_commas_to_list(self):
        data = "[1, 2, 3]"
        self.assertEquals(self.converter.convert(data), ["1", "2", "3"])

    def test_convert_list_str_to_list(self):
        data = "[1, 2,3]"
        self.assertEquals(self.converter.convert(data), ["1", "2", "3"])

    def test_convert_str_not_startswith_open_bracket_should_raise_error(self):
        data = "1, 2,3]"
        with self.assertRaises(ConverterException):
            self.converter.convert(data)


if __name__ == "__main__":
    unittest.main()
