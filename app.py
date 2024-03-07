import streamlit as st
import pandas as pd
import joblib

# Load the diabetes prediction model
model = joblib.load("diabetes_prediction2.pkl")

# Function to make predictions
def predict_diabetes(input_data):
    return model.predict(input_data)

# Mapping of categorical labels to integer values
genhlth_mapping = {
    'Excellent': 1,
    'Very Good': 2,
    'Good': 3,
    'Fair': 4,
    'Poor': 5
}

# Reverse mapping of integer values to categorical labels
genhlth_reverse_mapping = {v: k for k, v in genhlth_mapping.items()}

# Create a Streamlit web application
def main():
    st.title("Diabetes Health Indicator")

    # Create a sidebar
    st.sidebar.title('BMI Calculator (KG)')

    # Add a BMI calculator with height and weight inputs
    height = st.sidebar.number_input('Enter your height in cm', min_value=0.0)
    weight = st.sidebar.number_input('Enter your weight in KG', min_value=0.0)

    # Add a button to calculate BMI
    if st.sidebar.button('Calculate BMI'):
        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        st.sidebar.info(f'Your BMI: {bmi:.2f}')

    # Input columns and corresponding questions
    columns = [
        ("HighBP", "Have you ever been diagnosed with high blood pressure?"),
        ("HighChol", "Do you have high cholesterol levels?"),
        ("BMI", "What is your current BMI?"),
        ("Smoker", "Are you a smoker or have you smoked in the past?"),
        ("Stroke", "Have you ever experienced a stroke?"),
        ("HeartDiseaseorAttack", "Have you been diagnosed with heart disease or suffered a heart attack?"),
        ("PhysActivity", "How often do you engage in physical activities?"),
        ("HvyAlcoholConsump", "Do you consume alcohol heavily?"),
        ("DiffWalk", "Do you experience difficulty walking?"),
        ("Sex", "Are you male or female?"),
        ("Age", "What is your age?")
    ]

    # Create input form
    input_form = {}

    # Input form for general questions
    for column, question in columns[:9]:
        if column.lower() != 'age':
            if column.lower() != 'sex' and column.lower() != 'bmi':
                input_form[column] = st.radio(question, ['Yes', 'No'], index=None)
            elif column.lower() == 'bmi':
                input_form[column] = st.slider(question, 18.0, 50.0, step=0.1, value=18.0)
    
    # Input form for sex
    input_form['Sex'] = st.selectbox("Are you male or female?", ['Male', 'Female'], index=None)

    # Add new question for overall health
    selected_genhlth = st.selectbox("How is your overall health?", ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor'], index=None)
    input_form['GenHlth'] = genhlth_mapping.get(selected_genhlth, 0)

    # Display age information in an expander section
    with st.expander("ℹ️ Age Information"):
        age_info_table = {
            "Code": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            "Age Range": [
                "18-24 years old", "25-29 years old", "30-34 years old",
                "35-39 years old", "40-44 years old", "45-49 years old",
                "50-54 years old", "55-59 years old", "60-64 years old",
                "65-69 years old", "70-74 years old", "75-79 years old",
                "80 years old or older"
            ]
        }
        age_info_df = pd.DataFrame(age_info_table)
        st.table(age_info_df.style.set_properties(**{'text-align': 'left'}))

    # Input form for age
    input_form['Age'] = st.selectbox("What is your age?", [i for i in range(1, 13)], index=None)

    # Submit button
    if st.button("Submit"):
        # Check if all required fields are filled in
        if '' in input_form.values():
            st.error("Fill in all the values for better prediction.")
        else:
            # Convert inputs to DataFrame
            input_data = pd.DataFrame([input_form])

            # Reorder columns to match model's feature order
            input_data = input_data[['HighBP', 'HighChol', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack',
                                    'PhysActivity', 'HvyAlcoholConsump', 'GenHlth', 'DiffWalk', 'Sex', 'Age']]

            # Map 'Yes'/'No' and 'Male'/'Female' to 1/0
            input_data.replace({'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0}, inplace=True)

            # Perform diabetes prediction
            prediction = predict_diabetes(input_data)

            # Display output
            st.subheader("Diabetes Prediction:")
            if prediction[0] == 1:
                st.error("The person is predicted to be diabetic.")
            else:
                st.success("The person is predicted to be non-diabetic.")

# Run the application
if __name__ == "__main__":
    main()
