import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
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
      import('./pages/map/map.component').then((c) => c.MapComponent),
  },
];
