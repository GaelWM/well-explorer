import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { WellFormComponent } from './well-form/well-form.component';
import { Well, wellStatusOptions } from './well.model';
import { WellsService } from './wells.service';

@Component({
  selector: 'app-wells',
  templateUrl: './wells.component.html',
  imports: [CommonModule, FormsModule, MatDialogModule],
})
export class WellsComponent implements OnInit {
  readonly wellService = inject(WellsService);
  readonly dialog = inject(MatDialog);

  wells: Well[] = [];
  filteredWells: Well[] = [];
  statusOptions = wellStatusOptions;
  regionOptions: string[] = [];

  // Filters
  statusFilter: string = '';
  regionFilter: string = '';

  // Selected well for details view
  selectedWell: Well | null = null;

  wellToDelete: Well | null = null;

  ngOnInit(): void {
    this.loadWells();
  }

  openWellForm(): void {
    const dialogRef = this.dialog.open(WellFormComponent, {
      width: '600px',
      panelClass: 'transparent',
      data: { well: this.selectedWell },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.loadWells();
      }
    });
  }

  loadWells(): void {
    this.wellService.getWells().subscribe({
      next: (wells) => {
        console.log('wells: ', wells);
        this.wells = wells;
        this.filteredWells = [...wells];
        this.extractRegions();
      },
      error: (error) => {
        console.error('Error loading wells:', error);
        // In a real app, you would add proper error handling here
      },
    });
  }

  extractRegions(): void {
    // Extract unique regions from wells
    const uniqueRegions = new Set<string>();
    this.wells.forEach((well) => {
      if (well.region) {
        uniqueRegions.add(well.region);
      }
    });
    this.regionOptions = Array.from(uniqueRegions).sort();
  }

  applyFilters(): void {
    this.filteredWells = this.wells.filter((well) => {
      // Status filter
      if (this.statusFilter && well.status !== this.statusFilter) {
        return false;
      }

      // Region filter
      if (this.regionFilter && well.region !== this.regionFilter) {
        return false;
      }

      return true;
    });
  }

  resetFilters(): void {
    this.statusFilter = '';
    this.regionFilter = '';
    this.filteredWells = [...this.wells];
  }

  viewWellDetails(well: Well): void {
    this.selectedWell = well;
  }

  closeWellDetails(): void {
    this.selectedWell = null;
  }

  confirmDeleteWell(well: Well): void {
    this.wellToDelete = well;
  }

  cancelDelete(): void {
    this.wellToDelete = null;
  }

  deleteWell(): void {
    if (this.wellToDelete) {
      this.wellService.deleteWell(this.wellToDelete.id).subscribe({
        next: (success) => {
          if (success !== null) {
            // Remove well from arrays and refresh the view
            this.wells = this.wells.filter(
              (w) => w.id !== this.wellToDelete!.id
            );
            this.filteredWells = this.filteredWells.filter(
              (w) => w.id !== this.wellToDelete!.id
            );

            // In a real app, you would show a success notification
            console.log(`Well ${this.wellToDelete!.name} successfully deleted`);
          } else {
            // In a real app, you would show an error notification
            console.error(`Failed to delete well ${this.wellToDelete!.name}`);
          }

          // Close the confirmation dialog
          this.wellToDelete = null;
        },
        error: (error) => {
          console.error('Error deleting well:', error);
          // In a real app, you would show an error notification

          // Close the confirmation dialog
          this.wellToDelete = null;
        },
      });
    }
  }
}
