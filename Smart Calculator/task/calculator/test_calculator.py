import unittest
import calculator


class TestCalculator(unittest.TestCase):  # a test case for the calculator.py module

    def test_take_inputs(self):
        # tests the input modes
        self.assertEqual(calculator.take_inputs('17 9'),(True, ['17', '9']))

    def test_add(self):
        # tests for the add() function
        self.assertEqual(calculator.plus(['17', '9']), 26)
        self.assertEqual(calculator.plus(['-2', '5']), 3)
        #self.assertEqual(calculator.add(['3']), False)
        self.assertEqual(calculator.plus(['6', '4']), 10)

    def test_playground(self):
        self.assertEqual(calculator.playground("word"), True)


if __name__ == "__main__":
    unittest.main()