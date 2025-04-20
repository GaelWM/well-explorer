export class Well {
  id: number;
  name: string;
  lift_type: LiftType;
  region: string;
  latitude: number;
  longitude: number;
  installation_date?: string;
  depth: number;
  status: WellStatus;
  created_at?: Date;
  updated_at?: Date;

  constructor(model: Partial<Well>) {
    this.id = model.id || 0;
    this.name = model.name || '';
    this.lift_type = model.lift_type || LiftType.NF;
    this.region = model.region || '';
    this.latitude = model.latitude || 0;
    this.longitude = model.longitude || 0;
    this.installation_date = model.installation_date;
    this.depth = model.depth || 0;
    this.status = model.status || WellStatus.ACTIVE;
    this.created_at = model.created_at;
    this.updated_at = model.updated_at;
  }
}

export enum LiftType {
  NF = 'NF',
  GL = 'GL',
  ESP = 'ESP',
}

export const liftTypeOptions = [
  { value: LiftType.NF, label: 'Natural Flow' },
  { value: LiftType.GL, label: 'Gas Lift' },
  { value: LiftType.ESP, label: 'Electrical Submersible Pump' },
];

export enum WellStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  ABANDONED = 'abandoned',
}

export const wellStatusOptions = [
  { value: WellStatus.ACTIVE, label: 'Active' },
  { value: WellStatus.INACTIVE, label: 'Inactive' },
  { value: WellStatus.ABANDONED, label: 'Abandoned' },
];
