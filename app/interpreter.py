from multiprocessing import Queue
from time import sleep
from typing import Any
import os

import pyautogui
import pyperclip


class Interpreter:
    def __init__(self, status_queue: Queue):
        # MP Queue to put current status of execution in while processes commands.
        # It helps us reflect the current status on the UI.
        self.status_queue = status_queue

    def process_commands(self, json_commands: list[dict[str, Any]]) -> bool:
        """
        Reads a list of JSON commands and runs the corresponding function call as specified in context.txt
        :param json_commands: List of JSON Objects with format as described in context.txt
        :return: True for successful execution, False for exception while interpreting or executing.
        """
        for command in json_commands:
            success = self.process_command(command)
            if not success:
                return False  # End early and return
        return True

    def process_command(self, json_command: dict[str, Any]) -> bool:
        """
        Reads the passed in JSON object and extracts relevant details. Format is specified in context.txt.
        After interpretation, it proceeds to execute the appropriate function call.

        :return: True for successful execution, False for exception while interpreting or executing.
        """
        function_name = json_command['function']
        parameters = json_command.get('parameters', {})
        human_readable_justification = json_command.get('human_readable_justification')
        print(f'Now performing - {function_name} - {parameters} - {human_readable_justification}')
        self.status_queue.put(human_readable_justification)
        try:
            self.execute_function(function_name, parameters)
            return True
        except Exception as e:
            print(f'We are having a problem executing this - {e}')
            return False

    def execute_function(self, function_name: str, parameters: dict[str, Any]) -> None:
        """
        We are expecting only two types of function calls below
        1. time.sleep() - to wait for web pages, applications, and other things to load.
        2. pyautogui calls to interact with system's mouse and keyboard.
        """
        # Sometimes pyautogui needs warming up i.e. sometimes first call isn't executed hence padding a random call here
        pyautogui.press("command", interval=0.2)

        if function_name == "sleep" and parameters.get("secs"):
            sleep(parameters.get("secs"))
        elif hasattr(pyautogui, function_name):
            # Execute the corresponding pyautogui function i.e. Keyboard or Mouse commands.
            function_to_call = getattr(pyautogui, function_name)

            # Special handling for the 'write' function to support Vietnamese
            if function_name == 'write' and ('string' in parameters or 'text' in parameters):
                string_to_write = parameters.get('string') or parameters.get('text')
                interval = parameters.get('interval', 0.1)
                
                # Handle Vietnamese text by using pyperclip
                pyperclip.copy(string_to_write)
                pyautogui.hotkey('ctrl', 'v') if os.name == 'nt' else pyautogui.hotkey('command', 'v')
                
            elif function_name == 'press' and ('keys' in parameters or 'key' in parameters):
                keys_to_press = parameters.get('keys') or parameters.get('key')
                presses = parameters.get('presses', 1)
                interval = parameters.get('interval', 0.1)
                function_to_call(keys_to_press, presses=presses, interval=interval)
            elif function_name == 'hotkey':
                function_to_call(*parameters['keys'])
            else:
                function_to_call(**parameters)
        else:
            print(f'No such function {function_name} in our interface\'s interpreter')
