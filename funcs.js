const process = require('node:process');



// main function =======================================================================
async function main (profile,uid)  {

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
      let answer = body["data"]["user"]["recentPublicAndPinnedAnswersConnection"]["edges"][0]
      let url=answer["node"]["url"];
    if (! url.startsWith("https")){
        url="https://www.quora.com"+url;
    }

        return {"answer_id":answer["node"]["aid"],"url":url};
    }



// quora_cat function ==================================================================
async function quora_cat  (db,client){
    const data=db.all(`SELECT * FROM profiles `,[],(err,rows)=>{
        if(err) return console.error(err.message);
        rows.forEach((row) => {
            let profile_id = row["profileID"];
            let server_id = row["serverID"]
            let uid=row["uid"]
            main(profile_id,uid).then((value)=>{
                let answer_id=value["answer_id"].toString(16);
                let url=value["url"];
                const answers=db.all(`SELECT *  FROM answers WHERE answerID  =? AND serverID = ?`,[answer_id,server_id],(err,roww)=>{
                    if(err) return console.error(err.message);
                    if(roww.length==0){
                    const channels=db.all(`SELECT *  FROM channels WHERE serverID  =? `,[server_id],(err,rowws)=>{
                        if(err) return console.error(err.message);
                        if(rowws.length>0){
                            let channel_id=rowws[0]["channelID"];
                            let channel = client.channels.cache.find(channel => channel.id == channel_id);
                            channel.send(url);
                            db.run(`INSERT INTO answers VALUES (?,?)`,[server_id, answer_id],(err)=>{
                        if(err) return console.error(err.message);
                    });
                        }
                });       
                    }
            });

            }
     
       );
        });
           
}); 
    setTimeout(() => {
            quora_cat(db,client);
        }, 30000);
}


// add_user function ===================================================================
function add_user(db,server_id,profile_id,uid){

        const data=db.all(`SELECT *  FROM profiles WHERE profileID  = ? AND serverID = ?`,[profile_id,server_id],(err,row)=>{
            if(err) return console.error(err.message);
            if(row.length == 0){
                db.run(`INSERT INTO profiles VALUES  (?,?,?)`,[server_id,profile_id,uid],(err)=>{
                    if(err) return console.error(err.message);
                });
            }else{
                console.log("user aleardy in");
            }
        });

}


// remove_user function ================================================================

function remove_user(db,server_id,profile_id){
        const data=db.all(`SELECT *  FROM profiles WHERE profileID  = ? AND serverID = ?`,[profile_id,server_id],(err,row)=>{
            if(err) return console.error(err.message);
            if(row.length == 0){
                console.log("user aleardy deleted");
            }else{
                db.run(`DELETE FROM profiles WHERE serverID = ? AND profileID = ?`,[server_id,profile_id],(err)=>{
                    if(err) return console.error(err.message);
                });
            }
        });
}
// 

// set_channel function ================================================================
 function set_channel(db,server_id,channel_id){
        const data=db.all(`SELECT channelID  FROM channels WHERE serverID  =? `,[server_id],(err,row)=>{
            if(err) return console.error(err.message);
            if(row.length>0){
                db.run(`UPDATE channels SET channelID = ? WHERE serverID = ?`,[channel_id,server_id],(err)=>{
                    if(err) return console.error(err.message);
                });
            }else{
            db.run(`INSERT INTO channels VALUES (?,?)`,[server_id,channel_id],(err)=>{
                if(err) return console.error(err.message);
            });

            }
    });
 }


// Export ===============================================================================
module.exports= {   
quora_cat:quora_cat,
    add_user:add_user,
    remove_user:remove_user,
    set_channel:set_channel,
    
}
   
