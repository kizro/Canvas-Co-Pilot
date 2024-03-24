from openai import OpenAI
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import GetCourseDetail
import config as config
import os
from flask import Flask, request, render_template, session, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/prompt', methods=['GET', 'POST'])
def initial():
    # Your Canvas instance URL
    canvas_url = 'https://canvas.its.virginia.edu/'  # Change this to your Canvas instance URL
    # Your Canvas API access token
    access_token = '22119~CLb4HnemSSlWfgjg539RhvyoE7xfvgO3XGjQ9zbg7XQE4ylJ0pyWnwLrWtr1Au5V'  # Replace 'your_access_token' with your actual access token
    # The API endpoint for listing the current user's courses
    endpoint = '/api/v1/courses'
    # Parameters to fetch only actively enrolled courses
    params = {
        'enrollment_state': 'active',
        'per_page': 100  # Adjust based on how many courses you expect; helps with pagination
    }
    # Complete URL
    url = f'{canvas_url}{endpoint}'
    # Headers for the request, including the Authorization token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response 
        courses = response.json()
        # Filter courses by enrollment_term_id
        filtered_courses = [course for course in courses if course.get("enrollment_term_id") == 32]
    else:
        print(f'Failed to retrieve courses. Status code: {response.status_code}')
    # Get the user ID of the currently authenticated user
    user_response = requests.get(f'{canvas_url}/api/v1/users/self', headers=headers)
    if user_response.status_code == 200:
        user_id = user_response.json().get('id')
    else:
        print(f'Failed to retrieve user ID. Status code: {user_response.status_code}')
        user_id = None
    # Get course id and name
    for course in filtered_courses:
        course_id = course.get("id", "No ID")
        course_name = course.get("name", "No Name")

    data = request.get_json()
    userPrompt = data['message']

    #OpenAI API Key
    client = OpenAI(api_key=config.API_KEY)

    systemContent1 = '''You are an educational assistant. Return the word Assignments if the user asks for
    information regarding their assignments. Return the word Announcements if the user asks for information
    regarding their announcements. Return both words separated by a space if the user asks for both types of 
    information. Return the word Announcements if the user asks for anything similiar to the following:
    "Give me a list of all my course names." "List my courses." Return the word General if the user asks a general question
    that does not require specific information about their courses, assgnments, or announcements.
    
    '''
    chatResponse1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemContent1},
            {"role": "user", "content": userPrompt}
        ]
    )

    chatResponseFinal1 = chatResponse1.choices[0].message.content

    GetCourseDetail.clear_files()


    if "Assignments" in chatResponseFinal1:
        GetCourseDetail.get_course_assignments(filtered_courses, canvas_url, headers)

    if "Announcements" in chatResponseFinal1:
        GetCourseDetail.get_course_announcements(filtered_courses, canvas_url, headers)

    if "General" in chatResponseFinal1:
        # This section handles general queries by directly sending them to OpenAI's API
        general_query_system_content = "You are a knowledgeable assistant. Please provide helpful and informative responses to user queries."
        general_query_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": general_query_system_content},
                {"role": "user", "content": userPrompt}
            ]
        )
        
        # Extract the response from OpenAI's completion
        general_query_final_response = general_query_response.choices[0].message.content
        
        # You can now return this response directly to the frontend
        return jsonify({"response": general_query_final_response})
        


    #Converts text file to string
    def txtToString(file_name):
        file_path = file_name
        with open(file_path, 'r') as file:
            file_contents = file.read()
        
        return file_contents
    #Dictionary of types of prompt data
    prompt_dictionary = {"Assignments":txtToString("Assignments.txt"), "Announcements" : txtToString("Announcements.txt")}


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

    return jsonify({"response": chatResponseFinal2})


if __name__ == '__main__':
    app.run(debug=True,port=6524)