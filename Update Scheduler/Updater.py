import tkinter as tk
from tkinter import messagebox
from crontab import CronTab

def set_cron_job(hour, minute):
    # Create a cron object for the current user by specifying the user name directly
    cron = CronTab(user=True)  # Adjusted initialization
    cron.remove_all(comment="update_job")

    job = cron.new(command='sudo apt-get update && sudo apt-get upgrade -y', comment="update_job")
    job.minute.on(minute)
    job.hour.on(hour)
    cron.write()

    messagebox.showinfo("Success", f"Update scheduled at {hour:02d}:{minute:02d} every day.")

def clear_cron_job():
    # Create a cron object for the current user by specifying the user name directly
    cron = CronTab(user=True)  # Adjusted initialization
    cron.remove_all(comment="update_job")
    cron.write()

def validate_time(hour, minute):
    try:
        hour = int(hour)
        minute = int(minute)
        if 0 <= hour < 24 and 0 <= minute < 60:
            return True
        else:
            return False
    except ValueError:
        return False

def schedule_update():
    if toggle_var.get():  # Check if the toggle switch is on
        hour = hour_entry.get()
        minute = minute_entry.get()
        if validate_time(hour, minute):
            set_cron_job(int(hour), int(minute))
        else:
            messagebox.showerror("Error", "Invalid time. Please enter hour (0-23) and minute (0-59).")
    else:
        clear_cron_job()
        messagebox.showinfo("Disabled", "Scheduled updates have been disabled.")

# Create the GUI window
root = tk.Tk()
root.title("Update Scheduler")
root.geometry("400x275")

# Add a label
label = tk.Label(root, text="Set update time (24-hour format)")
label.pack(pady=10)

# Frame for hour and minute entries
frame = tk.Frame(root)
frame.pack(pady=10)

# Hour entry
hour_label = tk.Label(frame, text="Hour:")
hour_label.grid(row=0, column=0, padx=5, pady=5)
hour_entry = tk.Entry(frame, width=5)
hour_entry.grid(row=0, column=1, padx=5, pady=5)

# Minute entry
minute_label = tk.Label(frame, text="Minute:")
minute_label.grid(row=1, column=0, padx=5, pady=5)
minute_entry = tk.Entry(frame, width=5)
minute_entry.grid(row=1, column=1, padx=5, pady=5)

# Toggle switch
toggle_var = tk.BooleanVar(value=False)
toggle_switch = tk.Checkbutton(root, text="Enable Scheduling", variable=toggle_var, onvalue=True, offvalue=False)
toggle_switch.pack(pady=10)

# Apply Settings Button
apply_button = tk.Button(root, text="Apply Settings", command=schedule_update)
apply_button.pack(pady=20)

# Ensure the main loop is at the end
root.mainloop()
