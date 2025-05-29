import json
from datetime import datetime

class Expense:
    def __init__(self, category, amount, description, timestamp=None):
        self.category = category
        self.amount = amount
        self.description = description
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"{self.category}: ${self.amount} - {self.description} [{self.timestamp}] "


class ExpenseTracker:
    
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self.load_expenses()


    def add_expense(self, category, amount, description):
        try:
            amount = float(amount)  
            expense = Expense(category, amount, description)
            self.expenses.append(expense)
            self.save_expenses()
            print("Expense added successfully!")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def delete_expense(self, index):
        try:
            index = int(index) - 1
            if 0 <= index < len(self.expenses):
                removed = self.expenses.pop(index)
                self.save_expenses()
                print(f"Deleted: {removed}")
            else:
                print("Invalid index. Please choose a valid expense number.")
        except ValueError:
            print("Please enter a valid number.")


    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
        else:
            for idx, exp in enumerate(self.expenses, 1):
                print(f"{idx}. {exp}")
            total = sum(exp.amount for exp in self.expenses)
            print(f"\nTotal Expenses: ${total:.2f}")

    def save_expenses(self):
        with open(self.filename, "w") as file:
            json.dump([exp.__dict__ for exp in self.expenses], file, indent=4)


    def load_expenses(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                print("Loaded expenses from file.")  
                return [Expense(**entry) for entry in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Could not load expenses: {e}")  
            return []

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            category = input("Enter category (e.g., Food, Transport): ")
            amount = input("Enter amount: ")
            description = input("Enter description: ")
            tracker.add_expense(category, amount, description)
        
        elif choice == "2":
            tracker.view_expenses()
        
        elif choice == "3":
            tracker.view_expenses()
            idx = input("Enter the number of the expense to delete: ")
            tracker.delete_expense(idx)

        elif choice == "4":
            print("Exiting. Your expenses are saved.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()