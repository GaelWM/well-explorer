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

  getChannels(wellId: number): Observable<Channel[]> {
    return this.#http.get<Channel[]>(`/api/wells/${wellId}/channels`);
  }

  getChannelById(wellId: number, id: number): Observable<Channel | undefined> {
    return this.#http
      .get<Channel>(`${baseUrl}/api/wells/${wellId}/channels/${id}`)
      .pipe(map((channel) => channel || undefined));
  }

  getChannelData(wellId: number, id: number): Observable<ChannelData[]> {
    return this.#http.get<ChannelData[]>(
      `${baseUrl}/api/wells/${wellId}/channels/${id}/data`
    );
  }

  createChannel(
    wellId: number,
    channel: Partial<Channel>
  ): Observable<Channel> {
    return this.#http.post<Channel>(
      `${baseUrl}/api/wells/${wellId}/channels`,
      channel
    );
  }

  updateChannel(
    wellId: number,
    id: number,
    channel: Partial<Channel>
  ): Observable<Channel> {
    return this.#http.put<Channel>(
      `${baseUrl}/api/wells/${wellId}/channels/${id}`,
      channel
    );
  }

  deleteChannel(wellId: number, id: number): Observable<void> {
    return this.#http.delete<void>(
      `${baseUrl}/api/wells/${wellId}/channels/${id}`
    );
  }
}
