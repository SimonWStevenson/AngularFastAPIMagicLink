import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SecurityService {
  readonly ROOT_URL = 'http://localhost:8086/api';
  readonly thisUrl = '/login';
  httpOptions = {
    headers: new HttpHeaders({ 
      'Content-Type': 'application/json',
      'accept': 'application/json',
    })
  };

  constructor(
    private http: HttpClient,
    ) { }

  login(email: string): Observable<any> {
    let url = this.ROOT_URL + this.thisUrl + '/' + email;
    let options = this.httpOptions;
    let response = this.http.post(url, null, options);
    return response
  }
  
  isLoggedIn(): Observable<boolean> {
    let url = this.ROOT_URL + this.thisUrl
    let options = this.httpOptions
    let response = this.http.get<boolean>(url, options)
    return response
  }
}