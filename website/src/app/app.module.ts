import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { SecurityComponent } from './security/security.component';

import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from '../app/http-interceptors/auth-interceptor';
import { UnauthInterceptor } from '../app/http-interceptors/unauth-interceptor';
import { ListComponent } from './list/list.component';
import { SessionsComponent } from './sessions/sessions.component';
import { HomeComponent } from './home/home.component';
import { AuthGuard, LoginGuard } from './security/security.guard';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'login', component: SecurityComponent, canActivate: [LoginGuard] },
];

@NgModule({
  declarations: [
    AppComponent,
    SecurityComponent,
    ListComponent,
    SessionsComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: UnauthInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
