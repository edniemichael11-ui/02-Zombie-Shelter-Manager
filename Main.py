import Functions


if __name__ == "__main__":
    while True:
        Functions.print_main_menu()
        Action = Functions.get_user_input()
        if Action == "1":
            Functions.print_shelter_info()
            Functions.continue_code()
            Functions.clear_screen()
        elif Action == "2":
            Functions.print_change_choices()
            Changing = Functions.changing_value()
            Functions.change(Changing)
            Functions.clear_screen()
        elif Action == "3":
            lines = Functions.check_for_log()
            Functions.print_logs(lines)
        elif Action == "4":
            Functions.exit_code()
            break
        else:
            print("Invalid Entry")
       