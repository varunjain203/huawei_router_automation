# huawei-router-signal-refresh
Am currently using a Huawei CPE PRO 3 Model: H138-380.
I noticed the router sometime loses 5G signal leading to reduced speeds on 4G mode.
The fix is always going into router page and doing a signal test. This action refreshed the mobile signals received by the router and activates 5G speeds.
Thus I created an automation script that automatcically log-ins to your router and press the necessary buttons to this task every hour.
I have connected a raspberry Pi4 on the router's LAN port so it can connect to 192.168.8.1 which is the router web page.



Prerequisites & Setup for Raspberry Pi
1. System Installation
Raspberry Pi OS (especially the 64-bit version) is recommended. You must install the Chromium browser and its corresponding driver via the terminal, as standard pip install methods for WebDrivers often fail on ARM architecture.

Bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install Chromium and the Driver
sudo apt install -y chromium-browser chromium-chromedriver
2. Python Environment Setup (venv)
To avoid conflicting with system-wide packages, we create a virtual environment.

Bash
# Navigate to your script's folder
cd /home/pi/huawei_router_automation

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install Selenium
pip install selenium
Scheduling the Script with Cron
Since this script manages your router's signal optimization, you likely want it to run automatically (e.g., every morning at 4:00 AM).

Step 1: Get the Absolute Paths
Cron needs full paths to work correctly. Find yours by running:

Python Path: While the venv is active, type which python. (e.g., /home/pi/huawei_router_automation/venv/bin/python)

Script Path: Type readlink -f your_script_name.py. (e.g., /home/pi/huawei_router_automation/router-refresh.py)

Step 2: Edit Crontab
Open the cron scheduler:

Bash
crontab -e
Step 3: Add the Schedule
Add this line to the bottom of the file (adjusting the paths to match your results from Step 1):

Code snippet
00 04 * * * /home/pi/huawei_router_automation/venv/bin/python /home/pi/router-script/router-refresh.py >> /home/pi/router-script/log.txt 2>&1
Pro Tip: The >> ... 2>&1 part creates a log.txt file. If the script fails, you can check this file to see the error messages (like "Element Not Found").
