import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats
import numpy as np
import pandas as pd

class GraphRenderer:
    @staticmethod
    def draw_histogram(right_sub_frame, grades_data, task_index, mean=None, std_dev=None):
        # グラフの描画準備
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # データの準備
        if len(grades_data[0]) > task_index:
            data = [row[task_index] for row in grades_data if pd.notna(row[task_index])]
            counts, bins, patches = ax.hist(data, bins=50, density=True, alpha=0.6, color='g', rwidth=1)

            # PDFのプロット
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            if mean is not None and std_dev is not None and task_index < len(mean) and task_index < len(std_dev):
                p = stats.norm.pdf(x, mean[task_index], std_dev[task_index])
                ax.plot(x, p, 'k', linewidth=2)

        # キャンバスの作成と配置
        canvas = FigureCanvasTkAgg(fig, master=right_sub_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)