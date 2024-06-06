import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Session } from './session';

@Injectable({
  providedIn: 'root'
})
export class SessionsService {
  readonly ROOT_URL = 'http://localhost:8086/api';
  readonly sessionUrl = '/session';
  httpOptions = {
    headers: new HttpHeaders({ 
      'Content-Type': 'application/json',
      'accept': 'application/json',
    })
  };

  constructor(private http: HttpClient) {}
  getSessions(): Observable<Session[]> {
    let url = this.ROOT_URL + this.sessionUrl
    let options = this.httpOptions
    let response = this.http.get<Session[]>(url, options)
    return response
  }

  closeSession(session_id: number): Observable<Session>{
    let url = this.ROOT_URL + this.sessionUrl + '?session_id=' + session_id
    let options = this.httpOptions
    let response = this.http.delete<Session>(url, options)
    return response
  }
}
