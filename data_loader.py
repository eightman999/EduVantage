# data_loader.py
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
    mean = df.iloc[:, 1:].mean(skipna=True)
    mode = df.iloc[:, 1:].mode().iloc[0]
    median = df.iloc[:, 1:].median(skipna=True)
    std_dev = df.iloc[:, 1:].std(skipna=True)

    # Add the additional options
    options = df.columns[1:].tolist()
    options.extend(["全てのReport", "全てのExam", "SUM"])

    # Convert the list to a string before printing
    print("options: " + ', '.join(options))

    print("avg: " + str(mean))
    print("mode: " + str(mode))
    print("median: " + str(median))
    print("std_dev: " + str(std_dev))

    # Convert the DataFrame back to a list of lists for grades_data
    grades_data = df.values.tolist()

    return options, grades_data, mean, mode, median, std_dev