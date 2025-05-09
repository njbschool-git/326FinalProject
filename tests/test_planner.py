import unittest
from unittest.mock import patch
import os
import csv

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import planner
from planner import add_expense, read_expense_data, Transaction, report1, report2, report3, parse_args, EXPENSE_FILE

EXPENSE_FILE = "test_expenses.csv"

class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        """Create a temporary test CSV file."""
        self.test_file = "test_expenses.csv"
        planner.EXPENSE_FILE = self.test_file
        
        with open(self.test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Amount", "Category", "Description"])
            writer.writerow(["2025-04-01 12:00:00", "10.50", "food", "Lunch"])
            writer.writerow(["2025-04-02 13:00:00", "200.00", "rent", "April rent"])
            writer.writerow(["2025-04-03 14:00:00", "50.00", "utilities", "Electric bill"])
            
    def test_transaction_initialization_and_str(self):
        """Test that Transaction initializes correctly and __str__ formats properly."""
        txn = Transaction('2025-04-25 12:00:00', 12.50, 'Food', 'Lunch with friends')
        self.assertEqual(txn.date, '2025-04-25 12:00:00')
        self.assertEqual(txn.amount, 12.50)
        self.assertEqual(txn.category, 'Food')
        self.assertEqual(txn.description, 'Lunch with friends')
        self.assertEqual(str(txn), '2025-04-25 12:00:00 | $12.50 | Food | Lunch with friends')

    def tearDown(self):
        """Remove the test CSV file."""
        #if os.path.exists(self.test_file):
        #    os.remove(self.test_file)

    def test_add_expense(self):
        """Test adding a new expense to the CSV file."""
        add_expense(75.00, "travel", "Train ticket")
        data = read_expense_data()
        self.assertTrue(any(txn.description == "Train ticket" for txn in data))

    def test_read_expense_data(self):
        """Test reading expense data from the CSV file."""
        data = read_expense_data()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0].category, "food")
        
    def test_report1_summary_by_category_data(self):
        """Test if categories and their sums are correct."""
        data = read_expense_data()
        summary = {}
        for txn in data:
            summary[txn.category] = summary.get(txn.category, 0) + txn.amount

        self.assertEqual(summary["food"], 10.50)
        self.assertEqual(summary["rent"], 200.00)
        self.assertEqual(summary["utilities"], 50.00)

    def test_report2_monthly_expenses_data(self):
        """Test if months and their totals are correct."""
        data = read_expense_data()
        monthly_summary = {}
        for txn in data:
            month = txn.date[:7]
            monthly_summary[month] = monthly_summary.get(month, 0) + txn.amount      

    def test_report3_highest_expense(self):
        """Test retrieval of the highest single expense."""
        data = read_expense_data()
        max_txn = max(data, key=lambda x: x.amount)
        self.assertEqual(max_txn.amount, 200.00)
        self.assertEqual(max_txn.category, "rent")
        
    def test_parse_args_add_expense(self):
        """ Test parsing CLI arguments for adding an expense."""
        test_args = ["script_name", "ADDEXPENSE", "--amount", "25", "--category", "Food", "--description", "Dinner", "with", "family"]
        with patch('sys.argv', test_args):
            args = parse_args(sys.argv[1:])
            self.assertEqual(args.action, "ADDEXPENSE")
            self.assertEqual(args.amount, 25)
            self.assertEqual(args.category, "Food")
            self.assertEqual(args.description, ["Dinner", "with", "family"])



if __name__ == "__main__":
    unittest.main()