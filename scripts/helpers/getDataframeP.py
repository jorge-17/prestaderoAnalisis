import pandas as pd
from sqlalchemy import create_engine
from helpers.tools import limpiarMovimientos

def getObjectQuery(objeto):
    if objeto == 'get.TipoMovimientos':
        return "(select * from prestadero.tipomovimientos)"
    elif objeto == 'get.TipoMovimientos.tipomovimiento':
        return "(select tm.tipomovimiento from prestadero.tipomovimientos tm)"
    elif objeto == 'get.Movimientos.main':
        return "(select mov.autorizacion, date_trunc('month', mov.feoperacion) as feoperacion, mov.feoperacion as fereal, mov.tipo, mov.importe, mov.nombre_usuario_solicitante, t.tipomovimiento from postgres.prestadero.movimientos mov left join prestadero.tipomovimientos t on mov.idtipomovimiento = t.idtipomovimiento)"
    elif objeto == 'put.Movimientos':
        return "movimientos"
    else:
        return None

def getDataframeBD(userIn, passIn, objeto):
    query = getObjectQuery(objeto)

    if not query:
        raise ValueError(f"Objeto no reconocido: {objeto}")

    engine = create_engine(
        f"postgresql+psycopg2://{userIn}:{passIn}@localhost:5432/prestaderodb"
    )

    try:
        df = pd.read_sql(query, engine)
        print(f"Se consultó el objeto: {objeto}")
        return df

    except Exception as inst:
        print("Error al consultar BD")
        print(type(inst))
        print(inst)
        raise

def putDataframeDB(userIn, passIn, objeto, df):
    table = getObjectQuery(objeto)

    if not table:
        raise ValueError(f"Objeto no reconocido: {objeto}")

    engine = create_engine(
        f"postgresql+psycopg2://{userIn}:{passIn}@localhost:5432/prestaderodb"
    )

    try:
        df = limpiarMovimientos(df)
        
        with engine.begin() as conn:
            df.to_sql(
                table,
                conn,
                schema='prestadero',
                if_exists='append',
                index=False,
                method='multi'
            )
        print("Se almacenó exitosamente en base de datos")

    except Exception as inst:
        print("Error al insertar en BD")
        print(type(inst))
        print(inst)
        raise