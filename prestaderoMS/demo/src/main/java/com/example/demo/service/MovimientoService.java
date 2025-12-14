package com.example.demo.service;

import com.example.demo.model.Movimientos;
import com.example.demo.repository.MovimientoRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MovimientoService {

    private final MovimientoRepository repo;

    public MovimientoService(MovimientoRepository repo) {
        this.repo = repo;
    }

    public Page<Movimientos> listar(Pageable pageable) {
        return repo.findAll(pageable);
    }

    /* Por el momento no se podran guardar movimientos nuevos desde el front
    public Movimiento guardar(Movimiento u) {
        return repo.save(u);
    }*/
}
