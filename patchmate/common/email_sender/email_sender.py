#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from .email_content import EMAIL_CONTENT
from ..logger import logger


class EmailSender(object):
    """
    Patchmate wrapper for smtplib email sending
    """
    def __init__(self, login, password, smtp_server, sender, receivers_list, cc_list=None):
        """
        Constructor

        :param login: E-mail login
        :type login: str

        :param password: E-mail password
        :type password: str

        :param smtp_server: SMTP server address
        :type smtp_server: str

        :param sender: Sender email address
        :type sender: str

        :param receivers_list: List of receivers emails
        :type receivers_list: list

        :param cc_list: List of cc
        :type cc_list: list
        """
        self.sender = sender
        self.receivers_list = receivers_list
        self.cc_list = cc_list if cc_list else []
        self.smtp_obj = smtplib.SMTP_SSL(smtp_server)
        self.smtp_obj.login(login, password)

    def send_notification(self, message_content, to_cc=True):
        """
        Sends email with given content to all receivers and cc from cc_list if to_cc flag is set

        :param message_content: E-mail's text content
        :type message_content: str

        :param to_cc: Flag determines if email should be sent to receivers from cc_list or not (default: True)
        :type to_cc: bool
        """
        try:
            joined_receivers = ', '.join(self.receivers_list)
            joined_cc = ', '.join(self.cc_list) if to_cc else ""
            self.smtp_obj.sendmail(self.sender,
                                   self.receivers_list,
                                   EMAIL_CONTENT.format(sender=self.sender,
                                                        receivers=joined_receivers,
                                                        cc_list=joined_cc,
                                                        content=message_content))
            logger.debug("Successfully sent email from {} to {} and CC: {}".format(self.sender, joined_receivers, joined_cc))
        except smtplib.SMTPException as e:
            logger.error(e)
