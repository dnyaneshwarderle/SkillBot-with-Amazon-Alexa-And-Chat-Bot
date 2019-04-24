const app = require('express')();
const bodyParser = require('body-parser');

const cache = require('./alexa_app/session-cache.js');
const parser = require('./alexa_app/parse.js');

app.use(bodyParser.json());
const http = require('http').Server(app);
const io = require('socket.io')(http);

const axios = require("axios");

const email_sender = require("./email_sender");
const email_sender_obj = new email_sender();

global.mail;
function sendAlexa(response_obj){

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


}

io.on('connection', socket=> {
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
});

app.post('/alexa-webhook', (req, res) => {
    let body = req.body;
    // console.log(body);
    var requestObj = parser(body);
    var requestType = requestObj.requestType;
    var msg = requestObj.msg;
//found registered email ID of alexa
    const {
      apiAccessToken,
      apiEndpoint,
      user
    } = body.context.System;
    // console.log("apiAccessToken: ", apiAccessToken);
    // console.log("apiEndpoint: ", apiEndpoint);
    // console.log("userId: ", user.userId);

    const getEmailUrl = apiEndpoint.concat(
      `/v2/accounts/~current/settings/Profile.email`
    );
    // console.log("getEmailUrl", getEmailUrl);
console.log(getEmailUrl);
    let result = "";
    try {
      result =  axios.get(getEmailUrl, {
        headers: {
          Accept: "application/json",
          Authorization: "Bearer " + apiAccessToken
        }

      })

    } catch (error) {
      console.log(error);
    }
    result.then(function(data) {
        mail = data.data ;
})

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
                        "user_id": body.session.user.userId,
                        "session_id": sessionId,
                        "socket_id": sessionId,
                        "location": "",
                        "channel_id": "",
                        "group_id": "",
                        "team_id": "",
                        "email_id":mail,
                        "user_specified_id":{
                            "userdata": "" }
                },
                "time":{
                        "time_zone": ""
                },
                "chat_req": {
                        "message_id": body.request.requestId,
                        "chat_text": msg,
                        "chat_type": "message",
                        "chat_timestamp": body.request.timestamp
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
