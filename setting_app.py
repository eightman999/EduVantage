import customtkinter as ctk


class SettingsApp(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("200x350")
        # Initialize sidebar_frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        # Initialize settings_frame outside the visible area
        self.settings_frame = ctk.CTkFrame(self, width=600)
        # Ensure settings_frame starts completely outside the visible area
        self.settings_frame.place(x=self.winfo_screenwidth(), y=0)

        # Example button in sidebar_frame to trigger animation
        self.button_display = ctk.CTkButton(self.sidebar_frame, text="表示　＞", command=lambda: [self.display_settings(), self.animate_frames()], width=160)
        self.button_language = ctk.CTkButton(self.sidebar_frame, text="言語　＞", command=lambda: [self.language_settings(), self.animate_frames()],width=160)
        self.button_credit = ctk.CTkButton(self.sidebar_frame, text="クレジット　＞", command=lambda: [self.credit_settings(), self.animate_frames()], width=160)

        self.button_display.grid(row=0, column=0, pady=20, padx=20)
        self.button_language.grid(row=1, column=0, pady=20, padx=20)
        self.button_credit.grid(row=2, column=0, pady=20, padx=20)

        self.dark_mode_var = ctk.StringVar(value="off")
        self.dark_mode_switch = ctk.CTkSwitch(self.settings_frame, text="ダークモード", command=self.toggle_dark_mode,
                                              variable=self.dark_mode_var, onvalue="on", offvalue="off")


    def display_settings(self):
        self.clear_settings_frame()
        label = ctk.CTkLabel(self.settings_frame, text="表示設定", width= 180)
        label.grid(row=0, column=0, pady=10, padx=10)
        self.dark_mode_switch.grid(row=1, column=0, pady=10, padx=10)

    def language_settings(self):
        self.clear_settings_frame()
        label = ctk.CTkLabel(self.settings_frame, text="言語設定")
        label.grid(row=0, column=0, pady=10, padx=10)

    def credit_settings(self):
        self.clear_settings_frame()
        label = ctk.CTkLabel(self.settings_frame, text="クレジット")
        label.grid(row=0, column=0, pady=10, padx=10)

    def clear_settings_frame(self):
        for widget in self.settings_frame.winfo_children():
            widget.grid_forget()

    def animate_frames(self):
        # sidebar_frameを左にスライドアウト
        sidebar_start_x = 0  # sidebar_frameの開始X座標
        settings_start_x = self.winfo_width()  # settings_frameの開始X座標（ウィンドウの幅）

        for x in range(100, -1, -10):  # 100から0まで-10ずつ
            self.sidebar_frame.place(x=sidebar_start_x - x, y=0)  # sidebar_frameを左に移動
            self.settings_frame.place(x=settings_start_x - x * 2, y=0)  # settings_frameを右から移動
            self.update_idletasks()  # 画面の更新
            self.after(30)  # 50ミリ秒待機

        # アニメーション終了後、sidebar_frameを非表示にする
        self.sidebar_frame.place_forget()

        # settings_frameを最終位置に配置
        self.settings_frame.place(x=0, y=0)

    def toggle_dark_mode(self):
        if self.dark_mode_var.get() == "on":
            ctk.set_appearance_mode("dark")
            self.settings_frame.configure(fg_color="#000000")
            for widget in self.settings_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="#ffffff")
        else:
            ctk.set_appearance_mode("light")
            self.settings_frame.configure(fg_color="#ffffff")
            for widget in self.settings_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="#000000")
