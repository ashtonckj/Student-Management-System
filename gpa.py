from tkinter import *
from tkinter import messagebox
import random
import os

class GPACalculator:
    def __init__(self, master=None):
        # Allow passing in a master window
        if master is None:
            self.welcome_win = Tk()  # Only create Tk if no master provided
        else:
            self.welcome_win = master
            
        self.welcome_win.geometry("1200x750")
        self.welcome_win.title("GPA Calculator")
        
        self.scale_var = StringVar(value="4.0")  # Default scale value

        self.fields = [] 
        self.create_main_window()

    #background color
    def apply_background_color(self, window, mode):
        if mode == "dark":
            window.configure(bg="black")
        elif mode == "light":
            window.configure(bg="white")
        else: 
            light_colors = ["#ADD8E6", "#FFFFE0"]
            window.configure(bg=random.choice(light_colors))

    #main window (Welcome screen)
    def create_main_window(self):
        wel = Label(self.welcome_win, text='Welcome to GPA Calculator!', font=('Arial', 25, 'bold', 'italic'), bg=self.welcome_win.cget('bg'))
        wel.place(relx=0.5, rely=0.1, anchor=CENTER)

        # background button
        self.buttonDarkMode = Button(self.welcome_win, text="Dark Mode", font=('Times New Roman', 14), command=lambda: self.choose_mode("dark"))
        self.buttonDarkMode.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.buttonLightMode = Button(self.welcome_win, text="Light Mode", font=('Times New Roman', 14), command=lambda: self.choose_mode("light"))
        self.buttonLightMode.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.buttonRandomColorMode = Button(self.welcome_win, text="Random Light Color Mode", font=('Times New Roman', 14), command=lambda: self.choose_mode("random"))
        self.buttonRandomColorMode.place(relx=0.5, rely=0.4, anchor=CENTER)

        # enter grades button
        self.buttonGrade = Button(self.welcome_win, text="Click to enter your grades", font=('Times New Roman', 20), command=lambda: self.input_window("light"))
        self.buttonGrade.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.welcome_win.mainloop()

    # choose mode background
    def choose_mode(self, mode):
        self.apply_background_color(self.welcome_win, mode)
        self.buttonGrade.config(bg="lightgray")
        self.buttonGrade.config(command=lambda: self.input_window(mode))

    # second window (Input Form)
    def input_window(self, bg_color):
        self.welcome_win.withdraw()  # Hides the main window

        input_win = Toplevel()  # Use Toplevel to keep the main window hidden
        input_win.geometry('1200x750')
        input_win.title('GPA Calculator - Enter Grades')

        self.apply_background_color(input_win, bg_color) 

        title = Label(input_win, text='Enter Your Grade Information', font=('CourierNew', 25, 'bold', 'italic', 'underline'), bg=input_win.cget('bg'))
        title.place(relx=0.5, rely=0.1, anchor=CENTER)

        grade_label = Label(input_win, text='Enter your grade details below:', font=('Times New Roman', 15), bg=input_win.cget('bg'))
        grade_label.place(relx=0.5, rely=0.15, anchor=CENTER)

        # Fields for Student ID and Course
        student_id_label = Label(input_win, text="Student ID (12345):", font=('Times New Roman', 12), bg=input_win.cget('bg'))
        student_id_label.place(x=250, y=200)
        student_id_entry = Entry(input_win, font=('Times New Roman', 12), width=30)
        student_id_entry.place(x=350, y=200 + 30)

        course_label = Label(input_win, text="Course (DCS, DFT):", font=('Times New Roman', 12), bg=input_win.cget('bg'))
        course_label.place(x=550, y=200)
        course_entry = Entry(input_win, font=('Times New Roman', 12), width=30)
        course_entry.place(x=650, y=200 + 30)

        # Dropdown for scale selection
        scale_label = Label(input_win, text="Select Scale:", font=('Times New Roman', 12), bg=input_win.cget('bg'))
        scale_label.place(x=250, y=270)
        scale_dropdown = OptionMenu(input_win, self.scale_var, "4.0", "5.0")
        scale_dropdown.place(x=350, y=270)

        # Add more fields
        def add_fields():
            row_index = len(self.fields)
            subject_label = Label(input_win, text="Subject Code:", font=('Times New Roman', 12), bg=input_win.cget('bg'))
            subject_label.place(x=250, y=300 + row_index * 50)
            subject_entry = Entry(input_win, font=('Times New Roman', 12))
            subject_entry.place(x=350, y=300 + row_index * 50)

            grade_label = Label(input_win, text="Grade:", font=('Times New Roman', 12), bg=input_win.cget('bg'))
            grade_label.place(x=550, y=300 + row_index * 50)
            grade_entry = Entry(input_win, font=('Times New Roman', 12))
            grade_entry.place(x=650, y=300 + row_index * 50)

            credit_label = Label(input_win, text="Credit Hours:", font=('Times New Roman', 12), bg=input_win.cget('bg'))
            credit_label.place(x=850, y=300 + row_index * 50)
            credit_entry = Entry(input_win, font=('Times New Roman', 12))
            credit_entry.place(x=950, y=300 + row_index * 50)

            self.fields.append((subject_entry, grade_entry, credit_entry))

        for _ in range(1):  
            add_fields()

        # Add more fields button
        add_button = Button(input_win, text="Add More Subjects", font=('Times New Roman', 14), command=add_fields)
        add_button.place(relx=0.5, rely=0.75, anchor=CENTER) 

        # Calculate GPA button
        def calculateGPA():
            self.calculateGPA(student_id_entry, course_entry, input_win, bg_color)

        calculate_button = Button(input_win, text="Calculate GPA", font=('Times New Roman', 14), command=calculateGPA)
        calculate_button.place(relx=0.5, rely=0.85, anchor=CENTER)

        input_win.mainloop()


    # Validate input fields
    def validate_entry(self, entry, entry_type):
        value = entry.get()
        if entry_type == "subject" and not value.isalnum():
            messagebox.showerror("Invalid Input", "Subject Code should contain only letters and numbers (e.g., AAMS1234).")
            return False
        elif entry_type == "grade" and value not in ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F", "a+", "a", "a-", "b+", "b", "b-", "c+", "c", "f"]:
            messagebox.showerror("Invalid Input", "Grade should be one of the following: A+, A, A-, B+, B, B-, C+, C, F.")
            return False
        elif entry_type == "credit hour" and not value.isdigit():
            messagebox.showerror("Invalid Input", "Credit Hour should contain only digits.")
            return False
        return True

    # Function to calculate GPA
    def calculateGPA(self, student_id_entry, course_entry, input_win, bg_color):
        grades = []
        student_id = student_id_entry.get()
        course = course_entry.get()
        scale = self.scale_var.get()

        # Validate Student ID and Course input
        if not student_id.isdigit():
            messagebox.showerror("Invalid Input", "Student ID must be a number.")
            return

        if not course.isalpha():
            messagebox.showerror("Invalid Input", "Coursemust contain only letters.")
            return

        # Ensure all fields are filled
        if not student_id or not course:
            messagebox.showerror("Error", "Please enter Student ID and Course.")
            return
        
        # Validate each subject, grade, and credit hour before processing
        for subject_entry, grade_entry, credit_entry in self.fields:
            subject = subject_entry.get()
            grade = grade_entry.get()
            credit_hour = credit_entry.get()

            # Ensure fields are not empty
            if not subject or not grade or not credit_hour:
                messagebox.showerror("Error", "Please fill in all fields for each subject.")
                return

            # Validate each entry
            if not (self.validate_entry(subject_entry, "subject") and self.validate_entry(grade_entry, "grade") and self.validate_entry(credit_entry, "credit hour")):
                return  

            grades.append((subject, grade.strip().upper(), credit_hour))

        total_grade_points = 0
        total_credit_hours = 0

        # Grade point maps for 4.0 and 5.0 scales
        grade_point_map_4 = {
            "A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0,
            "B-": 2.7, "C+": 2.3, "C": 2.0, "F": 0.0
        }
        grade_point_map_5 = {
            "A+": 5.0, "A": 5.0, "A-": 4.7, "B+": 4.3, "B": 4.0,
            "B-": 3.7, "C+": 3.3, "C": 3.0, "F": 0.0
        }

        grade_point_map = grade_point_map_4 if scale == "4.0" else grade_point_map_5

        for grade in grades:
            subject, grade_letter, credit_hour = grade
            try:
                credit_hour = float(credit_hour)
                if credit_hour <= 0:
                    messagebox.showerror("Invalid Input", f"Invalid credit hour for {subject}: {credit_hour}. Must be positive.")
                    return

                grade_point = grade_point_map.get(grade_letter)
                if grade_point is None:
                    messagebox.showerror("Invalid Input", f"Invalid grade for {subject}: {grade_letter}. Please enter a valid grade.")
                    return

                total_grade_points += grade_point * credit_hour
                total_credit_hours += credit_hour
            except ValueError:
                messagebox.showerror("Invalid Input", f"Invalid input for credit hour in {subject}. Must be a number.")
                return

        # Calculate GPA
        if total_credit_hours > 0:
            gpa = total_grade_points / total_credit_hours
            self.display_result_window(grades, gpa, total_credit_hours, student_id, course, scale, input_win, bg_color)
            self.save_student_data(student_id, course, grades, gpa, scale)  # Save the data to file
        else:
            messagebox.showerror("Error", "No valid credit hours entered.")

    # Function to save the student's data
    def save_student_data(self, student_id, course, grades, gpa, scale):
        with open("student_data.csv", "a") as file:
            file.write(f"Student ID, Course, Subject Code, Grade, Credit Hour\n")
        
            for subject, grade, credit_hour in grades:
                file.write(f"{student_id}, {course}, {subject}, {grade}, {credit_hour}\n")

            
            file.write(f"GPA: {gpa:.4f}\n Scale: {scale}\n")

    # Result window
    def display_result_window(self, grades, gpa, total_credit_hours, student_id, course, scale, input_win, bg_color):
        input_win.destroy()

        result_win = Tk()
        result_win.geometry("1200x750")
        result_win.title("GPA Result")
        self.apply_background_color(result_win, bg_color)

        result_label = Label(result_win, text="Your GPA Calculation Result", font=('CourierNew', 20, 'bold'), bg=result_win.cget('bg'))
        result_label.pack(pady=20)

        # Show student info
        student_info_label = Label(result_win, text=f"Student ID: {student_id} | Course: {course} | Scale: {scale}", font=('Times New Roman', 16), bg=result_win.cget('bg'))
        student_info_label.pack(pady=10)

        gpa_label = Label(result_win, text=f"GPA: {round(gpa, 4)}", font=('Times New Roman', 16), bg=result_win.cget('bg'))
        gpa_label.pack(pady=10)

        total_credit_label = Label(result_win, text=f"Total Credit Hours: {total_credit_hours}", font=('Times New Roman', 16), bg=result_win.cget('bg'))
        total_credit_label.pack(pady=10)

        # Show data
        result_table = Frame(result_win, bg=result_win.cget('bg'))
        result_table.pack(pady=10)

        headers = ['Subject', 'Grade', 'Credit Hours']
        for idx, header in enumerate(headers):
            header_label = Label(result_table, text=header, font=('Times New Roman', 14, 'bold'), width=20, anchor="w", bg=result_win.cget('bg'))
            header_label.grid(row=0, column=idx, padx=10, pady=5)

        for idx, (subject, grade, credit_hour) in enumerate(grades, start=1):
            Label(result_table, text=subject, font=('Times New Roman', 12), width=20, anchor="w", bg=result_win.cget('bg')).grid(row=idx, column=0)
            Label(result_table, text=grade, font=('Times New Roman', 12), width=20, anchor="w", bg=result_win.cget('bg')).grid(row=idx, column=1)
            Label(result_table, text=credit_hour, font=('Times New Roman', 12), width=20, anchor="w", bg=result_win.cget('bg')).grid(row=idx, column=2)

        # Return to main window button
        def return_to_main():
            result_win.destroy()
            self.welcome_win.deiconify()  # Show main window again

        exit_button = Button(result_win, text="Exit", font=('Times New Roman', 14), command=result_win.quit)
        exit_button.pack(pady=20)

        return_button = Button(result_win, text="Return to Main", font=('Times New Roman', 14), command=return_to_main)
        return_button.pack(pady=20)

        result_win.mainloop()

if __name__ == "__main__":
    GPACalculator()
