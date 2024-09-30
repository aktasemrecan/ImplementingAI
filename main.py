from openai import OpenAI

from env import OPENAI_API_KEY

import requests

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

model="gpt-4o-mini"

# def get_endpoints(api_url):
#     try:
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             return list(data.keys())
#         else:
#             return f"fetching endpoints of API is failed: {response.status_code}"
#     except Exception as e:
#         return f"It is failed: {e}"


def get_api_request_url(prompt,max_tokens=100):
    try:
        response_AI = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": f"User gave an API documentation URL which is {user_api_url} . Please analyze all endpoints in this documentation and after that just provide API request URL according to given prompt from user ( If there are parameters which should be filled, then fill them randomly ). Do not write anything else."
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



def get_response_from_ai(prompt,max_tokens=200):
    request_api_url = get_api_request_url(prompt,max_tokens)
    print(request_api_url, "request_api_url")
    response_data = send_request(request_api_url)
    try:
        response_AI = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": f"You will receive a dataset called {response_data} and a question called {prompt}. Your task is to analyze the dataset and provide a direct answer to the question based on the data. The response should be as concise as possible, and include only the relevant answer. If the data does not provide the information needed to answer the question, respond with 'Data not found'. Avoid any unnecessary explanation or additional information."
                }

            ]
        )

        return response_AI.choices[0].message.content

    except Exception as e:
        return str(e)



user_api_url = input("Please tell me the API Url: ")

# endpoints = get_endpoints(user_api_url)

user_input = input("Tell me what you want to know: ")

print(get_response_from_ai(user_input))
