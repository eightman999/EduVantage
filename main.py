# main.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.filedialog
from data_loader import load_data
import numpy as np
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats
from scipy.interpolate import interp1d
import ED_logo

# Create the main window
root = tk.Tk()
windowmode = None
grades_data = None
mean = None
mode = None
median = None
std_dev = None
options = None
settings_window = None
task_index = None
right_sub_frame = None

root.title("EduVantage")
root.geometry("1280x720")  # Change the window size to 1280x720
data_address = ""

# Create a StringVar for the task name
task_name = tk.StringVar()
task_name.set("Report_ID")
submission_count = tk.StringVar()
# Create a StringVar for the statistics
mean_str = tk.StringVar()
mode_str = tk.StringVar()
median_str = tk.StringVar()


# Set the window icon
image = Image.open("GUI/minilogo.png")
photo = ImageTk.PhotoImage(image)
ed_logo = ED_logo.get_photo_image4icon()
root.iconphoto(False, photo)

# Define the main frames
left_frame = tk.Frame(root, width=150, height=50)  # Set the height to 50px
left_frame.pack(side="left", fill="y")

top_frame = tk.Frame(root, height=50)  # Set the height to 50px
top_frame.pack(side="top", fill="x")

center_frame = tk.Frame(root)
center_frame.pack(expand=True, fill="both")

# Add buttons to the left frame
settings_button_left = tk.Button(left_frame, text="設定", width=10, height=2)  # Set the height to 2 (approximately 50px)
settings_button_left.pack(pady=10)

home_button = tk.Button(left_frame, relief=tk.SUNKEN, text="ホーム", width=10, height=2)  # Set the height to 2 (approximately 50px)
home_button.pack(pady=10)

class_button = tk.Button(left_frame,relief=tk.RAISED, text="クラス", width=10, height=2)  # Set the height to 2 (approximately 50px)
class_button.pack(pady=10)

individual_button = tk.Button(left_frame,relief=tk.RAISED, text="個人", width=10, height=2)  # Set the height to 2 (approximately 50px)
individual_button.pack(pady=10)

# Add widgets to the top frame
dropdown = ttk.Combobox(top_frame, state="readonly", height=10)  # Set the height to 2 (approximately 50px)
dropdown.pack(side="left", padx=10, pady=10)

address_label = tk.Label(top_frame, text="address:", height=2)  # Set the height to 2 (approximately 50px)
address_label.pack(side="left", padx=10, pady=10)

address_entry = tk.Entry(top_frame, width=50)
address_entry.pack(side="left", padx=10, pady=10)

settings_button_top = tk.Button(top_frame, text="読み込み", width=10, height=2)  # Set the height to 2 (approximately 50px)
settings_button_top.pack(side="right", padx=10, pady=10)

# Placeholder for center content
center_content = tk.Label(center_frame, text="Center Content Area", bg="white")
center_content.pack(expand=True, fill="both", padx=10, pady=10)

# Define the event handlers for the buttons
def switch_to_home():
    global windowmode
    windowmode = 0
    for widget in center_frame.winfo_children():
        widget.destroy()

    # Create the center content
    global center_content
    center_content = tk.Label(center_frame, bg="white")
    center_content.pack(expand=True, fill="both", padx=10, pady=10)

    # Update the center content and button states
    center_content.config(image=ed_logo)
    center_content.image = ed_logo
    home_button.config(relief=tk.SUNKEN)
    class_button.config(relief=tk.RAISED)
    individual_button.config(relief=tk.RAISED)

def switch_to_class():
    global windowmode
    global task_index
    global right_sub_frame
    windowmode = 1
    # Clear the center frame
    for widget in center_frame.winfo_children():
        widget.destroy()

    if grades_data is None:
        # Show warning dialog
        tkinter.messagebox.showwarning("Warning", "データが読み込まれていません。")
        # Switch to home
        switch_to_home()
        return

    # Create the sub-frames
    left_sub_frame = tk.Frame(center_frame, width=200, bd=2, relief="solid")
    left_sub_frame.pack(side="left", fill="y")

    right_sub_frame = tk.Frame(center_frame, bd=2, relief="solid")
    right_sub_frame.pack(side="top", expand=True, fill="both")

    # Add widgets to the left sub-frame
    tk.Label(left_sub_frame, text="課題名: ").pack(anchor="w", padx=10, pady=5)
    # Bind the task_name StringVar to the label
    task_name_label = tk.Label(left_sub_frame, textvariable=task_name)
    task_name_label.pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="提出:").pack(anchor="w", padx=10, pady=5)
    # Bind the submission_count StringVar to the label
    submission_count_label = tk.Label(left_sub_frame, textvariable=submission_count)
    submission_count_label.pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="-" * 30).pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="平均点:").pack(anchor="w", padx=10, pady=5)
    # Bind the mean_str StringVar to the label
    mean_label = tk.Label(left_sub_frame, textvariable=mean_str)
    mean_label.pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="中央値:").pack(anchor="w", padx=10, pady=5)
    # Bind the median_str StringVar to the label
    median_label = tk.Label(left_sub_frame, textvariable=median_str)
    median_label.pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="最頻値:").pack(anchor="w", padx=10, pady=5)
    # Bind the mode_str StringVar to the label
    mode_label = tk.Label(left_sub_frame, textvariable=mode_str)
    mode_label.pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="-" * 30).pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="予想理解度 mm%").pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="予想意欲値 MM").pack(anchor="w", padx=10, pady=5)
    tk.Label(left_sub_frame, text="-" * 30).pack(anchor="w", padx=10, pady=5)
    # Placeholder for right sub-frame content
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    selected_option = dropdown.get()

    if selected_option in options:
        task_index = options.index(selected_option)
        if task_index + 1 < len(options):
            task_index += 1
        else:
            task_index = -1  # or any default value

    if len(grades_data[0]) > task_index:
        data = [row[task_index] for row in grades_data if pd.notna(row[task_index])]
        counts, bins, patches = ax.hist(data, bins=50, density=True, alpha=0.6, color='g', rwidth=1)

        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        if mean is not None and std_dev is not None and task_index < len(mean) and task_index < len(std_dev):
            p = stats.norm.pdf(x, mean[task_index], std_dev[task_index])
            ax.plot(x, p, 'k', linewidth=2)

    # Create a canvas and add it to the right sub-frame
    canvas = FigureCanvasTkAgg(fig, master=right_sub_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    # Create the bottom sub-frame for the buttons
    bottom_sub_frame = tk.Frame(center_frame, height=40)
    bottom_sub_frame.pack(side="top", fill="x")

    # Add buttons to the bottom sub-frame
    grade_rank_button = tk.Button(bottom_sub_frame, text="評定", width=15)
    grade_rank_button.pack(side="left", padx=10, pady=10)
    rank_button = tk.Button(bottom_sub_frame, text="順位", width=15)
    rank_button.pack(side="left", padx=10, pady=10)
    id_order_button = tk.Button(bottom_sub_frame, text="ID順", width=15)
    id_order_button.pack(side="left", padx=10, pady=10)
    bias_button = tk.Button(bottom_sub_frame, text="偏差", width=15)
    bias_button.pack(side="left", padx=10, pady=10)

    rank_button.config(command=display_rank)
    bias_button.config(command=switch_to_class)
    # Update the button states
    home_button.config(relief=tk.RAISED)
    class_button.config(relief=tk.SUNKEN)
    individual_button.config(relief=tk.RAISED)

def switch_to_individual():
    windowmode = 2
    print("Switching to class view...")
    if grades_data is None:
        # Show warning dialog
        tkinter.messagebox.showwarning("Warning", "データが読み込まれていません。")
        print("no data to class view...")
        # Switch to home
        switch_to_home()
    else:
        # Clear the center frame
        print("Switching to class view...")
        for widget in center_frame.winfo_children():
            widget.destroy()
        home_button.config(relief=tk.RAISED)
        class_button.config(relief=tk.RAISED)
        individual_button.config(relief=tk.SUNKEN)
    return

def load_data_from_file():
    global data_address
    global windowmode
    global grades_data
    global options  # Add this line
    settings_button_top.config(relief=tk.SUNKEN)
    print("Opening file dialog...")
    # Open the file dialog and get the selected file path
    data_address = tkinter.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if data_address:  # Check if a file was selected
        # Update the address entry with the selected file path
        address_entry.delete(0, tk.END)
        address_entry.insert(0, data_address)

        # Load the data from the CSV file
        options, grades_data, mean, mode, median, std_dev = load_data(data_address)

        # Set the options for the dropdown
        dropdown['values'] = options
        dropdown.set("課題を選択")

        print(grades_data)
    else:
        print("No file selected.")
    windowmode = 1
    settings_button_top.config(relief=tk.RAISED)

def open_settings():
    global settings_window  # Add this line
    settings_button_left.config(relief=tk.SUNKEN)
    settings_window = tk.Toplevel(root)
    settings_window.geometry("400x600")
    settings_window.title("設定")
    settings_window.protocol("WM_DELETE_WINDOW", close_settings)

def close_settings():
    settings_button_left.config(relief=tk.RAISED)
    settings_window.destroy()

def calculate_submission_count(grades_data, task_index):

    total_count = len(grades_data)
    # Count the number of non-NaN elements in the task_index column
    submission_count = sum(1 for row in grades_data if len(row) > task_index and pd.notna(row[task_index]))
    print("submission_count:"+str(submission_count))  # Convert submission_count to string before concatenating
    return f"{submission_count}/{total_count} ({submission_count/total_count*100:.2f}%)"

def on_dropdown_change(event):
    global windowmode
    selected_option = dropdown.get()
    task_name.set(selected_option)

    # Calculate the submission count for the selected task
    task_index = options.index(selected_option)
    if task_index + 1 < len(options):
        task_index += 1
    else:
        task_index = -1  # or any default value

    submission_count.set(calculate_submission_count(grades_data, task_index))

    # Update the statistics for the selected task
    if mean is not None and task_index < len(mean):
        mean_str.set(f"{mean[task_index]:.2f}")
    if mode is not None and task_index < len(mode):
        mode_str.set(f"{mode[task_index]:.2f}")
    if median is not None and task_index < len(median):
        median_str.set(f"{median[task_index]:.2f}")
    if selected_option == "全てのReport":
        # Display the "All Reports" view
        pass
    elif selected_option == "全てのExam":
        # Display the "All Exams" view
        pass
    elif selected_option == "SUM":
        # Display the "SUM" view
        pass
    else:
        # Display the view for the selected option
        pass
    print(windowmode)
    if windowmode == 1:
        switch_to_class()
    elif windowmode == 2:
        switch_to_individual()
    else:
        switch_to_home()

def display_rank():
    global right_sub_frame
    # Clear the right sub-frame
    for widget in right_sub_frame.winfo_children():
        widget.destroy()

    # Create a listbox in the right sub-frame
    listbox = tk.Listbox(right_sub_frame)
    listbox.pack(fill="both", expand=True)

    # Get the selected task
    selected_option = dropdown.get()

    if selected_option in options:
        task_index = options.index(selected_option)
        if task_index + 1 < len(options):
            task_index += 1
        else:
            task_index = -1  # or any default value

    # Create a list of tuples (ID, score) and sort it by score
    score_list = sorted((row[0], row[task_index]) for row in grades_data if pd.notna(row[task_index]))

    # Add the sorted scores to the listbox
    for id, score in score_list:
        listbox.insert(tk.END, f"ID: {id}, Score: {score}")

# Attach the event handlers to the buttons
home_button.config(command=switch_to_home)
class_button.config(command=switch_to_class)
individual_button.config(command=switch_to_individual)
settings_button_top.config(command=load_data_from_file)
settings_button_left.config(command=open_settings)

# Attach the event handler to the dropdown
dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

# Set the initial view to home
switch_to_home()

# Start the main event loop
root.mainloop()