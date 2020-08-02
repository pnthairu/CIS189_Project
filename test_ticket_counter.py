# Start Program
"""
Program: test_ticket_counter.py
Author: Paul Thairu
Last date modified: 07/31/2020

This program is for testing if user input is valid or invalid for example:
-1 user input will fail test because one cannot buy negative tickets
3 user inter will pass test
7 user input will fail test because the number of tickets purchased is more than 6
"""
import unittest
from TicketCounter import ticket_counter as tix

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_tickets(self):
        ticket_counter = tix.tickets_entry
        assert tix.tickets_entry


if __name__ == '__main__':
    unittest.main()

# End program
