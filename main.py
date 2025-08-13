import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from calendar_app import CalendarApp
from expense_tracker import ExpenseTracker
from gpa import GPACalculator

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("400x500")
        self.current_user = None
        self.setup_login_screen()
        
    def setup_login_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Login", font=("Arial", 20)).pack(pady=20)
        
        ttk.Label(frame, text="Username:").pack()
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack(pady=5)
        
        ttk.Label(frame, text="Password:").pack()
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(frame, text="Login", command=self.login).pack(pady=20)
        ttk.Button(frame, text="Register", command=self.setup_register_screen).pack()
        
    def setup_register_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Register", font=("Arial", 20)).pack(pady=20)
        
        ttk.Label(frame, text="Username:").pack()
        self.reg_username = ttk.Entry(frame)
        self.reg_username.pack(pady=5)
        
        ttk.Label(frame, text="Password:").pack()
        self.reg_password = ttk.Entry(frame, show="*")
        self.reg_password.pack(pady=5)
        
        ttk.Button(frame, text="Register", command=self.register).pack(pady=20)
        ttk.Button(frame, text="Back to Login", command=self.setup_login_screen).pack()
        
    def setup_main_menu(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text=f"Welcome, {self.current_user}", 
                 font=("Arial", 20)).pack(pady=20)
        
        ttk.Button(frame, text="Calendar App", 
                  command=self.launch_calendar).pack(pady=10, fill=tk.X)
        ttk.Button(frame, text="GPA Calculator", 
                  command=self.launch_gpa).pack(pady=10, fill=tk.X)
        ttk.Button(frame, text="Expenses Tracker", 
                  command=self.launch_expenses).pack(pady=10, fill=tk.X)
        ttk.Button(frame, text="Logout", 
                  command=self.setup_login_screen).pack(pady=20)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
            
        if username in users and users[username] == password:
            self.current_user = username
            self.setup_main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return
            
        users[username] = password
        
        with open('users.json', 'w') as f:
            json.dump(users, f)
            
        messagebox.showinfo("Success", "Registration successful")
        self.setup_login_screen()
    
    def launch_calendar(self):
        calendar_window = tk.Toplevel(self.root)
        calendar_app = CalendarApp(calendar_window)
        calendar_app.current_user = self.current_user
    
    def launch_gpa(self):
        gpa_window = tk.Toplevel(self.root)
        calculator = GPACalculator(gpa_window)
    
    def launch_expenses(self):
        expense_window = tk.Toplevel(self.root)
        expense_tracker = ExpenseTracker(expense_window)
        # Auto-login with current user
        expense_tracker.username = self.current_user
        expense_tracker.logged_in = True
        expense_tracker.load_expenses()  # Load the user's expenses
        expense_tracker.main_menu()  # Show the main menu

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()