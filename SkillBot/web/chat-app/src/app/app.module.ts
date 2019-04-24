import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app.routing';

import { AppComponent } from './app.component';
import { SignupComponent } from './signup/signup.component';
import { LandingComponent } from './landing/landing.component';
import { ProfileComponent } from './profile/profile.component';
import { HomeComponent } from './home/home.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { FooterComponent } from './shared/footer/footer.component';

import { HomeModule } from './home/home.module';
import { ChatbotComponent } from './chatbot/chatbot.component';

//import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { RegisterComponent } from './register/register.component';
import { ChatService } from './chat.service';
import { SocketDataService } from './websocket.service';
import { TestComponent } from './test/test.component';
import { TestgroundComponent } from './testground/testground.component'

//const config: SocketIoConfig = { url: 'http://localhost:4444', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    SignupComponent,
    LandingComponent,
    ProfileComponent,
    NavbarComponent,
    FooterComponent,
    ChatbotComponent,
    RegisterComponent,
    TestComponent,
    TestgroundComponent,
  ],
  imports: [
    BrowserModule,
    NgbModule.forRoot(),
    FormsModule,
    RouterModule,
    AppRoutingModule,
    HomeModule,
      
  ],
  providers: [ChatService, SocketDataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
