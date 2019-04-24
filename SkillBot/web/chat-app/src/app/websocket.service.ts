import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Observable } from 'rxjs/Observable';
import * as Rx from 'rxjs/Rx';
import { environment } from '../environments/environment';
import { observable } from 'rxjs';
import { ObserveOnOperator } from 'rxjs/internal/operators/observeOn';
import { AsyncScheduler } from 'rxjs/internal/scheduler/AsyncScheduler';


@Injectable()
export class SocketDataService {

   private socket;

   constructor() {
      this.socket = io('http://localhost:4201')
   }

  
   observer
   getSocketData(): Observable<any> {
       this.socket.on('response_to_web', (res) => {
          console.log("*-*-*-", res);
           this.observer.next(res);
       });
       return this.getSocketDataObservable();
   }

   getSocketDataObservable(): Observable<any> {
       return new Observable(observer => {
           this.observer = observer;
       });
   }

   sendMessage(msg:Object){
     console.log("Message:::::::::::::", msg);
     this.socket.emit("message_req", msg)
   }
   
}


// @Injectable({
//   providedIn: 'root'
// })
// export class WebsocketService {

//   //socket connection
//   private socket; 

//   constructor() { 
//     this.socket = io(environment.ws_url);
//   }

//   connect(): Rx.Subject<MessageEvent> { 
//     this.socket.on('response_to_web', (data) => {
//       var dddd = data;
//       console.log("received message from response_to_web server", data.chat_res.reply_text);
//     })

//     let observable = new Observable(observable => {
//        return () => {
//          this.socket.disconnect();
//        }
//     });

//     let observer = {
//        next: (data: object) => {
//          console.log("+++++++++++++++++",JSON.stringify(data))
//          this.socket.emit('message_req', JSON.stringify(data));
//        },
//     };

//     return Rx.Subject.create(observer, observable);
//   }


// }