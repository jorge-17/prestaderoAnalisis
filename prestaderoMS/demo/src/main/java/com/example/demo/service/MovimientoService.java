package com.example.demo.service;

import com.example.demo.model.Movimiento;
import com.example.demo.repository.MovimientoRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MovimientoService {

    private final MovimientoRepository repo;

    public MovimientoService(MovimientoRepository repo) {
        this.repo = repo;
    }

    public List<Movimiento> listar() {
        return repo.findAll();
    }

    /* Por el momento no se podran guardar movimientos nuevos desde el front
    public Movimiento guardar(Movimiento u) {
        return repo.save(u);
    }*/
}
