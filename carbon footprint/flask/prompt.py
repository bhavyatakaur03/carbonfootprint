import google.generativeai as genai

# Configure the API key
GOOGLE_API_KEY = "AIzaSyDJOtHLImQFBi_HKp7oqukOiL86SeX8Nq4"
genai.configure(api_key=GOOGLE_API_KEY)

# Specify the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Define the prompt and input prompt
para_prompt = "provide me with some recipes I will give you the ingredients and just give the recipes"
input_prompt = "beans, mushroom, carrot, pasta"

# Generate the response using the model
response = model.generate_content(para_prompt+input_prompt)

# Replace '' and '*' with '->'
modified_text = response.text.replace('*', '\n')

# Print the modified response text, ensuring correct encoding
print(modified_text.encode('utf-8').decode('utf-8'))