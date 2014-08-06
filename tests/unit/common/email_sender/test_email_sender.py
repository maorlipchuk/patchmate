#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import unittest
from mock import MagicMock

import patchmate.common.email_sender.email_sender as email_sender_module
from patchmate.common.logger import logger
from patchmate.common.email_sender import EmailSender
from patchmate.common.email_sender.email_content import EMAIL_CONTENT


class TestEmailSender(unittest.TestCase):
    def setUp(self):
        logger.disabled = True
        self.login = "login"
        self.password = "password"
        self.sender = "email@email"
        self.receivers_list = ['receiver1@email.com', 'receiver2@email.com']
        self.cc_list = ['cc1@email.com', 'cc2@email.com']
        self.smtp_server = "smtp_server.email.com"
        email_sender_module.smtplib.SMTP_SSL = MagicMock(spec=smtplib.SMTP_SSL)
        self.email_sender = EmailSender(self.login, self.password, self.smtp_server, self.sender, self.receivers_list, self.cc_list)

    def test_if_attributes_are_set_correctly(self):
        self.assertEqual(self.email_sender.sender, self.sender)
        self.assertEqual(self.email_sender.receivers_list, self.receivers_list)
        self.assertEqual(self.email_sender.cc_list, self.cc_list)
        self.email_sender.smtp_obj.login.assert_called_once_with(self.login, self.password)

    def test_send_notification_method_sends_emails_with_correct_params_with_cc_list(self):
        message_content = "Message content"
        self.email_sender.send_notification(message_content)
        filled_message = EMAIL_CONTENT.format(sender=self.sender,
                                              receivers=', '.join(self.receivers_list),
                                              cc_list=', '.join(self.cc_list),
                                              content=message_content)
        self.email_sender.smtp_obj.sendmail.assert_called_once_with(self.sender, self.receivers_list, filled_message)

    def test_send_notification_method_sends_emails_with_correct_params_without_cc_list(self):
        message_content = "Message content"
        self.email_sender.send_notification(message_content, to_cc=False)
        filled_message = EMAIL_CONTENT.format(sender=self.sender,
                                              receivers=', '.join(self.receivers_list),
                                              cc_list="",
                                              content=message_content)
        self.email_sender.smtp_obj.sendmail.assert_called_once_with(self.sender, self.receivers_list, filled_message)

    def test_send_notification_method_sends_emails_with_wrong_params_log_an_error(self):
        message_content = "Message content"
        logger.error = MagicMock()
        self.email_sender.smtp_obj.sendmail.side_effect = smtplib.SMTPException()
        self.email_sender.send_notification(message_content, to_cc=False)
        self.assertTrue(logger.error.called)


if __name__ == "__main__":
    unittest.main()
