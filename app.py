import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import numpy as np
import json

# Read dataset (CSV)
df_interact = pd.read_csv('data/relation.csv')

# Set header title
st.title('Network Graph Visualization of Stock-Stock Interactions')

# Define list of selection options and sort alphabetically
ticker_list = np.load('ticket.npy')
ticker_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
selected_tickers = st.multiselect('Select stock(s) to visualize', ticker_list)

# Set info message on initial site load
if len(selected_tickers) == 0:
    st.text('Choose at least 1 stock to start')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['Source'].isin(selected_tickers) | \
                                df_interact['Target'].isin(selected_tickers)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'Source', 'Target')

    # Initiate PyVis network object
    stock_net = Network(
                       height='400px',
                       width='100%',
                       bgcolor='#222222',
                       font_color='white'
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    stock_net.from_nx(G)

    # Generate network with specific layout settings
    stock_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        stock_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = 'html_files'
        stock_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)

st.markdown('#### Predict')
df = pd.read_csv('data/prediction.csv')
st.dataframe(df)
st.markdown('#### Analysis')
ticker = st.selectbox('Select stock to see change', ticker_list)
N = st.number_input(label="N = ", value = 5, min_value=0, max_value=100)
with open('top_relation.json') as json_file:
    top = json.load(json_file)
st.write(f'Top {N} companies that are significantly affected by this predicted change:', ', '.join(top[ticker][:N]))
changes = ["{} changes {}".format(ticker, list(df[df['Ticker'] == ticker]['Predict Change'])[0]) for ticker in top[ticker][:N]]
tmp = list(df[df['Ticker'] == ticker]['Predict Change'])[0]
st.write(f'{ticker} changes {tmp} leads to', '; '.join(changes))

# Footer
st.markdown(
    """
    <br>
    <h6><a href="https://github.com/ngtuthanhan/SP500_Predictor" target="_blank">GitHub Repo</a></h6>
    """, unsafe_allow_html=True
    )
