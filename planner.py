import sys
import argparse
import csv
from datetime import datetime
import os

EXPENSE_FILE = "expenses.csv"

class Transaction:
    """
    Class for a single financial transaction.
    
    Attributes:
        date (str): The date and time of the transaction.
        amount (float): The amount spent.
        category (str): The category of the expense.
        description (str): A brief description of the expense.
    """
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = float(amount)
        self.category = category
        self.description = description

    def __str__(self):
        return f"{self.date} | ${self.amount:.2f} | {self.category} | {self.description}"



def add_expense(amount, category, description):
    """
    Adds an expense entry to the CSV file.

    Args:
        amount (float): The amount spent.
        category (str): The category of the expense (e.g., food, travel).
        description (str): A brief description of the expense.

    Side Effects:
        Appends a new row to the 'expenses.csv' file and prints confirmation to the console.
    """
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expense = [date, amount, category, description]

    file_exists = os.path.isfile(EXPENSE_FILE)
    with open(EXPENSE_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Amount", "Category", "Description"])
        writer.writerow(expense)

    print(f"Expense added: ${amount} - {category} - {description}")



def report1(data):
    print("Report 1: Summary by Category")
    summary = {}
    for txn in data:
        summary[txn.category] = summary.get(txn.category, 0) + txn.amount
    for cat, total in summary.items():
        print(f"{cat}: ${total:.2f}")

def report2(data):
    print("Report 2: Monthly Expenses")
    summary = {}
    for txn in data:
        month = txn.date[:7]
        summary[month] = summary.get(month, 0) + txn.amount
    for month, total in sorted(summary.items()):
        print(f"{month}: ${total:.2f}")

def report3(data):
    print("Report 3: Largest Expenses")
    top_expenses = sorted(data, key=lambda x: x.amount, reverse=True)[:5]
    for txn in top_expenses:
        print(txn)
    


def parse_args(args_list):
    """
    Parses command-line arguments.

    Args:
        args_list (list): A list of arguments passed to the script.

    Returns:
        argparse.Namespace: Parsed arguments including action and any associated options.
    """
    parser = argparse.ArgumentParser(description="Track and report personal expenses via CLI.")
    parser.add_argument("action", choices=["ADDEXPENSE", "REPORT1", "REPORT2", "REPORT3"], help="Action to perform")
    parser.add_argument("--amount", type=float, help="Expense amount")
    parser.add_argument("--category", type=str, help="Expense category (e.g., food, travel, rent)")
    parser.add_argument("--description", type=str, nargs='+', help="Description of the expense")

    return parser.parse_args()



def read_expense_data():
    """
    Reads the expense data from the CSV file.

    Returns:
        list: A list of dictionaries containing the expense data.
    """
    if not os.path.isfile(EXPENSE_FILE):
        return []

    with open(EXPENSE_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [Transaction(row["Date"], row["Amount"], row["Category"], row["Description"]) for row in reader]



def main():
    """
    Entry point for the script.

    Processes command-line arguments and executes the appropriate action:
    - Adds an expense
    - Generates one of three placeholder reports
    """
    
    args = parse_args(sys.argv[1:])
    expense_data = read_expense_data()

    match args.action:
        case "ADDEXPENSE":
            if args.amount is None or args.category is None or args.description is None:
                print("Error: ADDEXPENSE requires --amount, --category, and --description")
                sys.exit(1)
            desc_text = ' '.join(args.description)
            print(f"Amount: {args.amount} Category: {args.category} Description: {desc_text}")
            add_expense(args.amount, args.category, desc_text)
        case "REPORT1":
            report1(expense_data)
        case "REPORT2":
            report2(expense_data)
        case "REPORT3":
            report3(expense_data)
        case _:
            print("Invalid action. Choose ADDEXPENSE, REPORT1, REPORT2, or REPORT3.")
    
    

if __name__ == "__main__":
    main()