import pandas as pd
import numpy as np

def load_data(data_address):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(data_address)

    # Replace '-' with NaN
    df.replace('-', np.nan, inplace=True)

    # Convert the DataFrame to numeric
    for column in df.columns[1:]:
        try:
            df[column] = pd.to_numeric(df[column])
        except ValueError:
            pass

    # Calculate the mean, mode, and median for each column, skipping the first column
    mean = df.iloc[:, 1:].mean(skipna=True).to_numpy()
    mode = df.iloc[:, 1:].mode().iloc[0].to_numpy()
    median = df.iloc[:, 1:].median(skipna=True).to_numpy()
    std_dev = df.iloc[:, 1:].std(skipna=True).to_numpy()

    # Calculate the additional options
    report_columns = [col for col in df.columns if 'Report' in col]
    exam_columns = [col for col in df.columns if 'Exam' in col]

    all_report_mean = df[report_columns].mean(skipna=True).mean()
    all_exam_mean = df[exam_columns].mean(skipna=True).mean()
    sum_mean = df.iloc[:, 1:].mean(skipna=True).mean()

    all_report_mode = df[report_columns].mode().iloc[0].mean()
    all_exam_mode = df[exam_columns].mode().iloc[0].mean()
    sum_mode = df.iloc[:, 1:].mode().iloc[0].mean()

    all_report_median = df[report_columns].median(skipna=True).mean()
    all_exam_median = df[exam_columns].median(skipna=True).mean()
    sum_median = df.iloc[:, 1:].median(skipna=True).mean()

    all_report_std_dev = df[report_columns].std(skipna=True).mean()
    all_exam_std_dev = df[exam_columns].std(skipna=True).mean()
    sum_std_dev = df.iloc[:, 1:].std(skipna=True).mean()

    # Append the additional options to the arrays
    mean = np.append(mean, [all_report_mean, all_exam_mean, sum_mean])
    mode = np.append(mode, [all_report_mode, all_exam_mode, sum_mode])
    median = np.append(median, [all_report_median, all_exam_median, sum_median])
    std_dev = np.append(std_dev, [all_report_std_dev, all_exam_std_dev, sum_std_dev])

    # Add the additional options
    options = df.columns[1:].tolist()
    options.extend(["全てのReport", "全てのExam", "SUM"])

    # Convert the DataFrame back to a list of lists for grades_data
    grades_data = df.values.tolist()

    # Extract the column names for grades_name
    grades_name = df.columns.tolist()

    # Calculate the additional data for grades_data
    all_report_data = [sum(row[i] for i in range(len(row)) if df.columns[i] in report_columns and pd.notna(row[i])) for
                       row in grades_data]
    all_exam_data = [sum(row[i] for i in range(len(row)) if df.columns[i] in exam_columns and pd.notna(row[i])) for row
                     in grades_data]
    sum_data = [all_report_data[i] + all_exam_data[i] for i in range(len(grades_data))]

    # Append the additional data to grades_data
    for i in range(len(grades_data)):
        grades_data[i].extend([all_report_data[i], all_exam_data[i], sum_data[i]])

    print("avg: " + str(mean))
    print("mode: " + str(mode))
    print("median: " + str(median))
    print("std_dev: " + str(std_dev))
    print("options: " + str(options))
    print("grades_data: " + str(grades_data))
    print("grades_name: " + str(grades_name))

    return options, grades_data, grades_name, mean, mode, median, std_dev