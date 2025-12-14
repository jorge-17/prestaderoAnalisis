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
    private Timestamp FeOperacion;
    private String Tipo;
    private Double Importe;
    private String Estatus;
    private String Referencia;
    private Integer IdTipoMovimiento;
    private String NombreSolicitante;


    public Movimientos() {}
    public Movimientos(String Autorizacion, Timestamp FeOperacion, String Tipo, Double Importe, String Estatus, String Referencia, Integer IdTipoMovimiento, String NombreSolicitante) {
            this.Autorizacion = Autorizacion;
            this.FeOperacion = FeOperacion;
            this.Tipo = Tipo;
            this.Importe = Importe;
            this.Estatus = Estatus;
            this.Referencia = Referencia;
            this.IdTipoMovimiento = IdTipoMovimiento;
            this.NombreSolicitante = NombreSolicitante;
        }

    public String getAutorizacion() {
        return Autorizacion;
    }

    public void setAutorizacion(String autorizacion) {
        Autorizacion = autorizacion;
    }

    public Date getFeOperacion() {
        return FeOperacion;
    }

    public void setFeOperacion(Timestamp feOperacion) {
        FeOperacion = feOperacion;
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

    public Integer getIdTipoMovimiento() {
        return IdTipoMovimiento;
    }

    public void setIdTipoMovimiento(Integer idTipoMovimiento) {
        IdTipoMovimiento = idTipoMovimiento;
    }

    public String getNombreSolicitante() {
        return NombreSolicitante;
    }

    public void setNombreSolicitante(String nombreSolicitante) {
        NombreSolicitante = nombreSolicitante;
    }
}
