import time
import json
from google_play_scraper import app, permissions

def get_app_privacy_practices(app_id):
    try:
        # Fetch app details
        app_details = app(app_id)

        # Extract privacy practices information
        privacy_practices = app_details.get('privacyPolicy', 'No privacy practices information available')

        return privacy_practices
    except Exception as e:
        return f"An error occurred: {e}"


def get_permissions(app_id):
    result = permissions(
        app_id,
        lang='en', # defaults to 'en'
        country='us', # defaults to 'us'
    )

    return result


if __name__ == "__main__":
    # Read list of app ids from txt file
    app_ids = []
    with open("app_list.txt") as file:
        app_ids = file.read().splitlines() 

    # JSON of data practices
    privacy = {}

    with open("dpp_human_gen_raw.json", 'r') as dpp_file:
        privacy = json.load(dpp_file)

    try:
        # Go through each app and pull the data practices
        for app_id in app_ids:
            # Only request if not already has it
            if app_id not in privacy:
                print(f'Pulling privacy practices for: {app_id}')
                privacy[app_id] = get_permissions(app_id)
                time.sleep(2)
    
    except Exception as e:
        print(e)
        print('Error occured, printing result to json')

    # Write the dictionary to a JSON file
    with open('dpp_human_gen_raw.json', 'w') as json_file:
        json.dump(privacy, json_file, indent=4)

