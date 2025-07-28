import tkinter as tk

root = tk.Tk()
root.title("Study Schedule Generator")
root.geometry("600x600")

title_label = tk.Label(root, text="📚 Study Schedule Generator", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Subject input
subject_label = tk.Label(root, text="Enter Subject Name:")
subject_label.pack()
subject_entry = tk.Entry(root, width=40)
subject_entry.pack(pady=5)

# Topics input
topics_label = tk.Label(root, text="Enter Topics (comma-separated):")
topics_label.pack()
topics_entry = tk.Entry(root, width=40)
topics_entry.pack(pady=5)

# Display added subjects
added_text = tk.Text(root, height=6, width=60)
added_text.pack(pady=10)

study_data = []

def add_subject():
    subject = subject_entry.get().strip()
    topics = topics_entry.get().strip()

    if subject and topics:
        topic_list = [t.strip() for t in topics.split(",")]
        study_data.append((subject, topic_list))
        added_text.insert(tk.END, f"{subject}: {', '.join(topic_list)}\n")
        subject_entry.delete(0, tk.END)
        topics_entry.delete(0, tk.END)

add_button = tk.Button(root, text="Add Subject & Topics", command=add_subject)
add_button.pack(pady=10)

# Exam timeline inputs
days_label = tk.Label(root, text="How many days until your exam?")
days_label.pack()
days_entry = tk.Entry(root, width=20)
days_entry.pack(pady=5)

hours_label = tk.Label(root, text="How many hours can you study per day?")
hours_label.pack()
hours_entry = tk.Entry(root, width=20)
hours_entry.pack(pady=5)

# Output box for schedule
output_text = tk.Text(root, height=12, width=70)
output_text.pack(pady=10)

def generate_plan():
    output_text.delete(1.0, tk.END)

    try:
        total_days = int(days_entry.get())
        hours_per_day = int(hours_entry.get())
    except ValueError:
        output_text.insert(tk.END, "Please enter valid numbers for days and hours.")
        return

    all_topics = []
    for subject, topics in study_data:
        for topic in topics:
            all_topics.append((subject, topic))

    if total_days == 0:
        output_text.insert(tk.END, "You must have at least 1 day until the exam.")
        return

    topics_per_day = max(1, len(all_topics) // total_days)
    schedule = []
    idx = 0

    for day in range(1, total_days + 1):
        today = []
        for _ in range(topics_per_day):
            if idx < len(all_topics):
                today.append(all_topics[idx])
                idx += 1
        schedule.append(today)

    while idx < len(all_topics):
        schedule[idx % total_days].append(all_topics[idx])
        idx += 1

    output_text.insert(tk.END, "📆 Your Study Plan:\n\n")
    for i, day in enumerate(schedule):
        output_text.insert(tk.END, f"Day {i+1}:\n")
        for subject, topic in day:
            output_text.insert(tk.END, f"  - {subject}: {topic}\n")
        output_text.insert(tk.END, "\n")

generate_button = tk.Button(root, text="Generate Plan", command=generate_plan, bg="green", fg="white", padx=10, pady=5)
generate_button.pack(pady=10)

# Bring window to front
print("✅ Full app running!")
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

root.mainloop()
