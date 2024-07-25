import customtkinter as ctk
import pandas as pd

class RankRendererCTK:
    @staticmethod
    def display_rank(right_sub_frame, grades_data, selected_option, options):
        # Clear the right sub-frame
        for widget in right_sub_frame.winfo_children():
            widget.destroy()

        # Create a CTkListbox in the right sub-frame
        listbox = ctk.CTkListbox(right_sub_frame)
        listbox.pack(fill="both", expand=True)

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
            listbox.insert("end", f"ID: {id}, Score: {score}")