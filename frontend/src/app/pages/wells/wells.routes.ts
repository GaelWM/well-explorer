import { Routes } from '@angular/router';
import { WellsComponent } from './wells.component';

export default [
  {
    path: '',
    component: WellsComponent,
  },
  {
    path: ':wellId',
    loadComponent: () =>
      import('../channels/channels.component').then((m) => m.ChannelsComponent),
  },
] as Routes;
