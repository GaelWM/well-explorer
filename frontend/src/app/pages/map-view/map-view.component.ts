import { Component, DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogService } from '../../shared/components/confirm-dialog/confirm-dialog.service';
import { WellsService } from '../wells/wells.service';
import { MapComponent } from './map/map.component';

@Component({
  selector: 'app-map-view',
  imports: [MapComponent],
  templateUrl: './map-view.component.html',
})
export class MapViewComponent {
  readonly wellService = inject(WellsService);
  readonly dialog = inject(MatDialog);
  readonly destroyRef = inject(DestroyRef);
  readonly confirmDialogService = inject(ConfirmDialogService);

  #wells$ = this.wellService
    .getWells()
    .pipe(takeUntilDestroyed(this.destroyRef));
  $wells = toSignal(this.#wells$, { initialValue: [] });
}
