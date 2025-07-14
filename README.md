🕹️ Speedrun.com Leaderboard Export Tool

A Python command-line application that lets you search for any game on Speedrun.com, view its categories, and export full leaderboard data to CSV or JSON — all without manually touching the API.
🚀 Features

    🔍 Search for games and select specific categories

    📊 Export leaderboard data in .csv or .json format

    ✅ Optional field selection (e.g., player name, time, date, platform)

    🧠 Automatically resolves player IDs to usernames

    🔄 Handles subcategories, platform filters, and emulated runs

    ⏱️ Built-in progress tracking and API rate limit awareness

    💥 Cuts manual data collection time by over 90%

📦 Example Usage

$ python Speedrun_Data_Cli.py
What game do you want to search for? Sonic Adventure 2
1: Sonic Adventure 2
2: Sonic Adventure 2: Battle
Which game do you want info for? 2
Would you like a copy of the json data to a file? (y/n) y
...

CSV output will include fields you select (e.g., real-time, in-game time, player name, etc.).
🛠️ Tech Stack

    Python 3

    requests

    json

    csv

📁 Output

    {game_name}_data.json — base game info (optional)

    {category_name}_leaderboard.csv — leaderboard export

    Automatically named for clarity and organization

💡 Future Plans

    GUI with Tkinter or PyQT

    Batch game/category export


🧠 Why This?

Working with the Speedrun.com API by hand is tedious. This tool turns a 15–20 minute multi-query process into a simple 30-second CLI interaction — ideal for speedrun analysts, game researchers, and hobbyist devs.
