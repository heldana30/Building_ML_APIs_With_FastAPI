import streamlit as st
import pandas as pd
import requests
import time

# Set page configuration
st.set_page_config(page_title="Sepsis Prediction App", page_icon="🩺", layout="wide")

# Set page title
st.title("Sepsis Prediction App")

# Define the tabs
tabs = st.tabs(["Home", "Predict"])

# Home Tab Content
with tabs[0]:
    st.header("Welcome to the Sepsis Prediction App")
    st.markdown("""
    This app uses machine learning models to predict the likelihood of a patient developing sepsis based on various medical indicators.

 
### Key Features
- **Model Selection**: The API supports multiple models including XGBoost and Random Forest.
- **Real-time Predictions**: Get immediate predictions for sepsis risk based on patient data.
- **User-friendly Interface**: Easy-to-use endpoints for making predictions.

### How It Works
1. **Data Collection**: Input patient data such as Plasma Glucose, Blood Pressure, BMI, Age, etc.
2. **Model Prediction**: The API processes the data and provides a prediction along with the probability of sepsis.
3. **Output**: The prediction and probability results are returned.

### Usage
To use the API, send a POST request to the respective endpoint with the patient data. The available endpoints are:
- `/xgboost_prediction`: For predictions using the XGBoost model.
- `/random_forest_prediction`: For predictions using the Random Forest model.

    ### How to Use
    1. Navigate to the **Predict** tab.
    2. Fill in the required input fields.
    3. Click the **Submit** button to get the prediction results.
    """)

    st.header("About the Developer")
    st.write("**Name:** Heldana Natnael")
    st.write("**Background:** Expert in data science, machine learning, and software development.")
    st.write("**Contact:** www.linkedin.com/in/heldana-n")
    
    # Footer
    st.markdown("""
        ---
        © 2024 Sepsis Prediction Project. All rights reserved.
    """)


# Predict Tab Content
with tabs[1]:
    st.header("Predict Sepsis")

    # Function for selecting models
    def select_model():
        col1, col2 = st.columns(2)
        with col1:
            choice = st.selectbox('Select a model', options=['xgboost', 'random_forest'], key='select_model')
        with col2:
            pass
        return choice

    # Function for making prediction
    def make_prediction():
        selected_model = st.session_state['select_model']
        age = st.session_state['age']
        insurance = 1 if st.session_state['insurance'] == 'Yes' else 0
        m11 = st.session_state['m11']
        pr = st.session_state['pr']
        prg = st.session_state['prg']
        ts = st.session_state['ts']
        pl = st.session_state['pl']
        sk = st.session_state['sk']
        bd2 = st.session_state['bd2']

        base_url = 'https://ml-api-with-fastapi.onrender.com/'
        url = base_url + f"{ 'xgboost_prediction' if selected_model == 'xgboost' else 'random_forest_prediction'}"

        data = {
            'PRG': prg, 'PL': pl, 'PR': pr, 'SK': sk, 'TS': ts, 'M11': m11, 'BD2': bd2, 'Age': age, 'Insurance': insurance
        }

        # Send POST request with JSON data using the json parameter
        response_status = requests.get(base_url)

        if response_status.status_code == 200:
            response = requests.post(url, json=data, timeout=30)
            pred_prob = (response.json()['results'])
            prediction = pred_prob['prediction']
            probability = pred_prob['probability']

            st.session_state['prediction'] = prediction
            st.session_state['probability'] = probability
        else:
            st.write('Unable to connect to the server. Try Again Later.')

    # Creating the form
    def display_form():
        select_model()

        with st.form('input_features'):
            col1, col2 = st.columns(2)
            with col1:
                st.write('### Patient Demographics')
                age = st.number_input('Age', min_value=0, max_value=100, step=1, key='age')
                insurance = st.selectbox('Insurance', options=['Yes', 'No'], key='insurance')

                st.write('### Vital Signs')
                m11 = st.number_input('BMI', min_value=10.0, format="%.2f", step=1.00, key='m11')
                pr = st.number_input('Blood Pressure', min_value=10.0, format="%.2f", step=1.00, key='pr')
                prg = st.number_input('PRG(plasma glucose)', min_value=10.0, format="%.2f", step=1.00, key='prg')

            with col2:
                st.write('### Blood Work')
                pl = st.number_input('PL(Blood Work Result 1)', min_value=10.0, format="%.2f", step=1.00, key='pl')
                sk = st.number_input('SK(Blood Work Result 2)', min_value=10.0, format="%.2f", step=1.00, key='sk')
                ts = st.number_input('TS(Blood Work Result 3)', min_value=10.0, format="%.2f", step=1.00, key='ts')
                bd2 = st.number_input('BD2(Blood Work Result 4)', min_value=10.0, format="%.2f", step=1.00, key='bd2')
            
            submit_button = st.form_submit_button('Submit')

            if submit_button:
                with st.spinner('Processing...'):
                    make_prediction()
                    time.sleep(2)  # Simulate delay

    if __name__ == '__main__':
        display_form()

        final_prediction = st.session_state.get('prediction')
        final_probability = st.session_state.get('probability')

        if final_prediction is None:
            st.write('Predictions will be shown here:')
            st.divider()
        else:
            if final_prediction.lower() == 'positive':
                st.markdown(f'### ')
                st.markdown(f'## Probability: {final_probability:.2f}%')
            else:
                st.markdown(f'### Patient is unlikely to develop sepsis.')
                st.markdown(f'## Probability: {final_probability:.2f}%')
