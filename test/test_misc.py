import unittest

from ijson import common

from .test_base import warning_catcher


class Misc(unittest.TestCase):
    """Miscelaneous unit tests"""

    def test_common_number_is_deprecated(self):
        with warning_catcher() as warns:
            common.number("1")
        self.assertEqual(len(warns), 1)
        self.assertEqual(DeprecationWarning, warns[0].category)