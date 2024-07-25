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
    with open("dpps.csv") as in_file:
        df = pd.read_csv(in_file)

        dpp_options = "\n".join(list(df["Permission"]))

    setup = f"Please reference code repository here [{code_src_link}] and give a list of the data practices used within the code. Your answer must include only options from the list of the provided app data practices. Please do not give any descriptions for each or formatting, such as quotations and hyphens. Your response should only be a list with each item on its own line. The possible data practices are as follows: "

    question_str = setup + "\n" + dpp_options
    return question_str


def save_response(app_id, answer):
    # Strip formatting and split the answer into list of the lines
    ai_response = re.sub('-{1} {1}|"', "", answer).splitlines().lower()

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