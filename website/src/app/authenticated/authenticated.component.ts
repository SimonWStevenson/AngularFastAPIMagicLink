import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-authenticated',
  templateUrl: './authenticated.component.html',
  styleUrls: ['./authenticated.component.css']
})
export class AuthenticatedComponent {
  readonly ROOT_URL = "http://localhost:8086/api";
  readonly authUrl = '/authenticated';
  httpOptions = {
    headers: new HttpHeaders({ 
      'Content-Type': 'application/json',
      'accept': 'application/json',
    })
  };
  responseData: any;
  constructor(private http: HttpClient) {}
  ngOnInit() {
    this.authenticate();
  }
  authenticate() {
    let url = this.ROOT_URL + this.authUrl
    let options = this.httpOptions
    this.http.get(url, options).subscribe(
      response => {
        this.responseData = response;
      }
    )
  }  
}
