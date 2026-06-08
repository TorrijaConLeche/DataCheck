import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UploadService {

  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  subirCSV(file: File) {
    const formData = new FormData();
    formData.append('archivo', file);

    return this.http.post(`${this.apiUrl}/datasets/subir`, formData);
  }
}

