import json
import pandas as pd


def consolidate_dpp_types(nested_dict):
    consolidated = {}

    # Go through each app
    for k, v in nested_dict.items():
        # Go through each dpp type
        for key in v:
            if key in consolidated:
                consolidated[key].extend(v[key])
                consolidated[key] = list(set(consolidated[key]))
            else:
                consolidated[key] = v[key]  

    return consolidated


def convert(data):
    # Flatten the data
    flattened_data = []
    for key, value_list in data.items():
        for value in value_list:
            flattened_data.append({'Category': key, 'Permission': value.lower()})
    
    # Create the DataFrame
    df = pd.DataFrame(flattened_data)

    return df


def main():
    # Load the nested JSON file
    with open('dpp_human_gen_raw.json', 'r') as json_file:
        data = json.load(json_file)

    # Extract values
    values = consolidate_dpp_types(data)

    # Convert to Data Frame
    df = convert(values)

    # Write the list to a txt file
    with open('dpps.json', 'w') as json_file:
        json.dump(values, json_file, indent=4)

    # Write the data frame to csv
    df.to_csv("dpps.csv", index=False)


if __name__ == "__main__":
    main()