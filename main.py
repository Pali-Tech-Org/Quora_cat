import discord, sqlite3, asyncio, threading
from utils.funcs import *
from time import sleep

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
TOKEN = ""

@client.event
async def on_message(message):
    command = message.content
    channel_id = message.channel.id
    server_ID = int(message.guild.id)
    server_id = str(server_ID)
    if message.author.id == 1210660779381231649:
        if command.startswith("qr!get_users"):
           db = sqlite3.connect('quora_bot.db')
           await get_users(client,db,channel_id)   
        elif command.startswith("qr!update_uid"):
            db = sqlite3.connect('quora_bot.db')
            profile_id = command.split(" ")[1]
            uid = command.split(" ")[2]
            update_uid(db,profile_id,uid)
    try:
        permission = message.author.top_role.permissions.kick_members
    except:
        permission = False
    if permission or message.author.id==1210660779381231649:
        if command.startswith("qr!set"):
            db = sqlite3.connect('quora_bot.db')
            set_channel(db, server_id, channel_id)
        elif command.startswith("qr!add"):
            db = sqlite3.connect('quora_bot.db')
            profile_id = command.split(" ")[1]
            uid = command.split(" ")[2]
            add_user(db,server_id, profile_id, uid)
        elif command.startswith("qr!remove"):
            profile_id = command.split(" ")[1]
            remove_user(db,server_id, profile_id)
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("running")
    await quora_cat(client)





if __name__ == '__main__':
    db = sqlite3.connect('quora_bot.db')
    #with open("Schema.sql") as file:
    #    for line in file.readlines():
    #        db.execute(line)
    #    db.commit()
    #db.close()
    client.run(TOKEN)


