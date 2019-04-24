'use strict';

const
  express       = require('express'),
  bodyParser    = require('body-parser'),
  app           = express().use(bodyParser.json()),
  cache         = require('./session-cache.js'),
  parser        = require('./parse.js');

app.listen(process.env.PORT || 5000, () => console.log('alexa-webhook is listening'));


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
  /////////////////////////////////
  var responseCallback = cache.popSessionResponse(sessionId);
  responseCallback.send({
    version: "string",
    response: {
      outputSpeech: {
        type: 'PlainText',
        text: "RESP- Unknown-Type"
      },
      reprompt: {
        outputSpeech: {
          type: "PlainText",
          text: "Would you like me to repeat"
        }
      },
      shouldEndSession: false
    }
  });
/////////////////////////////////


});


