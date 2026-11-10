import json
import os
import time

def clear_screen():
    """Clears the Screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def continue_code():
    """Continues the Code"""
    Action = input()

def exit_code():
    """Exits the code"""
    clear_screen()
    print("Exiting...")
    time.sleep(3)
    clear_screen()
    print("Offline")

def print_main_menu():
    """Prints the Main menu"""
    print("Zombie Shelter Manager")
    print("----------------------")
    print("1. View shelter information")
    print("2. Change a shelter value")
    print("3. View change log")
    print("4. Quit")

def get_user_input():
    """Gets User Input"""
    Action =  input("Action: ").strip().upper()
    print("\n")
    return Action

def print_change_choices():
    """Choices for changing bunker stuff"""
    print("What would you like to change?")
    print("------------------------------")
    print("A. Shelter Name")
    print("B. Leader")
    print("C. Survivors")
    print("D. Food")
    print("E. Water")
    print("F. Barricade's Health")
    print("G. Radio Status")

def changing_value():
    """Allows you to input which you would like to change"""
    while True:
        Action = get_user_input()
        if Action == "A":
            Changing = "shelter_name"
            return Changing
        elif Action == "B":
            Changing = "leader"
            return Changing
        elif Action == "C":
            Changing = "survivors"
            return Changing
        elif Action == "D":
            Changing = "food"
            return Changing
        elif Action == "E":
            Changing = "water"
            return Changing
        elif Action == "F":
            Changing = "barricade_health"
            return Changing
        elif Action == "G":
            Changing = "radio_working"
            return Changing
        else:
            print("Invalid Entry")

def change(change):
    """Changes the values for the bunker"""
    data = load_file("r")
    old_value = data[change]
    if change == "radio_working":
        radio_change(data)
    elif change in ("shelter_name", "leader"):
        name_changes(data, change)
    elif change in ("survivors", "food", "water", "barricade_health"):
        number_changes(data, change)
    else:
        raise ValueError(f"Unknown shelter value: {change}")

    new_value = data[change]

    with open("shelter.json", "w") as file:
        json.dump(data, file, indent=4)
        file.write("\n")
    if old_value != new_value:
        message = generate_log_message(change, old_value, new_value)
        create_log(message)


def radio_change(data):
    """Checks for Radio Change"""
    while True:
        Action = input("Is it working (Y/N): ").strip().upper()
        if Action == "Y":
            data["radio_working"] = True
            break
        elif Action == "N":
            data["radio_working"] = False
            break
        else:
            print("Invalid Entry")

def name_changes(data, change):
    """Change for Leader and Bunker Name"""
    while True:
        name = input("Enter the new value: ").strip()
        if len(name) > 0:
            data[change] = name
            break
        else:
            print("Invalid Entry")

def number_changes(data, change):
    """Changing the numbers"""
    while True:
        value = input("Enter the new value (whole number, 0 or greater): ").strip()
        try:
            number = int(value)
        except ValueError:
            print("Invalid Entry")
            continue

        if number >= 0:
            data[change] = number
            break
        print("Invalid Entry")


def load_file(x):
    """Loads the File"""
    with open("shelter.json", x) as file:
        shelter_info = json.load(file)
        return shelter_info
    
def print_shelter_info():
    """Prints the shelter Info"""
    clear_screen()
    shelter_info = load_file("r")
    print("Shelter Info")
    print("------------")
    print(f"Shelter Name: {shelter_info["shelter_name"]}")
    print(f"Leader: {shelter_info["leader"]}")
    print(f"Survivors: {shelter_info["survivors"]}")
    print(f"Food: {shelter_info["food"]}")
    print(f"Water: {shelter_info["water"]}")
    print(f"Barricade_Health: {shelter_info["barricade_health"]}")
    print(f"Radio Working:  {'Yes' if shelter_info['radio_working'] else 'No'}")


    
def check_for_log():
    """Checks for Log"""
    try:
        with open("shelter.log", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def print_logs(lines):
    """Prints the Logs"""
    clear_screen()
    print("Shelter Change Log")
    print("------------------")
    if not lines:
        print("No logs recorded yet.")
    else:
        for line in lines:
            print(line.strip())
    input("\nPress Enter to continue...")
    clear_screen()

def generate_log_message(change, old, new):
    """Generates the diffrent log messages"""
    if change == "survivors":
        difference = abs(new - old)
        if new > old:
            return f"{difference} survivor(s) were added to the shelter."
        else:
            return f"{difference} survivor(s) left the shelter."
    elif change == "food":
        difference = abs(new - old)

        if new > old:
            return f"{difference} food was added to storage."
        else:
            return f"{difference} food was consumed."
    elif change == "water":
        difference = abs(new - old)

        if new > old:
            return f"{difference} water was added to storage."
        else:
          return f"{difference} water was consumed."
    elif change == "barricade_health":
        difference = abs(new - old)
        if new > old:
            return f"Barricades were repaired. Health increased by {difference}."
        else:
            return f"Barricades were damaged. Health decreased by {difference}."
    elif change == "shelter_name":
        return f"Shelter was renamed from {old} to {new}."
    elif change == "leader":
        return f"{new} was appointed as the new leader."
    elif change == "radio_working":
        if new:
            return "Radio communications were restored."
        else:
            return "Radio communications were lost."

def create_log(message):
    """Creates the Log"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("shelter.log", "a") as file:
        file.write(f"[{timestamp}] {message}\n")