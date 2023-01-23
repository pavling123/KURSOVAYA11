from rc5 import RC5
import unittest
import os
import tempfile

class RC5FileTests(unittest.TestCase):

    def setUp(self):
        self.input_fd, self.input_filename = tempfile.mkstemp(dir=os.curdir)
        self.out_fd, self.out_filename = tempfile.mkstemp(dir=os.curdir)

    def tearDown(self):
        os.close(self.input_fd)
        os.unlink(self.input_filename)
        os.close(self.out_fd)
        os.unlink(self.out_filename)


if __name__ == "__main__":
    testRC5 = RC5(32, 12, b'\0' * 16)
    