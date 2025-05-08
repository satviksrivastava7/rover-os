import os
import time
import pyautogui
import pyperclip
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
    time.sleep(10)

def open_vs_code_terminal():
    pyautogui.hotkey('ctrl', 'shift', '`')
    time.sleep(2)

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

    if not api_key:
        raise ValueError("API_KEY environment variable not set.")
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        code_text = response.text.strip()
        if code_text.startswith('```python'):
            code_text = code_text.replace('```python', '').strip()
        if code_text.endswith('```'):
            code_text = code_text.replace('```', '').strip()
        return code_text
    except Exception as e:
        print(f"Error getting response from AI: {e}")
        return ""

def write_code_to_main_py():
    code = get_response()
    if not code:
        print("No code received from AI. Skipping write.")
        return

    print("Copying code to clipboard...")
    try:
        pyperclip.copy(code)
        time.sleep(1)

        print("Pasting code into VS Code and saving...")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        print("Code pasted and file saved.")

    except pyperclip.PyperclipException:
        print("Error: Could not access the clipboard. Make sure you have a clipboard tool installed (like xclip on Linux).")
    except Exception as e:
        print(f"An error occurred during code writing: {e}")

def run_main_py():
    open_vs_code_terminal()
    run_command_in_terminal("python main.py")

if __name__ == "__main__":
    open_vs_code()
    open_vs_code_terminal()
    setup_virtual_env()
    create_files()
    open_main_py()
    write_code_to_main_py()
    run_main_py()
