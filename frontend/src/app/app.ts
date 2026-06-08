import { Component} from '@angular/core';
import { UploadService } from './services/upload-service';

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  resultado: any;

  constructor(private uploadService: UploadService) {}

  onFileSelected(event: any) {
    const file: File = event.target.files[0];

    this.uploadService.subirCSV(file).subscribe(res => {
      this.resultado = res;
      console.log(res);
    });
  }
}
