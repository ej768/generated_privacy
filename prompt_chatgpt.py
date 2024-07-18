import os
import json
import pandas as pd
import re
from openai import OpenAI


def ask_chatgpt(question):
    '''
    Form request to chat gpt api
    '''
    # # Authentication
    # with open("chatgpt_apikey.txt", 'r') as key_file:
    #     openai.api_key = key_file.readline()

    client = OpenAI(
        # This is the default and can be omitted
        #api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


def formulate_question(code_src_link):
    return f"""
Please reference code repository here [{code_src_link}] and give a list of the data practices used within the code. Your answer to this question must include only options from the list of the provided app data practices. Please do not give any descriptions for each, just a list.

[
    "measure app storage space",
    "read sync settings",
    "download files without notification",
    "control vibration",
    "Google Play license check",
    "create accounts and set passwords",
    "change network connectivity",
    "record audio",
    "control flashlight",
    "read the contents of your USB storage",
    "modify your contacts",
    "modify or delete the contents of your USB storage",
    "read calendar events plus confidential information",
    "send sticky broadcast",
    "full network access",
    "disable your screen lock",
    "read phone status and identity",
    "add or remove accounts",
    "connect and disconnect from Wi-Fi",
    "send SMS messages",
    "read sync statistics",
    "run at startup",
    "view network connections",
    "capture video output",
    "read battery statistics",
    "draw over other apps",
    "read your own contact card",
    "read Google service configuration",
    "precise location (GPS and network-based)",
    "change your audio settings",
    "toggle sync on and off",
    "find accounts on the device",
    "view Wi-Fi connections",
    "retrieve running apps",
    "access Bluetooth settings",
    "approximate location (network-based)",
    "read Home settings and shortcuts",
    "read your contacts",
    "control Near Field Communication",
    "uninstall shortcuts",
    "take pictures and videos",
    "receive text messages (SMS)",
    "add or modify calendar events and send email to guests without owners' knowledge",
    "receive data from Internet",
    "read frame buffer",
    "use accounts on the device",
    "set wallpaper",
    "install shortcuts",
    "directly call phone numbers",
    "read call log",
    "allow Wi-Fi Multicast reception",
    "reorder running apps",
    "change screen orientation",
    "pair with Bluetooth devices",
    "prevent device from sleeping"
]
"""


def save_response(app_id, answer):
    # Strip formatting and split the answer into list of the lines
    ai_response = re.sub('-{1} {1}|"', "", answer).splitlines()

    # Save the response to a json file
    with open("dpp_ai_gen.json", "r") as file:
        json_obj = json.load(file)

    with open("dpp_ai_gen.json", "w") as file:
        json_obj[app_id] = ai_response
        json.dump(json_obj, file, indent=4)



def get_app_ids(app_ids):
    '''
    Takes a list of all the app ids and narrows it down to
    just those that haven't been prompted to Chat GPT yet
    '''
    # Open file with saved ai responses
    with open("dpp_ai_gen.json", 'r') as file:
        ai_data = json.load(file)
    
    return list(set(app_ids).difference(ai_data.keys()))


def main():
    # Get all the apps in the list
    with open("app_list.csv") as file:
        app_data = pd.read_csv(file)

    # Remove any apps without github links
    app_data = app_data[app_data['github_link'].notnull()]

    # Gets only apps that Chat GPT hasn't looked at
    app_ids = get_app_ids(app_data['app_id'].to_list())

    ### Cut down app list for
    # app_ids = app_ids[:1]
    
    for app_id in app_ids:
        # Ask Chat GPT about the data privacy practices
        code_src_link = app_data.loc[app_data['app_id'] == app_id, 'github_link'].values[0]
        question = formulate_question(code_src_link)
        print(question)
        answer = ask_chatgpt(question)
        print(answer)
        save_response(app_id, answer)

    print("Done!")

if __name__ == "__main__":
    main()