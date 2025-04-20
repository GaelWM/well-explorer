import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Observable } from 'rxjs';
import {
  ConfirmDialogComponent,
  ConfirmDialogData,
} from './confirm-dialog.component';

@Injectable({
  providedIn: 'root',
})
export class ConfirmDialogService {
  constructor(private dialog: MatDialog) {}

  /**
   * Opens a confirmation dialog
   * @param data Dialog configuration
   * @returns Observable that resolves to true if confirmed, false otherwise
   */
  openConfirmDialog(
    data: Partial<ConfirmDialogData> = {}
  ): Observable<boolean> {
    const dialogData: ConfirmDialogData = {
      title: data.title || 'Confirm Action',
      message: data.message || 'Are you sure you want to proceed?',
      confirmButtonText: data.confirmButtonText || 'Confirm',
      cancelButtonText: data.cancelButtonText || 'Cancel',
    };

    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      width: '400px',
      data: dialogData,
      disableClose: true,
    });

    return dialogRef.afterClosed();
  }
}
