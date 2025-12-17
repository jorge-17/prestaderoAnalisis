import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MovimientosGrafica } from './movimientos-grafica';

describe('MovimientosGrafica', () => {
  let component: MovimientosGrafica;
  let fixture: ComponentFixture<MovimientosGrafica>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MovimientosGrafica]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MovimientosGrafica);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
