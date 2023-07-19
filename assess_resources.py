#!/usr/bin/env python3

import psutil
import os
import textwrap
from datetime import datetime

#######################
## Epigenerate Users ##
#######################

epigenerate_users = {
#"ammadany": "ammadany@ucdavis.edu",
#"apmendio": "apmendiola@ucdavis.edu",
#"fugon": "ojgutierrez@ucdavis.edu",
#"gekuodza": "gekuodza@ucdavis.edu",
#"jlhuang": "jehuang@ucdavis.edu",
#"jmouat": "jmouat@ucdavis.edu",
#"kechau": "kchau@ucdavis.edu",
#"lwilli": "lwilli@ucdavis.edu",
#"osharifi": "osharifi@ucdavis.edu",
"vhaghani": "vhaghani@ucdavis.edu"
}

check_every_secs = 60 # How frequently to check memory usage in seconds
tot_ram_lim = 495 # Total RAM limit to exceed before notifying all users
user_ram_lim = 250 # RAM limit to exceed before notifying a specific user
logs_dir = '/share/lasallelab/programs/assess_resources/logs' # Path to put output logs

############################
## Calculate Memory Usage ##
############################

# Calculate total memory usage
def calculate_total_memory_usage():
    total_memory = psutil.virtual_memory().used / (1024 ** 3)  # Memory usage in GB
    return total_memory

# Get memory usage divisions per user 
def get_active_users_memory():
    active_users_memory = {}
    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB
            active_users_memory[user] = active_users_memory.get(user, 0) + memory_usage_gb
    return active_users_memory

###################
## Assess Memory ##
###################

# Run endless loop to assess memory 
i = 1
while i > 0:
    # Calculate memory
    os.system(f'sleep {check_every_secs}') # Wait for the specified amount of time
    mem_used = calculate_total_memory_usage() # Float
    mem_per_user = get_active_users_memory() # Dictionary
 
    # Email all active users if total memory usage exceeds total RAM limit
    if mem_used >= tot_ram_lim:
        for user, memory_usage in mem_per_user.items():
            if user in epigenerate_users:
                # Draft message
                users_info = '\n'.join([f'{user}: {memory_usage} GB' for user, memory_usage in mem_per_user.items()])
                notify_function = textwrap.dedent(f"""
                notify() {{
                    DETAILS='RAM usage on epigenerate has exceeded {tot_ram_lim} GB and will likely crash. Here are the current users and their memory usage:
                    
                    {users_info}
                    
                    As soon as you see this email, please coordinate with current users in the Epigenerate Slack channel to work out a solution. This can include killing a job if you are running a resource-intensive or non-urgent job.'
                    cat <<EOF | sendmail {epigenerate_users[user]}
                Subject: [URGENT] Impending Epigenerate Crash
                From: SSH Notification <vhaghani@epigenerate.ucdavis.edu>
                
                $DETAILS
                EOF
                }}
                """)
                notify_function = notify_function.replace(' '*4, '')
                # Save message into log file
                now = datetime.now()
                now = now.strftime("%Y_%m_%d_%H:%M:%S")
                os.system(f'touch {logs_dir}/{now}_{user}_epigenerate_total.sh')
                with open(f'{logs_dir}/{now}_{user}_epigenerate_total.sh', 'w') as f:
                    f.write(f'{notify_function}')
                os.system(f'chmod 777 {logs_dir}/{now}_{user}_epigenerate_total.sh')
                # Send notification 
                os.system(f'. {logs_dir}/{now}_{user}_epigenerate_total.sh && notify')
    
    # Email a user if they are using more than the user RAM limit 
    for user, memory_usage in mem_per_user.items():
        if memory_usage > user_ram_lim:
            # Draft message
            notify_function = textwrap.dedent(f"""
            notify() {{
                DETAILS='You are currently using {memory_usage} GB of RAM. Your user allotment is {user_ram_lim} GB. If you have already checked with other users that your usage is permitted, please disregard this message. If this was not intended, please reassess and adjust your job accordingly to prevent Epigenerate from crashing.'
                cat <<EOF | sendmail {epigenerate_users[user]}
            Subject: Epigenerate RAM Warning
            From: SSH Notification <vhaghani@epigenerate.ucdavis.edu>
            
            $DETAILS
            EOF
            }}
            """)
            # Save message into log file
            now = datetime.now()
            now = now.strftime("%Y_%m_%d_%H:%M:%S")
            os.system(f'touch {logs_dir}/{now}_{user}.sh')
            with open(f'{logs_dir}/{now}_{user}.sh', 'w') as f:
                f.write(f'{notify_function}')
            os.system(f'chmod 777 {logs_dir}/{now}_{user}.sh')
            # Send notification 
            os.system(f'. {logs_dir}/{now}_{user}.sh && notify')