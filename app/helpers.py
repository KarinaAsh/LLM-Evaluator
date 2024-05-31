import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Define BASEDIR for the Project
BASEDIR = Path(__file__).parents[1]

# Load environment variables locally
if os.path.isfile(os.path.join(BASEDIR, ".env")):
    load_dotenv(os.path.join(BASEDIR, ".env"))



def mistral(user_message,
            model,
            is_json=False):
    """
    Interact with the Mistral AI model to generate a response based on the user message.

    Args:
    ----
        user_message (str): The message input from the user to send to the AI model.
        model (str): The specific model to be used for generating the response.
        is_json (bool): Flag to determine if the response should be in JSON format. Defaults to False.

    Returns:
    -------
        str: The content of the response message from the AI model.

    """
    client = MistralClient(api_key=os.environ.get("MISTRAL_API_KEY", None))
    messages = [ChatMessage(role="user", content=user_message)]
    if is_json:
        chat_response = client.chat(
            model=model,
            messages=messages,
            response_format={"type": "json_object"})
    else:
        chat_response = client.chat(
            model=model,
            messages=messages)

    return chat_response.choices[0].message.content
