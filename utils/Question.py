import requests
import json
from utils.Profile import Profile
# get question that user asked
class Question:
    def __init__(self,username):
        self.profile = Profile(username)
    def get_question(self,number):
        return self.get_questions(number,1)[0]
    def get_questions(self,place,number):
      data = requests.post("https://www.quora.com/graphql/gql_para_POST?q=UserProfileQuestionsList_Questions_Query", 
        headers= {
          "accept": "*/*",
          "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
          "content-type": "application/json",
          "priority": "u=1, i",
          "quora-broadcast-id": "main-w-chan112-8888-react_qortkdpaqakmflwx-SN0z",
          "quora-canary-revision": "false",
          "quora-formkey": "377eeda81b0a8ddaa70ad38718ead6df",
          "quora-page-creation-time": "1750929906463054",
          "quora-revision": "9a4620e6b391f784fab9b77021eb5547559633bf",
          "quora-window-id": "react_qortkdpaqakmflwx",
          "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-origin",
          "cookie": "m-b=T_cZwccA4LkEiz3vCUyjkQ==; m-b_lax=T_cZwccA4LkEiz3vCUyjkQ==; m-b_strict=T_cZwccA4LkEiz3vCUyjkQ==; m-s=UpHEmzmd7LVWe0mCHZKAxw==; m-dynamicFontSize=regular; m-themeStrategy=auto; m-theme=dark; m-login=1; m-lat=EP/jbKxYL3dgAQbjjGQeLTGyFMaJW1fKn5wvLijokA==; m-uid=2563106278; __stripe_mid=8aec8b0c-6ff7-4ccc-88e7-692a7beeb4b0c9e5e2; __stripe_sid=c1ce70e2-5ed5-4071-85d1-5103ab352c06a023d1",
          "Referrer-Policy": "strict-origin-when-cross-origin"
        },
        json = {"queryName":"UserProfileQuestionsList_Questions_Query","variables":{"uid":int(self.profile.uid),"first":int(number),"after":int(place)-2},"extensions":{"hash":"9eec027d248067a8db8d058a53658270e2a1382a4257bb735c340dce34d244e5"}}
        
      )
      body = json.loads(data.text)
      following = body["data"]["user"]["recentPublicQuestionsConnection"]["edges"]
      urls = []
      for f in following:
          url = f["node"]["commentsPageUrl"].replace("/comments","")
          if not url.startswith("https:"):
              url = "https://www.quora.com" + url
          urls.append(url)
      if len(urls) == 0:
          return ["no question"]
      return urls