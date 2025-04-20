export class Channel {
  id: number;
  wellId: number;
  name: string;
  dateFrom: Date | null = null;
  dateTo: Date | null = null;
  createdAt?: Date;
  updatedAt?: Date;

  constructor(model: Partial<Channel>) {
    this.id = model.id || 0;
    this.wellId = model.wellId!;
    this.name = model.name || '';
    this.dateFrom = model.dateFrom || null;
    this.dateTo = model.dateTo || null;
    this.createdAt = model.createdAt;
    this.updatedAt = model.updatedAt;
  }
}

export type ChannelData = {
  time: number | string;
  value: number;
};
