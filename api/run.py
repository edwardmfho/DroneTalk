from flask import Flask, request 
from api.flight_control import Drone

app = Flask(__name__)
drone = Drone(DEBUG=True)

@app.route('/v1/create/flight-plan', methods=['GET'])
def create_flight_plan():
    commands = request.args.get('command')
    command_list = drone.execute(text_command=commands)
    return command_list

if __name__ == '__main__':
    app.run()
