import unittest
from urllib2 import urlopen, Request

class TestExample(unittest.TestCase):
    def setUp(self):
        self.host = "http://localhost:8000"
    def test_echo(self):
        r = Request(self.host + "/echo?with=test", None, {'Accept': "text/plain"})
        self.assertTrue('test' in urlopen(r).read())
    def test_words(self):
        r = Request(self.host + "/words/with/nihil", None, {'Accept': "text/plain"})
        self.assertTrue('nihilism' in urlopen(r).read())


if __name__ == "__main__":
    unittest.main()

