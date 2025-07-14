import json
import requests
import csv
import time

notify_user_of_api_bottleneck = False

# TODO maybe later you can make a gui for this
# but for now you just want to search for a game, get the category that you want, and then get the leaderboard for that category. nothing crazy right now. 

def prompt_user():
    name = input("What game do you want to search for? ")
    return name

def search_game(name):
    r = requests.get(f"https://www.speedrun.com/api/v1/games?name={name}")
    return r.json()["data"]

def get_game(game_data):
    while True:
        for i, game in enumerate(game_data, start=1):
            print(f"{i}: {game['names']['international']}")
        if(len(game_data) != 0):
            print(f"{len(game_data) + 1}: None of these — search again")

        try:
            choice = int(input("Which game do you want info for? "))
            if 1 <= choice <= len(game_data):
                break
            elif choice == len(game_data) + 1:
                new_name = prompt_user()
                game_data = search_game(new_name)
            else:
                print("Please enter a number from the list.")
        except ValueError:
            print("That's not a valid number. Try again.")

    json_answer = input("Would you like a copy of the json data to a file? (y/n) ")
    if json_answer.lower() == 'y':
        dump_json_to_file(game_data[choice-1], game_data[choice-1]['names']['international'])

    return game_data[choice - 1]

def get_international_game_name(game_data):
    return game_data["names"]["international"]

# this just returns the id of the game that we plan on using
def get_game_id(game_data):
    game_id = game_data["id"]
    return game_id

def dump_json_to_file(data, game_name):
    with open(f"{game_name}_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("JSON data saved to file!")

def get_game_category_data(game_id):
    category_data = requests.get(f"https://www.speedrun.com/api/v1/games/{game_id}/categories")
    category_data = category_data.json()["data"]
    for i, category in enumerate(category_data, start=1):
        print(f"{i}: {category['name']}")
    category_choice = int(input("Which category would you like to focus on? "))
    return category_data[category_choice-1]

def get_category_id(category_data):
    return category_data['id']

def get_category_name(category_data):
    return category_data['name']

def get_category_leaderboard(game_id, game_category, variable_info):
    has_variable_been_added = False
    if(variable_info == None):
        leaderboard_data = requests.get(f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{game_category}")
    else:
        for i, variable in enumerate(variable_info):
            if(variable_info[i]):
                variable_value = variable_info[i]['variable_value']
                variable_id = variable_info[i]['variable_id']
                if(not has_variable_been_added):
                    request_string: str = f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{game_category}?var-{variable_id}={variable_value}"
                    has_variable_been_added = True
                else:
                    request_string += f"&var-{variable_id}={variable_value}"
        leaderboard_data = requests.get(request_string)
    return leaderboard_data.json()["data"]

def get_number_of_variables(category_id):
    variables = requests.get(f"https://www.speedrun.com/api/v1/categories/{category_id}/variables")
    variables = variables.json()["data"]
    return len(variables)

def does_user_want_variables():
    while True:
        choice = input("Is there a certain variable that you want to get from this category? (y/n) \n")
        if(choice.lower() == 'y'):
            return True
        elif(choice.lower() == 'n'):
            return False
        else: return False

def did_user_skip_all_variables(current_variable_info):
    total_variable_count = len(current_variable_info)
    total_skipped = 0
    for i,variable in enumerate(current_variable_info):
        if(not current_variable_info[i]):
            total_skipped += 1
    if(total_skipped == total_variable_count):
        return True
    else: return False

def get_variable_info(category_id, total_number_of_variables):
    import requests

    variables = requests.get(f"https://www.speedrun.com/api/v1/categories/{category_id}/variables")
    variables = variables.json()["data"]
    variable_info = {}

    for i in range(total_number_of_variables):
        variable_labels = []
        arr = []
        variable_info[i] = {}

        variable_values = variables[i]['values']['values']

        print(f"\nChoose a value for: {variables[i]['name']}")
        for idx, variable in enumerate(variable_values, start=1):
            print(f"{idx}: {variable_values[variable]['label']}")
            arr.append(idx)
            variable_labels.append(variable)

        print("0: Skip this variable")

        variable_choice = -1
        while variable_choice not in arr and variable_choice != 0:
            try:
                variable_choice = int(input("Your choice: "))
                if variable_choice not in arr and variable_choice != 0:
                    print("Please pick a valid option or type 0 to skip.")
            except ValueError:
                print("Enter a number, please.")

        if variable_choice == 0:
            continue  # Skip this variable

        variable_label_choice = variable_labels[variable_choice - 1]
        variable_info[i]["variable_value"] = variable_label_choice
        variable_info[i]["variable_id"] = variables[i]['id']

    return variable_info



def choose_csv_fields():
    options = [
        ("Time", "time"),
        ("Player Names", "player"),
        ("Date", "date"),
        ("Platform", "platform")
    ]
    selected = set()
    while True:
        print("\nWhat info do you want in your CSV?")
        for i, (label, _) in enumerate(options, start=1):
            mark = "[x]" if i in selected else "[ ]"
            print(f"{i}. {label} {mark}")
        print(f"{len(options)+1}. Make CSV")
        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if choice == len(options) + 1:
            break
        elif 1 <= choice <= len(options):
            if choice in selected:
                selected.remove(choice)
            else:
                selected.add(choice)
        else:
            print("Invalid choice.")
    return [options[i-1][1] for i in sorted(selected)]

def check_different_times(leaderboard_data):
    #NOTE if this doesn't really end up working in the future. Then instead of counting the zeros, we can just 
    # look at the id for each one. 
    #this variable will just keep track of how many times each type of time tracking has a zero
    realtime_dif_counter = 0
    ingame_dif_counter = 0
    iteration_counter = 0
    leaderboard_data_runs = leaderboard_data['runs']
    for run_entry in leaderboard_data_runs:
        run = run_entry['run']
        run_times = run['times']

        #times
        primary_t = run_times['primary_t']
        realtime_t = run_times['realtime_t']
        ingame_t= run_times['ingame_t']

        #checking if the times are not zero and not equal to the primary time
        if(realtime_t != 0 and realtime_t != primary_t):
            realtime_dif_counter +=1
        if(ingame_t != 0 and ingame_t != primary_t):
            ingame_dif_counter+=1
        if(realtime_dif_counter >=10 or ingame_dif_counter >= 10):
            break
        if(iteration_counter < 15):
            iteration_counter+=1
        elif iteration_counter == 15:break

    #after iterating through, we check to see which ones we need to return
    if(ingame_dif_counter == 10 and realtime_dif_counter == 10):
        return "both"
    elif(realtime_dif_counter == 0 and ingame_dif_counter == 0):
        return "neither"
    elif(ingame_dif_counter == 10):
        return "ingame"
    elif(realtime_dif_counter == 10):
        return "realtime"
    return "neither"

def choose_time_fields(times_to_ask):
    if(times_to_ask == "neither"):
        return ["Primary"]
    options = [("Primary_Time", "Primary")]
    if(times_to_ask == "realtime"):
        options.append(("RealTime_Time", "RealTime"))
    elif(times_to_ask == "ingame"):
        options.append(("InGame_Time", "InGame"))
    elif(times_to_ask ==  "both"):
        options.append(("RealTime_Time", "RealTime"))
        options.append(("InGame_Time", "InGame"))
    selected = set()
    while True:
        print("\nWhat info do you want in your CSV?")
        for i, (label, _) in enumerate(options, start=1):
            mark = "[x]" if i in selected else "[ ]"
            print(f"{i}. {label} {mark}")
        print(f"{len(options)+1}. Make CSV")
        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if choice == len(options) + 1:
            break
        elif 1 <= choice <= len(options):
            if choice in selected:
                selected.remove(choice)
            else:
                selected.add(choice)
        else:
            print("Invalid choice.")
    return [options[i-1][1] for i in sorted(selected)]

def name_consoles(console_id, existing_consoles):
    if(console_id in existing_consoles):
        return existing_consoles[console_id]
    else:
        console_data = requests.get(f"https://www.speedrun.com/api/v1/platforms/{console_id}")
        console_data = console_data.json()
        console_name = console_data["data"]["name"]
        existing_consoles[id] = console_name
        return console_name

def print_progress_bar(current, total, length=40):
    percent = current / total
    filled = int(length * percent)
    bar = '█' * filled + '-' * (length - filled)
    print(f"\rFetching player names... |{bar}| {int(percent * 100)}% ({current}/{total})", end='', flush=True)

def player_id_to_player_name(player_id, total_players,current_player):
    global notify_user_of_api_bottleneck
    # Simulate a loading dot animation
    user_data = requests.get(f"https://www.speedrun.com/api/v1/users/{player_id}")
    if(total_players > 60):
        if(notify_user_of_api_bottleneck == False):
            print("Fetching player names — this may take a moment due to API limits...\n")
            notify_user_of_api_bottleneck = True
        print_progress_bar(current_player, total_players)
        time.sleep(0.5)
    user_data = user_data.json()
    user_names = user_data["data"]["names"]
    player_name = user_names["international"]
    return player_name

def get_highest_place(leaderboard_data):
    places = [entry["place"] for entry in leaderboard_data["runs"]]
    return max(places)

def create_csv(leaderboard_data, game_name, csv_fields, category_name):
    times_in_csv = []
    fieldnames = csv_fields
    if ('time' in fieldnames):
        times_to_ask = check_different_times(leaderboard_data)
        if(times_to_ask != 'neither'):
            print("What times would you like to have columns of?")
        times_in_csv = choose_time_fields(times_to_ask)
        fieldnames.remove("time")
    if (len(times_in_csv) != 1):
        for time in times_in_csv:
            fieldnames.append(time)
    else:
        fieldnames.append(times_in_csv[0])

    runs = leaderboard_data["runs"]

    total_players = get_highest_place(leaderboard_data) * len(runs[0]["run"]["players"])
    current_player = 0
    with open(f"{game_name}_{category_name}_leaderboard.csv", "w", newline="", encoding="utf-8") as csvfile:
            existing_platforms = {}
            writing_dictionary = {}
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i, run_entry in enumerate(runs, start=1):
                run = run_entry["run"]
                if("Primary" in fieldnames):
                    writing_dictionary["Primary"] = run["times"]["primary_t"]
                if("RealTime" in fieldnames):
                    writing_dictionary["RealTime"] = run["times"]["realtime_t"]
                if("InGame" in fieldnames):
                    writing_dictionary["InGame"] = run["times"]["ingame_t"]
                if("player" in fieldnames):
                    writing_dictionary["player"] = []
                    for player_index in range(len(run["players"])):
                        if "id" in run["players"][player_index]:
                            player_id = run["players"][player_index]["id"]
                            if(len(runs[0]["run"]["players"]) != 1):
                                writing_dictionary["player"].append(player_id_to_player_name(player_id, total_players, current_player))
                            else:
                                writing_dictionary["player"] = player_id_to_player_name(player_id, total_players, current_player)
                        else:
                            writing_dictionary["player"] = run["players"][player_index]["name"]
                        current_player+=1
                if("date" in fieldnames):
                    writing_dictionary["date"] = run["date"]
                if("platform" in fieldnames):
                    writing_dictionary["platform"] = name_consoles(run["system"]["platform"], existing_platforms)
                    if (run["system"]["emulated"] == True):
                        writing_dictionary["platform"] = f"emulated_{writing_dictionary["platform"]}"
                writer.writerow(writing_dictionary)
            print("CSV file has been created!")
            pass

def extract_leaderboard_to_csv_or_json(leaderboard_data, game_name, category_name):
    answer = 0
    json_file_name = f"{game_name}_{category_name}_leaderboard"
    while answer not in [1,2,3]:
        answer = int(input("Would you like the leaderboard extracted to a json or csv file? \n1. Json\n2. csv\n3. both\n"))
        if answer not in [1,2,3]:
            print("bro just pick a valid one...")
    if(answer == 1):
        dump_json_to_file(leaderboard_data, json_file_name)
    elif(answer == 2):
        csv_fields = choose_csv_fields()
        create_csv(leaderboard_data, game_name, csv_fields,category_name)
        pass
    else:
        dump_json_to_file(leaderboard_data, json_file_name)
        csv_fields = choose_csv_fields()
        create_csv(leaderboard_data, game_name, csv_fields,category_name)
        pass

#TODO: whenever te user picks the name for the game, have the file that's saved, but the actual name of the game, not what they typed in to look up the game.
def main():
    variable_info = []
    game_name = prompt_user()
    found_games = search_game(game_name)
    while not found_games:
        print("No games were found. Please be sure to include any hyphens or keywords.")
        game_name = prompt_user()
        found_games = search_game(game_name)
    game_data = get_game(found_games)
    international_game_name = get_international_game_name(game_data)
    game_id = get_game_id(game_data)
    game_category_data = get_game_category_data(game_id)
    category_id = get_category_id(game_category_data)
    category_name = get_category_name(game_category_data)
    #if no variable id is chosen, then it just returns as None
    number_of_variables = get_number_of_variables(category_id)
    if(number_of_variables >= 1):
        variable_choice = does_user_want_variables()
        if(variable_choice):
            variable_info = get_variable_info(category_id, number_of_variables)
            if(did_user_skip_all_variables(variable_info) == True):
                variable_info = None
        else: variable_info = None
    else:
        variable_info = None
    category_leaderboard_data = get_category_leaderboard(game_id, category_id, variable_info)
    extract_leaderboard_to_csv_or_json(category_leaderboard_data, international_game_name, category_name)

if __name__ == "__main__":
    main()