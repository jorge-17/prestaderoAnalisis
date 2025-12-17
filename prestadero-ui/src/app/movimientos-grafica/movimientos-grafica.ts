import { Component, Input, ViewChild, ElementRef, AfterViewInit, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Chart, registerables } from 'chart.js';
import { Movimiento } from '../services/movimientos.service';

Chart.register(...registerables);

@Component({
  selector: 'app-movimientos-grafica',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './movimientos-grafica.html'
})
export class MovimientosGraficaComponent implements AfterViewInit, OnChanges {

  @Input() movimientos: Movimiento[] = [];
  @ViewChild('chartCanvas') canvas!: ElementRef<HTMLCanvasElement>;

  chart?: Chart;
  viewReady = false;

  ngAfterViewInit() {
    this.viewReady = true;
    this.tryRender();
  }

  ngOnChanges() {
    this.tryRender();
  }

  tryRender() {
    if (!this.viewReady || !this.movimientos.length) return;

    if (this.chart) this.chart.destroy();

    this.chart = new Chart(this.canvas.nativeElement, {
      type: 'bar',
      data: {
        labels: this.movimientos.map(m => String(m.autorizacion)),
        datasets: [{
          label: 'Importe',
          data: this.movimientos.map(m => m.importe),
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }
}

