import customtkinter as ctk
import tkinter as tk


def update_label(task_name, string_var):
    # ラベルのテキストをStringVarの現在の値に更新
    task_name.configure(text=string_var.get())


class ClassViewRenderer:
    def __init__(self, parent, task_name, submission_count, mean_str, median_str, mode_str, mean_label, mode_label,
                 median_label, task_name_label, submission_count_label, student_total, submission_change, submission_rate):
        self.parent = parent
        self.task_name = task_name
        self.submission_count = submission_count
        self.mean_str = mean_str
        self.median_str = median_str
        self.mode_str = mode_str
        self.mean_label = mean_label
        self.mode_label = mode_label
        self.median_label = median_label
        self.task_name_label = task_name_label
        self.submission_count_label = submission_count_label
        self.student_total = student_total
        self.submission_change = submission_change
        self.submission_rate = submission_rate
        self.center_frame = ctk.CTkFrame(parent, width=200, height=100)
        self.center_frame.pack(side="left", fill="both", expand=True)

        # right_sub_frameの初期化と設定
        self.right_sub_frame = ctk.CTkFrame(parent, width=100, height=100)
        self.right_sub_frame.pack(side="right", fill="y")

        # 課題名ラベル
        self.task_name_label = ctk.CTkLabel(self.center_frame, textvariable=task_name)
        self.task_name_label.pack(anchor="w", padx=10, pady=5)
        # 提出ラベル
        self.submission_count_label = ctk.CTkLabel(self.center_frame, textvariable=submission_count)
        self.submission_count_label.pack(anchor="w", padx=10, pady=5)
        # 平均点ラベル
        self.mean_label = ctk.CTkLabel(self.center_frame, textvariable=mean_str)
        self.mean_label.pack(anchor="w", padx=10, pady=5)
        # 中央値ラベル
        self.median_label = ctk.CTkLabel(self.center_frame, textvariable=median_str)
        self.median_label.pack(anchor="w", padx=10, pady=5)
        # 最頻値ラベル
        self.mode_label = ctk.CTkLabel(self.center_frame, textvariable=mode_str)
        self.mode_label.pack(anchor="w", padx=10, pady=5)
        # 予想理解度ラベル
        ctk.CTkLabel(self.center_frame, text="予想理解度 mm%").pack(anchor="w", padx=10, pady=5)
        # 予想意欲値ラベル
        ctk.CTkLabel(self.center_frame, text="予想意欲値 MM").pack(anchor="w", padx=10, pady=5)



    def update_submission_count_label(self, submission_count, submission_change, submission_rate, rate_change,
                                      submission_count_label, student_total):
        # Textウィジェットを作成またはクリア
        submission_count_text = tk.Text(submission_count_label, height=2, borderwidth=0,
                                        background=submission_count_label.cget("background"))
        submission_count_text.tag_configure("positive", foreground="green")
        submission_count_text.tag_configure("negative", foreground="red")

        # 提出数の変動の記号と色を決定
        if submission_change >= 0:
            submission_change_str = f"↑{abs(submission_change)}人"
            submission_change_tag = "positive"
        else:
            submission_change_str = f"↓{abs(submission_change)}人"
            submission_change_tag = "negative"

        # 提出率の変動の記号と色を決定
        if rate_change >= 0:
            rate_change_str = f"↑{abs(rate_change)}%"
            rate_change_tag = "positive"
        else:
            rate_change_str = f"↓{abs(rate_change)}%"
            rate_change_tag = "negative"

        # テキストウィジェットに内容を挿入
        submission_count_text.insert("end", f"[{student_total}]中[{submission_count}]人（", "normal")
        submission_count_text.insert("end", submission_change_str, submission_change_tag)
        submission_count_text.insert("end", f"）：[{submission_rate}%]（", "normal")
        submission_count_text.insert("end", rate_change_str, rate_change_tag)
        submission_count_text.insert("end", "）", "normal")

        # テキストウィジェットを配置
        submission_count_text.pack()

        # テキストウィジェットの編集を無効化
        submission_count_text.configure(state="disabled")
