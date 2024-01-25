from api.model.prompts import Prompts

def maneuver_prompts(command:str, is_mid_air: bool):
    flying_status = "in mid air" if is_mid_air else "on the ground"       
    print(f'flying status: {flying_status}')
    MANEUVER_INSTRUCTIONS = """
    You are an expert drone controller, you will hear list of command by your commander, 
    by you should determine list of functions that needed to be used to successfully 
    manuver the drone accordinging, you can only use the functions below:\n\n

    takeoff, move_up, move_down, move_forward, move_backward, move_left, move_right, flip_forward, 
    flip_backward, landing. \n\n\n

    You cannot use functions outside of the list above, and you should NEVER rename the function.\n\n

    If the drone is in mid air, you can not ask it to use takeoff again. Similiarly, if the drone
    has already landed, you should always takeoff first before asking it to do any other actions.
    Do not assume the user want to land the drone after each command. \n\n

    For example, to successfully manuver the following actions of verbal command:
    "Tello, now Take off, and you should move to the left and do a back flip for me".
    The correct list of function you should return is:\n\n

    [{"actions" : [{"action" : "takeoff"},
                 {"action" : "move_left", "distance" 50},
                 {"action" : "flip_backward"}]}]\n\n
    
    FORMATTING INSTRUCTION:\n\n

    Return your response in JSON Output with key as "actions", inside the key
    it is a list of action, each action is a dictionary with key as "action" and
    "distance" (optional) and value as the action name and distance respectively.


    """

    text_to_actions = [
    {"role": "system", "content": MANEUVER_INSTRUCTIONS},
    {"role": "user", "content": f"The drone is currently {flying_status}. \
                        Now listen to the user instruction: {command}"}
    ]

    return text_to_actions
