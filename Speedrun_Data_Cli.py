import json
import requests

# TODO maybe later you can make a gui for this
# but for now you just want to search for a game, get the category that you want, and then get the leaderboard for that category. nothing crazy right now. 
# TODO whenever the user selects that they want the json with info on the game. name the file the name of the game then data so like "{game_name}_data.json"

def search_game(name):
    encoded_name = name.replace(" ", "%20")
    print(encoded_name)
    r = requests.get(f"https://www.speedrun.com/api/v1/games?name={name}")
    return r.json()["data"]

def get_game_id(game_data):
    for i, game in enumerate(game_data, start=1):
        print(f"{i}: {game['names']['international']}")
    choice = int(input("Which game do you want info for? "))
    json_answer = input("Would you like a copy of the json data to a file? (y/n) ")
    if json_answer.lower() == 'y':
        dump_json_to_file(game_data[choice-1], game_data[choice-1]['names']['international'])
    else:
        pass
    return game_data[choice - 1]["id"]

def dump_json_to_file(data, game_name):
    with open(f"{game_name}_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("JSON data saved to run_data.json")

def prompt_user():
    name = input("What game do you want to search for? ")
    return name

def main():
    name = prompt_user()
    game_data = search_game(name)
    game_id = get_game_id(game_data)


    # all the client logic and shit goes here
    
if __name__ == "__main__":
    main()


# json_answer = input("Would you like a copy of the json data to a file? (y/n) ")
#     if json_answer.lower() == "y":
#         dump_json_to_file(r.json())
#     else:
#         pass