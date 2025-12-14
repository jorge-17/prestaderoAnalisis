import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Movimiento {
  id: number;
  tipo: string;
  monto: number;
  fecha: string;
}

@Injectable({
  providedIn: 'root'
})
export class MovimientoService {

  private apiUrl = 'http://localhost:8080/api/movimientos';

  constructor(private http: HttpClient) {}

  listar(): Observable<Movimiento[]> {
    return this.http.get<Movimiento[]>(this.apiUrl);
  }
}
