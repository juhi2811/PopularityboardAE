import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import random
from geopy import geocoders
#gn = geocoders.GeoNames(username="juhic")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#sprint("Mumbai",gn.geocode("Mumbai"))
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df =pd.read_csv("/Users/juhic/Documents/ae_com.csv")
df['price_num']=df['price'].apply(lambda x: float(x.split("USD")[0]))
list_places=["Amsterdam", "New York", "Mumbai", "Tokyo"]
df['city']=[random.choice(list_places) for i in range(len(df))]
columns_cat=[c for c in list(df.columns) if c!="price"]
app.layout = html.Div([
    html.H2("Product popularity board"),
    html.H6("Choose feature for distribution"),
dcc.Dropdown(
                id='features',
                options=[{'label': i, 'value': i} for i in columns_cat],
                value="product_category"
            ),
             html.H6("Choose feature for price"),
dcc.Dropdown(
                id='features_cat',
                options=[{'label': i, 'value': i} for i in columns_cat],
                value="product_category"
            ),
dcc.Graph(
        id='distribution-graph',
    ),
dcc.Graph(
        id='price-graph',
    )

])


@app.callback(
    Output('distribution-graph', 'figure'),
    Input('features', 'value'))
def update_distbn(feature_x):
    if feature_x=="price":
        feat="price_num"
    else:
        feat=feature_x
    df_product = df.groupby(feature_x).count()
    df_product[feature_x]=df_product.index
    df_product= df_product.sort_values(by="pdp_url", ascending=False)
    print(df_product)
    fig_distbn=px.bar(df_product, x=feature_x, y="rating",title="Distribution of transactions among "+str(feat),labels={"rating": "Number of transactions"},color_discrete_sequence=["pink" for p in range(len(df_product))])
    return fig_distbn

@app.callback(
    Output('price-graph', 'figure'),
    Input('features_cat', 'value'))
def update_graph(feature_x):
    print(feature_x)
    df_product = df.groupby(feature_x).mean()
    df_product[feature_x] = df_product.index
    df_product['brand_name'] = list(df.groupby(feature_x).first()['brand_name'])
    df_product=df_product.sort_values(by="rating",ascending=False)
    fig_bar = px.bar(df_product, x=feature_x, y="price_num", color="brand_name", barmode="group",title="Average price per "+str(feature_x),labels={"price_num"})
    return fig_bar


if __name__ == '__main__':
    app.run_server(debug=True)
