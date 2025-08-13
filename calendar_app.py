import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import json
from tkinter import messagebox
import os

class Event:
    def __init__(self, title, date, time, category="default", invited_users=None):
        self.title = title
        self.date = date
        self.time = time
        self.category = category
        self.invited_users = invited_users or []
    
    def to_dict(self):
        return {
            'title': self.title,
            'date': self.date,
            'time': self.time,
            'category': self.category,
            'invited_users': self.invited_users
        }
    
    @classmethod
    def from_dict(cls, data):
        event = cls(data['title'], data['date'], data['time'], data['category'])
        event.invited_users = data.get('invited_users', [])
        return event

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar App")
        self.root.geometry("1200x700")
        
        self.events = []
        self.categories = ["Default", "Work", "Personal", "Meeting"]
        self.category_colors = {
            "Default": "gray",
            "Work": "blue",
            "Personal": "green",
            "Meeting": "red"
        }
        
        self.current_view = "monthly"
        self.load_events()
        self.setup_gui()
        
        self.current_user = "ashton"
        
    def setup_gui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for calendar
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # View selection at top of left frame
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="View:").pack(side=tk.LEFT)
        views = ["daily", "weekly", "monthly"]
        self.view_var = tk.StringVar(value="monthly")
        for view in views:
            ttk.Radiobutton(control_frame, text=view.capitalize(), variable=self.view_var, value=view, command=self.change_view).pack(side=tk.LEFT)
        
        # Content frame for calendar views
        self.content_frame = ttk.Frame(left_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Right frame for event management
        right_frame = ttk.Frame(main_container, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Event management section
        self.setup_event_panel(right_frame)
        
        # Initialize with monthly view
        self.show_monthly_view()
        
    def setup_event_panel(self, right_frame):
        ttk.Label(right_frame, text="Add New Event", font=("TkDefaultFont", 12, "bold")).pack(pady=(30,0))
        
        # Event details inputs
        self.event_title = ttk.Entry(right_frame, width=30)
        ttk.Label(right_frame, text="Title:").pack(pady=(10,0))
        self.event_title.pack(pady=(0,10))
        
        ttk.Label(right_frame, text="Time:").pack()
        time_frame = ttk.Frame(right_frame)
        time_frame.pack(pady=5)
        self.hour_var = tk.StringVar(value="00")
        self.minute_var = tk.StringVar(value="00")
        
        ttk.Spinbox(time_frame, from_=0, to=23, width=3,
                   textvariable=self.hour_var).pack(side=tk.LEFT)
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT)
        ttk.Spinbox(time_frame, from_=0, to=59, width=3, textvariable=self.minute_var).pack(side=tk.LEFT)
        
        ttk.Label(right_frame, text="Category:").pack(pady=(10,0))
        self.category_var = tk.StringVar(value=self.categories[0])
        category_dropdown = ttk.Combobox(right_frame, textvariable=self.category_var, values=self.categories, width=27)
        category_dropdown.pack(pady=5)
        
        ttk.Label(right_frame, text="Invite Users (comma-separated emails):").pack(pady=(10,0))
        self.invited_users_entry = ttk.Entry(right_frame, width=30)
        self.invited_users_entry.pack(pady=5)
        
        ttk.Button(right_frame, text="Add Event",
                  command=self.add_event).pack(pady=10)
        
        # Events list
        ttk.Label(right_frame, text="Events for Selected Date").pack(pady=(20,5))
        list_frame = ttk.Frame(right_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.events_listbox = tk.Text(list_frame, width=35, height=15, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.events_listbox.yview)
        
        ttk.Button(right_frame, text="Delete Selected Event",
                  command=self.delete_event).pack(pady=5)
    
    def show_daily_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        today = datetime.now()
        day_frame = ttk.Frame(self.content_frame)
        day_frame.pack(fill=tk.BOTH, expand=True)
        
        # 24-hour timeline
        for hour in range(24):
            hour_frame = ttk.Frame(day_frame)
            hour_frame.pack(fill=tk.X)
            ttk.Label(hour_frame, text=f"{hour:02d}:00",
                     width=10).pack(side=tk.LEFT)
            
            # Show events for this hour
            events_at_hour = [e for e in self.events 
                            if e.date == today.strftime('%Y-%m-%d') and 
                            int(e.time.split(':')[0]) == hour]
            
            for event in events_at_hour:
                event_label = ttk.Label(hour_frame, text=f"{event.title} ({event.category})", foreground=self.category_colors[event.category])
                event_label.pack(side=tk.LEFT)
    
    def show_weekly_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        week_frame = ttk.Frame(self.content_frame)
        week_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get current week dates
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        # Create columns for each day
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_frame = ttk.Frame(week_frame)
            day_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            ttk.Label(day_frame, text=day.strftime('%A\n%Y-%m-%d')).pack()
            
            # Show events for this day
            day_events = [e for e in self.events 
                          if e.date == day.strftime('%Y-%m-%d')]
            
            for event in day_events:
                event_label = ttk.Label(day_frame, text=f"{event.time} - {event.title}", foreground=self.category_colors[event.category])
                event_label.pack()
    
    def show_monthly_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.cal = Calendar(self.content_frame, selectmode='day', date_pattern='y-mm-dd')
        self.cal.pack(fill=tk.BOTH, expand=True)
        self.cal.bind('<<CalendarSelected>>', self.update_events_list)
        
        # Mark dates with events
        for event in self.events:
            self.cal.calevent_create(datetime.strptime(event.date, '%Y-%m-%d'), event.title, event.category)
    
    def change_view(self):
        view = self.view_var.get()
        if view == "daily":
            self.show_daily_view()
        elif view == "weekly":
            self.show_weekly_view()
        else:
            self.show_monthly_view()
    
    def add_event(self):
        title = self.event_title.get()
        if not title:
            messagebox.showwarning("Warning", "Please enter an event title")
            return
        
        invited_users = [email.strip() for email in 
                        self.invited_users_entry.get().split(',') if email.strip()]
        
        date = self.cal.get_date() if self.current_view == "monthly" else datetime.now().strftime('%Y-%m-%d')
        time = f"{self.hour_var.get()}:{self.minute_var.get()}"
        category = self.category_var.get()
        
        new_event = Event(title, date, time, category, invited_users)
        self.events.append(new_event)
        
        self.save_events()
        self.event_title.delete(0, tk.END)
        self.invited_users_entry.delete(0, tk.END)
        self.change_view()
        self.update_events_list()
    
    def delete_event(self):
        try:
            selection = self.events_listbox.tag_ranges(tk.SEL)
            if not selection:
                return
            
            # Get the line number of the selection start
            line_start = int(float(self.events_listbox.index(selection[0])))
            
            if self.current_view == "monthly":
                selected_date = self.cal.get_date()
                daily_events = [e for e in self.events if e.date == selected_date]
                if line_start // 5 < len(daily_events):  # 5 lines per event (including separator)
                    self.events.remove(daily_events[line_start // 5])
                    self.save_events()
                    self.change_view()
                    self.update_events_list()
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select an event to delete")
    
    def update_events_list(self, event=None):
        self.events_listbox.delete('1.0', tk.END)
        
        if self.current_view == "monthly":
            selected_date = self.cal.get_date()
            filtered_events = [e for e in self.events if e.date == selected_date]
        else:
            filtered_events = self.events
        
        for event in filtered_events:
            # Format event text with color and proper line breaks
            event_text = f"Title: {event.title}\n"
            event_text += f"Time: {event.time}\n"
            event_text += f"Category: {event.category}\n"
            if event.invited_users:
                event_text += f"Invited: {', '.join(event.invited_users)}\n"
            event_text += "-" * 30 + "\n"
            
            # Insert text with color tags
            tag_name = f"color_{event.category}"
            self.events_listbox.tag_configure(tag_name, 
                                           foreground=self.category_colors[event.category])
            self.events_listbox.insert(tk.END, event_text, tag_name)
  
    def save_events(self):
        events_data = [event.to_dict() for event in self.events]
        with open('calendar_events.json', 'w') as f:
            json.dump(events_data, f)
    
    def load_events(self):
        try:
            with open('calendar_events.json', 'r') as f:
                events_data = json.load(f)
                self.events = [Event.from_dict(data) for data in events_data]
        except FileNotFoundError:
            self.events = []

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()