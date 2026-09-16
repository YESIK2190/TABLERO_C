import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Validacion Operaciones',layout='wide')
st.title('Dashboard Comparativo de Operaciones')

base_file = st.file_uploader('BASE.xlsx', type=['xlsx'])
ventas_file = st.file_uploader('VALIDACION_VENTAS.xlsx', type=['xlsx'])
directas_file = st.file_uploader('VALIDACION_VENTAS_DIRECTAS.xlsx', type=['xlsx'])

if base_file and ventas_file and directas_file:
    base = pd.read_excel(base_file)
    ventas = pd.read_excel(ventas_file)
    directas = pd.read_excel(directas_file)

    total_base=len(base)
    total_ventas=len(ventas)
    total_directas=len(directas)

    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric('BASE',total_base)
    c2.metric('VENTAS',total_ventas)
    c3.metric('VENTAS DIRECTAS',total_directas)
    c4.metric('Dif. Ventas',total_base-total_ventas)
    c5.metric('Dif. Directas',total_base-total_directas)

    comp=pd.DataFrame({'Archivo':['BASE','VALIDACION_VENTAS','VALIDACION_DIRECTAS'],'Operaciones':[total_base,total_ventas,total_directas]})
    st.plotly_chart(px.bar(comp,x='Archivo',y='Operaciones',color='Archivo'),use_container_width=True)

    if 'RESPONSABLE' in base.columns:
        u=base.groupby('RESPONSABLE').size().reset_index(name='Operaciones')
        st.plotly_chart(px.bar(u,x='RESPONSABLE',y='Operaciones',title='Operaciones por Usuario'),use_container_width=True)

    if 'FIDEICOMISO' in directas.columns:
        f=directas.groupby('FIDEICOMISO').size().reset_index(name='Operaciones').sort_values('Operaciones',ascending=False)
        st.plotly_chart(px.bar(f.head(20),x='Operaciones',y='FIDEICOMISO',orientation='h',title='Top Fideicomisos'),use_container_width=True)

    if 'CONTABILIDAD' in directas.columns:
        p=directas.groupby('CONTABILIDAD').size().reset_index(name='Operaciones').sort_values('Operaciones',ascending=False)
        st.plotly_chart(px.bar(p.head(20),x='Operaciones',y='CONTABILIDAD',orientation='h',title='Portafolios'),use_container_width=True)

    st.dataframe(comp,use_container_width=True)
