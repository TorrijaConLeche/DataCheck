import { Routes } from '@angular/router';

import { HomePage } from './pages/home/home';
import { UploadPage } from './pages/upload/upload';
import { ConfirmPage } from './pages/confirm/confirm';
import { AnalyzePage } from './pages/analyze/analyze';
import { ResultsPage } from './pages/results/results';

export const routes: Routes = [
  { path: '',           component: HomePage },
  { path: 'subir',      component: UploadPage },
  { path: 'confirmar',  component: ConfirmPage },
  { path: 'analizar',   component: AnalyzePage },
  { path: 'resultados', component: ResultsPage },
  { path: '**',         redirectTo: '' },
];
