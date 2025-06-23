
import requests, json, sqlite3
import asyncio
import traceback

from time import sleep

def main (profile,uid,index):
    data = requests.post("https://www.quora.com/graphql/gql_para_POST?q=UserProfileAnswersMostRecent_RecentAnswers_Query", headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "priority": "u=1, i",
        "quora-broadcast-id": "main-w-chan56-8888-react_rhvancsuygqfyuyr-cDpr",
        "quora-canary-revision": "false",
        "quora-formkey": "c09446b6a4353625785caf758a343b55",
        "quora-page-creation-time": "1729078602586577",
        "quora-revision": "1c813001f1e3aaf70900b68e3048d997952573f5",
        "quora-window-id": "react_rhvancsuygqfyuyr",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "__stripe_mid=f6594168-c7f0-420b-82a8-7fe6b763193f62f4f7; m-b=i_igAWrJFmbh5MG8asajZQ==; m-b_lax=i_igAWrJFmbh5MG8asajZQ==; m-b_strict=i_igAWrJFmbh5MG8asajZQ==; m-s=Gxt5aGv550G90VnJghQ0fA==; m-theme=light; m-dynamicFontSize=regular; m-themeStrategy=auto; m-ql10n_ar=https%3A%2F%2Fqsbr.cf2.quoracdn.net%2F-4-l10n_main-30-ar-693686341370417f.translation.json; m-login=1; m-lat=BEwiRHlPCIVnpumlNW9YGfZo5PEZramsOqzoT9NdRA==; m-uid=2563106278; m-sa=1; __stripe_sid=56dea236-280f-42cc-a104-46a2fad728823aea18; __gads=ID=0fb3d626f75bb9e2:T=1729017358:RT=1729078447:S=ALNI_MYNK02o06NmmwgKSL-omaV80WcHjw; __gpi=UID=00000f3f02cef187:T=1729017358:RT=1729078447:S=ALNI_MY_mO-nrpi_D-xp4vgkNAb3bX36tA; __eoi=ID=b1ee6cd216f5e02c:T=1729017358:RT=1729078447:S=AA-AfjaWHALk6KDK3V7WejdvXFxs",
        "Referer": f"https://www.quora.com/profile/{profile}/answers",
        "Referrer-Policy": "strict-origin-when-cross-origin"
        },json={"queryName":"UserProfileAnswersMostRecent_RecentAnswers_Query","variables":{"uid":uid,"first":3,"after":str(index),"answerFilterTid": None},"extensions":{"hash":"87c0ab1d94902029565e396a4a0483108998ce98c4f1cce6ccf4f7c7a3fc4e03"}})
    body = json.loads(data.text)
    answer = body["data"]["user"]["recentPublicAndPinnedAnswersConnection"]["edges"][0]
    url = answer["node"]["url"]
    if not url.startswith("https"):
        url = "https://www.quora.com"+url
    
    return {"answer_id":answer["node"]["aid"],"url":url}
    

def update_uid(db,profile_id,uid):

    data = db.execute("SELECT *  FROM profiles WHERE profileID  = (?)",(profile_id,)).fetchall()
    if len(data) > 0:
        db.execute("UPDATE profiles SET uid = (?) WHERE profileID = (?)",(uid,profile_id))
        db.commit()

async def get_users(c,db,channel_id):
    text = ""
    data = db.execute("SELECT DISTINCT profileID,uid FROM profiles").fetchall()
    for row in data:
        text += str(row[0]) + " : " + str(row[1]) +"\n"
    channel = c.get_channel(channel_id)
    await channel.send(text)


async def quora_cat(client):
    
    while True:
        db = sqlite3.connect('quora_bot.db')
        try:
            data = db.execute("SELECT * FROM profiles").fetchall()
            for row in data:            
                profile_id = row[1]
                server_id = row[0]
                uid = row[2]
                indexes = [-1,0]
                for index in indexes:
                    await asyncio.sleep(5)
                    value = main(profile_id,uid,index)
                    answer_id = str(value["answer_id"])
                    url = value["url"]
                    answers = db.execute("SELECT *  FROM answers WHERE answerID  = (?) AND serverID = (?)",(answer_id,server_id)).fetchall()
                    if len(answers) == 0:
                        channels = db.execute("SELECT * FROM channels WHERE serverID  =? ",(server_id,)).fetchall()
                        if len(channels) > 0:
                            channel_id = channels[0][1]
                            channel = client.get_channel(channel_id)
                            await channel.send(url)
                            db.execute("INSERT INTO answers VALUES (?,?)",(server_id, answer_id))
                            db.commit()
        except Exception as e:
            print("Exception in quora_cat:")
            traceback.print_exc()

    
        db.close()
        await asyncio.sleep(600)


def add_user(db,server_id,profile_id,uid):
    data = db.execute("SELECT *  FROM profiles WHERE profileID  = (?) AND serverID = (?) ",(profile_id,server_id)).fetchall()
    if len(data) == 0:
        db.execute("INSERT INTO profiles VALUES  (?,?,?)",(server_id, profile_id, uid))
        db.commit()


def remove_user(db,server_id,profile_id):
    data = db.execute("SELECT *  FROM profiles WHERE profileID  = (?) AND serverID = (?)",(profile_id, server_id)).fetchall()
    if len(data) != 0:
        db.exute("DELETE FROM profiles WHERE serverID = (?) AND profileID = (?)",(server_id,profile_id))
        db.commit()

def set_channel(db,server_id,channel_id):
    data = db.execute("SELECT channelID  FROM channels WHERE serverID  = (?) ",(server_id,)).fetchall()
    if len(data) > 0:
        db.execute("UPDATE channels SET channelID = (?) WHERE serverID = (?)",(channel_id,server_id)).fetchall()
        db.commit()
    else:
        db.execute("INSERT INTO channels VALUES (?,?)",(server_id,channel_id))
        db.commit()



   
