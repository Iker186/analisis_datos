import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# 📥 Cargar el dataset
data = pd.read_csv('./data/social_media.csv')

# 🎨 Estilizar el Dashboard
st.set_page_config(page_title="Dashboard de Redes Sociales", layout="wide")

# 🎯 Título Principal
st.title("📊 Dashboard de Análisis de Redes Sociales")

# 📚 Mostrar vista previa del dataset
st.sidebar.header("Opciones de Visualización")
if st.sidebar.checkbox("Mostrar Dataset Completo", False):
    st.write("Vista Completa del Dataset:")
    st.dataframe(data, height=400)

# 🎈 Agregar filtro por País
selected_country = st.sidebar.selectbox("🌍 Selecciona un País:", 
                                        options=["Todos"] + sorted(data["Country"].unique().tolist()))

if selected_country != "Todos":
    data = data[data["Country"] == selected_country]

# 📊 Mostrar resumen estadístico
st.sidebar.subheader("📈 Resumen de Datos")
st.sidebar.write(f"👥 Total de Usuarios: {len(data)}")
st.sidebar.write(f"🌍 Países Únicos: {data['Country'].nunique()}")
st.sidebar.write(f"🏙️ Ciudades Únicas: {data['City'].nunique()}")

# 📈 Gráfico de Top 10 Países
st.subheader("🌍 Top 10 Países Más Frecuentes")
top_countries = data["Country"].value_counts().head(10)

fig, ax = plt.subplots()
top_countries.plot(kind="bar", ax=ax, color="skyblue")
ax.set_xlabel("País")
ax.set_ylabel("Cantidad de Usuarios")
ax.set_title("Top 10 Países Más Frecuentes")

st.pyplot(fig)

# 📊 Distribución de Género
st.subheader("🧑‍🤝‍🧑 Distribución de Género")
gender_counts = data["Gender"].value_counts()

fig2, ax2 = plt.subplots()
gender_counts.plot(kind="pie", ax=ax2, autopct="%1.1f%%", startangle=90, colors=["#FF9999", "#66B3FF"])
ax2.set_ylabel("")  # Quitar etiqueta del eje Y
ax2.set_title("Distribución de Género")
st.pyplot(fig2)

# 📅 Visualización de Edad
st.subheader("🎂 Distribución de Edad")
data["DOB"] = pd.to_datetime(data["DOB"], errors="coerce")
data["Edad"] = pd.to_datetime("today").year - data["DOB"].dt.year
age_distribution = data["Edad"].dropna()

fig3 = px.histogram(age_distribution, nbins=30, title="Distribución de Edad de Usuarios", color_discrete_sequence=["#FFA07A"])
st.plotly_chart(fig3, use_container_width=True)

# 🎯 Análisis de Intereses
st.subheader("🎨 Análisis de Intereses")
top_interests = data["Interests"].value_counts().head(10)
fig4 = px.bar(top_interests, x=top_interests.index, y=top_interests.values, 
              labels={"x": "Intereses", "y": "Cantidad"}, color_discrete_sequence=["#6A5ACD"])
st.plotly_chart(fig4, use_container_width=True)

# 📢 Información adicional en el sidebar
st.sidebar.markdown("---")
st.sidebar.info("📢 Recuerda que puedes filtrar por país para obtener análisis específicos.")

# 🚀 Footer
st.markdown("---")
st.markdown("📊 **Dashboard interactivo construido con [Streamlit](https://streamlit.io/)** 🚀")

