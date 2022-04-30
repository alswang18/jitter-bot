from email import header
import json
from urllib import response
import requests
import os 

def generate_payload(userIDs, names, messages):
    res = {
        "confidenceThreshold": 0.6,
        # <Optional,double| Minimum required confidence for the insight to be recognized. Value ranges between 0.0 to 1.0. Default value is 0.5.>
        "detectPhrases": "true",
        # <Optional,boolean| It shows Actionable Phrases in each sentence of conversation. These sentences can be found using the Conversation's Messages API. Default value is false.>
        "enableSummary": "true",
        "messages": [],
    }

    for name, userID, message in zip(names, userIDs, messages):
        res["messages"].append(
            {
            "payload": {
            "content": message,
            "contentType": "text/plain"
            },
            "from": {"name": name, "userId": userID}
            }
        )
    return res


def send_for_analysis(payload):
    url = "https://api.symbl.ai/v1/process/text"

    # set your access token here. See https://docs.symbl.ai/docs/developer-tools/authentication
    access_token = os.environ.get("SYMBOL_KEY", "")

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }

    responses = {
        400: "Bad Request! Please refer docs for correct input fields.",
        401: "Unauthorized. Please generate a new access token.",
        404: "The conversation and/or it's metadata you asked could not be found, please check the input provided",
        429: "Maximum number of concurrent jobs reached. Please wait for some requests to complete.",
        500: "Something went wrong! Please contact support@symbl.ai",
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        return response.json()
    else:
        print("Error", response.status_code)


def get_results(convo_id):
    url = f"https://api.symbl.ai/v1/conversations/{convo_id}/summary"

    access_token = os.environ.get("SYMBOL_KEY", "")

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    res = requests.request("GET", url, headers=headers)

    return res.json()
