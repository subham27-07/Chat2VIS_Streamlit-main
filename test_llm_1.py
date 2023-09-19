import streamlit as st
import pandas as pd
import numpy as np 
from lida import llm
from lida import Manager, TextGenerationConfig , llm
from lida.utils import plot_raster
from lida.datamodel import Goal, Summary
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
import openai


st.set_page_config(layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)


new_title = '<h1 style="font-family:sans-serif;text-align: center; color:Black; font-size: 42px;">Automated Data Analysis Tool</h1>'
st.markdown(new_title, unsafe_allow_html=True)

enc='utf-8'
spectra=st.sidebar.file_uploader("upload file", type={"csv",'txt'})

# spectra_df = None  # Initialize spectra_df

if spectra is None:
    st.write("Please upload the file to get started.")
else:
    spectra_df = pd.read_csv(spectra, encoding=enc)


with st.expander("Show me the data"):
    st.write(spectra_df)   


st.cache_resource(ttl=7200)
def main():
    global spectra_df
    dataset = spectra_df

    # Assuming you want the checkbox at the start of your app
    if st.sidebar.checkbox('Generate and Show Data Report'):
        df = spectra_df
        pr = gen_profile_report(df, explorative=True)

        with st.expander("Data Report", expanded=True):
            st_profile_report(pr)

@st.cache_resource(ttl=7200)
def gen_profile_report(df, *report_args, **report_kwargs):
    return df.profile_report(*report_args, **report_kwargs)


if __name__ == "__main__":
    main()


######################## Lida Componenet starts here ############################

my_key = st.text_input(label = ":key: Paste your key:", help="write down the authenticator",type="password")

lida = Manager(text_gen = llm("openai", api_key=my_key)) # 

# textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-16k", use_cache=True)

summary = lida.summarize(spectra_df, summary_method="default", textgen_config=textgen_config)
goals = lida.goals(summary, n=1, textgen_config=textgen_config)
# st.write(goals[0])

# try:
#     lida = Manager(text_gen = llm("openai", api_key=my_key))
#     textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-16k", use_cache=True)
#     summary = lida.summarize(spectra_df, summary_method="default", textgen_config=textgen_config)
#     goals = lida.goals(summary, n=1, textgen_config=textgen_config)

# except Exception as e:
#     print("Please provide a valid API key")
#     print(f"Original Error: {e}")





def plot_fig1(title, summary):
    davo = Goal(index=1, question=title, visualization='', rationale='Treat production budget as a categorical variable instead of quantitative')
    goals.append(davo)
    temp = Summary(name=summary['name'], file_name=summary['file_name'], dataset_description=summary['dataset_description'], field_names=summary['field_names'], fields=summary['fields'])
    library="seaborn"
    textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
    charts = lida.visualize(summary=temp, goal=davo, textgen_config=textgen_config, library=library)
    fig1 = plot_raster(charts[0].raster)
    st.pyplot(fig1)
    return charts

def plot_fig2(title1, code, summary):
    library="seaborn"
    textgen_config = TextGenerationConfig(n=1, temperature=0, use_cache=True)
    instructions = title1
    edited_charts = lida.edit(code=code, summary=summary, instructions=instructions, library=library, textgen_config=textgen_config)
    fig2 = plot_raster(edited_charts[0].raster)
    st.pyplot(fig2)

# Streamlit input
title = st.text_input('write your question here')
title1 = st.text_input('write your follow up question here')

charts = None
if title:
    charts = plot_fig1(title, summary)

if title1 and charts:
    plot_fig2(title1, charts[0].code, summary)


######################## Lida Componenet ends here ############################

######################## checkbox ############################

dataSummerizer = st.sidebar.checkbox('Summerize the data and goals for me ')

@st.cache_resource(ttl=7200)
def dataSummary():
    st.write(goals[0])

if dataSummerizer:
    dataSummary() 


@st.cache_resource(ttl=7200)
def visualExplanation(code, library="seaborn", textgen_config=None):
    explanations = lida.explain(code=code, library=library, textgen_config=textgen_config)
    for row in explanations[0]:
        st.write(row["section"], " : ", row["explanation"])
visualization = st.sidebar.checkbox('Show me the explanation of the visualization ')
if visualization and charts:
    library = "seaborn"
    textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
    visualExplanation(charts[0].code, library, textgen_config)

######################## checkbox ############################

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


