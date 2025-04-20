// channel-form.component.ts
import { CommonModule } from '@angular/common';
import {
  Component,
  EventEmitter,
  inject,
  Input,
  OnInit,
  Output,
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

@Component({
  selector: 'app-channel-form',
  templateUrl: './channel-form.component.html',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  styleUrls: ['./channel-form.component.css'],
})
export class ChannelFormComponent implements OnInit {
  readonly dialogRef = inject(MatDialogRef);

  @Input() channel: Channel | null = null;
  @Output() saveChannel = new EventEmitter<Partial<Channel>>();
  @Output() cancel = new EventEmitter<void>();

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
        name: [this.channel?.name || '', [Validators.required]],
        dateFrom: [this.formatDateForInput(this.channel?.dateFrom || null)],
        dateTo: [this.formatDateForInput(this.channel?.dateTo || null)],
      },
      { validators: this.dateOrderValidator }
    );

    // If editing, populate form with channel data
    if (this.channel) {
      this.channelForm.patchValue({
        name: this.channel.name,
        dateFrom: this.formatDateForInput(this.channel.dateFrom),
        dateTo: this.formatDateForInput(this.channel.dateTo),
      });
    }
  }

  // Custom validator to ensure dateTo is after dateFrom
  dateOrderValidator(control: AbstractControl): ValidationErrors | null {
    const dateFrom = control.get('dateFrom')?.value;
    const dateTo = control.get('dateTo')?.value;

    if (dateFrom && dateTo && new Date(dateFrom) > new Date(dateTo)) {
      control.get('dateTo')?.setErrors({ dateOrder: true });
      return { dateOrder: true };
    }

    // Clear the error if it's been fixed
    if (control.get('dateTo')?.hasError('dateOrder')) {
      control.get('dateTo')?.setErrors(null);
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
    if (formValues.dateFrom) {
      channelData.dateFrom = new Date(formValues.dateFrom);
    }

    if (formValues.dateTo) {
      channelData.dateTo = new Date(formValues.dateTo);
    }

    // Emit the channel data to parent component
    this.saveChannel.emit(channelData);
  }

  // Cancel form
  onCancel(): void {
    this.dialogRef.close();
    this.cancel.emit();
  }
}
