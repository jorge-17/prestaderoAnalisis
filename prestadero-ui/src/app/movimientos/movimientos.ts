import { Component, OnInit } from '@angular/core';
import { Movimiento, MovimientoService } from '../services/movimientos.service';
import { BrowserModule } from "@angular/platform-browser";

@Component({
  selector: 'app-movimientos',
  templateUrl: './movimientos.html',
  imports: [BrowserModule]
})
export class MovimientosComponent implements OnInit {

  movimientos: Movimiento[] = [];
  cargando = true;

  constructor(private movimientoService: MovimientoService) {}

  ngOnInit(): void {
    this.movimientoService.listar().subscribe({
      next: data => {
        this.movimientos = data;
        this.cargando = false;
      },
      error: err => {
        console.error(err);
        this.cargando = false;
      }
    });
  }
}
