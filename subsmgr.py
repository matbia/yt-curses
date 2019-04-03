import os

file_path = os.path.join(os.path.dirname(__file__), 'subscriptions.txt')

#Returns subscribed channels IDs as a list of strings
def get_subscribed_channels():
    try:
        subs_file = open(file_path, 'r')
    except IOError:
        subs_file = open(file_path, 'w') #Create new file if there isn't one
        return []

    #File to string list
    subs = []
    for line in subs_file:
        subs.append(line)
    subs_file.close()
    return subs

#Returns true if subscriptions file contains channel_id, otherwise returns false
def is_subscribed(channel_id):
    return channel_id in open(file_path).read()

#Retruns true if subscribed, false if unsubscribed
def toggle_subscription(channel_id):
    if is_subscribed(channel_id):
        #Delete line
        f = open(file_path, 'r')
        lines = f.readlines()
        f.close()
        f = open(file_path, 'w')
        for line in lines:
            if line != channel_id + '\n':
                f.write(line)
        f.close()
        return False
    with open(file_path, 'a') as file:
        #Append line
        file.write(channel_id + '\n')
        return True
