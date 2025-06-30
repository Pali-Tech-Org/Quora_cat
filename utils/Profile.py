import requests,re,json
from bs4 import BeautifulSoup

class Profile:
    def __init__(self,username):
        self.username = username
        self.uid = ""
        self.avatar = ""
        self.description = ""
        self.followers_counter = ""
        self.following_counter = ""
        self.total_views = ""
        self.month_views = ""
        self.profile_info()
    def get_data(self,title,text):
        data = ""
        i = text.find(title) 
        while True:
            data += text[i]
            i += 1
            if text[i] ==",":
                break
        return data.split(":")[1]
    def profile_info(self):
        data = requests.get(f"https://www.quora.com/profile/{self.username}", 
            headers= {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": "m-b=T_cZwccA4LkEiz3vCUyjkQ==; m-b_lax=T_cZwccA4LkEiz3vCUyjkQ==; m-b_strict=T_cZwccA4LkEiz3vCUyjkQ==; m-s=UpHEmzmd7LVWe0mCHZKAxw==; m-dynamicFontSize=regular; m-themeStrategy=auto; m-theme=dark; m-login=1; m-lat=EP/jbKxYL3dgAQbjjGQeLTGyFMaJW1fKn5wvLijokA==; m-uid=2563106278; __stripe_mid=8aec8b0c-6ff7-4ccc-88e7-692a7beeb4b0c9e5e2; __stripe_sid=834eb932-6e52-488c-8c12-44f3a432e332f4c285"
            }

        )
        
        
        soup = BeautifulSoup(data.text, 'html.parser')
        script_tags = soup.find_all("script")
        script_text = script_tags[-2].text

        self.followers_counter = self.get_data("followerCount",script_text)
        self.following_counter = self.get_data("followingCount",script_text)
        self.month_views = self.get_data("lastMonthPublicContentViews",script_text)
        self.total_views = self.get_data("allTimePublicContentViews",script_text)
        imgURl = soup.find("meta", attrs={"property": 'og:image'})['content']
        self.avatar = imgURl
        script_text = script_tags[3].text
        self.uid =  self.get_data("uid",script_text)
 
