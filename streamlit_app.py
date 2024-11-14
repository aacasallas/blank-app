import streamlit as st

#st.title("🎈 My new app")
#st.write(
    #"Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

from google.colab import drive
drive.mount('/content/drive')

#Conexion base de datos
conexion =sqlite3.connect('/content/drive/MyDrive/Analisis/Proyecto_Analisis/Prueba4.db')
cursor= conexion.cursor()
df_original=pd.read_sql("""SELECT * FROM LlamadasEmergencia limit 11;""",conexion)

#backup dataframe original
df_aux=df_original.copy()
df_aux

df_limpieza=pd.read_sql("""
SELECT Le.FECHA_INICIO_DESPLAZAMIENTO_MOVIL, Le.EDAD, Le.PRIORIDAD,
Le.CLASIFICACION_FINAL, Le.TIPO_INCIDENTE, Ge.Descripcion as GENERO,
 Lo.Descripcion as LOCALIDAD, Re.Descripcion as RED
FROM LlamadasEmergencia AS LE
INNER JOIN Genero as Ge ON LE.Id_Genero=Ge.id
INNER JOIN Red AS RE ON LE.Id_Red = Re.id
INNER JOIN Localidad AS Lo ON LE.Id_Localidad=Lo.id
WHERE
Ge.Descripcion in ('Femenino','Masculino')AND
Le.EDAD BETWEEN 6 and 100 AND
Le.prioridad in ('Alta','Baja','Media') AND
le.CLASIFICACION_FINAL NOT NULL AND
TIPO_INCIDENTE  NOT NULL
 """,conexion)
df_limpieza


df_ejercicio=df_limpieza.copy()

# traer los registros donde la clasificacion final es cancelado
#df_aux=df_ejercicio[df_ejercicio['CLASIFICACION_FINAL']=='Traslado'].count()
# total_traslados = df_ejercicio[df_ejercicio['CLASIFICACION_FINAL']=='Traslado'].shape[0]
# df_total_traslado = pd.DataFrame({'Total Traslados': [total_traslados]})

# total_desistimiento= df_ejercicio[df_ejercicio['CLASIFICACION_FINAL']=='Desistimiento'].shape[0]
# df_total_desistimiento = pd.DataFrame({'Total Traslados': [total_desistimiento]})

# total_Fallecido = df_ejercicio[df_ejercicio['CLASIFICACION_FINAL']=='Fallecido'].shape[0]
# df_total_Fallecido = pd.DataFrame({'Total Traslados': [total_Fallecido]})

# total_Cancelado = df_ejercicio[df_ejercicio['CLASIFICACION_FINAL']=='Cancelado'].shape[0]
# df_total_Cancelado = pd.DataFrame({'Total Traslados': [total_Cancelado]})

# print(f"Traslados  {total_traslados}")
# print(f"Desistimiento  {total_desistimiento}")
# print(f"Fallecido  {total_Fallecido}")
# print(f"Cancelado  {total_Cancelado}")

clasificacion_final_counts = df_ejercicio['CLASIFICACION_FINAL'].value_counts().to_dict()
data = {'Clasificación': list(clasificacion_final_counts.keys()),
        'Total': list(clasificacion_final_counts.values())}
df_clasificaciones = pd.DataFrame(data)
print(df_clasificaciones)

# Crear el gráfico de barras
sns.barplot(x="Clasificación", y="Total", data=df_clasificaciones)

# Añadir etiquetas y título (opcional)
plt.xlabel("Clasificación")
plt.ylabel("Total")
plt.title("Total de Llamadas por Clasificación")

# Rotar las etiquetas del eje x
plt.xticks(rotation=45, ha='right')

# Mostrar el gráfico
plt.show()
