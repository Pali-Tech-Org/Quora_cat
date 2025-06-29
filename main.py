import discord, sqlite3, asyncio, threading
from utils.funcs import *
from time import sleep
from utils.Question import Question
from utils.Post import Post
from utils.Follower import Follower
from utils.Following import Following
from utils.Answer import Answer
from utils.Profile import Profile
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
        elif command.startswith("qr!question "):
            _,profile,number = command.split()
            qr = Question(profile)
            await message.reply(qr.get_question(number))
        elif command.startswith("qr!questions "):
            _,profile,place,number = command.split()
            qr = Question(profile)
            questions = qr.get_questions(place,number)
            reply = ""
            for q in questions:
                reply += q + "\n"
            await message.reply(reply)
        elif command.startswith("qr!post "):
            _,profile,number = command.split()
            pst = Post(profile)
            await message.reply(pst.get_post(number))
        elif command.startswith("qr!posts "):
            _,profile,place,number = command.split()
            pst = Post(profile)
            posts = pst.get_posts(place,number)
            reply = ""
            for p in posts:
                reply += p + "\n"
            await message.reply(reply)
        elif command.startswith("qr!follower "):
            _,profile = command.split()
            fol = Follower(profile)
            cursor = 1
            amount = 10
            while True:
                followers = fol.get_followers(amount,cursor)
                msg = make_message(followers)
                cursor += amount
                await client.get_channel(message.channel.id).send(msg)
                await asyncio.sleep(20)
                if len(followers) < amount:
                    break
        elif msg.content.startswith("qr!following "):
            _,profile = msg.content.split()
            fol = Following(profile)
            cursor = 1
            amount = 10
            while True:
                followers = fol.get_following(amount,cursor)
                message = make_message(followers)
                cursor += amount
                await client.get_channel(msg.channel.id).send(message)
                await asyncio.sleep(20)
                if len(followers) < amount:
                    break
        elif command.startswith("qr!ansewer "):
            _,profile,number = command.split()
            ans = Answer(profile)
            await message.reply(ans.get_answer(number))
        elif command.startswith("qr!info "):
            _,profile = command.split()
            profile = Profile(profile)

            await message.reply(f"{profile.username}: {profile.uid}\n\
    Followers: {profile.followers_counter}\n\
    Following: {profile.following_counter}\n\
    This month views: {profile.month_views}\n\
    This total views: {profile.total_views}\n\
    [avatar]({profile.avatar})")
    if message.content.startswith("!boycott"):
        with open("data.json",encoding="utf-8") as f:
            d = f.read()
            boycotted_productes = json.loads(d)
        _,product = message.content.split()
        for pr in boycotted_productes["data"]:
            if pr["attributes"]["name"].casefold() == product.casefold():
               await message.reply(f"""yes, **{product.casefold()}** is on the b                                                                                                                                                             oycott list.

you want to see proof? type !proof **{product.casefold()}**""")
               return
        await message.reply("Product safe")
    if message.content.startswith("!proof"):
        with open("data.json",encoding="utf-8") as f:
            d = f.read()
            boycotted_productes = json.loads(d)
        _,product = message.content.split()
        for pr in boycotted_productes["data"]:
            if pr["attributes"]["name"].casefold() == product.casefold():
               await message.reply(f"""{pr["attributes"]["proof"]}""")
               return
        await message.reply("This product is safe")

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


