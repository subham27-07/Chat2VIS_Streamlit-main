#################################################################################
# Chat2VIS 
# https://chat2vis.streamlit.app/


#### New app ####
# https://chat2visapp.streamlit.app/#housing
#################################################################################

import pandas as pd
import openai
import streamlit as st
#import streamlit_nested_layout
from classes import get_primer,format_question,run_request
import warnings
warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_icon="chat2vis.png",layout="wide",page_title="LLM Powered NLP to Visualization")
st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            LLM Powered NLP to Visualization</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Creating Visualisations from Users Queries  \
            with Large Language Models</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<h4  style='text-align: center;font-size:small;color:grey;padding-top: 0rem;padding-bottom: .2rem;'>Chat2VIS: Generating Data \
                    Visualisations via Natural Language using ChatGPT, Codex and GPT-3 \
                 Large Language Models </h4>", unsafe_allow_html=True)


                 
st.sidebar.markdown("<h4  style='text-align:center;font-size:small;color:grey;padding-top: 0rem;padding-bottom: .2rem;'>Chat2VIS: Fine-Tuning Data Visualisations using Multilingual \
Natural Language Text and Pre-Trained Large Language Models </h4>", unsafe_allow_html=True)



available_models = {"ChatGPT-4": "gpt-4","ChatGPT-3.5": "gpt-3.5-turbo","GPT-3": "text-davinci-003",}

# List to hold datasets
if "datasets" not in st.session_state:
    datasets = {}
    # Preload datasets
    # datasets["Movies"] = pd.read_csv("movies.csv")
    datasets["Housing"] =pd.read_csv("housing.csv")
    # datasets["Cars"] =pd.read_csv("cars.csv")
    # datasets["Colleges"] =pd.read_csv("colleges.csv")
    # datasets["Customers & Products"] =pd.read_csv("customers_and_products_contacts.csv")
    # datasets["Department Store"] =pd.read_csv("department_store.csv")
    # datasets["Energy Production"] =pd.read_csv("energy_production.csv")
    st.session_state["datasets"] = datasets
else:
    # use the list already loaded
    datasets = st.session_state["datasets"]

my_key = st.text_input(label = ":key: OpenAI Key:", help="Please ensure you have an OpenAI API account with credit. ChatGPT Plus subscription does not include API access.",type="password")

with st.sidebar:
    # First we want to choose the dataset, but we will fill it with choices once we've loaded one
    dataset_container = st.empty()

    # Add facility to upload a dataset
    uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")
    index_no=0
    if uploaded_file is not None:
        # Read in the data, add it to the list of available datasets
        file_name = uploaded_file.name[:-4].capitalize()
        datasets[file_name] = pd.read_csv(uploaded_file)
        # Default for the radio buttons
        index_no = len(datasets)-1

    # Radio buttons for dataset choice
    chosen_dataset = dataset_container.radio(":bar_chart: Choose your data:",datasets.keys(),index=index_no)#,horizontal=True,)

    # Check boxes for model choice
    st.write(":brain: Choose your model(s):")
    # Keep a dictionary of whether models are selected or not
    use_model = {}
    for model_desc,model_name in available_models.items():
        label = f"{model_desc} ({model_name})"
        key = f"key_{model_desc}"
        use_model[model_desc] = st.checkbox(label,value=True,key=key)

# Text area for query
question = st.text_area(":eyes: What would you like to visualise?",height=10)
go_btn = st.button("Go...")

# Make a list of the models which have been selected
#model_dict = {model_name: use_model for model_name, use_model in use_model.items() if use_model}
#model_count = len(model_dict)
model_list = [model_name for model_name, choose_model in use_model.items() if choose_model]
model_count = len(model_list)

# Execute chatbot query
if go_btn and model_count > 0:
    # Place for plots depending on how many models
    plots = st.columns(model_count)
    # Get the primer for this dataset
    primer1,primer2 = get_primer(datasets[chosen_dataset],'datasets["'+ chosen_dataset + '"]')
    # Format the question
    question_to_ask = format_question(primer1,primer2 , question)    
    # Create model, run the request and print the results
    for plot_num, model_type in enumerate(model_list):
        with plots[plot_num]:
            st.subheader(model_type)
            try:
                # Run the question
                answer=""
                answer = run_request(question_to_ask, available_models[model_type], key=my_key)
                # the answer is the completed Python script so add to the beginning of the script to it.
                answer = primer2 + answer
                plot_area = st.empty()
                plot_area.pyplot(exec(answer))           
            except Exception as e:
                if type(e) == openai.error.APIError:
                    st.error("OpenAI API Error. Please try again a short time later.")
                elif type(e) == openai.error.Timeout:
                    st.error("OpenAI API Error. Your request timed out. Please try again a short time later.")
                elif type(e) == openai.error.RateLimitError:
                    st.error("OpenAI API Error. You have exceeded your assigned rate limit.")
                elif type(e) == openai.error.APIConnectionError:
                    st.error("OpenAI API Error. Error connecting to services. Please check your network/proxy/firewall settings.")
                elif type(e) == openai.error.InvalidRequestError:
                    st.error("OpenAI API Error. Your request was malformed or missing required parameters.")
                elif type(e) == openai.error.AuthenticationError:
                    st.error("Please enter a valid OpenAI API Key.")
                elif type(e) == openai.error.ServiceUnavailableError:
                    st.error("OpenAI Service is currently unavailable. Please try again a short time later.")                   
                else:
                    st.error("Unfortunately the code generated from the model contained errors and was unable to execute. ")

# Display the datasets in a list of tabs
# Create the tabs
tab_list = st.tabs(datasets.keys())

# Load up each tab with a dataset
for dataset_num, tab in enumerate(tab_list):
    with tab:
        # Can't get the name of the tab! Can't index key list. So convert to list and index
        dataset_name = list(datasets.keys())[dataset_num]
        st.subheader(dataset_name)
        st.dataframe(datasets[dataset_name])
        
# Insert footer to reference dataset origin  
footer="""<style>.footer {position: fixed;left: 0;bottom: 0;width: 100%;text-align: center;}</style><div class="footer">
<p> <a style='display: block; text-align: center;'> </a></p></div>"""
st.caption("")

# Hide menu and footer
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
