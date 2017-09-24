#!/usr/bin/python
import datetime
import os
import random
import subprocess
import time

# Function to get IP's current activity status
def get_status(my_ip):
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                    ['ping', '-c', '1','-i', '.15', my_ip], # Ping three packets with one second between pings
                    stdout=DEVNULL, #supress output
                    stderr=DEVNULL
            )
            return(True)
        except subprocess.CalledProcessError:
            return(False)

# Get the music status, i.e. whether it is playing or not
def music_status():
    long_command =  """mpc status | sed -n 2p | grep -oP "(?<=\[)[a-z]+" """
    proc = subprocess.Popen(long_command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if 'playing' in str(out):
        return(True)
    else:
        return(False)

# Get current playing song
def get_current_song():
    current_song = str(subprocess.check_output("mpc status | sed -n 1p", shell=True)).strip("'b").replace("\\n","")
    return(current_song)

# Return available Spotify playlists
def get_playlists():
    long_command =  """mpc lsplaylists"""
    proc = subprocess.Popen(long_command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    playlists_raw = str(out).split('\\n')
    playlists = [playlist.strip("'b").replace("\\n","") for playlist in playlists_raw if playlist != "'" and 'loading' not in playlist]
    return(playlists)

# Return random playlist
def get_random_playist():
    my_playlists = get_playlists()
    return(random.choice(my_playlists))

# Return time since last active
def get_time_since_active(my_dict):
    return(datetime.datetime.now() - my_dict['last_active_time'])

# Main script
def main():
    my_dict = {}
    # Local IP Address
    my_ip = '192.168.1.114'
    # Keep last active time in dictionary
    my_dict['last_active_time'] = datetime.datetime.now()
    my_dict['current_song'] = ''
    # Loop indefinitely
    while True:
        # Get whether music is currently playing
        my_dict['on_state'] = music_status()
        # Check if IP is pingable and reassign last_active_time if it is
        if get_status(my_ip):
            my_dict['last_active_time'] = datetime.datetime.now()
        else:
            pass
        #print("Time Since Active: {}".format(my_dict['time_since_active']))
        # Calculate time since last active
        my_dict['time_since_active'] = get_time_since_active(my_dict)
        current_song = get_current_song()
        # If >15min of iphone not being connected and if the music is on, pause the music
        # If iphone has been active less than 15 minutes ago and the on_state is off, turn music on
        if my_dict['time_since_active'] < datetime.timedelta(minutes=15) and my_dict['on_state'] == True:
            if my_dict['current_song'] != current_song:
               #print("Playing {} | {}  ".format(my_random_playlist, current_song))
                my_dict['current_song'] = current_song
            else:
                pass
        elif my_dict['time_since_active'] < datetime.timedelta(minutes=15) and my_dict['on_state'] == False:
            # Get random playlist
            # Suppress errors to devnull
            with open(os.devnull, 'w') as devnull:
                # This is a bit messy, as there are some playlists that are unable to be loaded :/
                result = None
                while result is None:
                    try:
                        my_random_playlist = get_random_playist()
                        my_command = "mpc clear && mpc load '{}' && mpc random on && mpc shuffle && mpc play &".format(my_random_playlist)
                        output = subprocess.check_output(my_command, stderr=devnull, shell=True)
                        # Output initial playlist and beginning song
                        my_dict['on_state'] = True
                        my_dict['current_song'] = current_song
                        # assign result to something to break while result loop
                        result = "Success"
                    except:
                       #print("Playing {} failed. Trying another playlist".format(my_random_playlist))
                        pass
                # After successful playlist fetching,#print playlist and song
                current_song = get_current_song()
               #print("Playing: {} | {} ".format(my_random_playlist, current_song))
                # Assign current song to correct dictionary
                my_dict['current_song'] = current_song
        elif my_dict['time_since_active'] > datetime.timedelta(minutes=15) and my_dict['on_state'] == True:
            os.system('/usr/bin/mpc pause')
            # Assign the on_state to be off
            my_dict['on_state'] = False
        else:
            pass

if __name__ == "__main__":
    main()

