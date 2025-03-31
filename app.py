import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests 

def post_spark_job(user, repo, job, token, codeurl, dataseturl):
    url = f'https://api.github.com/repos/{user}/{repo}/dispatches'
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"  
    }
    
    payload = {
        "event_type": job,
        "client_payload": {
            "codeurl": codeurl,
            "dataseturl": dataseturl
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 204:
        st.success("✅ Workflow disparado correctamente!")
    else:
        st.error(f"❌ Error al disparar el workflow: {response.status_code}")
        try:
            st.write(response.json())
        except ValueError:
            st.write(response.text)

st.header("spark-submit Job")

col1, col2 = st.columns(2)

with col1:
    github_user  = st.text_input('Github user', value='Iker186')
    github_repo  = st.text_input('Github repo', value='analisis_datos')
    spark_job    = st.text_input('Spark job', value='spark')

with col2:
    github_token = st.text_input('Github token', value='', type="password")  
    code_url     = st.text_input('Code URL', value='https://raw.githubusercontent.com/Iker186/analisis_datos/main/spark_process.py')
    dataset_url  = st.text_input('Dataset URL', value='https://raw.githubusercontent.com/Iker186/analisis_datos/main/data/social_media.csv')

if st.button("POST spark submit"):
   post_spark_job(github_user, github_repo, spark_job, github_token, code_url, dataset_url)


def get_spark_results(url_results):
    if not url_results:
        st.error("❌ URL de resultados no proporcionada.")
        return
    
    response = requests.get(url_results)
    
    if response.status_code == 200:
        try:
            st.write(response.json())
        except ValueError:
            st.write(response.text)
    else:
        st.error(f"❌ Error al obtener resultados: {response.status_code}")
