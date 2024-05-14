const process = require('node:process');


module.exports= async function main (profile,uid)  {

    const response = await fetch("https://www.quora.com/graphql/gql_para_POST?q=UserProfileAnswersMostRecent_RecentAnswers_Query", {
      "headers": {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,en-GB;q=0.8,fr-FR;q=0.7,fr;q=0.6",
        "content-type": "application/json",
        "priority": "u=1, i",
        "quora-broadcast-id": "main-w-chan67-8888-react_yulofggaqorbpnbq-HXWI",
        "quora-canary-revision": "false",
        "quora-formkey": "767e1d3891740330422b6557e33eb288",
        "quora-page-creation-time": "1714248218393841",
        "quora-revision": "435d777e3f9e7eb231842d3baf1cb53580944711",
        "quora-window-id": "react_yulofggaqorbpnbq",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "m-b=Z_eMuSEcAFHmSyX_Cd-FNQ==; m-b_lax=Z_eMuSEcAFHmSyX_Cd-FNQ==; m-b_strict=Z_eMuSEcAFHmSyX_Cd-FNQ==; m-s=MxSjN-h2UzIPa5MlTjDcpA==; m-dynamicFontSize=regular; m-themeStrategy=auto; m-theme=dark; m-login=1; m-lat=ug0eVthhx1uOAzoD1X6d4PchV1OnkgHio2L3YUI/GQ==; m-uid=2563106278; __stripe_mid=23085ba8-4b04-4974-8206-a02e969d89299bfef6; __stripe_sid=8f24f4d2-f833-4193-b3e7-80fa4a208deb6bd6d2; m-sa=1; __gads=ID=0b2ff041bf06bade:T=1714248166:RT=1714248166:S=ALNI_MaioT2AAbNYytrPodf3wRBWRUiTWw; __gpi=UID=00000d68ec6493b3:T=1714248166:RT=1714248166:S=ALNI_MYMp5Ccb9nJr0EDHvdzYlDNiiRKWw; __eoi=ID=d721c89e3d8c3455:T=1714248166:RT=1714248166:S=AA-AfjZgFHb4Cc-aAhJ2e6CNfLPW",
        "Referer": "https://www.quora.com/profile/"+profile+"/answers",
        "Referrer-Policy": "strict-origin-when-cross-origin"
      },
      "body": "{\"queryName\":\"UserProfileAnswersMostRecent_RecentAnswers_Query\",\"variables\":{\"uid\":"+uid+",\"first\":3,\"after\":\"0\",\"answerFilterTid\":null},\"extensions\":{\"hash\":\"f81036e47d9442c0b295c1b8fdce706183e0d41e3afffbbd97abf210dc6ae302\"}}",
      "method": "POST"
    });
      const body = await response.json();
      answer = body["data"]["user"]["recentPublicAndPinnedAnswersConnection"]["edges"][0]
      url=answer["node"]["url"];
    if (! url.startsWith("https")){
        url="https://www.quora.com"+url;
    }

        return {"answer_id":answer["node"]["aid"],"url":url};
    }
    
