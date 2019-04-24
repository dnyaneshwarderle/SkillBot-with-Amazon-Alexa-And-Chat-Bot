var reminders = require('alexa-reminders')
debugger;
reminders.login('Echo Dot', 'dnderle10@gmail.com', 'Derle@10', function(error, response, config){
  reminders.setReminder('Ask Alexa team for a proper Reminders API', null, config, function(error, response){
    console.log(response)
  })
})
