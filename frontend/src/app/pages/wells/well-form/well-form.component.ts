// well-form.component.ts
import { DIALOG_DATA } from '@angular/cdk/dialog';
import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { liftTypeOptions, Well, wellStatusOptions } from '../well.model';
import { WellsService } from '../wells.service';

@Component({
  selector: 'app-well-form',
  templateUrl: './well-form.component.html',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
})
export class WellFormComponent implements OnInit {
  readonly dialogRef = inject(MatDialogRef);
  readonly data = inject(DIALOG_DATA) as { well: Well | undefined };
  readonly fb = inject(FormBuilder);
  readonly wellService = inject(WellsService);
  readonly router = inject(Router);

  wellForm!: FormGroup;
  well: Well = new Well({});
  isEditMode = false;
  liftTypeOptions = liftTypeOptions;
  statusOptions = wellStatusOptions;

  ngOnInit(): void {
    this.initForm();

    if (this.data.well) {
      this.isEditMode = true;
      this.loadWell(this.data.well.id);
    }
  }

  // Initialize the form with validators
  initForm(): void {
    this.wellForm = this.fb.group({
      name: [this.data.well?.name, [Validators.required]],
      liftType: [this.data.well?.liftType, [Validators.required]],
      region: [this.data.well?.region, [Validators.required]],
      latitude: [
        this.data.well?.latitude,
        [Validators.required, Validators.min(-90), Validators.max(90)],
      ],
      longitude: [
        this.data.well?.longitude,
        [Validators.required, Validators.min(-180), Validators.max(180)],
      ],
      installationDate: [
        this.data.well?.installationDate,
        [this.maxDateValidator],
      ],
      depth: [
        this.data.well?.depth,
        [Validators.required, Validators.min(0.01)],
      ],
      status: [this.data.well?.status, [Validators.required]],
    });
  }

  // Get form controls for easier access in the template
  get f() {
    return this.wellForm.controls;
  }

  // Custom validator for installation date (cannot be in the future)
  maxDateValidator(control: any) {
    if (!control.value) {
      return null;
    }

    const today = new Date();
    const inputDate = new Date(control.value);

    if (inputDate > today) {
      return { maxDate: true };
    }

    return null;
  }

  // Load well data for editing
  loadWell(id: number): void {
    this.wellService.getWellById(id).subscribe({
      next: (well) => {
        if (well) {
          this.well = well;

          // Format the installation date to YYYY-MM-DD for the date input
          let installationDateStr: string | null = null;
          if (well.installationDate) {
            const date = new Date(well.installationDate);
            installationDateStr = date.toISOString().split('T')[0];
          }

          // Patch form values
          this.wellForm.patchValue({
            name: well.name,
            liftType: well.liftType,
            region: well.region,
            latitude: well.latitude,
            longitude: well.longitude,
            installationDate: installationDateStr,
            depth: well.depth,
            status: well.status,
          });
        } else {
          this.router.navigate(['/wells']);
          // In a real app, you would also show a notification that the well was not found
        }
      },
      error: (error) => {
        console.error('Error loading well:', error);
        this.router.navigate(['/wells']);
        // In a real app, you would also show an error notification
      },
    });
  }

  // Form submit handler
  onSubmit(): void {
    if (this.wellForm.invalid) {
      // Mark all fields as touched to trigger validation messages
      Object.keys(this.wellForm.controls).forEach((key) => {
        const control = this.wellForm.get(key);
        control?.markAsTouched();
      });
      return;
    }

    // Create a new Well object from form values
    const formValues = this.wellForm.value;
    const wellData: Partial<Well> = {
      name: formValues.name,
      liftType: formValues.liftType,
      region: formValues.region,
      latitude: formValues.latitude,
      longitude: formValues.longitude,
      depth: formValues.depth,
      status: formValues.status,
    };

    // Add installation date if provided
    if (formValues.installationDate) {
      wellData.installationDate = new Date(formValues.installationDate);
    }

    // Add ID if in edit mode
    if (this.isEditMode) {
      wellData.id = this.well.id;
    }

    // Create or update the well
    if (this.isEditMode) {
      this.updateWell(wellData);
    } else {
      this.createWell(wellData);
    }
  }

  // Create a new well
  createWell(wellData: Partial<Well>): void {
    this.wellService.createWell(wellData).subscribe({
      next: () => {
        this.router.navigate(['/wells']);
        // In a real app, you would also show a success notification
      },
      error: (error) => {
        console.error('Error creating well:', error);
        // In a real app, you would also show an error notification
      },
    });
  }

  // Update an existing well
  updateWell(wellData: Partial<Well>): void {
    this.wellService.updateWell(wellData.id!, wellData).subscribe({
      next: () => {
        this.router.navigate(['/wells']);
        // In a real app, you would also show a success notification
      },
      error: (error) => {
        console.error('Error updating well:', error);
        // In a real app, you would also show an error notification
      },
    });
  }

  // Cancel and return to wells list
  onCancel(): void {
    this.dialogRef.close();
  }
}
