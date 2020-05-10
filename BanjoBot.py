import os
import asyncio
import discord
#from dotenv import load_dotenv

#load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = "NzA4NzExMDI2MDEwNDg4OTUz.XrbdXA.agDmGt31H3IPPsplwijF4Qim2h4"
emoji_EU = "🌍"
emoji_NA = "🌎"
emoji_SEA = "🌏"
client = discord.Client()

def get_member(id):
    for member in client.get_all_members():
        if id == member.id:
            return member



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author.bot:
        if "Please react to this message to join the leagues of your choice " + emoji_EU + " - Europe " + emoji_NA + " - NA " + emoji_SEA + " - SEA" in message.content:
            await message.add_reaction(emoji_EU)
            await message.add_reaction(emoji_NA)
            await message.add_reaction(emoji_SEA)
        #if "BBL# has been started. Accept by reacting to the ✅ emoji. Password: " in message.content:
            #await message.add_reaction("✅")

    if message.content.startswith('$Register'):
        #if message is from administrator
        channel = message.channel
        await channel.send("Please react to this message to join the leagues of your choice " + emoji_EU + " - Europe " + emoji_NA + " - NA " + emoji_SEA + " - SEA")

@client.event
async def on_reaction_add(reaction, user):
    member = get_member(user.id)
    channel = reaction.message.channel
    guild_id = reaction.message.guild.id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
    role = None
    if channel.name == 'register' and user != client.user:
        if str(reaction.emoji) == emoji_EU:
            role = discord.utils.find(lambda r : r.name == "EU", guild.roles)
        elif str(reaction.emoji) == emoji_NA:
            role = discord.utils.find(lambda r : r.name == "NA", guild.roles)
        elif str(reaction.emoji) == emoji_SEA:
            role = discord.utils.find(lambda r : r.name == "SEA", guild.roles)
        if role == None:
            pass
        else:
            await member.add_roles(role)


client.run(TOKEN)