import logging
import json

from typing import List, Optional
from openai import OpenAI

from djitellopy import Tello
from dotenv import load_dotenv

from api.model.audios import VerbalCommands
from api.llm.stt.listen import transcribe_audio
from api.llm.functions.get_actions import get_actions

logging.basicConfig(level=logging.DEBUG)


class Drone:
    def __init__(self, is_dotenv: bool=True, DEBUG: bool=False, DEMO_MODE: bool = False):
        self.drone = Tello()
        self.is_mid_air = False
        self.DEBUG = DEBUG
        self.DEMO_MODE = DEMO_MODE

        if is_dotenv:
            load_dotenv()

        if not self.DEBUG:
            logging.info('Connecting to Drone...')
            self.connect()

        # OpenAI
        self.llm = OpenAI()
    
    def connect(self):
        self.drone.connect()

    def prepare_commands(self, actions: List): 
        commands_dict = {
            "takeoff": self.drone.takeoff,
            "landing": self.drone.land,
            "move_up": self.drone.move_up,
            "move_down": self.drone.move_down,
            "move_forward": self.drone.move_forward,
            "move_backward": self.drone.move_back,
            "move_left": self.drone.move_left,
            "move_right": self.drone.move_right,
            "flip_forward": self.drone.flip_forward,
            "flip_backward": self.drone.flip_back
        }

        if self.DEMO_MODE:
            maneuver_steps = [{
                "action": self.drone.takeoff,
            }, 
            {
                "action": self.drone.flip_back,
            },
            {
                "action": self.drone.flip_forward
            },
            {
                "action": self.drone.land
            }]

            return maneuver_steps

        else:
            # Prepare list of maneuver actions to be taken
            maneuver_steps = []
            # For each action, get the function from the dictionary
            for action in actions:
                maneuver = {}
                print('action:' + action['action'])
                print('distance:' + str(action.get('distance', None)))
                maneuver['action'] = commands_dict.get(action['action'])

                if action.get('distance', None) is not None:
                    maneuver['distance'] = action['distance']
                    
                maneuver_steps.append(maneuver) 

            return maneuver_steps

    def execute(self, 
                    audio_command: Optional[VerbalCommands] = None,
                    text_command: Optional[str] = None,) -> List:
        logging.info('Manuvering drone...')
        if audio_command is not None:
            actions = transcribe_audio(audio)
            return get_actions(text=actions.content, client=self.llm, is_mid_air=self.is_mid_air, DEMO_MODE=self.DEMO_MODE)
        if text_command is not None:
            if len(text_command.strip()) == 0:
                return logging.info('Empty command given, please try again...')
            if text_command == 'exit':
                logging.info('Exiting...')
                exit()
            actions = get_actions(text_command, self.llm)
            logging.info('Actions:')
            logging.info(actions)
            command_list = self.prepare_commands(actions)

            self.is_mid_air = True if ('takeoff' in command_list) and ('landing' not in command_list) else False
            
            print(command_list)
            
        if self.DEBUG:
            logging.debug('Returning command list, no action taken.')
            return json.dumps({
            "status" : 200,
            "data" : actions}
            )
        else:
            logging.info("Executing actions...")
            for command in command_list:
                if command.get('distance') is not None:
                    command['action'](command['distance'])
                else:
                    command['action']()

        return json.dumps({
            "status" : 200,
            "data" : actions}
            )
    
    
if __name__ == '__main__':
    DEMO_MODE = False
    drone = Drone(DEBUG=True, DEMO_MODE=DEMO_MODE)
    
    if DEMO_MODE:
        text_command = 'Tello, now Take off, and you should move to the left by 20cm and do a front flip for me, then land.'
        print(drone.execute(text_command=text_command))
    else:
        while True:
            text_command = input('Give out a list of command: ')
            print(drone.execute(text_command=text_command))