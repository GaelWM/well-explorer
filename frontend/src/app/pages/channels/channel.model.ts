export class Channel {
  id: number;
  well_id: number;
  name: string;
  date_from: Date | null = null;
  date_to: Date | null = null;
  created_at?: Date;
  updated_at?: Date;

  constructor(model: Partial<Channel>) {
    this.id = model.id || 0;
    this.well_id = model.well_id!;
    this.name = model.name || '';
    this.date_from = model.date_from || null;
    this.date_to = model.date_to || null;
    this.created_at = model.created_at;
    this.updated_at = model.updated_at;
  }
}

export type ChannelData = {
  time: number | string;
  value: number;
};
