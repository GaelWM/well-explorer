import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'wells',
    pathMatch: 'full',
  },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./pages/dashboard/dashboard.component').then(
        (c) => c.DashboardComponent
      ),
  },
  {
    path: 'wells',
    loadChildren: () => import('./pages/wells/wells.routes'),
  },
  {
    path: 'map',
    loadComponent: () =>
      import('./pages/map-view/map-view.component').then(
        (c) => c.MapViewComponent
      ),
  },
];
