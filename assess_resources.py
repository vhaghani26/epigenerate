#!/usr/bin/env python3

import psutil
import time
import os
import textwrap
from datetime import datetime

###############
## Variables ##
###############

epigenerate_users = {
"ammadany": "ammadany@ucdavis.edu",
"apmendio": "apmendiola@ucdavis.edu",
"fugon": "ojgutierrez@ucdavis.edu",
"gekuodza": "gekuodza@ucdavis.edu",
"jlhuang": "jehuang@ucdavis.edu",
"jmouat": "jmouat@ucdavis.edu",
"kechau": "kchau@ucdavis.edu",
"lwilli": "lwilli@ucdavis.edu",
"osharifi": "osharifi@ucdavis.edu",
"vhaghani": "vhaghani@ucdavis.edu"
}

check_every_secs = 1 # How frequently to check memory usage in seconds
tot_ram_lim = 495 # Total RAM limit to exceed before notifying all users
user_ram_lim = 250 # RAM limit to exceed before notifying a specific user
logs_dir = '/share/lasallelab/programs/assess_resources/logs' # Path to put output logs
sender_email = 'vhaghani@epigenerate.ucdavis.edu' # Email from which notifications get sent about RAM usage

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

'''
def get_active_users_memory():
    active_users_memory = {}
    active_users_pids = {}  # To track unique PIDs for each user

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']

            # Check if the PID is already counted for this user
            if pid not in active_users_pids.get(user, set()):
                memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB
                active_users_memory[user] = active_users_memory.get(user, 0) + memory_usage_gb
                active_users_pids.setdefault(user, set()).add(pid)

    return active_users_memory
'''

'''
def get_active_users_memory():
    active_users_memory = {}

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB

            # Update the memory usage for the current user
            active_users_memory[user] = active_users_memory.get(user, 0) + memory_usage_gb

    return active_users_memory
'''

'''
def get_active_users_memory():
    active_users_memory = {}

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB

            # Keep track of unique PIDs for each user
            if user not in active_users_memory:
                active_users_memory[user] = set()
            active_users_memory[user].add(pid)

    # Calculate memory usage for each unique PID and sum it for each user
    for user, pids in active_users_memory.items():
        total_memory_gb = sum(psutil.Process(pid).memory_info().rss / (1024 ** 3) for pid in pids)
        active_users_memory[user] = total_memory_gb

    return active_users_memory
'''

'''
def get_active_users_memory():
    active_users_memory = {}

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB

            # Calculate the total memory usage for each user
            if user not in active_users_memory:
                active_users_memory[user] = 0
            active_users_memory[user] += memory_usage_gb

    return active_users_memory
'''

'''
def get_active_users_memory():
    active_users_memory = {}

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB

            # Calculate the number of PIDs associated with this process
            num_pids = len(psutil.Process(pid).children(recursive=True)) + 1

            # Divide the memory usage equally among the PIDs associated with the process
            memory_usage_gb /= num_pids

            # Calculate the total memory usage for each user
            if user not in active_users_memory:
                active_users_memory[user] = 0
            active_users_memory[user] += memory_usage_gb

    return active_users_memory    
'''

'''
def get_active_users_memory():
    active_users_memory = {}

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB

            # Calculate the total memory usage for each user
            if user not in active_users_memory:
                active_users_memory[user] = memory_usage_gb
            else:
                active_users_memory[user] += memory_usage_gb

    return active_users_memory
'''

'''
def get_active_users_memory():
    active_users_memory = {}

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB

            # Debug print to check individual process memory usage
            print(f"PID: {pid}, User: {user}, Memory Usage: {memory_usage_gb} GB")

            # Calculate the total memory usage for each user
            if user not in active_users_memory:
                active_users_memory[user] = memory_usage_gb
            else:
                active_users_memory[user] += memory_usage_gb

    # Debug print to check total memory usage per user
    print("Total Memory Usage Per User:")
    for user, memory_usage_gb in active_users_memory.items():
        print(f"{user}: {memory_usage_gb} GB")

    return active_users_memory

# Test the function
get_active_users_memory()
'''

'''
def get_active_users_memory():
    active_users_memory = {}

    for process in psutil.process_iter(['pid', 'username', 'memory_info']):
        if process.info['memory_info'].rss:
            pid = process.info['pid']
            user = process.info['username']
            memory_usage_gb = process.info['memory_info'].rss / (1024 ** 3)  # Memory usage in GB

            # Debug print to check individual process memory usage
            print(f"PID: {pid}, User: {user}, Memory Usage: {memory_usage_gb} GB")

            # Calculate the total memory usage for each user
            if pid not in active_users_memory:
                active_users_memory[pid] = memory_usage_gb

    # Debug print to check total memory usage per user
    print("Total Memory Usage Per User:")
    for user, memory_usage_gb in active_users_memory.items():
        print(f"{user}: {memory_usage_gb} GB")

    return active_users_memory

# Test the function
get_active_users_memory()
'''

'''
def get_active_users_memory(process_data):
    memory_usage_per_user = {}
    
    for process_info in process_data:
        user = process_info['User']
        memory_usage = process_info['Memory Usage']
        
        # Convert memory usage to GB if it is in bytes
        if 'GB' not in memory_usage:
            memory_usage = float(memory_usage.split()[0]) / (1024 * 1024 * 1024)
        
        # If the user is already in the dictionary, add the memory usage to the existing value
        if user in memory_usage_per_user:
            memory_usage_per_user[user] += memory_usage
        else:
            memory_usage_per_user[user] = memory_usage
            
    return memory_usage_per_user
    
print("above\n")
'''

'''
def get_active_users_memory():
    process_data = []
    for proc in psutil.process_iter(['pid', 'username', 'memory_info']):
        try:
            pid = proc.info['pid']
            username = proc.info['username']
            memory_usage = proc.info['memory_info'].rss
            process_data.append({'PID': pid, 'User': username, 'Memory Usage': memory_usage})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    memory_usage_per_user = {}
    
    for process_info in process_data:
        user = process_info['User']
        memory_usage = process_info['Memory Usage'] / (1024 * 1024 * 1024)  # Convert to GB
        
        # If the user is already in the dictionary, add the memory usage to the existing value
        if user in memory_usage_per_user:
            memory_usage_per_user[user] += memory_usage
        else:
            memory_usage_per_user[user] = memory_usage
            
    return memory_usage_per_user   
'''

'''
def get_active_users_memory():
    process_data = []
    for proc in psutil.process_iter(['pid', 'username', 'memory_info']):
        try:
            pid = proc.info['pid']
            username = proc.info['username']
            memory_usage = proc.info['memory_info'].rss
            process_data.append({'PID': pid, 'User': username, 'Memory Usage': memory_usage})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    memory_usage_per_user = {}
    
    for process_info in process_data:
        user = process_info['User']
        memory_usage = process_info['Memory Usage'] / (1024 * 1024 * 1024)  # Convert to GB
        
        # If the user is already in the dictionary, add the memory usage to the existing value
        if user in memory_usage_per_user:
            memory_usage_per_user[user] += memory_usage
        else:
            memory_usage_per_user[user] = memory_usage
            
    return memory_usage_per_user
'''

'''
def get_active_users_memory():
    memory_usage_per_user = {}
    for proc in psutil.process_iter(['pid', 'username', 'memory_info']):
        try:
            pid = proc.info['pid']
            username = proc.info['username']
            memory_info = proc.info['memory_info']
            memory_usage = memory_info.rss / (1024 * 1024 * 1024)  # Convert to GB
            
            # Adjust for shared memory by subtracting the shared memory from the total memory
            if psutil.version_info >= (5, 8, 0):
                shared_memory = memory_info.shared / (1024 * 1024 * 1024)  # Convert to GB (psutil 5.8.0+)
                memory_usage -= shared_memory

            # If the user is already in the dictionary, add the memory usage to the existing value
            if username in memory_usage_per_user:
                memory_usage_per_user[username] += memory_usage
            else:
                memory_usage_per_user[username] = memory_usage
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return memory_usage_per_user    
'''
    
###################
## Assess Memory ##
###################

# Initialize a flag to assess whether an email has been sent
total_email_sent = False
user_email_sent = {user: False for user in epigenerate_users}

# Run endless loop to assess memory 
while True:
    # Calculate memory
    time.sleep(check_every_secs) # Wait for the specified amount of time
    mem_used = calculate_total_memory_usage() # Float
    mem_per_user = get_active_users_memory() # Dictionary

#########################
## Assess Total Memory ##
#########################

    # Email all active users if total memory usage exceeds total RAM limit
    if mem_used >= tot_ram_lim:
        if not total_email_sent:
            for user, memory_usage in mem_per_user.items():
                if user in epigenerate_users:
                    # Draft message
                    users_info = '\n'.join([f'{user}: {memory_usage} GB' for user, memory_usage in sorted(mem_per_user.items(), key=lambda x: x[1], reverse=True)])
                    notify_function = textwrap.dedent(f"""
                    notify() {{
                        DETAILS='RAM usage on epigenerate has exceeded {tot_ram_lim} GB and will likely crash. Here are the current users and their memory usage:
                        
                        {users_info}
                        
                        As soon as you see this email, please coordinate with current users in the Epigenerate Slack channel to work out a solution. This can include killing a job if you are running a resource-intensive or non-urgent job.'
                        cat <<EOF | sendmail {epigenerate_users[user]}
                    Subject: [URGENT] Impending Epigenerate Crash
                    From: SSH Notification <{sender_email}>
                    
                    $DETAILS
                    EOF
                    }}
                    """)
                    notify_function = notify_function.replace(' '*5, '')
                    # Save message into log file
                    now = datetime.now()
                    now = now.strftime("%Y_%m_%d_%H:%M:%S")
                    os.system(f'touch {logs_dir}/{now}_{user}_epigenerate_total.sh')
                    with open(f'{logs_dir}/{now}_{user}_epigenerate_total.sh', 'w') as f:
                        f.write(f'{notify_function}')
                    os.system(f'chmod 777 {logs_dir}/{now}_{user}_epigenerate_total.sh')
                    # Send notification 
                    #os.system(f'. {logs_dir}/{now}_{user}_epigenerate_total.sh && notify')
                    # Update flag
                    total_email_sent = True
    
    if mem_used < tot_ram_lim:
        total_email_sent = False 
    
    print("Total memory usage has been checked...")
    
########################
## Assess User Memory ##
########################
 
    # Email a user if they are using more than the user RAM limit 
    for user, memory_usage in mem_per_user.items():
        if memory_usage > user_ram_lim and not user_email_sent[user]:
            # Draft message
            notify_function = textwrap.dedent(f"""
            notify() {{
                DETAILS='You are currently using {memory_usage} GB of RAM. Your user allotment is {user_ram_lim} GB. If you have already checked with other users that your usage is permitted, please disregard this message. If this was not intended, please reassess and adjust your job accordingly to prevent Epigenerate from crashing.'
                cat <<EOF | sendmail {epigenerate_users[user]}
            Subject: Epigenerate RAM Warning
            From: SSH Notification <{sender_email}>
            
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
            #os.system(f'. {logs_dir}/{now}_{user}.sh && notify')
            # Update user flag
            user_email_sent[user] = True
            
        if memory_usage < user_ram_lim:
            user_email_sent[user] = False 
            
    print("User memory has been checked...")
    print(mem_per_user)
    break