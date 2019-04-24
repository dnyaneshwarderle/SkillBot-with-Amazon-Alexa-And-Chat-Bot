const app = require('express')();
const bodyParser = require('body-parser');
const cache = require('./alexa_app/session-cache.js');
const parser = require('./alexa_app/parse.js');

app.use(bodyParser.json());
const http = require('http').Server(app);
const io = require('socket.io')(http);

const email_sender = require("./email_sender");
const email_sender_obj = new email_sender();

//const messages = [];

//app.get('/', (req, res) => res.send("Hello World"));

function sendAlexa(response_obj){
    /////////////////////////////////
    var sessionId = response_obj.identifier.session_id;
    var responseCallback = cache.popSessionResponse(sessionId);
    responseCallback.send({
      version: "string",
      response: {
        outputSpeech: {
          type: 'PlainText',
          text: response_obj.chat_res.reply_text
        },
        reprompt: {
          outputSpeech: {
            type: "PlainText",
            text: ""
          }
        },
        shouldEndSession: false
      }
    });
  /////////////////////////////////

}
  
io.on('connection', socket=> {
    //console.log(`socket ${socket.id} has connected`);
    console.log('user connected');

    socket.on('disconnect', function(){
        console.log('user disconected');
    });


    socket.on('send_email', function(otp, email_id){
        console.log('user send_email');
        email_sender_obj.send_email(otp, email_id);
    });

    socket.on('message_req', (message) => {
        console.log("message received:",  message, null, 4);
        // message.identifier.socket_id = socket.id;
        // message.identifier.user_id = socket.id;
         io.emit('message_req_worker', message);
    });

    socket.on('response_to_service', (resp_message) => {

        console.log("response_to_service==",  resp_message, null, 4);
        if (resp_message.channel == "alexa"){
            sendAlexa(resp_message);
        }else{
            io.emit('response_to_web', resp_message);
        }
         
    });


    //io.emit('messages', object.keys(messages));

});


app.post('/alexa-webhook', (req, res) => {
    let body = req.body;
  
    var requestObj = parser(body);
    var requestType = requestObj.requestType;
    var msg = requestObj.msg;
    var sessionId = requestObj.sessionId;
  
    console.log("-------================---------");
    console.log("requestType : ", JSON.stringify(requestType, null, 4));
  
    console.log("");
    console.log("msg : ", JSON.stringify(msg, null, 4));
    console.log("");
    console.log("-------================---------");
  
    cache.insertSession(sessionId, res);
    if (msg.trim() && requestType == "IntentRequest"){

    
            var message_obj = {
                "name" : {
                        "first_name": "",
                        "middle_name": "",
                        "last_name": "",
                        "mob": ""
                },
                "identifier":{
                        "user_id": "",
                        "session_id": sessionId,
                        "socket_id": sessionId,
                        "location": "",
                        "channel_id": "",
                        "group_id": "",
                        "team_id": "",
                        "email_id":"",
                        "user_specified_id":{
                            "userdata": "" }
                },
                "time":{
                        "time_zone": ""
                },
                "chat_req": {
                        "message_id": "",
                        "chat_text": msg,
                        "chat_type": "message",
                        "chat_timestamp": ""
                },
                "chat_res":{
                        "reply_id": "",
                        "reply_text": "",
                        "reply_timestamp": "",
                        "additional_param":{
                        },
                        "reply_action": ""
                },
                "channel": "alexa"
            }

            io.emit('message_req_worker', message_obj);

    }else if(requestType == "LaunchRequest"){
        sendAlexa({
            "identifier": { "session_id": sessionId},
            "chat_res": { "reply_text": "Hello, Welcome to skill bot."}})
    }else if(requestType == "StopRequest"){
        sendAlexa({
            "identifier": { "session_id": sessionId},
            "chat_res": { "reply_text": "Thank you for visiting skill bot."}})
    }else{
        sendAlexa({
            "identifier": { "session_id": sessionId},
            "chat_res": { "reply_text": ""}})
    }
    
  
});


http.listen(4201, () => {
    console.log('Listening on port 4201');
})
