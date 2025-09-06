create table prestadero.detallemovimiento
(
    autorizacion integer not null,
    concepto     varchar(100),
    monto        double precision
);

alter table prestadero.detallemovimiento
    owner to jrodarte;

