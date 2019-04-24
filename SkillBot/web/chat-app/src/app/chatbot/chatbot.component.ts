import { Component, OnInit } from '@angular/core';
// import { ChatService } from '../chat.service';
import { SocketDataService } from '../websocket.service';
import { stringify } from '@angular/core/src/render3/util';
import { Observable, Subject } from 'rxjs/Rx';
import { Subscription } from 'rxjs';
import { ArrayType } from '@angular/compiler';



@Component({
  moduleId: module.id,
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})

export class ChatbotComponent implements OnInit {
  
  username: "olivia";
  messages: Subject<any>;
  messages1: Subject<any>;
  str: string;
  
  
  date= new Date().toLocaleString(undefined, {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
  
  
  socket: SocketIOClient.Socket;
  
  chatArray: string[]=new Array()
  sub: Subscription;
  chatbotResponseArray: string[] = new Array()
  
  str1: string;

  constructor(private socketDataService: SocketDataService) {}

    ngOnInit() {
      this.getSocketData();
    }

    getSocketData(): void {
    this.sub = this.socketDataService.getSocketData()
      .subscribe(data => {
        console.log("*-*-*-*-*-", data);
        //this.chatbotResponseArray.push(data.chat_res.reply_text);
        this.chatArray.push(data.chat_res.reply_text);
    })
  }

  sendMessage() {
    var message_obj = {
      "name" : {
              "first_name": "",
              "middle_name": "",
              "last_name": "",
              "mob": ""
      },
      "identifier":{
              "user_id": "",
              "session_id": "",
              "socket_id":"",
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
              "chat_text": this.str,
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
      "channel": ""
    }

    this.socketDataService.sendMessage(message_obj)

    console.log("chat msg",this.str);
    //this.chatArray.push(this.str);
    
    this.str1=this.str;
    this.str="";
  }

}