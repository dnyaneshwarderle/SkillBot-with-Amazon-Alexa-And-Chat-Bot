var nodemailer = require("nodemailer");

var transporter = nodemailer.createTransport({
    service : 'gmail',
    auth : {
        user : 'gamesareyoukidding@gmail.com',
        pass : 'AdminKajal@123'
    }
});


module.exports = function(){
    console.log("In otp sender");
    this.send_email = function(otp, email_id){

        var mailOptions={
            from : 'gamesareyoukidding@gmail.com',
            //to : 'kajalchauhan.mscit.17@gmail.com',
            to : email_id,
            subject : "welcome to Skill Bot Email verification",
            // html: ("Hello, <br>"
            //  +"here is your one time password "
            //  +otp)


            html: (`<head>
                        <style>
                            form{
                                min-height: 600px;
                                height: auto;
                                width: 400px;
                                outline-width: 50px;
                                border-style: solid;
                                border-color: grey;
                                border-width: 3px;
                            }
                            img{
                                margin-top: 10px;
                                border-style: solid;
                                border-radius: 50%;
                                border-color: purple;
                                border-width: 5px;
                            }
                            p{
                                font-family: sans-serif;
                            }
                        </style>
                        </head>
                        <body>
                            <center>
                                <form>

                                    <img src="skill.png">
                                    <h2>Skill Bot</h2>

                                    <br><br>

                                    <h2>your one time password is</h2><br>
                                    <h4>`+otp+`</h4>

                                    <hr>

                                    <p>use this otp to login for first time & then change your password</p>


                                </form>
                            </center>
                        </body>`
        )

        }

        console.log(mailOptions);

        transporter.sendMail(mailOptions, function(error, response){
            if(error){
                console.log(error);
            res.end("error");
            }else{
                console.log("Message sent: " + response.message);
            res.end("sent");
                }
        });
    }


}
