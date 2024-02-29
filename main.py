import requests
import time
import json
import os
from colorama import Fore, Style

def read_statuses(file_name):
    with open(file_name, "r") as file:
        return [line.strip() for line in file.readlines()]

def get_user_info(token):
    header = {
        'authorization': token
    }
    r = requests.get("https://discord.com/api/v9/users/@me", headers=header)
    if r.status_code == 200:
        user_info = r.json()
        return user_info["username"] + "#" + user_info["discriminator"], True
    else:
        return "Token invalid", False

def change_status(token, message):
    header = {
        'authorization': token
    }
    jsonData = {
        "status": "online",  # online, idle, invisible, dnd
        "custom_status": {
            "text": message,
        }
    }
    r = requests.patch("https://discord.com/api/v8/users/@me/settings", headers=header, json=jsonData)
    return r.status_code

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

def gradient_text(text):
    num_chars = len(text)
    start_color = Fore.BLUE
    end_color = Fore.CYAN

    # Define the range of color values for each component (R, G, B)
    start_rgb = (0, 0, 139)  # Dark Blue
    end_rgb = (0, 255, 255)  # Light Blue

    # Calculate the color step for each component
    color_step = [(end - start) / num_chars for start, end in zip(start_rgb, end_rgb)]

    # Apply gradient to each character
    gradient_text = ""
    for i, char in enumerate(text):
        # Calculate the interpolated color for this character
        interpolated_color = tuple(int(start + i * step) for start, step in zip(start_rgb, color_step))
        color = f"\033[38;2;{interpolated_color[0]};{interpolated_color[1]};{interpolated_color[2]}m"
        gradient_text += color + char

    return gradient_text + Style.RESET_ALL  # Reset color at the end

def main():
    config = load_config()
    token = config["token"]
    clear_enabled = config["clear_enabled"]
    clear_interval = config["clear_interval"]
    sleep_interval = config["sleep_interval"]

    status_count = 0

    while True:
        user_info, is_valid_token = get_user_info(token)
        statuses = read_statuses("text.txt")
        for status in statuses:
            time_formatted = time.strftime("%I:%M %p:")
            status_colored = gradient_text(status)
            print(f"{time_formatted} Status changed for: {user_info}. New status: {status_colored} Made By Pronhubstar/Germanized")
            change_status(token, status)
            status_count += 1
            time.sleep(sleep_interval)
            if clear_enabled and status_count % clear_interval == 0:
                clear_console()

if __name__ == "__main__":
    main()
