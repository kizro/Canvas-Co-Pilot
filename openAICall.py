from openai import OpenAI
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import config

#OpenAI API Key
client = OpenAI(api_key=config.API_KEY)


#Converts text file to string
def txtToString(file_name):
    file_path = file_name
    with open(file_path, 'r') as file:
        file_contents = file.read()
    
    return file_contents

#Dictionary of types of prompt data
prompt_dictionary = {"Assignments":txtToString("Assignments.txt"), "Announcements" : txtToString("Announcements.txt")}

userPrompt = '''Give me a list of my upcoming assignments for Data Structures and give me the most
recent annoucement for intro phys 1 workshop.
 '''

systemContent1 = '''You are an educational assistant. Return the word Assignments if the user asks for
information regarding their assignments. Return the word Announcements if the user asks for information
regarding their announcements. Return both words separated by a space if the user asks for both types of 
information.
'''

chatResponse1 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": systemContent1},
        {"role": "user", "content": userPrompt}
    ]
)

chatResponseFinal1 = chatResponse1.choices[0].message.content

print(chatResponseFinal1)

promptList = chatResponseFinal1.split()

systemContent2 = '''You are an educational assistant. 
    Use the following data to answer user query: \n'''

for x in promptList:

    systemContent2 = systemContent2 + prompt_dictionary[x] + "\n"

systemContent2 = systemContent2 + "This is the current time:" + str(datetime.now(ZoneInfo("America/New_York")))

chatResponse2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": systemContent2},
        {"role": "user", "content": userPrompt}
    ]
)

chatResponseFinal2 = chatResponse2.choices[0].message.content

print(chatResponseFinal2)

