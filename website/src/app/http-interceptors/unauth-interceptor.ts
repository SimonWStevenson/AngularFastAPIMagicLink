// unauthorized.interceptor.ts
import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpRequest, HttpHandler, HttpErrorResponse } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { Router } from '@angular/router';

@Injectable()
export class UnauthInterceptor implements HttpInterceptor {
  constructor(private router: Router) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 400 || error.status === 401) {
          //console.error('Unauthorized request:', error);
          const errorMessage = error.error.detail || 'Something went wrong';
          this.router.navigate(['/expired'], { queryParams: { message: errorMessage } });
        }
        return throwError(error);
      })
    );
  }
}
