import { Routes } from '@angular/router';
import { WellsComponent } from './wells.component';

export default [
  {
    path: '',
    component: WellsComponent,
  },
  {
    path: ':well_id',
    loadComponent: () =>
      import('../channels/channels.component').then((m) => m.ChannelsComponent),
    children: [
      {
        path: 'channels',
        loadComponent: () =>
          import('../channels/channels.component').then(
            (m) => m.ChannelsComponent
          ),
      },
    ],
  },
] as Routes;
