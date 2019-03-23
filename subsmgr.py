import os

file_path = os.path.join(os.path.dirname(__file__), 'subscriptions')

#Returns subscribed channels IDs as a list of strings
def get_subscribed_channels():
    try:
        subscriptions_file = open(file_path, 'r')
    except IOError:
        subscriptions_file = open(file_path, 'w') #Create new file if there isn't one
        return [] #Return empty list

    #File to string list
    subscriptions = []
    for line in subscriptions_file:
        subscriptions.append(line)
    subscriptions_file.close()
    return subscriptions

#Returns true if subscriptions file contains channel_id
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
