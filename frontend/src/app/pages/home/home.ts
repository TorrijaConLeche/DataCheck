import { Component } from '@angular/core';

import { UploadService } from '../../core/services/upload.service';
import { DatasetInfo } from '../../models/dataset-info';

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomePage {
  resultado: DatasetInfo | null = null;

  constructor(private uploadService: UploadService) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) {
      return;
    }

    this.uploadService.subirCSV(file).subscribe(res => {
      this.resultado = res;
      console.log(res);
    });
  }
}
