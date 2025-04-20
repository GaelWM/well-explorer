import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Channel, ChannelData } from './channel.model';

const baseUrl = environment.apiUrl;

@Injectable({
  providedIn: 'root',
})
export class ChannelsService {
  #http = inject(HttpClient);

  getChannels(well_id: number): Observable<Channel[]> {
    return this.#http.get<Channel[]>(`${baseUrl}/wells/${well_id}/channels`);
  }

  getChannelById(well_id: number, id: number): Observable<Channel | undefined> {
    return this.#http
      .get<Channel>(`${baseUrl}/wells/${well_id}/channels/${id}`)
      .pipe(map((channel) => channel || undefined));
  }

  getChannelData(well_id: number, id: number): Observable<ChannelData[]> {
    return this.#http.get<ChannelData[]>(
      `${baseUrl}/wells/${well_id}/channels/${id}/data`
    );
  }

  createChannel(
    well_id: number,
    channel: Partial<Channel>
  ): Observable<Channel> {
    return this.#http.post<Channel>(
      `${baseUrl}/wells/${well_id}/channels`,
      channel
    );
  }

  updateChannel(
    well_id: number,
    id: number,
    channel: Partial<Channel>
  ): Observable<Channel> {
    return this.#http.put<Channel>(
      `${baseUrl}/wells/${well_id}/channels/${id}`,
      channel
    );
  }

  deleteChannel(well_id: number, id: number): Observable<void> {
    return this.#http.delete<void>(
      `${baseUrl}/wells/${well_id}/channels/${id}`
    );
  }

  generateChannelData(
    well_id: number,
    id: number,
    channel: Partial<Channel>
  ): Observable<Channel> {
    return this.#http.post<Channel>(
      `${baseUrl}/wells/${well_id}/channels/${id}/generator/populate`,
      {
        well_id: well_id,
        channel_id: id,
        date_from: channel.date_from,
        date_to: channel.date_to,
      }
    );
  }
}
