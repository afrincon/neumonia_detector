import unittest
import .ui.ui

class test_ui(unittest.TestCase):
  def test_class_setup(self):
    ui.ui.App()

if __name__ == '__main__':
    unittest.main()

