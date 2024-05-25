import { Component } from '@angular/core';
import { HttpClient,  HttpHeaders, HttpParams } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email: string = '';
  readonly ROOT_URL = "http://localhost:8086/api";
  readonly loginUrl = '/login/';
  httpOptions = {
    headers: new HttpHeaders({ 
      'Content-Type': 'application/json',
      'accept': 'application/json',
    })
  };
  responseData: any;
  isLoading: boolean = false;

  constructor(private http: HttpClient) {}

  submitEmail() {
    this.isLoading = true;
    let url = this.ROOT_URL + this.loginUrl + this.email
    let options = this.httpOptions
    this.http.post(url, null, options).subscribe(
      response => {
        this.responseData = response;
        this.isLoading = false;
      },
      error => {
        this.isLoading = false;
        console.error(error);
      }
    )
  }
}
