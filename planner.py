import sys
import argparse
import csv
from datetime import datetime
import os

EXPENSE_FILE = "expenses.csv"

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

#Can be anything you want - just made it up  (The data is from the file for your reports!) 
def report1(data):
    print("Report 1: Summary by Category (placeholder)")

#Can be anything you want - just made it up
def report2(data):
    print("Report 2: Total Expenses Over Time (placeholder)")

#Can be anything you want - just made it up
def report3(data):
    print("Report 3: Highest Single Expenses (placeholder)")    
    


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
        return list(reader)
    
    
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