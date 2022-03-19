import json
import pandas as pd


def write_to_json(file_name, dictionary):
    """Write an iterable object to a JSON file."""
    print("Writing to file...")
    file_name = file_name + '.json'
    if "../" in file_name or file_name[0] == "/":
        raise RuntimeError()
    with open(file_name, 'w') as json_file:
        json.dump(dictionary, json_file)
    print("Written")


def df_to_csv(df, csv_name):
    """Write a Dataframe to a CSV file."""
    print("Writing to file...")
    df.to_csv(csv_name, index=True)


def csv_to_df(csv):
    """Write CSV to pandas dataframe."""
    df = pd.read_csv(csv)
    return df
