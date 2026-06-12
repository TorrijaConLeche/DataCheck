import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_URL } from '../api.config';
import { RulesPayload, RulesResponse } from '../../models/rules';

@Injectable({
  providedIn: 'root'
})
export class RulesService {

  constructor(private http: HttpClient) {}

  configurarReglas(datasetId: string, payload: RulesPayload): Observable<RulesResponse> {
    return this.http.post<RulesResponse>(
      `${API_URL}/datasets/${datasetId}/rules`,
      payload
    );
  }
}
