import json

#this creates the expense. Example: grocery, $10, fruits
class Expense:
    
    def __init__(self, category, amount, description):
        self.category = category
        self.amount = amount
        self.description = description
#This translates the code for human understanding
    def __str__(self):
        return f"{self.category}: ${self.amount} - {self.description}"

#Manages expense entries, file storage, and user interaction.
class ExpenseTracker:
    
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self.load_expenses()

#adds and saves expense like a notebook.
    def add_expense(self, category, amount, description):
        try:
            amount = float(amount)  # Ensure the amount is a number
            expense = Expense(category, amount, description)
            self.expenses.append(expense)
            self.save_expenses()
            print("Expense added successfully!")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

#Displays all expenses.
    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
        else:
            for idx, exp in enumerate(self.expenses, 1):
                print(f"{idx}. {exp}")

#Saves expenses to a JSON file.
    def save_expenses(self):
        with open(self.filename, "w") as file:
            json.dump([exp.__dict__ for exp in self.expenses], file, indent=4)

#Loads expenses from a JSON file
    def load_expenses(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return [Expense(**entry) for entry in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
#creates display menu
def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            category = input("Enter category (e.g., Food, Transport): ")
            amount = input("Enter amount: ")
            description = input("Enter description: ")
            tracker.add_expense(category, amount, description)
        
        elif choice == "2":
            tracker.view_expenses()
        
        elif choice == "3":
            print("Exiting. Your expenses are saved.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()