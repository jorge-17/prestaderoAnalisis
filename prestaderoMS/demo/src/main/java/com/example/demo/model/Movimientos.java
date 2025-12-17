package com.example.demo.model;

import jakarta.persistence.*;

import java.sql.Timestamp;
import java.util.Date;

@Entity
@Table(name = "movimientos")
public class Movimientos {

    @Id
    @Column(name = "autorizacion")
    private String Autorizacion;
    private Timestamp Feoperacion;
    private String Tipo;
    private Double Importe;
    private String Estatus;
    private String Referencia;
    private Integer Idtipomovimiento;
    private String Nombre_usuario_solicitante;


    public Movimientos() {}
    public Movimientos(String Autorizacion, Timestamp FeOperacion, String Tipo, Double Importe, String Estatus, String Referencia, Integer Idtipomovimiento, String Nombre_usuario_solicitante) {
            this.Autorizacion = Autorizacion;
            this.Feoperacion = FeOperacion;
            this.Tipo = Tipo;
            this.Importe = Importe;
            this.Estatus = Estatus;
            this.Referencia = Referencia;
            this.Idtipomovimiento = Idtipomovimiento;
            this.Nombre_usuario_solicitante = Nombre_usuario_solicitante;
        }

    public String getAutorizacion() {
        return Autorizacion;
    }

    public void setAutorizacion(String autorizacion) {
        Autorizacion = autorizacion;
    }

    public Date getFeOperacion() {
        return Feoperacion;
    }

    public void setFeOperacion(Timestamp feOperacion) {
        Feoperacion = feOperacion;
    }

    public String getTipo() {
        return Tipo;
    }

    public void setTipo(String tipo) {
        Tipo = tipo;
    }

    public Double getImporte() {
        return Importe;
    }

    public void setImporte(Double importe) {
        Importe = importe;
    }

    public String getEstatus() {
        return Estatus;
    }

    public void setEstatus(String estatus) {
        Estatus = estatus;
    }

    public String getReferencia() {
        return Referencia;
    }

    public void setReferencia(String referencia) {
        Referencia = referencia;
    }

    public Integer getIdtipomovimiento() {
        return Idtipomovimiento;
    }

    public void setIdtipomovimiento(Integer Idtipomovimiento) {
        Idtipomovimiento = Idtipomovimiento;
    }

    public String getNombre_usuario_solicitante() {
        return Nombre_usuario_solicitante;
    }

    public void setNombre_usuario_solicitante(String Nombre_usuario_solicitante) {
        Nombre_usuario_solicitante = Nombre_usuario_solicitante;
    }
}
