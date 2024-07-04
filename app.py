import chainlit as cl
import yaml
import remote_api
import deploy_local

# read YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

mode = config['Mode']


@cl.step(type="tool")
async def tool(message):
    result = ""
    if mode == "local":
        result = deploy_local.request_local_llm(message)
    elif mode == "remote":
        result = remote_api.remote_api(message)
    else:
        raise Exception("The model can only be either remote or local")
    # await cl.sleep(2)
    return result


'''
This function will be called every time a user inputs a message in the UI
'''


@cl.on_message
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """

    input = message.content
    print(input)

    # # Upload file
    # if "sentiment" in message:
    #     file = None
    #     while file == None:
    #         file = cl.ask_for_file(title="Please upload a text file to analyse", accept=["text/plain"])

    final_answer = await cl.Message(content="Generating responses...").send()

    # Call the tool
    final_answer.content = await tool(input)

    await final_answer.update()


'''
Do something when start the application

'''


@cl.on_chat_start
def start():
    print("init...")
    content = "This is an LLM UI"
    cl.send_message(content=content)
