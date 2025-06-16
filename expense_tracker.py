import json
import os
from datetime import datetime

class Expense:
    def __init__(self, type, amount, description):
        self.type = type
        self.amount = amount
        self.description = description

    def __str__(self):
        return f"{self.type} - ${self.amount:.2f} - {self.description}"

    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "description": self.description,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class ExpenseManager:
    def __init__(self, file_path="expenses.json"):
        self.file_path = file_path

    def add_expense(self):
        type = input("Please enter type of expense (grocery, gas etc.): ")
        amount_input = input("Please enter amount for expense: ")
        description = input("Please enter description for expense: ")

        try:
            amount = float(amount_input)
        except ValueError:
            print("Please enter a valid number for the amount.")
            return

        expense = Expense(type, amount, description)
        expense_data = expense.to_dict()

        all_expenses = []

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    all_expenses = json.load(file)
                except json.JSONDecodeError:
                    pass  

        all_expenses.append(expense_data)

        with open(self.file_path, "w") as file:
            json.dump(all_expenses, file, indent=4)

        print("Expense added and saved!")

    def view_expenses(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    all_expenses = json.load(file)
                    if not all_expenses:
                        print(" There are no expenses recorded.")
                        return
                    else:
                        print("--- Recorded Expenses ---")
                        for i, ex in enumerate(all_expenses, start=1):
                            timestamp = ex.get("timestamp", "No timestamp")
                            print(f"{i}. {ex['type']} - ${ex['amount']} - {ex['description']} - [{timestamp}]")
                        total = sum(ex['amount'] for ex in all_expenses)
                        print(f"\nTotal Expenses: ${total:.2f}")
                except json.JSONDecodeError:
                    print(" Could not read expenses. File is corrupted.")
        else:
            print(" There are no expenses recorded.")

    def delete_expense(self):
        if not os.path.exists(self.file_path):
            print("There are no expenses recorded.")
            return

        with open(self.file_path, "r") as file:
            try:
                all_expenses = json.load(file)
                if not all_expenses:
                    print("There are no expenses recorded.")
                    return
                else:
                    print("--- Recorded Expenses ---")
                    for i, ex in enumerate(all_expenses, start=1):
                        print(f"{i}. {ex['type']} - ${ex['amount']} - {ex['description']}")

            except json.JSONDecodeError:
                print("Could not read expenses. File is corrupted.")
                return
            
        try:
            remove_index = int(input("Please enter the number of the entry to delete: "))
            if 1 <= remove_index <= len(all_expenses):
                deleted = all_expenses.pop(remove_index - 1)
                print(f"Deleted: {deleted['type']} - ${deleted['amount']} - {deleted['description']}")

                with open(self.file_path, "w") as file:
                    json.dump(all_expenses, file, indent=4)

                print("Expense deleted successfully.")
            else:
                print("Invalid number selected.")

        except ValueError:
            print("Please enter a valid number.")

def run():
    manager = ExpenseManager()
    while True:
        print("\nWelcome to the expense manager main menu")
        print("\n1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            manager.add_expense()
        elif choice == "2":
            manager.view_expenses()
        elif choice == "3":
            manager.delete_expense()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    run()