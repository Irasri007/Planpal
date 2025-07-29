import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading

class StudyScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Schedule Generator")
        self.subjects = {}
        self.today_topics = []
        self.completed_topics = set()
        self.progress_var = tk.DoubleVar(value=0)

        # UI Layout
        self.setup_ui()

        # Start thread to reset progress at 8AM
        self.schedule_reset_check()

    def setup_ui(self):
        tk.Label(self.root, text="📚 Study Schedule Generator", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.subject_entry = tk.Entry(self.root, width=40)
        self.subject_entry.insert(0, "Enter Subject Name")
        self.subject_entry.pack(pady=5)

        self.topic_entry = tk.Entry(self.root, width=40)
        self.topic_entry.insert(0, "Enter Topics (comma-separated)")
        self.topic_entry.pack(pady=5)

        self.output_display = tk.Text(self.root, height=5, width=60)
        self.output_display.pack(pady=10)

        self.progress_label = tk.Label(self.root, text="Daily Progress")
        self.progress_label.pack()
        self.progress = tk.Scale(self.root, variable=self.progress_var, from_=0, to=100, orient="horizontal", length=300, state="disabled")
        self.progress.pack()

        tk.Button(self.root, text="Add Subject & Topics", command=self.add_subject_topics).pack(pady=5)

        tk.Label(self.root, text="Days until exam:").pack()
        self.days_entry = tk.Entry(self.root)
        self.days_entry.pack()

        tk.Label(self.root, text="Hours per day:").pack()
        self.hours_entry = tk.Entry(self.root)
        self.hours_entry.pack()

        tk.Button(self.root, text="Generate Schedule", command=self.generate_schedule).pack(pady=10)

        self.checklist_frame = tk.LabelFrame(self.root, text="Checklist for Today's Topics")
        self.checklist_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def add_subject_topics(self):
        subject = self.subject_entry.get().strip()
        topics = [t.strip() for t in self.topic_entry.get().split(",") if t.strip()]
        if subject and topics:
            self.subjects[subject] = topics
            self.output_display.insert(tk.END, f"{subject}: {', '.join(topics)}\n")
            self.subject_entry.delete(0, tk.END)
            self.topic_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please enter both subject and topics.")

    def generate_schedule(self):
        try:
            total_days = int(self.days_entry.get())
            hours_per_day = float(self.hours_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for days and hours.")
            return

        # Flat list of all topics
        all_topics = [(s, t) for s, topics in self.subjects.items() for t in topics]
        total_topics = len(all_topics)
        topics_per_day = max(1, total_topics // total_days)

        # Today's topics
        self.today_topics = all_topics[:topics_per_day]
        self.completed_topics.clear()
        self.refresh_checklist()

    def refresh_checklist(self):
        for widget in self.checklist_frame.winfo_children():
            widget.destroy()

        for subject, topic in self.today_topics:
            var = tk.IntVar()
            cb = tk.Checkbutton(
                self.checklist_frame, text=f"{subject}: {topic}", variable=var,
                command=lambda s=subject, t=topic, v=var: self.update_progress(s, t, v)
            )
            cb.pack(anchor='w')

    def update_progress(self, subject, topic, var):
        if var.get():
            self.completed_topics.add((subject, topic))
        else:
            self.completed_topics.discard((subject, topic))

        if self.today_topics:
            percent_complete = (len(self.completed_topics) / len(self.today_topics)) * 100
            self.progress_var.set(percent_complete)

    def schedule_reset_check(self):
        def reset_loop():
            while True:
                now = datetime.now()
                next_reset = now.replace(hour=8, minute=0, second=0, microsecond=0)
                if now >= next_reset:
                    next_reset += timedelta(days=1)

                delay = (next_reset - now).total_seconds()
                threading.Timer(delay, self.reset_daily_progress).start()
                break

        threading.Thread(target=reset_loop, daemon=True).start()

    def reset_daily_progress(self):
        self.progress_var.set(0)
        self.completed_topics.clear()
        self.refresh_checklist()
        self.schedule_reset_check()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyScheduleApp(root)
    root.mainloop()
