import streamlit as st
import pandas as pd
import numpy as np 
from lida import llm
from lida import Manager, TextGenerationConfig , llm
from lida.utils import plot_raster
from lida.datamodel import Goal, Summary
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
import altair as alt

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


st.cache_resource(ttl=3600)
def main():
    global spectra_df
    dataset = spectra_df

    # Assuming you want the checkbox at the start of your app
    if st.sidebar.checkbox('Generate and Show Data Report'):
        df = spectra_df
        pr = gen_profile_report(df, explorative=True)

        with st.expander("Data Report", expanded=True):
            st_profile_report(pr)

@st.cache_resource(ttl=3600)
def gen_profile_report(df, *report_args, **report_kwargs):
    return df.profile_report(*report_args, **report_kwargs)

# @st.cache(allow_output_mutation=True)
# def gen_profile_report(df, *report_args, **report_kwargs):
#     return df.profile_report(*report_args, **report_kwargs)

if __name__ == "__main__":
    main()


######################## Lida Componenet starts here ############################
# my_key = st.text_input(label = ":key: Paste your key:", help="write down the authenticator",type="password")
# lida = Manager(text_gen = llm("openai", api_key=my_key)) # 
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)
# textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4", use_cache=True)

summary = lida.summarize(spectra_df, summary_method="default", textgen_config=textgen_config)
goals = lida.goals(summary, n=1, textgen_config=textgen_config)
# st.write(goals[0])




title = st.text_input('write your question here')
title1 = st.text_input('write your follow up question here')

i = 1
davo = Goal(index=1, question=title, visualization='', rationale='Treat production budget as a categorical variable instead of quantitative')
goals.append(davo)
temp = Summary(name=summary['name'], file_name=summary['file_name'], dataset_description=summary['dataset_description'], field_names=summary['field_names'], fields=summary['fields'])
library="altair"
textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
charts = lida.visualize(summary=temp, goal=davo, textgen_config=textgen_config, library=library)
spec = charts[0].spec 
new_chart = alt.Chart.from_dict(spec)
new_chart.data = lida.data
fig1=new_chart

# plot raster image of chart
# fig1=plot_raster(charts[0].raster)

st.pyplot(fig1)


code = charts[0].code
textgen_config = TextGenerationConfig(n=1, temperature=0, use_cache=True)

instructions=title1
# instructions = ["Show only action and adventure movies", "What about movies that have grossed over 100 million?"]
edited_charts = lida.edit(code=code,  summary=summary, instructions=instructions, library=library, textgen_config=textgen_config)
fig2=plot_raster(edited_charts[0].raster)

st.pyplot(fig2)

# def process_first_input():
#     i = 1
#     davo = Goal(index=1, question=title, visualization='', rationale='Treat production budget as a categorical variable instead of quantitative')
#     goals.append(davo)
#     temp = Summary(name=summary['name'], file_name=summary['file_name'], dataset_description=summary['dataset_description'], field_names=summary['field_names'], fields=summary['fields'])
#     library="seaborn"
#     textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
#     charts = lida.visualize(summary=temp, goal=davo, textgen_config=textgen_config, library=library)
#     # plot raster image of chart
#     fig1=plot_raster(charts[0].raster)

#     st.pyplot(fig1)
#     return charts


# title = st.text_input('write your question here')
# title1 = st.text_input('write your follow up question here')



# if title:  # checks if title is not an empty string
#     process_first_input()





######################## Lida Componenet ends here ############################

######################## checkbox ############################

dataSummerizer = st.sidebar.checkbox('Summerize the data and goals for me ')

@st.cache_resource(ttl=3600)
def dataSummary():
    st.write(goals[0])

if dataSummerizer:
    dataSummary() 

@st.cache_resource(ttl=3600)
def visualExplanation():
    explanations = lida.explain(code=code, library=library, textgen_config=textgen_config)
    for row in explanations[0]:
        st.write(row["section"]," : ", row["explanation"])

 



visualization = st.sidebar.checkbox('Show me the explanation of the visualization ')
if visualization:
    visualExplanation()
######################## checkbox ############################

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)





# def selector(select):
#     global selectOptions

#     if select == 'Topic Modelling':
#         with st.expander("Expand Me to see Topic Modelling Analysis"):
#             st.markdown('<p style="font-family:sans-serif;text-align: left; color:Black;font-size: 16px;">Topic Models are very useful for the purpose for document clustering, organizing large blocks of textual data, information retrieval from unstructured text and feature selection.</p>', unsafe_allow_html=True)
           
            
#         ind=selectOptions.index('Topic Modelling')
#         selectOptions.pop(ind)
#         addSelect()
       
#     elif select == 'Sentiment Analysis':
#         with st.expander("Expand Me to see the Sentiment Analysis"):
#             st.markdown('<p style="font-family:sans-serif;text-align: left; color:Black;font-size: 16px;">Sentiment analysis, also referred to as opinion mining, is an approach to natural language processing (NLP) that identifies the emotional tone behind a body of text. This is a popular way for organizations to determine and categorize opinions about a product, service, or idea.</p>', unsafe_allow_html=True)
          
#         ind=selectOptions.index('Sentiment Analysis')
#         selectOptions.pop(ind)
#         addSelect()
    
#     elif select == 'Hastag Analysis':
#         with st.expander("Expand Me to see the Hastag Analysis"):
#             st.markdown('<p style="font-family:sans-serif;text-align: left; color:Black;font-size: 18px;">Hastag Analysis is used to measure the social media reach of hashtag campaign and its mentions. To measure social media engagement around your hashtag. To discover social media sentiment around a hashtag.</p>', unsafe_allow_html=True)
            
#         ind=selectOptions.index('Hastag Analysis')
#         selectOptions.pop(ind)
#         addSelect()

#     elif select == 'Hate Speech Analysis':
#         with st.expander("Expand Me to see the HateSpeech Analysis"):
#             st.markdown('<p style="font-family:sans-serif;text-align: left; color:Black;font-size: 18px;">Hate Speech in the form of racist and sexist remarks are a common occurance on social media.“Hate speech is defined as any communication that disparages a person or a group on the basis of some characteristics such as race, color, ethnicity, gender, sexual orientation, nationality, religion, or other characteristic.</p>', unsafe_allow_html=True)
            
            
#         ind=selectOptions.index('Hate Speech Analysis')
#         selectOptions.pop(ind)
#         addSelect()

#     elif select == 'Emotion Analysis':
#         with st.expander("Expand Me to see the Emotion Analysis"):
#             st.markdown('<p style="font-family:sans-serif;text-align: left; color:Black;font-size: 18px;">Emotion analysis is the process of identifying and analyzing the underlying emotions expressed in textual data. Emotion analytics can extract the text data from multiple sources to analyze the subjective information and understand the emotions behind it.</p>', unsafe_allow_html=True)
#         ind=selectOptions.index('Emotion Analysis')
#         selectOptions.pop(ind)
#         addSelect()

# key=1

# selectOptions=['Add Analysis Tasks','Sentiment Analysis' ,'Hate Speech Analysis' , 'Hastag Analysis', 'Topic Modelling', 'Emotion Analysis']


# def addSelect():
#     global key
#     global selectOptions
#     with st.expander("Add Analysis Tasks"):
#         select= st.selectbox( '',selectOptions,key=str(key))
#     key+=1

#     selector(select)


# addSelect()