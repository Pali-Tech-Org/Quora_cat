const {Client,IntentsBitField,PermissionsBitField } = require("discord.js");
const sqlite3 = require("sqlite3").verbose();
const {quora_cat} = require("./funcs.js");

//================================================================================================
const db = new sqlite3.Database("./quora_bot.db",sqlite3.OPEN_READWRITE,(err)=>{
    if(err) return console.error(err.message)
});

//================================================================================================
const client = new Client({
intents:[
    IntentsBitField.Flags.Guilds, 
    IntentsBitField.Flags.GuildMembers, 
    IntentsBitField.Flags.GuildMessages, 
    IntentsBitField.Flags.MessageContent, 
],
});

//================================================================================================




//================================================================================================
client.on('ready',(c)=>{
console.log("bot ready");
quora_cat(db,c);
});
//================================================================================================
client.on('messageCreate',(msg)=>{
    if(msg.member.permissions.has(PermissionsBitField.Flags.KickMembers)){
    const channel_id = msg.channelId;
    const server_id = msg.guildId.toString(16);
    const command=msg.content;
    if(command.startsWith("qr!set")){
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
    else if(command.startsWith("qr!add")){
        const profile_id=command.split(" ")[1];
        const uid=command.split(" ")[2];
        const server_id = msg.guildId.toString(16);
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
    else if(command.startsWith("qr!remove")){
        const profile_id=command.split(" ")[1];

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
    }
}
);

//================================================================================================
client.login("Token");
