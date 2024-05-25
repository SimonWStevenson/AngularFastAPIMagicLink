import { HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor() {}
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const authReq = req.clone({
      withCredentials: true
    });

    // send cloned request with header to the next handler.
    return next.handle(authReq);
  }
}