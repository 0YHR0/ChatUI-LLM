import yaml
import requests

# read YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# get the value from yaml
API_URL = config['Remote_API']['API_URL']
headers = config['Remote_API']['Headers']
parameters = config['Parameters']
top_k = parameters['Top_k']
top_p = parameters['Top_p']
temperature = parameters['Temperature']
max_new_tokens = parameters['Max_New_Tokens']

def remote_api(message: str):
    print(API_URL)
    print(headers)
    output = query({
        "inputs": message,
        "parameters": {
            "top_k": top_k,
            "top_p": top_p,
            "temperature": temperature,
            "max_new_tokens": max_new_tokens,

        }
    })
    return output[0]['generated_text']


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


