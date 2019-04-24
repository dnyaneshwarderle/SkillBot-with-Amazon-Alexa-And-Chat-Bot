import { NgModule } from '@angular/core';
import { CommonModule, } from '@angular/common';
import { BrowserModule  } from '@angular/platform-browser';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { SignupComponent } from './signup/signup.component';
import { LandingComponent } from './landing/landing.component';
import { NucleoiconsComponent } from './components/nucleoicons/nucleoicons.component';
import { ChatbotComponent } from './chatbot/chatbot.component';
import { RegisterComponent } from './register/register.component';
import { TestComponent } from './test/test.component';
import { TestgroundComponent } from './testground/testground.component';
import { from } from 'rxjs';

const routes: Routes =[
    { path: 'home',             component: LandingComponent },
    { path: 'user-profile',     component: ProfileComponent },
    { path: 'signup',           component: SignupComponent },
    { path: 'register',           component: RegisterComponent },
    { path: 'chatbot',           component: ChatbotComponent },
    { path: 'landing',          component: HomeComponent },
    { path: 'nucleoicons',      component: NucleoiconsComponent },
    { path: 'test',             component: TestComponent },
    { path: 'testground',       component: TestgroundComponent },
    { path: '', redirectTo: 'home', pathMatch: 'full' }
];

@NgModule({
  imports: [
    CommonModule,
    BrowserModule,
    RouterModule.forRoot(routes)
  ],
  exports: [
  ],
})
export class AppRoutingModule { }
