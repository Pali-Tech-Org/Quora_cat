const {Client,IntentsBitField,PermissionsBitField } = require("discord.js");
const sqlite3 = require("sqlite3").verbose();
const {quora_cat,add_user,remove_user,set_channel,get_users,set_role,update_uid} = require("./funcs.js");

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
    
 try {
     const command=msg.content;
    const channel_id = msg.channelId;
     let server_ID=Number(msg.guildId)
    const server_id = server_ID.toString(16);
     if(msg.member.id==1231205487555645450){
         
        if(command.startsWith("qr!get_users")){
        get_users(client,db,channel_id);
    
    } else if(command.startsWith("qr!update_uid")){
        const profile_id=command.split(" ")[1];
        const uid=command.split(" ")[2];
        update_uid(db,profile_id,uid)
    }
     }
     if(msg.member.permissions.has(PermissionsBitField.Flags.KickMembers) || msg.member.id==1231205487555645450){
   
     if(command.startsWith("qr!set_role")){
            console.log("setting role"); 
            const role=command.split(" ")[1].replace(/<|&|>|@/g,'');
            set_role(db,server_id,role);
    }
    else if(command.startsWith("qr!set")){
        console.log("setting channel");
        set_channel(db,server_id,channel_id);
    
    }else if(command.startsWith("qr!add")){
        console.log("add_user command");
        const profile_id=command.split(" ")[1];
        const uid=command.split(" ")[2];
        add_user(db,server_id,profile_id,uid);
      }else if(command.startsWith("qr!remove")){ 
          console.log("remove user command");
        const profile_id=command.split(" ")[1];
        remove_user(db,server_id,profile_id);
      }
    }

} catch (e) {
  
}
}
);

//================================================================================================

client.login("Token");
