import os
import shutil

global enabled_channels
global channel_list_path
channel_list_path = './servers/channel_list.txt'


def bot_init():
    global enabled_channels
    global channel_list_path
    with open(channel_list_path) as channel_list_file:
        temp_list = [int(i) for i in channel_list_file.read().splitlines()]
        if temp_list:
            enabled_channels = [int(i) for i in channel_list_file.read().splitlines()]


def add_message(message):
    channel_path = "./servers/" + str(message.guild.id) + "/" + str(message.channel.id) + ".txt"
    if message.channel.id in enabled_channels:
        with open(channel_path, 'a', encoding='utf-8') as markov_data_file:
            for x in range(len(message.attachments)):
                markov_data_file.write(message.attachments[x].url + "\n")
            markov_data_file.write(message.content + "\n")


def get_data(message):
    channel_path = "./servers/" + str(message.guild.id) + "/" + str(message.channel.id) + ".txt"
    with open(channel_path, 'r') as path:
        return path.read()


def add_channel(guild_id: int, channel_id: int):
    global enabled_channels
    if channel_id not in enabled_channels:
        channel_path = "./servers/" + str(guild_id)
        os.makedirs(channel_path, 0o777, exist_ok=True)
        print(channel_path)
        with open(channel_list_path, 'a') as channel_list:
            channel_list.write(str(channel_id) + '\n')
            enabled_channels.append(channel_id)
            print('channel added to internal list and file')
        return True
    else:
        print('attempted to add channel, but its already enabled')
        return False


def remove_channel(channel_id: int):
    global enabled_channels
    global channel_list_path

    if enabled_channels.count(channel_id) == 0:
        return False
    else:
        enabled_channels.remove(channel_id)
        print("removed channel: " + str(channel_id))
        with open(channel_list_path, 'w+') as channel_list:
            channel_list.truncate(0)
            for channel in enabled_channels:
                channel_list.write(str(channel) + '\n')
        return True


def purge_server(guild):
    delete_path = "./servers/" + str(guild.id)
    if os.path.exists(delete_path):
        shutil.rmtree(delete_path)
        print("server folder purged: " + str(guild.id))
        for channel in guild.text_channels:
            if channel.id in enabled_channels:
                remove_channel(channel.id)
        return True
    else:
        print("server doesnt exist")
        return False


def purge_channel(guild_id: int, channel_id: int):
    delete_path = "./servers/" + str(guild_id) + "/" + str(channel_id) + ".txt"
    if os.path.exists(delete_path):
        remove_channel(channel_id)
        os.remove(delete_path)
        print("channel " + str(channel_id) + " server " + str(guild_id) + " has been purged")
        return True
    else:
        print("channel didnt have data in the first place")
        return False
