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

