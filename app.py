import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests  # <--- Falta importar requests

def post_spark_job(user, repo, job, token, codeurl, dataseturl):
    # Define la URL del endpoint
    url = f'https://api.github.com/repos/{user}/{repo}/dispatches'
    
    # Define los headers para la autenticación
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"  # Autenticación aquí
    }
    
    # Define el payload para el evento
    payload = {
        "event_type": job,
        "client_payload": {
            "codeurl": codeurl,
            "dataseturl": dataseturl
        }
    }
    
    # Enviar la solicitud POST
    response = requests.post(url, json=payload, headers=headers)
    
    # Verificar la respuesta
    if response.status_code == 204:
        st.success("✅ Workflow disparado correctamente!")
    else:
        st.error(f"❌ Error al disparar el workflow: {response.status_code}")
        st.write(response.json())
  
st.header("spark-submit Job")

github_user  =  st.text_input('Github user', value='Iker186')
github_repo  =  st.text_input('Github repo', value='analisis_datos')
spark_job    =  st.text_input('Spark job', value='spark')
github_token =  st.text_input('Github token', value='')
code_url     =  st.text_input('Code URL', value='https://raw.githubusercontent.com/Iker186/analisis_datos/main/spark_process.py')
dataset_url  =  st.text_input('Dataset URL', value='https://raw.githubusercontent.com/Iker186/analisis_datos/main/data/social_media.csv')

if st.button("POST spark submit"):
   post_spark_job(github_user, github_repo, spark_job, github_token, code_url, dataset_url)



def get_spark_results(url_results):
    response = requests.get(url_results)
    st.write(response)

    if  (response.status_code ==  200):
        st.write(response.json())


