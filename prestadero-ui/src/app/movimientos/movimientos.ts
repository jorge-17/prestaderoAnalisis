import { Component, OnInit } from '@angular/core';
import { Movimiento, MovimientoService } from '../services/movimientos.service';
import { CommonModule } from '@angular/common';
import { MovimientosGraficaComponent } from '../movimientos-grafica/movimientos-grafica';

@Component({
  selector: 'app-movimientos',
  templateUrl: './movimientos.html',
  standalone: true,
  imports: [CommonModule, MovimientosGraficaComponent]
})
export class MovimientosComponent implements OnInit {

  movimientos: Movimiento[] = [];

  constructor(private movimientoService: MovimientoService) {}

  ngOnInit(): void {    

    this.movimientoService.listar().subscribe({
      next: data => {
        console.log('MOVIMIENTOS:', data);
        this.movimientos = data;
      },
      error: err => {
        console.error(err);
      }
    });
  }
}
