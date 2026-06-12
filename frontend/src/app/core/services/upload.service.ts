import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_URL } from '../api.config';
import { DatasetInfo } from '../../models/dataset-info';

@Injectable({
  providedIn: 'root'
})
export class UploadService {

  constructor(private http: HttpClient) {}

  subirCSV(file: File): Observable<DatasetInfo> {
    const formData = new FormData();
    formData.append('archivo', file);

    return this.http.post<DatasetInfo>(`${API_URL}/datasets/subir`, formData);
  }
}
