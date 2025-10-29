# save_as_comma_csv.py
import pandas as pd

df = pd.read_csv("calair_tiemporeal.csv", sep=";", dtype=str)  # leer todo como texto
# Asegurar padding de MES y DIA: convertir a int y formatear con 2 dígitos si existen
if 'MES' in df.columns:
    df['MES'] = df['MES'].str.zfill(2)
if 'DIA' in df.columns:
    df['DIA'] = df['DIA'].str.zfill(2)

# (Opcional) quitar espacios alrededor de nombres de columna/valores
df.columns = df.columns.str.strip()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

df.to_csv("calair_tiemporeal_comma.csv", index=False)
print("CSV convertido: data/calair_tiemporeal_comma.csv")
