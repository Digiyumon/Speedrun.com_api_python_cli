# Speedrun.com Data Export Tool
A Python command-line application that lets you search for any game on Speedrun.com, view its categories, and export full leaderboard data to CSV or JSON — all without manually touching the API. You can export the necessary information such as player names, date, times and platform. 

I created this because working with the API manually is an incredible hassle and I couldn't find anything that already accomplished what this program sets out to do. Instead of having to find the game id, then the specific category, along with the variables and put those into the url, you can just use this application to do all that for you. 


## Installation

🚀 How to Use This Tool

This script lets you quickly search for a game on speedrun.com, select a category, and export leaderboard data to CSV or JSON — no more digging through the API manually.
📦 Step 1: Install Python

If you don't have Python 3 installed, download it here:
👉 https://www.python.org/downloads/

    Make sure to check “Add Python to PATH” during installation!

📁 Step 2: Download the Project

You can either:

    Click the green Code button on GitHub → Download ZIP
    Then extract the folder.

OR

    Use Git:

    git clone https://github.com/yourusername/speedrun-data-exporter.git
    cd speedrun-data-exporter

📄 Step 3: Create requirements.txt

    If it’s not already included, create a new text file called requirements.txt in the project folder and add this line:

    requests

    Save the file.
🔧 Step 4: Install Required Packages

    In your terminal or command prompt, navigate to the project folder and run:
    
    pip install -r requirements.txt
    
    This installs the requests library used for API access.
🏁 Step 5: Run the Program

Once everything’s installed, run:

python Speedrun_Data_Cli.py

Follow the on-screen prompts to:

    Search for a game

    Select categories and subcategories

    Choose what data to export

    Output to a .csv or .json file
    
## Usage/Examples

📦 Example Usage

    $ python Speedrun_Data_Cli.py
    
    What game do you want to search for? Sonic Adventure 2
    
    1: Sonic Adventure 2

    2: Sonic Adventure 2: Battle
    
    Which game do you want info for? 2
    
    Would you like a copy of the json data to a file? (y/n) y
    
    ...
## Lessons Learned

Learned a lot about how to use requests from an API and the data that comes along with it. How to traverse the data and ensure that I'm getting the data that I need. Also about file formatting and how to export necessary data to the file types that are requested. 
## Roadmap
Not much really, I was thinking about making a gui for this, but it's not that serious. Just fixing any bugs that are requested if this becomes popular enough. Other than that, i'm kinda done with it. 
