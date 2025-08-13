# Student Management System
A comprehensive student management system that integrates a Calendar App, GPA Calculator, and Expense Tracker to help students organize their academic life and finances.

## Getting Started
### Prerequisites
- Python
- Tkinter library (usually comes with Python)

### Installation
1. Clone this repository or download all the files
2. Ensure you have all the required files:
   - main.py
   - calendar_app.py
   - gpa.py
   - expense_tracker.py

### Running the Application
1. Open terminal/command prompt
2. Navigate to the project directory
3. Run the following command:
```bash
pip install tkcalendar
```
```bash
python main.py
```

### First Time Setup
1. When you first run the application, you'll need to register an account
2. Click the "Register" button on the login screen
3. Create a username and password
4. Log in with your new credentials

## File Structure
```
student-management-system/
├── main.py                 # Main application entry point
├── calendar_app.py         # Calendar functionality
├── gpa.py                  # GPA calculator
├── expense_tracker.py      # Expense tracking system
├── calendar_events.json    # Calendar data storage
├── username_expanses.json  # Expanses data storage
└── users.json              # User data storage
```

## Usage Notes
- All data is saved locally
- Each user has their own separate data
- You must log in to access any features
- Logout through the main menu
