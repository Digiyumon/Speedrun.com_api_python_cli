

https://github.com/user-attachments/assets/e7783eea-c28e-4877-9b19-cd2eb743cea6



# Speedrun.com Data Export Tool

A CLI application for searching games on Speedrun.com, selecting categories, and exporting full leaderboard data to CSV or JSON. 

Working with the Speedrun.com API manually requires looking up game IDs, category keys, and variable parameters. This tool automates those steps through interactive prompts. It exports player names, run dates, times, and platform data, and can optionally upload exports directly to a Google Cloud Storage bucket if a `key.json` file is provided.

## Installation

### Prerequisites
* Python 3.8 or higher installed on your system.

### Setup

1. **Clone the repository:**
   git clone [https://github.com/Digiyumon/speedrun-data-exporter.git](https://github.com/Digiyumon/speedrun-data-exporter.git)
   cd speedrun-data-exporter
   Create and activate a virtual environment:
    
   - Linux/macOS:
    python3 -m venv venv
    source venv/bin/activate

   - Windows (Command Prompt):
    python -m venv venv
    venv\Scripts\activate
   
   - Windows (PowerShell):
    python -m venv venv
    .\venv\Scripts\Activate.ps1

2. **Install dependencies:**
pip install -r requirements.txt

Run the script from your terminal:
"python Speedrun_Data_Cli.py"

Follow the prompts to:

1. Search for a game title.

2. Select a game and category from the search results.

3. Choose your desired output format (.csv or .json).

4. (Optional) Provide Google Cloud Storage credentials to upload the exported file.

Example:
$ python Speedrun_Data_Cli.py

What game do you want to search for? Sonic Adventure 2

1: Sonic Adventure 2
2: Sonic Adventure 2: Battle

Which game do you want info for? 2

Would you like a copy of the json data to a file? (y/n) y
