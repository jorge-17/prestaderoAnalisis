package com.example.demo.controller;

import com.example.demo.model.Movimientos;
import com.example.demo.service.MovimientoService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/movimientos")
@CrossOrigin(origins = "http://localhost:4200") // Para desarrollo. En producción limita orígenes.
public class MovimientoController {

    private final MovimientoService service;

    public MovimientoController(MovimientoService service) {
        this.service = service;
    }

    @GetMapping
    public List<Movimientos> listar() {
        return service.listar();
    }

    /*@PostMapping
    public Usuario guardar(@RequestBody Usuario usuario) {
        return service.guardar(usuario);
    }*/
}
