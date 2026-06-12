import { Component, computed, signal } from '@angular/core';

import { UploadService } from '../../core/services/upload.service';
import { RulesService } from '../../core/services/rules.service';
import { DatasetInfo } from '../../models/dataset-info';
import { FeatureConstraints, RulesPayload } from '../../models/rules';

interface RestriccionEdit {
  minTexto: string;
  maxTexto: string;
  allowedValuesTexto: string;
  regex: string;
  notNull: boolean;
}

const RESTRICCION_VACIA: RestriccionEdit = {
  minTexto: '',
  maxTexto: '',
  allowedValuesTexto: '',
  regex: '',
  notNull: false,
};

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomePage {

  datasetInfo = signal<DatasetInfo | null>(null);
  errorSubida = signal<string | null>(null);

  targetColumn = signal<string>('');
  restricciones = signal<Map<string, RestriccionEdit>>(new Map());
  columnaParaRestriccion = signal<string>('');

  feedbackExito = signal<string | null>(null);
  feedbackError = signal<string[] | null>(null);
  enviando = signal<boolean>(false);

  seccionSubirAbierta = signal<boolean>(true);
  seccionInfoAbierta = signal<boolean>(false);
  seccionConfigAbierta = signal<boolean>(false);

  columnasDisponibles = computed(() => this.datasetInfo()?.columns_info ?? []);
  columnasRestriccion = computed(() =>
    this.columnasDisponibles().filter(c => c.name !== this.targetColumn())
  );
  columnasConRestriccion = computed(() => Array.from(this.restricciones().keys()));
  targetDtype = computed(() => {
    const target = this.targetColumn();
    return this.columnasDisponibles().find(c => c.name === target)?.dtype ?? '';
  });

  constructor(
    private uploadService: UploadService,
    private rulesService: RulesService
  ) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) {
      return;
    }

    this.errorSubida.set(null);
    this.feedbackExito.set(null);
    this.feedbackError.set(null);

    this.uploadService.subirCSV(file).subscribe({
      next: info => {
        this.datasetInfo.set(info);
        this.targetColumn.set('');
        this.restricciones.set(new Map());
        this.columnaParaRestriccion.set('');
        this.seccionSubirAbierta.set(false);
        this.seccionInfoAbierta.set(true);
        this.seccionConfigAbierta.set(true);
      },
      error: err => {
        const detail = err?.error?.detail ?? err?.error?.message ?? 'No se pudo subir el archivo';
        this.errorSubida.set(detail);
      }
    });
  }

  onTargetChange(value: string): void {
    this.targetColumn.set(value);
    const nuevas = new Map(this.restricciones());
    if (nuevas.has(value)) {
      nuevas.delete(value);
    }
    this.restricciones.set(nuevas);
    if (this.columnaParaRestriccion() === value) {
      this.columnaParaRestriccion.set('');
    }
  }

  onColumnaRestriccionChange(value: string): void {
    this.columnaParaRestriccion.set(value);
  }

  toggleSeccion(seccion: 'subir' | 'info' | 'config'): void {
    if (seccion === 'subir') {
      this.seccionSubirAbierta.update(v => !v);
    } else if (seccion === 'info') {
      this.seccionInfoAbierta.update(v => !v);
    } else {
      this.seccionConfigAbierta.update(v => !v);
    }
  }

  agregarRestriccion(): void {
    const col = this.columnaParaRestriccion();
    if (!col || this.restricciones().has(col)) {
      return;
    }
    const nuevas = new Map(this.restricciones());
    nuevas.set(col, { ...RESTRICCION_VACIA });
    this.restricciones.set(nuevas);
    this.columnaParaRestriccion.set('');
  }

  quitarRestriccion(col: string): void {
    const nuevas = new Map(this.restricciones());
    nuevas.delete(col);
    this.restricciones.set(nuevas);
  }

  actualizarRestriccion(col: string, cambios: Partial<RestriccionEdit>): void {
    const actuales = this.restricciones();
    const edicion = actuales.get(col);
    if (!edicion) {
      return;
    }
    const nuevas = new Map(actuales);
    nuevas.set(col, { ...edicion, ...cambios });
    this.restricciones.set(nuevas);
  }

  parsearNumerico(texto: string): number | null {
    if (texto === '' || texto === null) {
      return null;
    }
    const n = Number(texto);
    return Number.isNaN(n) ? null : n;
  }

  parsearAllowedValues(texto: string): (string | number)[] | null {
    const partes = texto
      .split(',')
      .map(p => p.trim())
      .filter(p => p !== '');
    if (partes.length === 0) {
      return null;
    }
    return partes.map(p => {
      const n = Number(p);
      return Number.isNaN(n) ? p : n;
    });
  }

  construirPayload(): RulesPayload | null {
    const info = this.datasetInfo();
    if (!info) {
      return null;
    }
    const target = this.targetColumn();
    if (!target) {
      return null;
    }

    const constraints: Record<string, FeatureConstraints> = {};
    for (const [col, ed] of this.restricciones().entries()) {
      const allowed = this.parsearAllowedValues(ed.allowedValuesTexto);
      const min = this.parsearNumerico(ed.minTexto);
      const max = this.parsearNumerico(ed.maxTexto);
      const regex = ed.regex.trim() === '' ? null : ed.regex;

      const fc: FeatureConstraints = {
        min: min,
        max: max,
        allowed_values: allowed,
        regex: regex,
        not_null: ed.notNull,
      };
      constraints[col] = fc;
    }

    return { target_column: target, constraints };
  }

  guardarConfiguracion(): void {
    const info = this.datasetInfo();
    if (!info) {
      return;
    }
    const payload = this.construirPayload();
    if (!payload) {
      this.feedbackError.set(['Debes seleccionar una columna objetivo']);
      this.feedbackExito.set(null);
      return;
    }

    this.enviando.set(true);
    this.feedbackError.set(null);
    this.feedbackExito.set(null);

    this.rulesService.configurarReglas(info.dataset_id, payload).subscribe({
      next: resp => {
        this.enviando.set(false);
        if (resp.status === 'configured') {
          this.feedbackExito.set('Configuración guardada correctamente');
          this.feedbackError.set(null);
        } else {
          this.feedbackError.set(resp.errors ?? ['Error desconocido']);
          this.feedbackExito.set(null);
        }
      },
      error: err => {
        this.enviando.set(false);
        const detail = err?.error?.errors ?? err?.error?.detail ?? err?.error?.message ?? 'No se pudo guardar la configuración';
        this.feedbackError.set(Array.isArray(detail) ? detail : [String(detail)]);
        this.feedbackExito.set(null);
      }
    });
  }
}
