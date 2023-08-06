from ctypes import alignment
from pydeck.bindings.layer import Layer
import streamlit as st
import altair as alt
import pydeck as pdk
import pandas as pd
import numpy as np
import base64
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="AVC",page_icon=":hospital:" ,layout='wide')  
################################################################################################################################
# Carregando dados de internação por AVC na DRS XIII - São joão
df_sj_internacoes = pd.read_csv(
    './avc_internacoes_regiao_saojoao_2008_2021.csv',
     skiprows=5, sep=';', header=0, nrows = 16,
      encoding='latin-1')

df_sj_internacoes['Município'] = df_sj_internacoes['Município'].str.replace('\d+', '')
df_melt = df_sj_internacoes.melt(id_vars =['Município']) 
df_melt = df_melt.rename(columns={'variable': 'Mês/Ano'})
df_melt = df_melt.rename(columns={'value': 'Internações'})



df_melt = df_melt.set_index('Mês/Ano')
df_melt = df_melt.drop("Total")
df_melt = df_melt.reset_index()

#time_range = pd.DataFrame(pd.date_range(start='2008-01-01', end='2021-05-01', freq='M'))
time_range = pd.date_range('2008-01-01','2021-05-01', 
              freq='M').strftime("%Y-%m").tolist()

#df_melt['Mês/Ano'] = pd.DataFrame(list(np.repeat(time_range, n)))
#df_melt['Mês/Ano'] = pd.to_datetime(df_melt['Mês/Ano'])
df_melt['Mês/Ano'] = np.array(pd.Series(list(np.repeat(time_range, 16))), dtype=np.datetime64)


lat_sj = [-21.5323, -21.7701, -21.6562, -22.1832, -22.4363, -21.4708, -22.3708, -22.432, -21.8135, -21.9695, -21.5958, -21.7151, -21.7023, -21.4656, -21.8357, -21.8357]
long_sj = [-46.6499, -47.0919, -46.7411, -46.7624, -46.8222, -47.0006, -46.9378, -46.9582, -47.2563, -46.7989, -46.8896, -46.8232, -47.2814, -46.7527, -46.8806, -46.8806]
#df_melt['latitude'] = lat_sj
#df_melt['longitude'] = long_sj

###########################################################################################
# Carregando dados de óbito por AVC na DRS XIII - São João
df_sj_obitos = pd.read_csv(
    './avc_obitos_regiao_saojoao_2008_2021.csv',
     skiprows=5, sep=';', header=0, nrows = 16,
      encoding='latin-1')

df_sj_obitos['Município'] = df_sj_obitos['Município'].str.replace('\d+', '')
df_melt_obitos = df_sj_obitos.melt(id_vars =['Município']) 
df_melt_obitos = df_melt_obitos.rename(columns={'variable': 'Mês/Ano'})
df_melt_obitos = df_melt_obitos.rename(columns={'value': 'Óbitos'})


df_melt_obitos = df_melt_obitos.set_index('Mês/Ano')
df_melt_obitos = df_melt_obitos.drop("Total")
df_melt_obitos = df_melt_obitos.reset_index()


df_melt_obitos['Mês/Ano'] = np.array(pd.Series(list(np.repeat(time_range, 16))), dtype=np.datetime64)

#lat = [-21.5323, -21.7701, -21.6562, -22.1832, -22.4363, -21.4708, -22.3708, -22.432, -21.8135, -21.9695, -21.5958, -21.7151, -21.7023, -21.4656, -21.8357, -21.8357] * 160
#long = [-46.6499, -47.0919, -46.7411, -46.7624, -46.8222, -47.0006, -46.9378, -46.9582, -47.2563, -46.7989, -46.8896, -46.8232, -47.2814, -46.7527, -46.8806, -46.8806] * 160

#df_melt_obitos['latitude'] = lat
#df_melt_obitos['longitude'] = long

#######################################################################################
#Carregando dados de internação por AVC na DRS XIV - Ribeirão Preto
df_rp_internacoes = pd.read_csv('./avc_internacoes_regiao_ribeiraopreto_2008_2021.csv', skiprows=5, sep=';', header=0, nrows = 18, encoding='latin-1')
df_rp_internacoes['Município'] = df_rp_internacoes['Município'].str.replace('\d+', '')

df_melt_rp_internacoes = df_rp_internacoes.melt(id_vars =['Município']) 
df_melt_rp_internacoes = df_melt_rp_internacoes.rename(columns={'variable': 'Mês/Ano'})
df_melt_rp_internacoes = df_melt_rp_internacoes.rename(columns={'value': 'Internações'})



df_melt_rp_internacoes = df_melt_rp_internacoes.set_index('Mês/Ano')
df_melt_rp_internacoes = df_melt_rp_internacoes.drop("Total")
df_melt_rp_internacoes = df_melt_rp_internacoes.reset_index()

n_rp_intern = 18
df_melt_rp_internacoes['Mês/Ano'] = np.array(pd.Series(list(np.repeat(time_range, n_rp_intern))), dtype=np.datetime64)



lat_rp = [-21.0239, -20.8916, -21.2753, -21.34, -21.3607, -21.2554, -21.018, -21.2616, -20.9981, -21.0231, -21.1767, -21.7312,
 -21.4703, -21.0869, -21.4781, -21.2114, -21.1434, -21.1434]
long_rp = [-47.3727, -47.5856, -47.3048, -47.7295, -48.2282, -48.3224, -47.7645, -48.4966, -48.2155, -48.0377, -47.8208, -47.4959,
 -47.3621, -47.1501, -47.5507, -47.5964, -48.007, -48.007]

#df_melt_rp_internacoes['latitude'] = lat_rp
#df_melt_rp_internacoes['longitude'] = long_rp


##################################################################################################################################
# Carregando dados de óbitos por AVC na DRS XIV - Ribeirão Preto
df_rp_obitos = pd.read_csv('./avc_obito_regiao_ribeiraopreto_2008_2021.csv', skiprows=5, sep=';', header=0, nrows = 17, encoding='latin-1')
df_rp_obitos['Município'] = df_rp_obitos['Município'].str.replace('\d+', '')

df_melt_rp_obitos = df_rp_obitos.melt(id_vars =['Município']) 
df_melt_rp_obitos = df_melt_rp_obitos.rename(columns={'variable': 'Mês/Ano'})
df_melt_rp_obitos = df_melt_rp_obitos.rename(columns={'value': 'Óbitos'})



df_melt_rp_obitos = df_melt_rp_obitos.set_index('Mês/Ano')
df_melt_rp_obitos = df_melt_rp_obitos.drop("Total")
df_melt_rp_obitos = df_melt_rp_obitos.reset_index()

n_rp_ob = 17
df_melt_rp_obitos['Mês/Ano'] = np.array(pd.Series(list(np.repeat(time_range, n_rp_ob))), dtype=np.datetime64)


lat_rp_ob = [-21.0239, -20.8916, -21.2753, -21.34, -21.3607, -21.2554, -21.018, -21.2616, -20.9981, -21.0231, -21.1767, -21.7312,
 -21.4703, -21.4781, -21.2114, -21.1434, -21.1434]
long_rp_ob = [-47.3727, -47.5856, -47.3048, -47.7295, -48.2282, -48.3224, -47.7645, -48.4966, -48.2155, -48.0377, -47.8208, -47.4959,
 -47.3621, -47.5507, -47.5964, -48.007, -48.007]
#df_melt_rp_obitos_time['latitude'] = lat_rp_ob
#df_melt_rp_obitos_time['longitude'] = long_rp_ob
#df_melt_rp_obitos['latitude'] = lat_rp_ob
#df_melt_rp_obitos['longitude'] = long_rp_ob


# Config Streamlit Backgroung

main_bg = "sample.jpeg"
main_bg_ext = "jpeg"

side_bg = "sample.jpeg"
side_bg_ext = "jpeg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# FILTERING DATA BY Year SELECTED

year_to_filter = st.sidebar.slider("Selecione o ano:", 2008, 2021)
month_to_filter = st.sidebar.slider("Selecione o mês:", 1, 12)

if month_to_filter == 1:
    month = 'janeiro'
if month_to_filter == 2:
    month = 'fevereiro'
if month_to_filter == 3:
    month = 'março'
if month_to_filter == 4:
    month = 'abril'
if month_to_filter == 5:
    month = 'maio'
if month_to_filter == 6:
    month = 'junho'
if month_to_filter == 7:
    month = 'julho'
if month_to_filter == 8:
    month = 'agosto'
if month_to_filter == 9:
    month = 'setembro'
if month_to_filter == 10:
    month = 'outubro'
if month_to_filter == 11:
    month = 'novembro'
if month_to_filter == 12:
    month = 'dezembro'



#st.markdown("<h1 style='text-align: center; color: black;'>Ocorrências de, color: red; AVC</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>Comparativo AVC - DRS XIII e XIV </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center: white; '>Exemplo utilizando somente um CID de AVC. Demais CIDs a serem incluídos </h3>", unsafe_allow_html=True)
#st.write("Ocorrências por DRS no ano de " , year_to_filter)
st.write(f"Ocorrências por DRS em {month} de {year_to_filter}")
#st.markdown("<h1 style='text-align: center; color: red;'>Ocorrências por DRS no ano de ...</h1>", unsafe_allow_html=True)



#data = df_melt_time[df_melt_time['Mês/Ano'].dt.year == year_to_filter]
#data = df_melt[df_melt['Mês/Ano'].dt.year == year_to_filter]
data = df_melt[(df_melt['Mês/Ano'].dt.year == year_to_filter) & (df_melt['Mês/Ano'].dt.month == month_to_filter)]
data = data.replace({'-':0})
data['Internações']= pd.to_numeric(data['Internações'])
data = data.groupby('Município')['Internações'].sum()
data = pd.DataFrame(data).reset_index()
data['lat'] = lat_sj
data['lon'] = long_sj
#data = data.astype(str) #Bug da versão 0.85 do streamlit


data_sj_obitos = df_melt_obitos[(df_melt_obitos['Mês/Ano'].dt.year == year_to_filter) & (df_melt_obitos['Mês/Ano'].dt.month == month_to_filter)]
data_sj_obitos = data_sj_obitos.replace({'-':0})
data_sj_obitos['Óbitos']= pd.to_numeric(data_sj_obitos['Óbitos'])
data_sj_obitos = data_sj_obitos.groupby('Município')['Óbitos'].sum()
data_sj_obitos = pd.DataFrame(data_sj_obitos).reset_index()
data_sj_obitos['lat'] = lat_sj
data_sj_obitos['lon'] = long_sj

data_rp_internacoes = df_melt_rp_internacoes[(df_melt_rp_internacoes['Mês/Ano'].dt.year == year_to_filter) & (df_melt_rp_internacoes['Mês/Ano'].dt.month == month_to_filter)]
data_rp_internacoes = data_rp_internacoes.replace({'-':0})
data_rp_internacoes['Internações']= pd.to_numeric(data_rp_internacoes['Internações'])
data_rp_internacoes = data_rp_internacoes.groupby('Município')['Internações'].sum()
data_rp_internacoes = pd.DataFrame(data_rp_internacoes).reset_index()
data_rp_internacoes['lat'] = lat_rp
data_rp_internacoes['lon'] = long_rp

data_rp_obitos = df_melt_rp_obitos[(df_melt_rp_obitos['Mês/Ano'].dt.year == year_to_filter) & (df_melt_rp_obitos['Mês/Ano'].dt.month == month_to_filter)]
data_rp_obitos = data_rp_obitos.replace({'-':0})
data_rp_obitos['Óbitos']= pd.to_numeric(data_rp_obitos['Óbitos'])
data_rp_obitos = data_rp_obitos.groupby('Município')['Óbitos'].sum()
data_rp_obitos = pd.DataFrame(data_rp_obitos).reset_index()
data_rp_obitos['lat'] = lat_rp_ob
data_rp_obitos['lon'] = long_rp_ob


# Criando os gráficos

c = alt.Chart(data).mark_bar(height=20).encode(x=alt.X('Internações', scale=alt.Scale(domain=[0,200])), y='Município', tooltip=['Internações'], color=alt.Color('Município', legend=None)).properties(
    title='DRS XIII - São João da Boa Vista - Internações por AVC', width=610, height=300)


d = alt.Chart(data_sj_obitos).mark_bar().encode(x=alt.X('Óbitos', scale=alt.Scale(domain=[0,30])), y=alt.Y('Município', axis=None), tooltip=['Óbitos'], color=alt.Color('Município', legend=None)).properties(
    title='DRS XIII - São João da Boa Vista - Óbitos por AVC', width=600, height=300)


e = alt.Chart(data_rp_internacoes).mark_bar().encode(x=alt.X('Internações', scale=alt.Scale(domain=[0,200])), y='Município', tooltip=['Internações'], color=alt.Color('Município', legend=None)).properties(
    title='DRS XIV - Ribeirão Preto - Internações por AVC', width=600, height=300)


f = alt.Chart(data_rp_obitos).mark_bar().encode(x=alt.X('Óbitos', scale=alt.Scale(domain=[0,30])), y=alt.Y('Município', axis=None), tooltip=['Óbitos'], color=alt.Color('Município', legend=None)).properties(
    title='DRS XIV - Ribeirão Preto - Óbitos por AVC', width=600, height=300)




c | d
e | f

# criando a camada
data_map = data.set_index('Município').reset_index()
data_rp_internacoes_map = data_rp_internacoes.set_index('Município').reset_index()

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]


view = pdk.data_utils.compute_view(data[["lon", "lat"]])
view.zoom = 7.2
view.width = 1390

sj = pdk.Layer(
    "HeatmapLayer",
    data=data_map,
    opacity=1.5,
    get_position=["lon", "lat"],
    aggregation=pdk.types.String("MEAN"),
    color_range=COLOR_BREWER_BLUE_SCALE,
    threshold=1,
    get_weight="Internações",
    pickable=True,
)

rp = pdk.Layer(
    "HeatmapLayer",
    data=data_rp_internacoes_map,
    opacity=1.5,
    get_position=["lon", "lat"],
    threshold=0.75,
    aggregation=pdk.types.String("MEAN"),
    get_weight="Internações",
    pickable=True,
)


r = pdk.Deck(
    layers=[sj, rp],
    initial_view_state=view,
    map_provider="mapbox",
    map_style=pdk.map_styles.CARTO_ROAD,
    tooltip={"text": "Concentração de Internações DRS XIII em azul, Concentração de Internações DRS XIV em laranja"},
)

r.to_html("heatmap_layer.html")
st.pydeck_chart(r)
