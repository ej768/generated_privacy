import json

def extract_values_recursive(obj, values_list):
    """Recursively extract values from nested JSON."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            extract_values(value, values_list)
    elif isinstance(obj, list):
        for item in obj:
            extract_values(item, values_list)
    else:
        values_list.append(str(obj))

def extract_values(data):
    dict_permissions = {}
    # Go through each app and put each ptype in list
    for app in data:
        values = []
        for ptype in data[app]:
            values += data[app][ptype]

        dict_permissions[app] = values
    
    return dict_permissions


def main():
    # Load the nested JSON file
    with open('dpp_human_gen_raw.json', 'r') as json_file:
        data = json.load(json_file)

    # Extract values
    values = []
    values = extract_values(data)

    # Unique values only
    # values = list(set(values))
    
    # Write the list to a txt file
    with open('dpp_human_gen.json', 'w') as json_file:
        json.dump(values, json_file, indent=4)

if __name__ == "__main__":
    main()
