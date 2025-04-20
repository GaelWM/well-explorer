export class Well {
  id: number;
  name: string;
  liftType: LiftType;
  region: string;
  latitude: number;
  longitude: number;
  installationDate?: Date;
  depth: number;
  status: WellStatus;
  createdAt?: Date;
  updatedAt?: Date;

  constructor(model: Partial<Well>) {
    this.id = model.id || 0;
    this.name = model.name || '';
    this.liftType = model.liftType || LiftType.NF;
    this.region = model.region || '';
    this.latitude = model.latitude || 0;
    this.longitude = model.longitude || 0;
    this.installationDate = model.installationDate;
    this.depth = model.depth || 0;
    this.status = model.status || WellStatus.ACTIVE;
    this.createdAt = model.createdAt;
    this.updatedAt = model.updatedAt;
  }
}

export enum LiftType {
  NF = 'Natural Flow',
  GL = 'Gas Lift',
  ESP = 'Electrical Submersible Pump',
}

export const liftTypeOptions = [
  { value: LiftType.NF, label: 'Natural Flow' },
  { value: LiftType.GL, label: 'Gas Lift' },
  { value: LiftType.ESP, label: 'Electrical Submersible Pump' },
];

export enum WellStatus {
  ACTIVE = 'Active',
  INACTIVE = 'Inactive',
  ABANDONED = 'Abandoned',
}

export const wellStatusOptions = [
  { value: WellStatus.ACTIVE, label: 'Active' },
  { value: WellStatus.INACTIVE, label: 'Inactive' },
  { value: WellStatus.ABANDONED, label: 'Abandoned' },
];
