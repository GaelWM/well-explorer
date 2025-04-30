import { CommonModule } from '@angular/common';
import {
  Component,
  computed,
  DestroyRef,
  effect,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { RouterLink } from '@angular/router';
import { ConfirmDialogService } from '../../shared/components/confirm-dialog/confirm-dialog.service';
import { MapComponent } from '../map-view/map/map.component';
import { WellFormComponent } from './well-form/well-form.component';
import { LiftType, Well, WellStatus, wellStatusOptions } from './well.model';
import { WellsService } from './wells.service';

@Component({
  selector: 'app-wells',
  templateUrl: './wells.component.html',
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    RouterLink,
    MapComponent,
  ],
})
export class WellsComponent {
  readonly wellService = inject(WellsService);
  readonly dialog = inject(MatDialog);
  readonly destroyRef = inject(DestroyRef);
  readonly confirmDialogService = inject(ConfirmDialogService);

  #wells$ = this.wellService
    .getWells()
    .pipe(takeUntilDestroyed(this.destroyRef));
  $wells = toSignal(this.#wells$, { initialValue: [] });

  $filteredWells = signal<Well[]>([]);

  $regionOptions = computed(() => {
    const uniqueRegions = new Set<string>();
    this.$wells().forEach((well) => {
      if (well.region) {
        uniqueRegions.add(well.region);
      }
    });
    return Array.from(uniqueRegions).sort();
  });

  $statusOptions = signal(wellStatusOptions);

  WellStatus = WellStatus;
  LiftType = LiftType;

  // Filters
  statusFilter: string = '';
  regionFilter: string = '';
  depthFilter: number | undefined = undefined;

  // Selected well for details view
  selectedWell: Well | null = null;

  wellToDelete: Well | null = null;

  constructor() {
    effect(() => {
      this.$filteredWells.set(this.$wells());
    });
  }

  openWellForm(): void {
    const dialogRef = this.dialog.open(WellFormComponent, {
      width: '600px',
      panelClass: 'transparent',
      data: { well: null },
    });

    dialogRef.afterClosed().subscribe(() => {
      // Refresh the well list after closing the dialog
      this.#wells$.subscribe((wells) => {
        this.$filteredWells.set(wells);
      });
    });
  }

  applyFilters(): void {
    this.$filteredWells.update((wells) => {
      // Reset filtered wells to all wells
      wells = [...this.$wells()];

      // Apply status filter
      if (this.statusFilter) {
        wells = wells.filter((well) => well.status === this.statusFilter);
      }

      // Apply region filter
      if (this.regionFilter) {
        wells = wells.filter((well) => well.region === this.regionFilter);
      }

      // Depth filter
      const depthFilter = this.depthFilter;
      if (depthFilter !== undefined) {
        wells = wells.filter((w) => {
          return w.depth > depthFilter;
        });
      }

      return wells;
    });
  }

  resetFilters(): void {
    this.statusFilter = '';
    this.regionFilter = '';
    this.$filteredWells.set(this.$wells());
  }

  editWell(event: Event, well: Well): void {
    event.preventDefault();
    event.stopPropagation();

    this.selectedWell = well;
    const dialogRef = this.dialog.open(WellFormComponent, {
      width: '600px',
      panelClass: 'transparent',
      data: { well: this.selectedWell },
    });
    dialogRef.afterClosed().subscribe(() => {
      // Refresh the well list after closing the dialog
      this.#wells$.subscribe((wells) => {
        this.$filteredWells.set(wells);
      });
    });
  }

  viewWellDetails(event: Event, well: Well): void {
    event.preventDefault();
    event.stopPropagation();

    this.selectedWell = well;
  }

  deleteWell(event: Event, well: Well): void {
    event.preventDefault();
    event.stopPropagation();

    this.confirmDialogService
      .openConfirmDialog({
        title: 'Delete Confirmation',
        message:
          'Are you sure you want to delete this well? This action cannot be undone.',
      })
      .subscribe((result) => {
        if (result) {
          this.wellService.deleteWell(well.id).subscribe({
            next: (success) => {
              if (success !== null) {
                this.$filteredWells.update((wells) =>
                  wells.filter((w) => w.id !== well!.id)
                );
              } else {
                console.error(
                  `Failed to delete well ${this.wellToDelete!.name}`
                );
              }
            },
            error: (error) => {
              console.error('Error deleting well:', error);
            },
          });
        }
      });
  }
}
