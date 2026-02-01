import pandas as pd


def limpiarMovimientos(df):
    print(df.isnull().sum())
    df = df.fillna(
        {
            "referencia": "N/A",
            "nombre_usuario_solicitante": "DESCONOCIDO",
            "tipo": "N/A",
        }
    )
    df = df.dropna(subset=["autorizacion", "importe", "tipo"])

    df["autorizacion"] = df["autorizacion"].astype(str)
    df["feoperacion"] = pd.to_datetime(df["feoperacion"], errors="coerce")
    df["femovimiento"] = pd.to_datetime(df["femovimiento"], errors="coerce")
    df["tipo"] = df["tipo"].astype(str)
    df["importe"] = pd.to_numeric(df["importe"], errors="coerce")
    df["estatus"] = df["estatus"].astype(str)
    df["referencia"] = df["referencia"].astype(str)
    df["idtipomovimiento"] = pd.to_numeric(
        df["idtipomovimiento"], errors="coerce"
    ).astype("Int64")

    df = df.dropna(subset=["importe", "feoperacion"])
    df = df.replace(r"^\s*$", None, regex=True)

    print(df.dtypes)

    df["femovimiento"] = df["femovimiento"].dt.date
    df["feoperacion"] = df["feoperacion"].dt.date

    #print(df.dtypes)

    df = df.where(pd.notnull(df), None)

    '''print(df["feoperacion"].isna().sum())
    print(df["femovimiento"].isna().sum())
    print("----------------------------------------------")
    print(df.head())
    print(df.dtypes)
    print(df.isna().sum())'''

    return df
