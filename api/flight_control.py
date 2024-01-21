import logging

from typing import List, Optional
from openai import OpenAI

from djitellopy import Tello
from dotenv import load_dotenv

from api.model.audios import VerbalCommands
from api.llm.stt.listen import transcribe_audio
from api.llm.functions.get_actions import get_actions

logging.basicConfig(level=logging.INFO)


class Drone:
    def __init__(self, is_dotenv=True, DEBUG=False):
        self.drone = Tello()
        if is_dotenv:
            load_dotenv()

        if not DEBUG:
            
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
            return get_actions(actions.content, self.llm)
        if text_command is not None:
            if len(text_command.strip()) == 0:
                return logging.info('Empty command given, please try again...')
            if text_command == 'exit':
                logging.info('Exiting...')
                exit()
            actions = get_actions(text_command, self.llm)
            print('Actions: ', sep=" ")
            print(actions)
            command_list = self.prepare_commands(actions)
            
            for command in command_list:
                if command.get('distance') is not None:
                    command['action'](command['distance'])
                else:
                    command['action']()
            return command_list
    
    
if __name__ == '__main__':
    drone = Drone(DEBUG=True)
    while True:
        text_command = input('Give out a list of command: ')
        # text_command = "Tello, now Take off, and you should move to the left by 20cm and do a back flip for me"
        print(drone.execute(text_command=text_command))