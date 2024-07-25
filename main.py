import customtkinter as ctk
from tkinter import filedialog

import pandas as pd
from PIL._tkinter_finder import tk

from class_view_renderer import ClassViewRenderer
from data_loader import load_data_from_file
from graph_renderer import GraphRenderer
from rank_renderer import RankRendererCTK
from ED_logo import icon_loader  # ED_logo.pyから関数をインポート
from setting_app import SettingsApp

# メインウィンドウの設定
root = ctk.CTk()
root.title("EduVantage")
root.geometry("1280x720")

# グローバル変数の初期化
grades_data = []
options = []
mean = []
mode = []
median = []
std_dev = []
All_Report_avg = []
All_Report_mode = []
All_Report_median = []
All_Report_std_dev = []
All_Exam_avg = []
All_Exam_mode = []
All_Exam_median = []
All_Exam_std_dev = []
submission_count = ctk.StringVar(root)
task_name = ctk.StringVar(root)
mean_str = ctk.StringVar(root)
mode_str = ctk.StringVar(root)
median_str = ctk.StringVar(root)
submission_count_label = None
task_name_label = None
mean_label = None
mode_label = None
median_label = None
student_total = None
submission_change = None
submission_rate = None


# データロード関数
def load_data():
    global grades_data, options, mean, mode, median, std_dev, \
        All_Report_avg, All_Report_mode, All_Report_median, All_Report_std_dev, \
        All_Exam_avg, All_Exam_mode, All_Exam_median, All_Exam_std_dev
    data_address = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if data_address:
        loader = load_data_from_file()  # load_data_from_fileクラスのインスタンスを作成
        loaded_data = loader.load_data(data_address)  # load_dataメソッドを呼び出してデータを読み込む
        # 必要に応じてloaded_dataから個々の値を取り出す
        options = loaded_data[0]
        sub_dropdown.configure(values=options)  # ドロップダウンメニューの選択肢を設定
        sub_dropdown.set("課題を選択")
    else:
        print("ファイルが選択されていません。")


# GUIのレイアウト設定
mode_frame = ctk.CTkFrame(root, width=150, height=720)
mode_frame.pack(side="left", fill="y")

top_bar = ctk.CTkFrame(root, height=50)
top_bar.pack(side="top", fill="x")

center_frame = ctk.CTkFrame(root)
# center_frame.pack(expand=True, fill="both")

sub_dropdown = ctk.CTkComboBox(top_bar, values=options)
sub_dropdown.pack(side="left", padx=10, pady=10)
sub_dropdown.set("データを選択")

load_button = ctk.CTkButton(top_bar, text="データを読み込む", command=load_data, height=40)
load_button.pack(side="right", padx=10, pady=10)

right_sub_frame = ctk.CTkFrame(center_frame)

# 設定ボタン
settings_button_left = ctk.CTkButton(mode_frame, text="設定", width=100, height=40,
                                     command=SettingsApp)  # Adjust width and height as needed

# 設定ボタンの下にセパレーターを追加
separator = ctk.CTkLabel(mode_frame, text="---------------------------", width=100, height=1)

# ホームボタン
home_button = ctk.CTkButton(mode_frame, text="ホーム", width=100,
                            height=40, )  # customtkinter allows specifying fg_color for relief effect

# クラスボタン
class_button = ctk.CTkButton(mode_frame, text="クラス", width=100, height=40)

# 個人ボタン
individual_button = ctk.CTkButton(mode_frame, text="個人", width=100, height=40)

modification_button = ctk.CTkButton(mode_frame, text="データ変更", width=100, height=40)

settings_button_left.pack(pady=10, padx=20)
separator.pack(pady=5, padx=5)
home_button.pack(pady=20, padx=20)
class_button.pack(pady=20, padx=20)
individual_button.pack(pady=20, padx=20)
modification_button.pack(pady=120, padx=20)
class_view_renderer = ClassViewRenderer(root, task_name=task_name, submission_count=submission_count, mean_str=mean_str,
                                        median_str=median_str, mode_str=mode_str, mean_label=mean_label,
                                        mode_label=mode_label, median_label=median_label,
                                        task_name_label=task_name_label, submission_count_label=submission_count_label,
                                        student_total=student_total, submission_change=submission_change,
                                        submission_rate=submission_rate)

# dropdownの選択変更イベントをon_dropdown_changeにバインド
sub_dropdown.bind("<<ComboboxSelected>>", lambda event: on_dropdown_change())


def toggle_buttons(pressed_button):
    # すべてのボタンをリストに格納
    buttons = [home_button, class_button, individual_button, modification_button]

    for button in buttons:
        if button == pressed_button:
            button.configure(state="disabled")  # 押されたボタンを無効にする
        else:
            button.configure(state="normal")  # 他のボタンを有効にする


# 各ボタンのcommand属性を更新
settings_button_left.configure(command=lambda: SettingsApp(root))
home_button.configure(command=lambda: toggle_buttons(home_button))
class_button.configure(command=lambda: [toggle_buttons(class_button), class_view_renderer])
individual_button.configure(command=lambda: toggle_buttons(individual_button))
modification_button.configure(command=lambda: toggle_buttons(modification_button))


def on_dropdown_change():
    print("Dropdown changed")
    selected_option = sub_dropdown.get()
    task_name.set(selected_option)
    print(selected_option)

    if selected_option in ["全てのReport", "全てのExam"]:
        submission_count.set("N/A")
    else:
        task_index = options.index(selected_option)
        if task_index + 1 < len(options):
            task_index += 1
        else:
            task_index = -1

        submission_count.set(calculate_submission_count(task_index))

    if mean is not None and task_index < len(mean):
        mean_str.set(f"{mean[task_index]:.2f}")
    if mode is not None and task_index < len(mode):
        mode_str.set(f"{mode[task_index]:.2f}")
    if median is not None and task_index < len(median):
        median_str.set(f"{median[task_index]:.2f}")
    class_view_renderer.update_submission_count_label(submission_change, submission_rate,
                                                      submission_count_label,
                                                      student_total)


def calculate_submission_count(task_index):
    total_count = len(grades_data)
    submission_count = sum(1 for row in grades_data if len(row) > task_index and pd.notna(row[task_index]))
    return f"{submission_count}/{total_count} ({submission_count / total_count * 100:.2f}%)"


def display_rank():
    for widget in right_sub_frame.winfo_children():
        widget.destroy()

    listbox = ctk.CTkListbox(right_sub_frame)
    listbox.pack(fill="both", expand=True)

    selected_option = sub_dropdown.get()

    if selected_option in options:
        task_index = options.index(selected_option)
        if task_index + 1 < len(options):
            task_index += 1
        else:
            task_index = -1

    score_list = sorted((row[0], row[task_index]) for row in grades_data if pd.notna(row[task_index]))

    for id, score in score_list:
        listbox.insert("end", f"ID: {id}, Score: {score}")


# Start the GUI's main event loop
root.mainloop()
