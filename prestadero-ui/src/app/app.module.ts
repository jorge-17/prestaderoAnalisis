import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    CommonModule
  ]
})
export class AppModule {}
