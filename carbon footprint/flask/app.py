from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import joblib

import re 
import google.generativeai as genai





# Load the ColumnTransformer
with open('cf.pkl', 'rb') as file:
    cf = pickle.load(file)

app = Flask(__name__)

# Load the first model (using joblib)
with open('model.joblib', 'rb') as f:
    model = joblib.load(f)

# Load the second model (using pickle)
with open('random_forest_model.pkl', 'rb') as f:
    model1 = joblib.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/options')
def options():
    return render_template('options.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@app.route('/individualfootprint')
def individualfootprint():
    return render_template('individualsurvey.html')

@app.route('/nationalfootprint')
def nationalfootprint():
    return render_template('nationalsurvey.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Set default values
    defaults = {
        'Recycling_Glass': False,
        'Recycling_Metal': 0,
        'Recycling_Plastic': 0,
        'Recycling_Paper': 0,
        'Cooking_With_Oven': False,
        'Cooking_With_Microwave': 0,
        'Cooking_With_Grill': 0,
        'Cooking_With_Airfryer': 0,
        'Cooking_With_Stove': 0
    }

    # Update defaults with actual user input
    data = {**defaults, **data}

    # Convert to DataFrame
    input_data = pd.DataFrame(data, index=[0])

    # Transform the input data and make prediction
    transformed_input = cf.transform(input_data)
    prediction = model.predict(transformed_input)
    
    GOOGLE_API_KEY = "AIzaSyC_Noz73FQAQxb4VrmW98RhFG81WbWX-2U"
    genai.configure(api_key=GOOGLE_API_KEY)
    genai_model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Clear and explicit prompt
    para_prompt = (
        "Based on the following data, provide 5 clear and concise suggestions "
        "to reduce carbon footprint. Please number the suggestions:"
    )
    
    input_prompt_str = str(input_data.to_dict(orient='records')[0])
    response = genai_model.generate_content(para_prompt + input_prompt_str)
    
    modified_text = re.sub(r'[\*\d]', '', response.text)
    points = modified_text.split('.')
    formatted_text = '\n'.join([point.strip() + '.' for point in points if point.strip()])
    
    print(formatted_text.encode('utf-8').decode('utf-8'))
    
    
    para_prompt2="give me the number of trees i owe to the enviornment based on the following info,just give me like a number, nothing else, no text nothing, just a number:"
    input_prompt_str2 = str(input_data.to_dict(orient='records')[0])
    response2 = genai_model.generate_content(para_prompt2 + input_prompt_str2)
    
    print(response2.text)
    
    return jsonify({'prediction': prediction[0], 'suggestions': formatted_text,'trees':response2.text})

@app.route('/predictnational', methods=['POST'])
def predictnational():
    data1 = request.json
    print("Received data:", data1) 
    
    # Convert to DataFrame
    input_data1 = pd.DataFrame(data1, index=[0])
    
    # Transform the input data and make prediction
   
    prediction1 = model1.predict(input_data1)
    
    GOOGLE_API_KEY = "AIzaSyC_Noz73FQAQxb4VrmW98RhFG81WbWX-2U"
    genai.configure(api_key=GOOGLE_API_KEY)
    genai_model = genai.GenerativeModel('gemini-1.5-flash')
    para_prompt = "provide me with some suggestions as to how carbon footprint can be reduced based on the data(its in percentage):(give me answer in only 5 points and nothing else, just 5 lines) the data is: cereal yeild, foreign district investment per gdp(in percentage), gross national income per capita, energy per capita, urbon population aggloration, protected area,population growth,uraban population groth percentage,"
    input_prompt_str = str(input_data1.to_dict(orient='records')[0])
    print(input_prompt_str)
    response = genai_model.generate_content(para_prompt + input_prompt_str)
    modified_text = re.sub(r'[\*\d]', '', response.text)
    points = modified_text.split('.')
    formatted_text = '\n'.join([point.strip() + '.' for point in points if point.strip()])
    
    print(formatted_text.encode('utf-8').decode('utf-8'))
    
    
    para_prompt2="give me the number of trees i owe to the enviornment based on the following info,just give me like a number, nothing else, no text nothing, just a number:"
    input_prompt_str2 = str(input_data1.to_dict(orient='records')[0])
    response2 = genai_model.generate_content(para_prompt2 + input_prompt_str2)
    
    print(response2.text)
    
    return jsonify({'prediction': prediction1[0], 'suggestions': formatted_text, 'trees' : response2.text})

if __name__ == '__main__':
    app.run(debug=True)
