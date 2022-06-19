
#import streamlit as st
#import pandas as pd
#import gdown
#
#id = 1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ
#@st.experimental_memo
#def download_data():
#  #https://drive.google.com/uc?id=
#  url = "https://drive.google.com/uc?id=1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ"
#  output= "data.csv"
#  gdown.download(url,output,quiet = False)
#  
#download_data()
#data = pd.read_csv("data.csv", sep = ";", parse_dates = ["FECHA_CORTE","FECHA_RESULTADO"])
#Simplificado = data.drop(columns = ["DISTRITO","FECHA_CORTE","FECHA_RESULTADO","UBIGEO","id_persona"])

import pandas as pd
import numpy as np
import streamlit as st
import gdown
import os

#Título
st.title('Casos positivos por COVID-19 en el Perú')
st.text("La información contenida en esta página web permite acceder al Dataset “Casos positivos por COVID-19” elaborado por el Ministerio de Salud (MINSA) del Perú. Este ha registrado el monitoreo diario de los casos positivos de covid-19 confirmados con cualquier tipo de prueba hasta el día 23 de mayo de 2022. Cada registro es equivalente a una persona, así como su sexo, edad y distintos niveles de ubicación geográfica: departamento, provincia y distrito. El Dataset original se encuentra en subido en la página oficial del gobierno del Perú (https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa.)")

#Carga del Dataset

# Lectura de datos desde CSV
#id = 1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ
if not os.path.exists('downloads'):
  os.makedirs('downloads')

@st.experimental_memo
def download_data():
  #https://drive.google.com/uc?id=
  url = "https://drive.google.com/uc?id=1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ"
  output = "downloads/data.csv"
  gdown.download(url,output,quiet = False)
  
download_data()
df = pd.read_csv("downloads/data.csv", sep = ";", parse_dates = ["FECHA_CORTE","FECHA_RESULTADO"])
# Simplificacion del dataset (retiro de columnas)
df = df.drop(columns = ["DISTRITO","FECHA_CORTE","FECHA_RESULTADO","UBIGEO","id_persona"])

#Código de filtros

#Construccion del set/list de departamentos (Valores unicos sin NA)
set_departamentos = np.sort(df['DEPARTAMENTO'].dropna().unique())
#Seleccion del departamento
opcion_departamento = st.selectbox('Selecciona un departamento', set_departamentos)
df_departamentos = df[df['DEPARTAMENTO'] == opcion_departamento]
num_filas = len(df_departamentos.axes[0]) 

#Construccion del set/list de provincias (Valores unicos sin NA)
set_provincias = np.sort(df_departamentos['PROVINCIA'].dropna().unique())
#Seleccion de la provincia
opcion_provincia = st.selectbox('Selecciona una provincia', set_provincias)
df_provincias = df_departamentos[df_departamentos['PROVINCIA'] == opcion_provincia]
num_filas = len(df_provincias.axes[0]) 

st.write('Numero de registros:', num_filas)

#Código de gráficos

#Generacion de los dataframe de frecuencias
df_sexo = df_provincias.SEXO.value_counts()
df_edad = df_provincias.EDAD.value_counts()
df_metodox = df_provincias.METODODX.value_counts()

#Ploteo de las frecuencias
st.bar_chart(df_sexo)
st.bar_chart(df_edad)
st.bar_chart(df_metodox)
