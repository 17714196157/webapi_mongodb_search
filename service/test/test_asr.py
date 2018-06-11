# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     test_asr
   Description :
   Author :       yu.zhang
   date：          18-5-11
-------------------------------------------------
"""

from unittest import TestCase
from service import create_app
import os


class TestAsr(TestCase):
    XUNFEI_ASR_URL = "/xunfei/asr"

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_asr_post(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test1.wav")
        payload = {
            "filepath": file_path,
        }
        resp = self.client.post(self.XUNFEI_ASR_URL, json=payload).json
        self.assertEqual(resp['code'], '0000')
