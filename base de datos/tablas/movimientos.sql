create table prestadero.movimientos
(
    autorizacion               text,
    feoperacion                timestamp with time zone,
    tipo                       text,
    importe                    double precision,
    estatus                    text,
    referencia                 text,
    idtipomovimiento           integer,
    nombre_usuario_solicitante varchar(100)
);

alter table prestadero.movimientos
    owner to jrodarte;

