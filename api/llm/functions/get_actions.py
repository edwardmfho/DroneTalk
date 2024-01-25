import json

from typing import List
from openai import OpenAI
from api.llm.prompts.pilots.prompts import maneuver_prompts

from dotenv import load_dotenv

def get_actions(text: str, client: OpenAI, is_mid_air: bool = False, DEMO_MODE: bool = False) -> List:
    """
    Returns a list of actions based on the text input.
    """
    if DEMO_MODE:
        return ["demo_move"]
    else:
        messages = maneuver_prompts(text, is_mid_air=is_mid_air)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=messages
        )

        actions = json.loads(response.choices[0].message.content)
        return actions.get('actions')

        


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    text = "Tello, now Take off, and land"
    actions = get_actions(text, client)

    print(actions)