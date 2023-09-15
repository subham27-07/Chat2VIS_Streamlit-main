import streamlit as st
import pandas as pd
import numpy as np 
from lida import llm
from lida import Manager, TextGenerationConfig , llm
from lida.utils import plot_raster
from lida.datamodel import Goal, Summary


lida = Manager(text_gen = llm("openai", api_key='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')) # 
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)

data=pd.read_csv('movies.csv')

summary = lida.summarize(data, summary_method="default", textgen_config=textgen_config)
goals = lida.goals(summary, n=1, textgen_config=textgen_config)
st.write(goals[0])




i = 1

title = st.text_input('write your question here')


davo = Goal(index=1, question=title, visualization='', rationale='Treat production budget as a categorical variable instead of quantitative')
goals.append(davo)
temp = Summary(name=summary['name'], file_name=summary['file_name'], dataset_description=summary['dataset_description'], field_names=summary['field_names'], fields=summary['fields'])
library="seaborn"
textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
charts = lida.visualize(summary=temp, goal=davo, textgen_config=textgen_config, library=library)
# plot raster image of chart
plot_raster(charts[0].raster)

st.pyplot()
