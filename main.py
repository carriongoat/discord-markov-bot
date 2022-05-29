import discord
import asyncio
import markov
import channel_management

# gortass


class DiscordClient(discord.Client):

    async def on_ready(self):
        channel_management.bot_init()
        print('connected')

    async def on_message(self, message):

        if message.author == client.user:
            return

        if message.content.startswith('!gen') or client.user in message.mentions:
            if message.channel.id in channel_management.enabled_channels:
                markov_message = markov.markov_message_gen(channel_management.get_data(message))
                if markov_message is not None:
                    await message.channel.send(str(markov_message))
                    print('sending ' + str(markov_message) + ' in ' + str(message.channel.id))
                else:
                    await message.channel.send('Not enough data to train :pleading_face:')
                    print('not enough data to train with')
            else:
                await message.channel.send('you havent enabled this channel goofy:bangbang:')

        elif message.content.startswith('!readenable'):
            # enable reading a channel.
            if channel_management.add_channel(message.guild.id, message.channel.id):
                await message.channel.send('markov enabled for ' + message.channel.mention)
                print('wrote new channel id to channel_list')
            else:
                await message.channel.send('this channel is already enabled goofass')

        elif message.content.startswith('!help'):
            await message.channel.send("!gen: generate a sentence\n"
                                       "!readenable: enable markov in current channel\n"
                                       "!readdisable: disable markov reading current channel\n"
                                       "!purgechannel: delete the channel's recorded markov data, remove channel\n"
                                       "!purgeserver: delete whole server's data and remove all channels\n"
                                       "WARNING! purges cant be undone!!! dont do it if folks dont want you to!\n"
                                       ":boom::bangbang:AGAIN: PURGE IS IMMEDIATE AND UNDOABLE:bangbang::boom:\n"
                                       "this bot does not allow for control of whats recorded past permitting channels to be read.\n"
                                       "if thats a problem, readenable only a quarantine channel.\n")

        elif message.content.startswith('!readdisable'):
            if channel_management.remove_channel(message.channel.id):
                await message.channel.send("channel's been removed")
            else:
                await message.channel.send("channel's not in the list:interrobang:")

        elif message.content.startswith("!purgechannel"):
            if channel_management.purge_channel(message.guild.id, message.channel.id):
                await message.channel.send("All Channel Data Purged :boom::boom::boom:")
            else:
                await message.channel.send("no data for channel!")

        elif message.content.startswith("!purgeserver"):
            if channel_management.purge_server(message.guild):
                await message.channel.send("Entire Server's Data Purged :boom::boom::boom:")
            else:
                await message.channel.send("no data for server!")

        else:
            channel_management.add_message(message)


client = DiscordClient()
client.run('')
