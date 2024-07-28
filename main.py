import math
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import tkinter.filedialog

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from data_loader import load_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats
import ui_loader
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

# Create the main window
root = tk.Tk()
windowmode = None
grades_data = None
grades_name = None
grade_setting = [["E", 0, 30], ["D", 31, 50], ["C", 51, 70], ["B", 71, 90], ["A", 91, 150]]
task_names = None
mean = None
mode = None
median = None
std_dev = None
options = None
settings_window = None
task_index = None
right_sub_frame = None
is_saved = True

# Load the default font
default_font = ui_loader.get_default_font()

# Apply the default font to the entire application
root.option_add("*Font", default_font.get_name())

root.title("EduVantage")
root.geometry("1280x720")  # Change the window size to 1280x720
data_address = ""
pdfmetrics.registerFont(TTFont('PC-9800', 'GUI/fonts/default.ttf'))

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
ed_logo = ui_loader.get_photo_image4icon()
root.iconphoto(False, photo)

# Define the main frames
left_frame = tk.Frame(root, width=150, height=50)  # Set the height to 50px
left_frame.pack(side="left", fill="y")

top_frame = tk.Frame(root, height=50)  # Set the height to 50px
top_frame.pack(side="top", fill="x")

center_frame = tk.Frame(root)
center_frame.pack(expand=True, fill="both")

# Add buttons to the left frame
settings_button_left = tk.Button(left_frame, text="設定", width=10,
                                 height=2)  # Set the height to 2 (approximately 50px)
settings_button_left.pack(pady=10)

home_button = tk.Button(left_frame, relief=tk.SUNKEN, text="ホーム", width=10,
                        height=2)  # Set the height to 2 (approximately 50px)
home_button.pack(pady=10)

class_button = tk.Button(left_frame, relief=tk.RAISED, text="クラス", width=10,
                         height=2)  # Set the height to 2 (approximately 50px)
class_button.pack(pady=10)

individual_button = tk.Button(left_frame, relief=tk.RAISED, text="個人", width=10,
                              height=2)  # Set the height to 2 (approximately 50px)
individual_button.pack(pady=10)

# Add widgets to the top frame
dropdown = ttk.Combobox(top_frame, state="readonly", height=10)  # Set the height to 2 (approximately 50px)
dropdown.pack(side="left", padx=10, pady=10)

address_label = tk.Label(top_frame, text="address:", height=2)  # Set the height to 2 (approximately 50px)
address_label.pack(side="left", padx=10, pady=10)

address_entry = tk.Entry(top_frame, width=50)
address_entry.pack(side="left", padx=10, pady=10)

settings_button_top = tk.Button(top_frame, text="読み込み", width=10,
                                height=2)  # Set the height to 2 (approximately 50px)
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
    # tk.Label(left_sub_frame, text="予想理解度 mm%").pack(anchor="w", padx=10, pady=5)
    # tk.Label(left_sub_frame, text="予想意欲値 MM").pack(anchor="w", padx=10, pady=5)
    # tk.Label(left_sub_frame, text="-" * 30).pack(anchor="w", padx=10, pady=5)
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
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontproperties(default_font)

    # Create a canvas and add it to the right sub-frame
    canvas = FigureCanvasTkAgg(fig, master=right_sub_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    # Create the bottom sub-frame for the buttons
    bottom_sub_frame = tk.Frame(center_frame, height=40)
    bottom_sub_frame.pack(side="top", fill="x")

    # Add buttons to the bottom sub-frame
    # grade_rank_button = tk.Button(bottom_sub_frame, text="評定", width=15)
    # grade_rank_button.pack(side="left", padx=10, pady=10)
    id_order_button = tk.Button(bottom_sub_frame, text="ID順", width=15)
    id_order_button.pack(side="left", padx=10, pady=10)
    # bias_button = tk.Button(bottom_sub_frame, text="偏差", width=15)
    # bias_button.pack(side="left", padx=10, pady=10)

    # rank_button.config(command=display_rank)
    # bias_button.config(command=display_standard_deviation)
    id_order_button.config(command=display_id_order)

    if selected_option == "全てのReport":
        trend_button = tk.Button(bottom_sub_frame, text="推移", width=15)
        trend_button.pack(side="left", padx=10, pady=10)
        trend_button.config(command=display_report_trends)

    if selected_option == "全てのExam":
        trend_button = tk.Button(bottom_sub_frame, text="推移", width=15)
        trend_button.pack(side="left", padx=10, pady=10)
        trend_button.config(command=display_exam_trends)

    # Update the button states
    home_button.config(relief=tk.RAISED)
    class_button.config(relief=tk.SUNKEN)
    individual_button.config(relief=tk.RAISED)


# Update the graph functions to use the new apply_font_to_graph function
def apply_font_to_plot(ax, default_font):
    for line in ax.get_lines():
        line.set_label(line.get_label())
    ax.legend(prop=default_font)
    ax.title.set_fontproperties(default_font)
    ax.xaxis.label.set_fontproperties(default_font)
    ax.yaxis.label.set_fontproperties(default_font)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontproperties(default_font)


# Update the graph functions to use the new apply_font_to_plot function
def display_exam_trends():
    global right_sub_frame
    for widget in right_sub_frame.winfo_children():
        widget.destroy()

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    exam_columns = [col for col in options if 'Exam' in col and col != "全てのExam"]
    exam_means = [mean[options.index(col)] for col in exam_columns]
    exam_modes = [mode[options.index(col)] for col in exam_columns]
    exam_medians = [median[options.index(col)] for col in exam_columns]

    ax.plot(exam_columns, exam_means, marker='o', label='平均')
    ax.plot(exam_columns, exam_modes, marker='o', label='最頻')
    ax.plot(exam_columns, exam_medians, marker='o', label='中央')

    ax.set_title('Exam の 点数推移')
    ax.set_xlabel('Exams')
    ax.set_ylabel('Values')
    ax.legend()

    apply_font_to_plot(ax, default_font)

    canvas = FigureCanvasTkAgg(fig, master=right_sub_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def display_report_trends():
    global right_sub_frame
    for widget in right_sub_frame.winfo_children():
        widget.destroy()

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    report_columns = [col for col in options if 'Report' in col and col != "全てのReport"]
    report_means = [mean[options.index(col)] for col in report_columns]
    report_modes = [mode[options.index(col)] for col in report_columns]
    report_medians = [median[options.index(col)] for col in report_columns]

    ax.plot(report_columns, report_means, marker='o', label='平均')
    ax.plot(report_columns, report_modes, marker='o', label='最頻')
    ax.plot(report_columns, report_medians, marker='o', label='中央')

    ax.set_title('Report の 点数推移')
    ax.set_xlabel('Reports')
    ax.set_ylabel('Values')
    ax.legend()

    apply_font_to_plot(ax, default_font)

    canvas = FigureCanvasTkAgg(fig, master=right_sub_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def load_data_from_file():
    global data_address
    global windowmode
    global grades_data
    global grades_name
    global options
    global mean
    global mode
    global median
    global std_dev
    global weight
    global pass_score

    settings_button_top.config(relief=tk.SUNKEN)
    print("Opening file dialog...")
    data_address = tkinter.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if data_address:
        address_entry.delete(0, tk.END)
        address_entry.insert(0, data_address)

        options, grades_data, grades_name, mean, mode, median, std_dev = load_data(data_address)

        dropdown['values'] = options
        dropdown.set("課題を選択")

        weight = [1] * len(options)
        pass_score = [60] * len(options)

        print(grades_data)
    else:
        print("No file selected.")
    windowmode = 1
    settings_button_top.config(relief=tk.RAISED)


def open_settings():
    global settings_window
    settings_button_left.config(relief=tk.SUNKEN)
    settings_window = tk.Toplevel(root)
    settings_window.geometry("400x600")
    settings_window.title("設定")
    settings_window.protocol("WM_DELETE_WINDOW", close_settings)

    # 課題セクション
    task_frame = tk.LabelFrame(settings_window, text="課題", padx=10, pady=10)
    task_frame.pack(fill="x", padx=10, pady=10)

    for i, task in enumerate(options):
        if task not in ["全てのReport", "全てのExam", "SUM"]:
            task_button = tk.Button(task_frame, text=task, command=lambda i=i: open_task_dialog(i))
            task_button.pack(fill="x", padx=10, pady=5)

    # 評定セクション
    evaluation_frame = tk.LabelFrame(settings_window, text="評定", padx=10, pady=10)
    evaluation_frame.pack(fill="x", padx=10, pady=10)

    evaluation_button = tk.Button(evaluation_frame, text="評定設定", width=10, command=open_evaluation_settings)
    evaluation_button.pack(pady=10)

    # 元データセクション
    data_frame = tk.LabelFrame(settings_window, text="元データ", padx=10, pady=10)
    data_frame.pack(fill="x", padx=10, pady=10)

    edit_button = tk.Button(data_frame, text="編集", width=10, command=open_edit_dialog)
    edit_button.pack(pady=10)


def open_evaluation_settings():
    global grade_setting
    evaluation_dialog = tk.Toplevel(settings_window)
    evaluation_dialog.geometry("400x300")
    evaluation_dialog.title("評定設定")

    # Create the frame for the list and buttons
    list_frame = tk.Frame(evaluation_dialog)
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create the Treeview for the grade settings
    columns = ("評定", "最低", "最高")
    grade_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
    for col in columns:
        grade_tree.heading(col, text=col)
    grade_tree.pack(side="left", fill="both", expand=True)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=grade_tree.yview)
    grade_tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Add buttons for adding and removing rows
    button_frame = tk.Frame(evaluation_dialog)
    button_frame.pack(fill="x", padx=10, pady=10)

    add_button = tk.Button(button_frame, text="+", command=lambda: add_grade_setting(grade_tree))
    add_button.pack(side="left", padx=5)

    remove_button = tk.Button(button_frame, text="-", command=lambda: remove_grade_setting(grade_tree))
    remove_button.pack(side="left", padx=5)

    save_button = tk.Button(button_frame, text="保存",
                            command=lambda: save_evaluation_settings(evaluation_dialog, grade_tree))
    save_button.pack(side="right", padx=5)

    # Load existing grade settings
    if grade_setting:
        for grade in grade_setting:
            grade_tree.insert("", "end", values=(grade[0], str(grade[1]), str(grade[2])))

    # Bind double-click event to edit cell
    grade_tree.bind("<Double-1>", lambda event: edit_cell(event, grade_tree))


def save_evaluation_settings(dialog, tree):
    global grade_setting
    grade_setting = []
    for item in tree.get_children():
        values = tree.item(item, "values")
        grade_setting.append([values[0], int(values[1]), int(values[2])])
    dialog.destroy()


def edit_cell(event, tree):
    # Get the region clicked
    region = tree.identify("region", event.x, event.y)
    if region == "cell":
        # Get the column and row clicked
        column = tree.identify_column(event.x)
        row = tree.identify_row(event.y)
        if row and column:
            # Get the cell value
            item = tree.item(row)
            values = item["values"]
            col_index = int(column.replace("#", "")) - 1

            # Create an Entry widget for editing
            entry = tk.Entry(tree)
            entry.insert(0, values[col_index])
            entry.select_range(0, tk.END)
            entry.focus()

            # Place the Entry widget in the cell
            bbox = tree.bbox(row, column)
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

            # Bind events to save the edited value
            entry.bind("<Return>", lambda e: save_edit(entry, tree, row, col_index))
            entry.bind("<FocusOut>", lambda e: save_edit(entry, tree, row, col_index))


def save_edit(entry, tree, row, col_index):
    # Get the new value from the Entry widget
    new_value = entry.get()
    # Update the Treeview item with the new value
    values = list(tree.item(row, "values"))
    values[col_index] = new_value
    tree.item(row, values=values)
    # Destroy the Entry widget
    entry.destroy()


def add_grade_setting(tree):
    tree.insert("", "end", values=("新しい評定", "0", "100"))


def remove_grade_setting(tree):
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)


def open_edit_dialog():
    global is_saved
    is_saved = True  # ダイアログを開いた時点では保存されているとみなす

    edit_dialog = tk.Toplevel(settings_window)
    edit_dialog.geometry("600x400")
    edit_dialog.title("CSVファイルの編集")

    # CSVファイルを読み込む
    df = pd.read_csv(data_address)

    # Treeviewウィジェットを作成
    tree = ttk.Treeview(edit_dialog, columns=list(df.columns), show='headings')
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    # 列ヘッダーを設定
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    # データをTreeviewに挿入
    for index, row in df.iterrows():
        tree.insert('', 'end', values=list(row))

    # セル編集のためのイベントバインド
    def on_double_click(event):
        item = tree.selection()[0]
        column = tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1
        entry = tk.Entry(edit_dialog)
        entry.insert(0, tree.item(item, 'values')[column_index])
        entry.bind('<Return>', lambda e: update_cell(entry, item, column_index))
        entry.place(x=event.x, y=event.y)

    def update_cell(entry, item, column_index):
        new_value = entry.get()
        values = list(tree.item(item, 'values'))
        values[column_index] = new_value
        tree.item(item, values=values)
        entry.destroy()
        global is_saved
        is_saved = False

    tree.bind('<Double-1>', on_double_click)

    # ボタンフレーム
    button_frame = tk.Frame(edit_dialog)
    button_frame.pack(fill="x", padx=10, pady=10)

    # 上書き保存ボタン
    save_button = tk.Button(button_frame, text="上書き保存", command=lambda: save_csv(tree, data_address))
    save_button.pack(side="left", padx=5)

    # 名前をつけて保存ボタン
    save_as_button = tk.Button(button_frame, text="名前をつけて保存", command=lambda: save_csv_as(tree))
    save_as_button.pack(side="left", padx=5)

    # 警告ラベル
    warning_label = tk.Label(button_frame, text="※自動計算によって定義されている場合、データが壊れることがあります",
                             fg="red")
    warning_label.pack(side="right", padx=5)

    # 閉じるボタン
    close_button = tk.Button(button_frame, text="閉じる", command=lambda: close_edit_dialog(edit_dialog))
    close_button.pack(side="right", padx=5)


def save_csv(tree, file_path):
    global is_saved
    # Treeviewからデータを取得してDataFrameに変換
    columns = [tree.heading(col)['text'] for col in tree['columns']]
    data = [[tree.set(item, col) for col in tree['columns']] for item in tree.get_children()]
    df = pd.DataFrame(data, columns=columns)

    # CSVファイルに保存
    df.to_csv(file_path, index=False, encoding='utf-8')
    is_saved = True  # 保存が成功したらフラグを更新
    reload_data()


def save_csv_as(tree):
    global is_saved
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        save_csv(tree, file_path)


def close_edit_dialog(dialog):
    global is_saved
    if not is_saved:
        if not messagebox.askyesno("警告", "変更が保存されていません。閉じてもよろしいですか？"):
            return
    dialog.destroy()


def reload_data():
    global grades_data, options, mean, mode, median, std_dev

    # 保存先のアドレスを取得
    file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    # data_loaderモジュールのload_data関数を呼び出してデータを再読み込み
    options, grades_data, mean, mode, median, std_dev = load_data(file_path)

    messagebox.showinfo("情報", "データが再読み込みされました。")


def open_task_dialog(task_index):
    dialog = tk.Toplevel(settings_window)
    dialog.geometry("300x200")
    dialog.title(f"{options[task_index]} 設定")

    tk.Label(dialog, text="重みづけ:").pack(anchor="w", padx=10, pady=5)
    weight_entry = tk.Entry(dialog)
    weight_entry.insert(0, weight[task_index])
    weight_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(dialog, text="合格点:").pack(anchor="w", padx=10, pady=5)
    pass_score_entry = tk.Entry(dialog)
    pass_score_entry.insert(0, pass_score[task_index])
    pass_score_entry.pack(fill="x", padx=10, pady=5)

    def save_task_settings():
        weight[task_index] = float(weight_entry.get())
        pass_score[task_index] = float(pass_score_entry.get())
        dialog.destroy()

    save_button = tk.Button(dialog, text="決定", command=save_task_settings)
    save_button.pack(pady=10)


def close_settings():
    settings_button_left.config(relief=tk.RAISED)
    settings_window.destroy()


def calculate_submission_count(grades_data, task_index):
    total_count = len(grades_data)
    # Count the number of non-NaN elements in the task_index column
    submission_count = sum(1 for row in grades_data if len(row) > task_index and pd.notna(row[task_index]))
    print("submission_count:" + str(submission_count))  # Convert submission_count to string before concatenating
    return f"{submission_count}/{total_count} ({submission_count / total_count * 100:.2f}%)"


def on_dropdown_change(event):
    global windowmode
    global mode
    global mean
    global median
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
    print("task_index:" + str(task_index))
    print("mean:" + str(mean))
    print("mode:" + str(mode))
    print("median:" + str(median))
    if mean is not None and task_index < len(mean):
        mean_str.set(f"{mean[task_index]:.2f}")
        print("平均　:" + str(mean[task_index]))
    if mode is not None and task_index < len(mode):
        mode_str.set(f"{mode[task_index]:.2f}")
        print("最頻値:" + str(mode[task_index]))
    if median is not None and task_index < len(median):
        median_str.set(f"{median[task_index]:.2f}")
        print("中央値:" + str(median[task_index]))
    else:
        # Display the view for the selected option
        pass
    print(windowmode)
    if windowmode == 1:
        switch_to_class()
    elif windowmode == 2:
        display_individual()
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


def display_standard_deviation():
    global right_sub_frame
    # Clear the right sub-frame
    for widget in right_sub_frame.winfo_children():
        widget.destroy()

    # Create a figure for the standard deviation graph
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Get the selected task
    selected_option = dropdown.get()
    if selected_option in options:
        task_index = options.index(selected_option)
        if task_index + 1 < len(options):
            task_index += 1
        else:
            task_index = -1  # or any default value

    if len(grades_data[0]) > task_index:
        data = [row[task_index] for row in grades_data if pd.notna(row[task_index])]
        std_dev_value = np.std(data)
        ax.hist(data, bins=50, density=True, alpha=0.6, color='g', rwidth=1)
        ax.axvline(std_dev_value, color='r', linestyle='dashed', linewidth=1)
        ax.set_title('Standard Deviation')

    # Create a canvas and add it to the right sub-frame
    canvas = FigureCanvasTkAgg(fig, master=right_sub_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def display_id_order():
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

    # Create a list of tuples (ID, score, deviation, pass/fail) and sort it by ID
    score_list = []
    for row in grades_data:
        if pd.notna(row[task_index]):
            id = row[0]
            score = row[task_index]
            deviation = (score - mean[task_index]) / std_dev[task_index] * 10 + 50
            pass_fail = "合格" if score >= pass_score[task_index] else "不合格"
            score_list.append((id, score, deviation, pass_fail))

    score_list.sort(key=lambda x: x[0])

    # Add the sorted scores to the listbox with color coding for pass/fail
    for id, score, deviation, pass_fail in score_list:
        item_text = f"ID: {id}, 得点: {score}, 偏差値: {deviation:.2f}, "
        listbox.insert(tk.END, item_text + pass_fail)
        index = listbox.size() - 1
        if pass_fail == "合格":
            listbox.itemconfig(index, {'fg': 'green'})
        else:
            listbox.itemconfig(index, {'fg': 'red'})


def display_individual():
    global task_names, right_sub_frame, grades_data, grades_name, id_label, subject_entry, teacher_entry, report_card_frame, evaluation_label, comment_entry, center_content, tree, mean, std_dev, pass_score

    if grades_data is None or not grades_data:
        messagebox.showwarning("Warning", "データが読み込まれていません。")
        switch_to_home()
        return None

    if right_sub_frame is None or not right_sub_frame.winfo_exists():
        right_sub_frame = tk.Frame(center_frame, bd=2, relief="solid")
        right_sub_frame.pack(side="top", expand=True, fill="both")

    for widget in right_sub_frame.winfo_children():
        widget.destroy()

    # 左側のフレーム
    left_frame = tk.Frame(right_sub_frame)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # 右側のフレーム（成績表用）
    report_card_frame = tk.Frame(right_sub_frame)
    report_card_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # 操作セクション
    operation_frame = tk.LabelFrame(left_frame, text="操作")
    operation_frame.pack(fill="y", padx=10, pady=10)

    # IDドロップダウン
    id_list = [int(row[0]) for row in grades_data]
    selected_id = tk.IntVar(value=1)  # 初期データとしてID:1を使用
    id_combobox = ttk.Combobox(operation_frame, textvariable=selected_id, values=id_list, state="readonly")
    id_combobox.pack(pady=10)
    id_combobox.bind("<<ComboboxSelected>>", lambda event: update_display(selected_id.get()))

    # # プリントボタン
    # print_button = tk.Button(operation_frame, text="プリント", command=lambda: print_report(selected_id.get()))
    # print_button.pack(pady=10)

    # PDFで保存ボタン
    save_pdf_button = tk.Button(operation_frame, text="PDFで保存", command=lambda: save_to_pdf(selected_id.get()))
    save_pdf_button.pack(pady=10)

    # # PDFを送信ボタン
    # send_pdf_button = tk.Button(operation_frame, text="PDFを送信", command=lambda: send_pdf(selected_id.get()))
    # send_pdf_button.pack(pady=10)

    # 成績表セクション
    report_card_label_frame = tk.LabelFrame(report_card_frame, text="成績表")
    report_card_label_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(report_card_label_frame, text="ID:").pack(anchor="w")
    id_label = tk.Label(report_card_label_frame, text="1")  # 初期データとしてID:1を使用
    id_label.pack(anchor="w")

    tk.Label(report_card_label_frame, text="教科:").pack(anchor="w")
    subject_entry = tk.Entry(report_card_label_frame)
    subject_entry.pack(anchor="w")
    subject_entry.insert(0, "教科を入力")  # デフォルト値を設定

    tk.Label(report_card_label_frame, text="担当:").pack(anchor="w")
    teacher_entry = tk.Entry(report_card_label_frame)
    teacher_entry.pack(anchor="w")
    teacher_entry.insert(0, "担当を入力")  # デフォルト値を設定

    # [全てにセット]ボタン
    set_all_button = tk.Button(report_card_label_frame, text="[全生徒にセット]", command=set_all_subject_teacher)
    set_all_button.pack(anchor="w")

    # 評定
    tk.Label(report_card_label_frame, text="評定:").pack(anchor="w")
    evaluation_label = tk.Label(report_card_label_frame, text="")
    evaluation_label.pack(anchor="w")

    # コメント欄
    tk.Label(report_card_label_frame, text="コメント:").pack(anchor="w")
    comment_entry = tk.Text(report_card_label_frame, height=5, width=40)
    comment_entry.pack(anchor="w")
    comment_entry.insert("1.0", "コメントを入力")

    # Treeview for 課題名, 得点, 平均点, 合否, 順位
    columns = ("課題名", "得点", "平均点", "合否", "順位")
    tree = ttk.Treeview(report_card_label_frame, columns=columns, show="headings", height=10)
    tree.column("課題名", width=100)
    tree.column("得点", width=50)
    tree.column("平均点", width=50)
    tree.column("合否", width=50)
    tree.column("順位", width=50)
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    # 課題名をgrades_nameから取得（最後の四つを除く）
    task_names = grades_name[1:-1]

    selected_data = update_display(1)  # 初期データとしてID:1を使用

    if selected_data is None:
        return

    for i, task_name in enumerate(task_names):
        tree.insert("", "end", values=(
            task_name, selected_data[i], mean[i], "合格" if selected_data[i] >= pass_score[i] else "不合格", i + 1))


def set_all_subject_teacher():
    global grades_data, subject_entry, teacher_entry, std_output_list, comment_entry

    subject = subject_entry.get()
    teacher = teacher_entry.get()
    comment = comment_entry.get()

    std_output_list = []
    for row in grades_data:
        new_row = row.copy()
        new_row[1] = subject  # Assuming the subject is in the second column
        new_row[2] = teacher  # Assuming the teacher is in the third column
        new_row[3] = comment  # Assuming the comment is in the fourth column
        std_output_list.append(new_row)

    messagebox.showinfo("情報", "全てのIDに教科と担当が設定されました。")


def save_to_pdf(selected_id):
    # Open a directory selection dialog
    directory = filedialog.askdirectory()
    if not directory:
        return

    # Create the PDF file path
    pdf_path = os.path.join(directory, f"成績表_{selected_id}.pdf")

    # Create a canvas object
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Add the title
    c.setFont("PC-9800", 16)
    c.drawString(100, height - 50, "成績表")

    # Retrieve the values from display_individual
    subject = subject_entry.get()
    teacher = teacher_entry.get()
    evaluation = evaluation_label.cget("text")
    comment = comment_entry.get("1.0", tk.END).strip()

    # ID and other labels
    c.setFont("PC-9800", 12)
    c.drawString(50, height - 100, "ID:")
    c.drawString(250, height - 100, f"{selected_id}")
    c.drawString(350, height - 100, "教科：")
    c.drawString(450, height - 100, subject)
    c.drawString(350, height - 130, "担当：")
    c.drawString(450, height - 130, teacher)

    # Table headers
    c.drawString(90, height - 220, "課題名")
    c.drawString(190, height - 220, "得点")
    c.drawString(290, height - 220, "平均点")
    c.drawString(390, height - 220, "合否")
    c.drawString(490, height - 220, "順位")

    # Table row lines
    c.line(50, height - 190, 550, height - 190)  # Top border
    c.line(50, height - 230, 550, height - 230)  # Headers bottom border

    # Vertical lines
    c.line(50, height - 190, 50, height - 355)
    c.line(150, height - 190, 150, height - 355)
    c.line(250, height - 190, 250, height - 355)
    c.line(350, height - 190, 350, height - 355)
    c.line(450, height - 190, 450, height - 355)
    c.line(550, height - 190, 550, height - 355)

    # Draw the tree data
    y_position = height - 250
    for row in tree.get_children():
        values = tree.item(row, "values")
        c.drawString(90, y_position, values[0])  # 課題名
        c.drawString(190, y_position, values[1])  # 得点
        avg_score = round(float(values[2]), 2)  # 平均点を四捨五入して小数点第二位までに収める
        c.drawString(290, y_position, str(avg_score))  # 平均点
        c.drawString(390, y_position, values[3])  # 合否
        c.drawString(490, y_position, values[4])  # 順位
        y_position -= 20

    # Grading section
    c.drawString(50, height - 400, "評定：")
    c.rect(100, height - 415, 50, 30)  # Box for grade
    c.drawString(120, height - 395, evaluation)

    # Comment section
    c.drawString(105, height - 412, "コメント")
    c.rect(100, height - 470, 400, 70)  # Box for comment
    c.drawString(105, height - 426, comment)

    # Save the PDF
    c.showPage()
    c.save()

    messagebox.showinfo("情報", f"PDFが保存されました: {pdf_path}")

#
# def print_report():
#     pass
#
#
# def send_pdf():
#     pass


def switch_to_individual():
    global center_content
    for widget in center_frame.winfo_children():
        widget.destroy()
    center_content = display_individual()


first_execution = True


def update_display(selected_id):
    global task_names, grades_data, tree, mean, std_dev, pass_score, grades_name, grade_setting

    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Find the selected data by ID
    selected_data = next((row for row in grades_data if row[0] == selected_id), None)
    if selected_data is None:
        messagebox.showerror("Error", "選択されたIDのデータが見つかりません。")
        return None

    # Insert data into the treeview
    for i, task_name in enumerate(task_names):
        score = selected_data[i + 1] if i + 1 < len(selected_data) else ""
        average_score = mean[i + 1] if i + 1 < len(mean) else ""
        pass_fail = "合格" if score >= pass_score[i + 1] else "不合格"

        # Calculate rank
        scores = [row[i + 1] for row in grades_data if pd.notna(row[i + 1])]
        scores.sort(reverse=True)
        rank = scores.index(score) + 1 if score in scores else ""

        tree.insert("", "end", values=(task_name, score, average_score, pass_fail, rank))

    # 評定の計算
    final_score = selected_data[-1]  # 最後のデータを取得
    evaluation = "未評価"
    for grade in grade_setting:
        if grade[1] <= final_score <= grade[2]:
            evaluation = grade[0]
            break

    # 評定を表示
    evaluation_label.config(text=evaluation)

    id_label.config(text=str(selected_id))
    if not first_execution:
        subject_entry.delete(0, tk.END)
        subject_entry.insert(0, selected_data[1])  # Assuming the subject is in the second column
        teacher_entry.delete(0, tk.END)
        teacher_entry.insert(0, selected_data[2])  # Assuming the teacher is in the third column
        comment_entry.delete(0, tk.END)
        comment_entry.insert(0, selected_data[3])  # Assuming the comment is in the fourth column

    return selected_data


# Attach the event handlers to the buttons
home_button.config(command=switch_to_home)
class_button.config(command=switch_to_class)
settings_button_top.config(command=load_data_from_file)
settings_button_left.config(command=open_settings)
individual_button.config(command=switch_to_individual)

# Attach the event handler to the dropdown
dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

# Set the initial view to home
switch_to_home()

# Start the main event loop
root.mainloop()
