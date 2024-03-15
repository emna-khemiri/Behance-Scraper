import json

def save_data_to_json(data, filename):
    """
    Saves data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")
