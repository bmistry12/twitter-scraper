import json


def write_to_json(file_name, dictionary):
    """Write an iterable object to a JSON file."""
    file_name = file_name + '.json'
    with open(file_name, 'w') as json_file:
        json.dump(dictionary, json_file)
    print("Written")


def df_to_csv(df, csv_name):
    """Write a Dataframe to a CSV file."""
    df.to_csv(csv_name, index=True)
