import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Well } from './well.model';

const baseUrl = environment.apiUrl;

@Injectable({
  providedIn: 'root',
})
export class WellsService {
  #http = inject(HttpClient);

  getWells(): Observable<Well[]> {
    return this.#http
      .get<Well[]>(`${baseUrl}/wells`)
      .pipe(map((wells) => wells.map((w) => new Well(w))));
  }

  getWellById(id: number): Observable<Well | undefined> {
    return this.#http
      .get<Well>(`${baseUrl}/wells/${id}`)
      .pipe(map((well) => new Well(well) || undefined));
  }

  createWell(well: Partial<Well>): Observable<Well> {
    return this.#http.post<Well>(`${baseUrl}/wells`, well);
  }

  updateWell(id: number, well: Partial<Well>): Observable<Well> {
    return this.#http.put<Well>(`${baseUrl}/wells/${id}`, well);
  }

  deleteWell(id: number): Observable<void> {
    return this.#http.delete<void>(`${baseUrl}/wells/${id}`);
  }
}
