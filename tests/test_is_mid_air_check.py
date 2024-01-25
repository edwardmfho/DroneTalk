import pytest
import json

from api.flight_control import Drone

tello = Drone(DEBUG=True, DEMO_MODE=False)

def test_takeoff():
    instruction = "Hey take off."

    response = json.loads(tello.execute(text_command=instruction))
    assert response['data'][0] == {"action" : "takeoff"}

def test_mid_air():
    instructions = ["Hey take off and do a backflip.", "Now move to the right and land", "Do a backflip"]
    responses = []
    for instruction in instructions:
        response = json.loads(tello.execute(text_command=instruction))['data']
        responses.append(response)

    assert responses[0] == [{"action" : "takeoff"}, {"action" : "flip_backward"}]
    assert responses[1] == [{'action': 'takeoff'}, {'action': 'move_right', 'distance': 50}, {'action': 'landing'}]
    assert responses[2] == [{'action': 'takeoff'}, {'action': 'flip_backward'}]

def test_wrong_landing():
    instruction = "Hey land now."
    response = json.loads(tello.execute(text_command=instruction))
    assert response['data'] == [{"action" : "takeoff"}, {"action" : "landing"}]
