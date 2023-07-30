#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City


class TestCity(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super(TestCity, self).__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
