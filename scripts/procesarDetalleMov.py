def procesarDetalleMov(aut,arrDetalle):
    arrDetalleNuevo = []
    for i in arrDetalle:
        dictAuto = dict(("autorizacion", aut))
        dictCon = dict(("concepto", i.split(':')[0]))
        dcitMon = dict(("monto", i.split(':')[1]))
        arrDetalleNuevo.append([dictAuto,dictCon,dcitMon])

    dictDetalleNuevo = dict(arrDetalleNuevo)
    return dictDetalleNuevo

procesarDetalleMov(103124028,["Principal: 0.0000", "Interes: 0.0000", "Impuesto Interes:  0.0000", "Moratorios: 0.0028",  "Impuesto Moratorios: 0.0004", "IVA Comisión Moratorios:  0.00000"])