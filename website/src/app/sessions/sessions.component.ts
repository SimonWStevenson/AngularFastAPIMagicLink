import { Component } from '@angular/core';
import { SessionsService } from './sessions.service';
import { Session } from './session';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sessions',
  templateUrl: './sessions.component.html',
  styleUrls: ['./sessions.component.css']
})

export class SessionsComponent {
  sessions: Session[] = [];
  constructor(
    private sessionService: SessionsService,
    private router: Router
    ){}

  ngOnInit(): void {
    this.sessionService.getSessions().subscribe({
      next: (response) => {
        this.sessions = response
      },
      error: (error) => {
        console.error('Error getting sessions:', error);
      }
    });
  }
  closeSession(session_id: number){
    this.sessionService.closeSession(session_id).subscribe({
      next: (response) => {
        if (response.id === session_id){
          if (response.id === session_id) {
            this.router.navigate(['/login']);
          }
          this.sessions = this.sessions.filter(s => s.id !== session_id);
        }
      },
      error: (error) => {
        console.error('Error deleting session:', error);
      }
    });
  }
}
