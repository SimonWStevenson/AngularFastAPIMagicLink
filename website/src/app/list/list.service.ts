import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Note } from './note';
import { Observable, catchError, map, of, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ListService {
  readonly ROOT_URL = 'http://localhost:8086/api';
  readonly getNotesUrl = '/notes/';
  readonly addNoteUrl = '/note/';
  httpOptions = {
    headers: new HttpHeaders({ 
      'Content-Type': 'application/json',
      'accept': 'application/json',
    })
  };

  constructor(private http: HttpClient) {}

  getNotes(): Observable<Note[]> {
    let url = this.ROOT_URL + this.getNotesUrl
    let options = this.httpOptions
    let response = this.http.get<Note[]>(url, options)
    return response
  }

  addNote(note: string): Observable<Note>{
    let url = this.ROOT_URL + this.addNoteUrl + '?note=' + note
    let body = note
    let options = this.httpOptions
    let response = this.http.post<Note>(url, body, options)
    return response
  }

}
