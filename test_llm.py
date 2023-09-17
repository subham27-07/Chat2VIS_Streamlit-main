import streamlit as st
import pandas as pd
import numpy as np 
from lida import llm
from lida import Manager, TextGenerationConfig , llm
from lida.utils import plot_raster
from lida.datamodel import Goal, Summary




# data=pd.read_csv('movies.csv')

st.set_option('deprecation.showPyplotGlobalUse', False)


enc='utf-8'
spectra=st.sidebar.file_uploader("upload file", type={"csv",'txt'})
if spectra is not None:
    spectra_df=pd.read_csv(spectra)

st.write(spectra_df)


# lida = Manager(text_gen = llm("openai", api_key='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')) # 
# textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)

# summary = lida.summarize(spectra_df, summary_method="default", textgen_config=textgen_config)
# goals = lida.goals(summary, n=1, textgen_config=textgen_config)
# st.write(goals[0])




# i = 1

# title = st.text_input('write your question here')


# davo = Goal(index=1, question=title, visualization='', rationale='Treat production budget as a categorical variable instead of quantitative')
# goals.append(davo)
# temp = Summary(name=summary['name'], file_name=summary['file_name'], dataset_description=summary['dataset_description'], field_names=summary['field_names'], fields=summary['fields'])
# library="seaborn"
# textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
# charts = lida.visualize(summary=temp, goal=davo, textgen_config=textgen_config, library=library)
# # plot raster image of chart
# fig1=plot_raster(charts[0].raster)

# st.pyplot(fig1)


# code = charts[0].code
# textgen_config = TextGenerationConfig(n=1, temperature=0, use_cache=True)
# instructions = ["Show only action and adventure movies", "What about movies that have grossed over 100 million?"]
# edited_charts = lida.edit(code=code,  summary=summary, instructions=instructions, library=library, textgen_config=textgen_config)
# fig2=plot_raster(edited_charts[0].raster)

# st.pyplot(fig2)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)