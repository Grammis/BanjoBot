import os
import asyncio
import discord
from Hemligheter import TOKEN
from SteamID import get_64bit_steam_id


client = discord.Client()

global_guild_id = 708618012738977822
global_guild = None

emoji_EU = "🌍"
emoji_NA = "🌎"
emoji_SEA = "🌏"
emoji_AP = "📙"
emoji_CD = "📘"
emoji_both = "📚"
emoji_steam = None # Custom emoji, retreived in the setup function

# Emojis
def setup():
    global emoji_steam
    global_guild = discord.utils.find(lambda g : g.id == global_guild_id, client.guilds)
    emoji_steam = discord.utils.get(global_guild.emojis, name='steam')

def get_member(id):
    for member in client.get_all_members():
        if id == member.id:
            return member

@client.event
async def on_ready():
    setup()
    print(f'{client.user} has connected to Discord!')


#Messages for the bot
@client.event
async def on_message(message):
    #Message from bot
    if message.author.bot == True:
        #Reaction for the bot in the welcome channel
        if "React below to get started" in message.content:
            await message.add_reaction(emoji_steam)
        #Reactions for the players to join the specific leagues
        if "**REACT TO JOIN THE LEAGUE OF YOUR CHOICE**" in message.content:
            await message.add_reaction(emoji_EU)
            await message.add_reaction(emoji_NA)
            await message.add_reaction(emoji_SEA)
        #if "BBL# has been started. Accept by reacting to the ✅ emoji. Password: " in message.content:
            #await message.add_reaction("✅")
        if "React below to join" in message.content:
            await message.add_reaction(emoji_AP)
            await message.add_reaction(emoji_CD)
            await message.add_reaction(emoji_both)


    #Message from Moderator
    if message.author.bot == False:
        try:
            #Get Roles from user
            listRoles = [x.name for x in message.author.roles]
        except:
            listRoles = []
        correct_role = "Administrator" in listRoles or "Moderator" in listRoles
        #muted = "muted" in listRoles
        if correct_role and listRoles != []:
            #Message for the welcome channel
            if message.content.startswith('$welcome') and message.channel.name == 'welcome':
                channel = message.channel
                await channel.send("Welcome to the Dota 2 Banjoball Discord League! In order to sign up you have to send the bot the url of your steam profile.")
                await channel.send("React below to get started")
                return
            #Message for the register channel
            if message.content.startswith('$register') and message.channel.name == 'register':
                channel = message.channel
                await channel.send(emoji_EU + " " + emoji_NA + " " + emoji_SEA)
                await channel.send("**REACT TO JOIN THE LEAGUE OF YOUR CHOICE**")
                await channel.send("" + emoji_EU + " **= EUROPE** " + emoji_NA + " **= NA** " + emoji_SEA + " **= SEA**")
                return
            #Message for the league channels
            if message.content.startswith('$queue') and (message.channel.name == 'eu' or message.channel.name == 'na' or message.channel.name == 'sea'):
                channel = message.channel
                await channel.send("React below to join")
                await channel.send(emoji_AP + " **= ALL PICK** "+ emoji_CD + " **= CAPTAIN'S DRAFT** " + emoji_both + " **= BOTH**")
                return
        elif listRoles != []:
            def is_me(m):
                return m.author == client.user
            if message.content.startswith('$welcome') and message.channel.name == 'welcome':
                channel = message.channel
                await channel.send("You do not have permission.")
                await asyncio.sleep(2)
                await channel.purge(limit=1, check=is_me)
                return
            if message.content.startswith('$register') and message.channel.name == 'register':
                channel = message.channel
                await channel.send("You do not have permission.")
                await asyncio.sleep(2)
                await channel.purge(limit=1, check=is_me)
                return 
            if message.content.startswith('$queue') and (message.channel.name == 'eu' or message.channel.name == 'na' or message.channel.name == 'sea'):
                channel = message.channel
                await channel.send("You do not have permission.")
                await asyncio.sleep(2)
                await channel.purge(limit=1, check=is_me)
                return 
        else:
            #Message from User
            if message.author.bot == False:
                if 'a' in message.content:
                    print(message.channel)
                    #print(get_64bit_steam_id(message.content))
                    print(type(message.author.id))
                    unregistered_player = str(message.author.id)
                    #guild = discord.utils.find(lambda g : g.id == global_guild_id, client.guilds)
                    member_in_guild = discord.utils.find(lambda m: m.id == message.author.id, global_guild_id)
                    if unregistered_player == member_in_guild:
                        print(str(unregistered_player))

"""DMChannel == private:
if 'http://steamcommunity.com/id' in message.content:
# if Userid is in the system already don't allow them otherwise add
player_steamid = get_64bit_steam_id(message.content)
print(player_steamid) 
#and is not a registered user:
#url = 
#steam64_from_url(url, htthp_timeout=30)"""




#Reactions for the bot
@client.event
async def on_reaction_add(reaction, user):
    member = get_member(user.id)
    channel = reaction.message.channel
    guild_id = reaction.message.guild.id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
    role = None


    #Emoji reactions for the register channel
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
            if role not in member.roles:
                await member.add_roles(role)
                print("Assigned user: " + str(member) + ", with the " + role.name + " role")
            else:
                print(str(member) + ", has the " + role.name + " role already")
    if channel.name == 'eu' and user != client.user:
        if str(reaction.emoji) == emoji_AP:
            print('All Pick')
        elif str(reaction.emoji) == emoji_CD:
            print('Captains Draft')
        elif str(reaction.emoji) == emoji_both:
            print('Both')

    if channel.name == 'eu' and user != client.user:
        if str(reaction.emoji) == emoji_AP:
            print('All Pick')
        elif str(reaction.emoji) == emoji_CD:
            print('Captains Draft')
        elif str(reaction.emoji) == emoji_both:
            print('Both')


                
    #Emoji reaction for welcome channel
    if channel.name == 'welcome' and user != client.user:
        if reaction.emoji == emoji_steam:
            await member.send('Copy the URL that this link provides for your steam profile and send it back to the bot: http://steamcommunity.com/my/profile')
            




try:
    client.run(TOKEN)
except KeyboardInterrupt:
    print("Shutting down...")