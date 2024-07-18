import json


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
    values = extract_values(data)
    
    # Write the list to a txt file
    with open('dpp_human_gen.json', 'w') as json_file:
        json.dump(values, json_file, indent=4)

if __name__ == "__main__":
    main()
