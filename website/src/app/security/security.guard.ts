import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { SecurityService } from './security.service';

export const AuthGuard: CanActivateFn = (): Observable<boolean> => {
    const securityService = inject(SecurityService);
    const router = inject(Router);
    return securityService.isLoggedIn().pipe(
        map(isLoggedIn => {
            if(!isLoggedIn){
                router.navigate(['/login']);
                return false;
            }
            return true;
        })
    )
}

export const LoginGuard: CanActivateFn = (): Observable<boolean> => {
    const securityService = inject(SecurityService);
    const router = inject(Router);
    return securityService.isLoggedIn().pipe(
        map(isLoggedIn => {
            if(isLoggedIn){
                router.navigate(['/home']);
                return false;
            }
            return true;
        })
    )
}