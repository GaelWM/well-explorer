import { DIALOG_DATA } from '@angular/cdk/dialog';
import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  inject,
  Input,
  OnInit,
} from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Channel } from '../channel.model';
import { ChannelsService } from '../channels.service';

@Component({
  selector: 'app-channel-form',
  templateUrl: './channel-form.component.html',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ChannelFormComponent implements OnInit {
  readonly dialogRef = inject(MatDialogRef);
  readonly channelService = inject(ChannelsService);

  readonly data = inject(DIALOG_DATA) as {
    channel: Channel | null;
    well_id: number;
  };

  @Input() channel: Channel | null = null;

  channelForm!: FormGroup;
  formError: string | null = null;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.initForm();
  }

  // Initialize the form with validation
  initForm(): void {
    this.channelForm = this.fb.group(
      {
        id: [this.channel?.id || this.data.channel?.id || null],
        well_id: [this.data.well_id || this.channel?.well_id],
        name: [
          this.data.channel?.name || this.channel?.name,
          [Validators.required],
        ],
        date_from: [
          this.formatDateForInput(
            this.data.channel?.date_from || this.channel?.date_from || null
          ),
        ],
        date_to: [
          this.formatDateForInput(
            this.data.channel?.date_to || this.channel?.date_to || null
          ),
        ],
      },
      { validators: this.dateOrderValidator }
    );

    // If editing, populate form with channel data
    if (this.channel) {
      this.channelForm.patchValue({
        name: this.channel.name,
        date_from: this.formatDateForInput(this.channel.date_from),
        date_to: this.formatDateForInput(this.channel.date_to),
      });
    }
  }

  // Custom validator to ensure date_to is after date_from
  dateOrderValidator(control: AbstractControl): ValidationErrors | null {
    const date_from = control.get('date_from')?.value;
    const date_to = control.get('date_to')?.value;

    if (date_from && date_to && new Date(date_from) > new Date(date_to)) {
      control.get('date_to')?.setErrors({ dateOrder: true });
      return { dateOrder: true };
    }

    // Clear the error if it's been fixed
    if (control.get('date_to')?.hasError('dateOrder')) {
      control.get('date_to')?.setErrors(null);
    }

    return null;
  }

  // Format date to YYYY-MM-DD for the date input
  formatDateForInput(date: Date | null): string | null {
    if (!date) {
      return null;
    }

    const d = new Date(date);
    const year = d.getFullYear();
    const month = (d.getMonth() + 1).toString().padStart(2, '0');
    const day = d.getDate().toString().padStart(2, '0');

    return `${year}-${month}-${day}`;
  }

  // Get form controls for easier access in the template
  get f() {
    return this.channelForm.controls;
  }

  // Form submission
  onSubmit(): void {
    if (this.channelForm.invalid) {
      // Mark all fields as touched to trigger validation messages
      Object.keys(this.channelForm.controls).forEach((key) => {
        const control = this.channelForm.get(key);
        control?.markAsTouched();
      });
      return;
    }

    this.formError = null;

    // Create a channel object from form values
    const formValues = this.channelForm.value;
    const channelData: Partial<Channel> = {
      name: formValues.name,
    };

    // Convert string dates to Date objects
    if (formValues.date_from) {
      channelData.date_from = new Date(formValues.date_from);
    }

    if (formValues.date_to) {
      channelData.date_to = new Date(formValues.date_to);
    }

    channelData.well_id = this.data.well_id;

    if (this.channel) {
      this.channelService
        .updateChannel(
          this.data.well_id,
          this.channel.id,
          channelData as Channel
        )
        .subscribe((channelData) => {
          if (channelData) {
            this.dialogRef.close();
          } else {
            this.formError = 'Failed to save channel data.';
          }
        });
    } else {
      this.channelService
        .createChannel(this.data.well_id, channelData as Channel)
        .subscribe((channelData) => {
          if (channelData) {
            this.dialogRef.close();
          } else {
            this.formError = 'Failed to save channel data.';
          }
        });
    }
  }

  // Cancel form
  onCancel(): void {
    this.dialogRef.close();
  }
}
