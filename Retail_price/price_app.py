from ctypes.wintypes import SIZE
from email.policy import default
import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import random

# https://streamlit.io/
# https://docs.streamlit.io/
# https://docs.streamlit.io/library/api-reference


def read_in_data():
    """Read in data from a CSV file."""
    return pd.read_csv('/Users/juhic/Documents/ae_com.csv')

# set a title
st.title('Product price Dashboard')

df = read_in_data()
df['price_num']=df['price'].apply(lambda x: float(x.split("USD")[0]))
columns_cat=[c for c in list(df.columns) if c!="price"]
df["rating_int"]=df["rating"].apply(lambda x: round(x,0))
st.markdown('## This is the retail data we used for this analysis')
# st.markdown('This is our original data what we will use in this example')
st.write(df)

# create a graphs
# first create some filters

st.markdown('## Shopping Data interactive')

components = list(df['rating_int'].unique())
make_choice = st.sidebar.selectbox('Select rating:', components)
# create some widgets what we can use for filtering
# create radio button:
class_multiselect = st.multiselect('Select rating', list(df['rating_int'].unique()), default=[5.00])
# create a slider:
age_slider = st.slider('Price range', min(df["price_num"]), max(df["price_num"]), (min(df["price_num"]), max(df["price_num"])))

titanic_data_filtered = df[(df['rating_int'].isin(class_multiselect)) &
                                    (df['price_num'] >= age_slider[0]) & (df['price_num'] <= age_slider[1])]

#calculate the number of survivors by group using the filtered data
survival_rate_stat = df.groupby(['rating_int']).agg(
        price_num=('price_num', 'mean'),
        count = ('price_num', 'count')
    ).reset_index()
#print(df["rating"].unique())
brand_stat = df.groupby(['brand_name']).agg(
        price_num=('price_num', 'mean'),
        count = ('price_num', 'count')
    ).reset_index()
# create a bar chart
fig1 = px.bar(brand_stat, x='brand_name', y='price_num')
# fig2=px.figure()
fig2=px.box(survival_rate_stat, x='rating_int', y='price_num')

# fig2.add_trace(px.scatter(survival_rate_stat, x='rating_int', y='price_num',size="count"))


# show the chart on the DB
st.plotly_chart(fig1)

st.plotly_chart(fig2)

#show calculated data
show_calculted_data = st.checkbox('Show calculated data', value=False)
if show_calculted_data:
    st.write(survival_rate_stat)

#show filtered data
show_filtered_data_cb = st.checkbox('Show filtered data', value=False)
if show_filtered_data_cb:
    st.write(titanic_data_filtered)