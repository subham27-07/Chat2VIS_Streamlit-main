import pandas as pd
import numpy as np
import streamlit as st
from nl4dv import NL4DV
import altair as alt
from altair import vega, vegalite
import os
from IPython.display import display

data_url=pd.read_csv('movies.csv')

label_attribute = None
dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}
nl4dv_instance = NL4DV(verbose=False,
                       debug=True,
                       data_url=data_url,
                       label_attribute=label_attribute,
                       dependency_parser_config=dependency_parser_config
                       )

response = nl4dv_instance.analyze_query("Visualize rating and budget")

display(alt.display.html_renderer(response['visList'][0]['vlSpec']), raw=True)