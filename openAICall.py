from openai import OpenAI
import requests

#OpenAI API Key
client = OpenAI(api_key="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")


#Converts text file to string
def txtToString(file_name):
    file_path = file_name
    with open(file_path, 'r') as file:
        file_contents = file.read()
    
    return file_contents

#Dictionary of types of prompt data
prompt_dictionary = {"Assignments":txtToString("Assignments.txt")}

userPrompt = "Give me a list of my assignments for Intro to Entrepreneurship"

systemContent1 = '''You are an educational assistant. Return the word Assignments if the user asks for
information regarding their assignments.
'''

chatResponse1 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": systemContent1},
        {"role": "user", "content": userPrompt}
    ]
)

chatResponseFinal1 = chatResponse1.choices[0].message.content

systemContent2 = '''You are an educational assistant. 
Use the following data to answer user query: \n''' + prompt_dictionary[chatResponseFinal1] 

chatResponse2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": systemContent2},
        {"role": "user", "content": userPrompt}
    ]
)

chatResponseFinal2 = chatResponse2.choices[0].message.content

print(chatResponseFinal2)

