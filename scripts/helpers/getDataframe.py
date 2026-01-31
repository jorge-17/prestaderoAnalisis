
def getObjectQuery(objeto):
    if objeto == 'get.TipoMovimientos':
        return "(select * from prestadero.tipomovimientos)"
    elif objeto == 'get.TipoMovimientos.tipomovimiento':
        return "(select tm.tipomovimiento from prestadero.tipomovimientos tm)"
    elif objeto == 'get.Movimientos.main':
        return "(select mov.autorizacion, date_trunc('month', mov.feoperacion) as feoperacion, mov.feoperacion as fereal, mov.tipo, mov.importe, mov.nombre_usuario_solicitante, t.tipomovimiento from postgres.prestadero.movimientos mov left join prestadero.tipomovimientos t on mov.idtipomovimiento = t.idtipomovimiento)"
    elif objeto == 'put.Movimientos':
        return "prestadero.movimientos"
    else:
        return None

def getDataframeBD(userIn, passIn, objeto, ss):
    objectQuery = getObjectQuery(objeto)

    try:
        df = ss.read.format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/prestaderodb") \
            .option("dbtable", objectQuery) \
            .option("user", userIn) \
            .option("password", passIn) \
            .option("driver", "org.postgresql.Driver") \
            .load()
        print(f"Se consultan el objeto: {objeto}")
    except Exception as inst:
        print(type(inst))    # the exception type
        print(inst.args)     # arguments stored in .args
        print(inst)   

    return df

def putDataframeDB(userIn, passIn, objeto, df):
    objectQuery = getObjectQuery(objeto)

    try:
        df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/prestaderodb") \
            .option("dbtable", objectQuery) \
            .option("user", userIn) \
            .option("password", passIn) \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
        print("Se almaceno exitosamente en base de datos")
    except Exception as inst:
        print(type(inst))    # the exception type
        print(inst.args)     # arguments stored in .args
        print(inst) 