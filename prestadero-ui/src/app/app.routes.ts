import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MovimientosComponent } from './movimientos/movimientos';

export const routes: Routes = [
  { path: 'movimientos', component: MovimientosComponent },
  { path: '', redirectTo: 'movimientos', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
