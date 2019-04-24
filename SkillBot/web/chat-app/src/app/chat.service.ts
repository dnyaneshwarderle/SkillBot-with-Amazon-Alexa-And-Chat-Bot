import { Injectable } from '@angular/core';
import { SocketDataService } from './websocket.service';
import { Observable, Subject } from 'rxjs/Rx';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

//   messages: Subject<any>;

//   constructor(private wsService: SocketDataService) {
//     this.messages = <Subject<any>>wsService
//       .connect()
//       .map((response: any): any => {
//           return response;
//       })
//    }
   
//    receiveMsg(replymsg){
//    }

//    sendMsg(msg) {
//      var message_obj = {
//           "name" : {
//                   "first_name": "",
//                   "middle_name": "",
//                   "last_name": "",
//                   "mob": ""
//           },
//           "identifier":{
//                   "user_id": "",
//                   "session_id": "",
//                   "location": "",
//                   "channel_id": "",
//                   "group_id": "",
//                   "team_id": "",
//                   "email_id":"",
//                   "user_specified_id":{
//                       "userdata": "" }
//           },
//           "time":{
//                   "time_zone": ""
//           },
//           "chat_req": {
//                   "message_id": "",
//                   "chat_text": msg,
//                   "chat_type": "message",
//                   "chat_timestamp": ""
//           },
//           "chat_res":{
//                   "reply_id": "",
//                   "reply_text": "",
//                   "reply_timestamp": "",
//                   "additional_param":{
//                   },
//                   "reply_action": ""
//           },
//           "channel": ""
//       }

//      this.messages.next(message_obj);
     

//    }
}
