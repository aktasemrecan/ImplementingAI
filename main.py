from openai import OpenAI

from env import OPENAI_API_KEY

import requests

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

model="gpt-4o-mini"

def get_endpoints(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            return list(data.keys())
        else:
            return f"fetching endpoints of API is failed: {response.status_code}"
    except Exception as e:
        return f"It is failed: {e}"




def get_api_request_url(prompt,max_tokens=80):
    try:
        response_AI = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": f"User gave API URL is {user_api_url} and API endpoints: {endpoints} . Please just provide API request URL. Do not write anything else"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        return response_AI.choices[0].message.content

    except Exception as e:
        return str(e)



def send_request(request_api_url):
    try:
        requests.get(request_api_url)
        if requests.get(request_api_url).status_code == 200:
            data = requests.get(request_api_url).json()
            return data
        else:
            return "It is failed to get response from Request Api Url"
    except Exception as e:
        return str(e)



def get_response_from_ai(prompt,max_tokens=80):
    request_api_url = get_api_request_url(prompt,max_tokens)
    print(request_api_url, "request_api_url")
    response_data = send_request(request_api_url)
    # print(response_data, "response_data")
    try:
        response_AI = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": f"Can you analyse the data what I give: {response_data} and according to this data, please answer the question: {prompt} ."
                               f"Please now give the answer in format which is given:"
                               f"Answer: Here should be understandable response for a human"
                },
            ]
        )


        return response_AI.choices[0].message.content

    except Exception as e:
        return str(e)



user_api_url = input("Please tell me the API Url: ")

endpoints = get_endpoints(user_api_url)

user_input = input("Tell me what you want to know: ")

print(get_response_from_ai(user_input))
