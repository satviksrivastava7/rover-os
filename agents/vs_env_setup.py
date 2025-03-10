import os
import subprocess
import time
import pyautogui
from google import genai

def open_vs_code():
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    pyautogui.write('cmd')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.write('d:')
    pyautogui.press('enter')
    pyautogui.write('mkdir experiment')
    pyautogui.press('enter')
    pyautogui.write('cd experiment')
    pyautogui.press('enter')
    pyautogui.write('code .')
    pyautogui.press('enter')
    time.sleep(3)
    subprocess.run('')

def open_vs_code_terminal():
    pyautogui.hotkey('ctrl', 'shift', '`')
    time.sleep(1)

def run_command_in_terminal(command):
    pyautogui.write(command)
    pyautogui.press('enter')
    time.sleep(2)

def setup_virtual_env():
    run_command_in_terminal("python -m venv env")
    time.sleep(2)
    run_command_in_terminal("./env/Scripts/activate")

def create_files():
    for file in ["readme.md", "requirements.txt", "main.py"]:
        run_command_in_terminal(f"type nul > {file}")
        time.sleep(1)

def open_main_py():
    run_command_in_terminal("code main.py")
    time.sleep(2)

def get_response():
    prompt = "Write a Python function to check if a number is prime, call it 10 times with different numbers, and print results."
    api_key = os.getenv('API_KEY')
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text

def write_code_to_main_py():
    code = get_response()
    pyautogui.write(code)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)

def run_main_py():
    open_vs_code_terminal()
    run_command_in_terminal("python main.py")

if __name__ == "__main__":
    open_vs_code()
    #open_vs_code_terminal()
    #setup_virtual_env()
    #create_files()
    #open_main_py()
    #write_code_to_main_py()
    #run_main_py()
