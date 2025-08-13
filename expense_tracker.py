import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1200x700")
        
        # Data initialization
        self.expenses = []
        self.categories = ("Food", "Transport", "Entertainment", "Bills", "Others")
        self.budget = 0

        # Initialize user details
        self.username = ""
        self.logged_in = False

    def load_users(self):
        """Load user data from file"""
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                return json.load(file)
        return {}

    def save_users(self, users):
        """Save user data to file"""
        with open("users.json", "w") as file:
            json.dump(users, file)

    def login(self):
        """Login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.root, text="Username:").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        def validate_login():
            """Validate user login"""
            users = self.load_users()
            username = username_entry.get()
            password = password_entry.get()

            if username in users and users[username] == password:
                self.username = username
                self.logged_in = True
                self.load_expenses()  # Load user-specific expenses after login
                self.main_menu()
            else:
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(self.root, text="Login", command=validate_login, width=10).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.signup, width=10).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.root.quit, width=10).pack(pady=5)

    def signup(self):
        """Signup screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Sign Up", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username:").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        def create_account():
            """Create a new account"""
            users = self.load_users()
            username = username_entry.get()
            password = password_entry.get()

            if username in users:
                messagebox.showerror("Error", "Username already exists.")
            elif username and password:
                users[username] = password
                self.save_users(users)
                messagebox.showinfo("Success", "Account created successfully. You can now log in.")
                self.login()
            else:
                messagebox.showerror("Error", "Username and password cannot be empty.")

        tk.Button(self.root, text="Create Account", command=create_account, width=15).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.login, width=10).pack(pady=5)

    def main_menu(self):
        """Main menu after login"""
        if not self.logged_in:
            messagebox.showerror("Error", "You must log in first.")
            self.login()
            return

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create menu buttons
        tk.Label(self.root, text="Expense Tracker", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Log Expense", command=self.log_expense, width=20).pack(pady=5)
        tk.Button(self.root, text="View Expenses", command=self.view_expenses, width=20).pack(pady=5)
        tk.Button(self.root, text="Analyze Spending", command=self.analyze_spending, width=20).pack(pady=5)
        tk.Button(self.root, text="Set Budget", command=self.set_budget, width=20).pack(pady=5)
        # tk.Button(self.root, text="Logout", command=self.logout, width=20).pack(pady=5)

    def logout(self):
        """Logs the user out and returns to login screen"""
        self.logged_in = False
        self.username = ""
        self.expenses = []  # Clear expenses
        self.budget = 0  # Reset budget
        self.login()

    def log_expense(self):
        """Logs an expense entered by the user"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Label and input fields for expense
        tk.Label(self.root, text="Log Expense", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(self.root)
        amount_entry.pack(pady=5)

        tk.Label(self.root, text="Category:").pack(pady=5)
        category_combo = ttk.Combobox(self.root, values=self.categories, state="readonly")
        category_combo.pack(pady=5)

        tk.Label(self.root, text="Description:").pack(pady=5)
        description_entry = tk.Entry(self.root)
        description_entry.pack(pady=5)

        def save_expense():
            """Validates and saves the expense data"""
            try:
                amount = float(amount_entry.get())
                category = category_combo.get()
                description = description_entry.get()

                # Input validation
                if amount <= 0:
                    raise ValueError("Amount should be greater than 0.")
                if not category:
                    raise ValueError("Please select a category.")
                if not description:
                    raise ValueError("Description cannot be empty.")

                # Add expense to the list
                self.expenses.append({"amount": amount, "category": category, "description": description})
                self.save_expenses()  # Save to file after logging

                # Check if total expenses exceed budget
                total_expenses = sum(expense["amount"] for expense in self.expenses)
                if total_expenses > self.budget:
                    messagebox.showwarning("Warning", f"Your total expenses have exceeded the budget of RM {self.budget:.2f}. Total: RM {total_expenses:.2f}")

                messagebox.showinfo("Success", "Expense logged successfully!")
                self.main_menu()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Save", command=save_expense, width=10).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=10).pack(pady=5)

    def view_expenses(self):
        """Displays all logged expenses"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="View Expenses", font=("Arial", 16)).pack(pady=10)

        # Create treeview to display expenses
        tree = ttk.Treeview(self.root, columns=("Amount", "Category", "Description"), show="headings")
        tree.heading("Amount", text="Amount")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        tree.pack(pady=10, fill=tk.BOTH, expand=True)

        for expense in self.expenses:
            tree.insert("", "end", values=(expense["amount"], expense["category"], expense["description"]))

        # Check if total expenses exceed budget
        total_expenses = sum(expense["amount"] for expense in self.expenses)
        if total_expenses > self.budget:
            messagebox.showwarning("Warning", f"Your total expenses have exceeded the budget of RM {self.budget:.2f}. Total: RM {total_expenses:.2f}")

        tk.Button(self.root, text="Back", command=self.main_menu, width=10).pack(pady=5)

    def analyze_spending(self):
        """Analyzes the spending by category"""
        if not self.expenses:
            messagebox.showerror("Error", "No expenses to analyze.")
            return

        category_totals = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense["category"]] += expense["amount"]

        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Spending Analysis")
        analysis_window.geometry("300x300")

        tk.Label(analysis_window, text="Spending by Category", font=("Arial", 14)).pack(pady=10)

        total_spent = sum(category_totals.values())
        for category, total in category_totals.items():
            # Handle percentage calculation
            percentage = (total / total_spent) * 100 if total_spent > 0 else 0
            tk.Label(analysis_window, text=f"{category}: RM {total:.2f} ({percentage:.1f}%)").pack(pady=2)

        tk.Button(analysis_window, text="Close", command=analysis_window.destroy).pack(pady=10)

    def set_budget(self):
        """Sets the user's monthly budget"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Set Monthly Budget", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Enter Budget:").pack(pady=5)
        budget_entry = tk.Entry(self.root)
        budget_entry.pack(pady=5)

        def save_budget():
            """Validates and saves the budget"""
            try:
                budget = float(budget_entry.get())
                
                if budget <= 0:
                    raise ValueError("Budget should be greater than 0.")

                self.budget = budget
                self.save_budget_to_file()  # Save to user-specific budget file
                messagebox.showinfo("Success", "Budget set successfully!")
                self.main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        tk.Button(self.root, text="Save", command=save_budget, width=10).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=10).pack(pady=5)

    def load_expenses(self):
        """Loads expenses from a file"""
        if self.username and os.path.exists(f"{self.username}_expenses.json"):
            with open(f"{self.username}_expenses.json", "r") as file:
                self.expenses = json.load(file)

        if self.username and os.path.exists(f"{self.username}_budget.json"):
            with open(f"{self.username}_budget.json", "r") as file:
                self.budget = json.load(file)

    def save_expenses(self):
        """Saves expenses to a file"""
        if self.username:
            with open(f"{self.username}_expenses.json", "w") as file:
                json.dump(self.expenses, file)

    def save_budget_to_file(self):
        """Saves budget to a file"""
        if self.username:
            with open(f"{self.username}_budget.json", "w") as file:
                json.dump(self.budget, file)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = ExpenseTracker(root)
    app.login()  # Start with the login screen
    root.mainloop()
