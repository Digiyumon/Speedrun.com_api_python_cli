import json
import requests

# TODO maybe later you can make a gui for this
# but for now you just want to search for a game, get the category that you want, and then get the leaderboard for that category. nothing crazy right now. 

#TODO ask the user if they want to get any variables for the game?
# much like with sonic adventure 2, where you can have certain variables for the category, maybe they need a certain variable

# Prompts the user and asks what game they want to search for
def prompt_user():
    name = input("What game do you want to search for? ")
    return name

# Searches the api for the name provided from prompt_user()
def search_game(name):
    r = requests.get(f"https://www.speedrun.com/api/v1/games?name={name}")
    return r.json()["data"]


# After getting the json with all the games, we want to specify which game from the list we want data of
def get_game(game_data):
    for i, game in enumerate(game_data, start=1):
        print(f"{i}: {game['names']['international']}")
    choice = int(input("Which game do you want info for? "))
    json_answer = input("Would you like a copy of the json data to a file? (y/n) ")
    if json_answer.lower() == 'y':
        dump_json_to_file(game_data[choice-1], game_data[choice-1]['names']['international'])
    else:
        pass
    return game_data[choice - 1]

# this just returns the id of the game that we plan on using
def get_game_id(game_data):
    game_id = game_data["id"]
    return game_id

# if we want the json of anything, this will make that for us
# parameters: data we want a json file of, and the name of the source
# returns: nothing
def dump_json_to_file(data, game_name):
    with open(f"{game_name}_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("JSON data saved to run_data.json")

# prompts the user for what category they would like to have the data about
def get_game_category(game_id):
    category_data = requests.get(f"https://www.speedrun.com/api/v1/games/{game_id}/categories")
    category_data = category_data.json()["data"]
    for i, category in enumerate(category_data, start=1):
        print(f"{i}: {category['name']}")
    category_choice = int(input("Which category would you like to focus on? "))
    return category_data[category_choice-1]

def get_category_id(category_data):
    return category_data['id']

# returns the leaderboard data with the game and category that has been chosen.
def get_category_leaderboard(game_id, game_category, variable_id):
    if(variable_id == None):
        leaderboard_data = requests.get(f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{game_category}")
    else:
        leaderboard_data = requests.get(f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{game_category}")
    return leaderboard_data.json()["data"]


#TODO PRINT THE LABEL FOR THE VARIABLE, NO ONE IS GOING TO KNOW WHAT THE FUCK 4QY7X-WHATEVER IS
def get_variable_info(category_id):
    variable_info = {}
    variable_choice = 0
    while True:
        arr = []
        choice = input("Is there a certain variable that you want to get from this category? (y/n) \n")
        if(choice.lower() == 'y'):
            variables = requests.get(f"https://www.speedrun.com/api/v1/categories/{category_id}/variables")
            variables = variables.json()["data"]
            variable_values = variables[0]['values']['values']
            for i, variable in enumerate(variable_values, start=1):
                print(f"{i}: {variable_values[variable]['label']}")
                arr.append(i)
            while variable_choice not in arr:
                variable_choice = int(input("Which variable would you like to use?"))
                if(variable_choice not in arr):
                    print("Just pick one of the valid options please...")
            variable_choice = variable_values[variable_choice-1]
            variable_info["variable_value"] = variable_choice
            variable_info["variable_id"] = variables[0]['id']
            return variable_info
        elif(choice.lower() == 'n'):
            return
        else:
            print("Please select a valid response...")



def create_csv(leaderboard_data):
    pass

def extract_leaderboard_to_csv_or_json(category_leaderboard, game_name):
    answer = 0
    json_file_name = f"{game_name}_leaderboard"
    while answer not in [1,2,3]:
        answer = int(input("Would you like the leaderboard extracted to a json or csv file? \n1. Json\n2. csv\n3. both\n"))
        if answer not in [1,2,3]:
            print("bro just pick a valid one...")
    if(answer == 1):
        dump_json_to_file(category_leaderboard, json_file_name)
    elif(answer == 2):
        pass
    else:
        dump_json_to_file(category_leaderboard, json_file_name)
        pass


def main():
    game_name = prompt_user()
    found_games = search_game(game_name)
    while not found_games:
        print("No games were found. Please be sure to include any hyphens or keywords.")
        game_name = prompt_user()
        found_games = search_game(game_name)
    game_data = get_game(found_games)
    game_id = get_game_id(game_data)
    game_category_data = get_game_category(game_id)
    category_id = get_category_id(game_category_data)
    #if no variable id is chosen, then it just returns as None
    variable_info = get_variable_info(category_id)
    category_leaderboard_data = get_category_leaderboard(game_id, category_id, variable_info)
    extract_leaderboard_to_csv_or_json(category_leaderboard_data, game_name)

if __name__ == "__main__":
    main()