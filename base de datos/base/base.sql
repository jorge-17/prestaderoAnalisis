create database postgres
    with owner postgres;

comment on database postgres is 'default administrative connection database';

grant connect, create, temporary on database postgres to jrodarte;

create sequence prestadero.movimiento;

alter sequence prestadero.movimiento owner to jrodarte;

create sequence prestadero."movimientosFK";

alter sequence prestadero."movimientosFK" owner to jrodarte;

create sequence prestadero."movimientoFK";

alter sequence prestadero."movimientoFK" owner to jrodarte;

create sequence prestadero."movFK";

alter sequence prestadero."movFK" owner to jrodarte;

create table prestadero.usuario
(
    claveusuario  integer not null,
    nombreusuario varchar not null,
    codigousuario varchar not null
);

alter table prestadero.usuario
    owner to jrodarte;

create table prestadero.tipomovimientos
(
    idtipomovimiento integer generated always as identity (maxvalue 99)
        constraint tipomovimientos_pk
            primary key,
    tipomovimiento   varchar not null
);

alter table prestadero.tipomovimientos
    owner to jrodarte;

create table prestadero.detallemovimiento
(
    autorizacion integer not null,
    concepto     varchar(100),
    monto        double precision
);

alter table prestadero.detallemovimiento
    owner to jrodarte;

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

create table prestadero.prestamos
(
    usuario_inversionista      integer          not null,
    monto_fondeado             double precision not null,
    plazo_meses                integer          not null,
    tasa_anual                 double precision,
    calificacion               varchar(5)       not null,
    estatus                    varchar(50)      not null,
    detalle_estatus            varchar(50)      not null,
    sub_estatus                varchar(50),
    ingreso_mensual            double precision not null,
    gasto_mensual_total        double precision not null,
    ocupacion                  varchar(100),
    nivel_de_estudios          varchar(50)      not null,
    fecha_liberado             date             not null,
    fecha_fondeo               date             not null,
    destino                    varchar(100)     not null,
    id_solicitud_de_credito    integer          not null,
    nombre_usuario_solicitante varchar(100)     not null,
    capital_pagado             double precision not null,
    interes_ordinario_pagado   double precision not null,
    iva_pagado_interes         double precision not null,
    moratorios_pagados         double precision not null,
    iva_moratorios_pagados     double precision not null,
    recuperacion               double precision not null,
    estado                     varchar(100)     not null,
    municipio                  varchar(50)      not null
);

alter table prestadero.prestamos
    owner to jrodarte;
