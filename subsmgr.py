from os import path

subs_path = path.join(path.dirname(__file__), 'subscriptions.txt')

#Create new subscriptions file if there isn't one yet
if not path.exists(subs_path):
    with open(subs_path, 'w') as f:
        pass

#Returns subscribed channels IDs as a list of strings
def get_subscribed_channels():
    with open(subs_path) as f:
        return f.read().splitlines()

#Returns true if subscriptions file contains channel_id, otherwise returns false
def is_subscribed(channel_id):
    with open(subs_path) as f:
        return channel_id in f.read()

#Retruns true if subscribed, false if unsubscribed
def toggle_subscription(channel_id):
    if is_subscribed(channel_id):
        with open(subs_path) as f:
            lines = f.read().splitlines()

        lines.remove(channel_id)

        with open(subs_path, 'w') as f:
            if len(lines):
                f.write('\n'.join(lines) + '\n')
        return False

    with open(subs_path, 'a') as file:
        file.write(channel_id + '\n')
    return True
