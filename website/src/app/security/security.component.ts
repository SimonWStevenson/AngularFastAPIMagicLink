import { Component } from '@angular/core';
import { SecurityService } from './security.service';

@Component({
  selector: 'app-security',
  templateUrl: './security.component.html',
  styleUrls: ['./security.component.css']
})

export class SecurityComponent {
  email: string = '';
  responseData: any;
  isLoading: boolean = false;

  constructor(
    private securityService: SecurityService,
  ) {}

  ngOnInit(): void {
  }

  submitEmail() {
    this.isLoading = true;
    this.securityService.login(this.email).subscribe({
      next: (response) => {
        this.responseData = response;
        this.isLoading = false;
      },
      error: (error) => {
        this.isLoading = false;
        console.error(error);
        this.isLoading = false;
      }
    })
  }
}
