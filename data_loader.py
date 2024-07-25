import pandas as pd
import numpy as np
class load_data_from_file:
    def __init__(self):
        # 初期化コード
        pass

    def load_data(self, data_address):
        # CSVファイルからデータを読み込む
        df = pd.read_csv(data_address)
        # 平均計算用のDataFrameを作成し、"-"を0に置換
        df_for_avg = df.replace('-', 0).fillna(0)

        # 元のDataFrameで"-"をNaNに置換し、数値に変換できない値をNaNに置換
        df.replace('-', np.nan, inplace=True)
        for column in df.columns[1:]:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            df_for_avg[column] = pd.to_numeric(df_for_avg[column], errors='coerce')

        report_columns = df.filter(regex='Report').columns
        exam_columns = df.filter(regex='Exam').columns

        grades_data = []
        submission_counts = {}  # 各課題の提出数を格納する辞書
        submission_rates = {}  # 各課題の提出率を格納する辞書

        for column in report_columns:
            # 各Report列でNaNでない値の数をカウント（提出数）
            submission_count = df[column].notna().sum()
            # 提出率 = 提出数 / 全生徒数
            submission_rate = submission_count / len(df)
            submission_counts[column] = submission_count
            submission_rates[column] = submission_rate
            student_total = len(df)

        for i in range(len(df)):
            student_data = df.iloc[i].tolist()
            # 平均計算用のDataFrameから平均値を計算
            report_avg = df_for_avg.loc[i, report_columns].mean()
            exam_avg = df_for_avg.loc[i, exam_columns].mean()
            # NaNを考慮して元のデータに平均値を追加
            student_data.extend([report_avg if not np.isnan(report_avg) else np.nan,
                                 exam_avg if not np.isnan(exam_avg) else np.nan])
            grades_data.append(student_data)

        # 全生徒のReportとExamの平均値を計算
        All_Report_avg = df_for_avg[report_columns].mean(axis=1).mean()
        All_Report_mode = df_for_avg[report_columns].mode(axis=1).iloc[0].mode()[0]
        All_Report_median = df_for_avg[report_columns].median(axis=1).median()
        All_Report_std_dev = df_for_avg[report_columns].std(axis=1).std()

        All_Exam_avg = df_for_avg[exam_columns].mean(axis=1).mean()
        All_Exam_mode = df_for_avg[exam_columns].mode(axis=1).iloc[0].mode()[0]
        All_Exam_median = df_for_avg[exam_columns].median(axis=1).median()
        All_Exam_std_dev = df_for_avg[exam_columns].std(axis=1).std()

        # ドロップダウンメニューの選択肢を設定
        options = df.columns[1:].tolist()
        options.extend(["全てのReport", "全てのExam", "SUM"])

        # コンソールにデータの概要を出力
        print("DataFrame Overview:\n", df)
        print("\nOptions:", options)
        print("\nGrades Data:", grades_data)
        print("\nSubmission Counts:", submission_counts)
        print("\nSubmission Rates:", submission_rates)
        print("\nAll Report Average:", All_Report_avg)
        print("\nAll Report Mode:", All_Report_mode)
        print("\nAll Report Median:", All_Report_median)
        print("\nAll Report Standard Deviation:", All_Report_std_dev)
        print("\nAll Exam Average:", All_Exam_avg)
        print("\nAll Exam Mode:", All_Exam_mode)
        print("\nAll Exam Median:", All_Exam_median)
        print("\nAll Exam Standard Deviation:", All_Exam_std_dev)


        return (options, grades_data, All_Report_avg, All_Report_mode, All_Report_median, All_Report_std_dev, All_Exam_avg, All_Exam_mode, All_Exam_median, All_Exam_std_dev, student_total
                )
    def calculate_submission_details(submissions):
        # submissionsは(提出数, 提出率)のタプルのリスト
        details = []
        for i in range(len(submissions)):
            if i == 0:
                # 初回のデータは変動がないため、0を追加
                details.append([submissions[i][0], submissions[i][1], 0, 0])
            else:
                # 前回との提出数の変動
                count_change = submissions[i][0] - submissions[i-1][0]
                # 前回との提出率の変動
                rate_change = submissions[i][1] - submissions[i-1][1]
                details.append([submissions[i][0], submissions[i][1], count_change, rate_change])
        return details

