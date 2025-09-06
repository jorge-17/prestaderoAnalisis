create table prestadero.tipomovimientos
(
    idtipomovimiento integer generated always as identity (maxvalue 99)
        constraint tipomovimientos_pk
            primary key,
    tipomovimiento   varchar not null
);

alter table prestadero.tipomovimientos
    owner to jrodarte;

