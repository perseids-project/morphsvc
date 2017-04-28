from unittest import TestCase
from morphsvc import morphsvc

class BaseTest(TestCase):

    def setUp(self):
        self.client = morphsvc.app.test_client()
        morphsvc.init_app(morphsvc.app, config_file='config.cfg')

