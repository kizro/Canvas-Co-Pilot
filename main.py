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
import sqlite3

app = Flask(__name__)
CORS(app) 

@app.route('/', methods=['GET', 'POST'])
def initial():

    canvas_url = 'https://canvas.its.virginia.edu/' 

    access_token = config.CANVAS_API_KEY

    endpoint = '/api/v1/courses'

    params = {
        'enrollment_state': 'active',
        'per_page': 100 
    }

    url = f'{canvas_url}{endpoint}'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:

        courses = response.json()

        filtered_courses = [course for course in courses if course.get("enrollment_term_id") == 32]
    else:
        print(f'Failed to retrieve courses. Status code: {response.status_code}')

    user_response = requests.get(f'{canvas_url}/api/v1/users/self', headers=headers)
    if user_response.status_code == 200:
        user_id = user_response.json().get('id')
    else:
        print(f'Failed to retrieve user ID. Status code: {user_response.status_code}')
        user_id = None

    for course in filtered_courses:
        course_id = course.get("id", "No ID")
        course_name = course.get("name", "No Name")
    
    conn = sqlite3.connect('canvas_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT,
        data_type TEXT,
        name TEXT,
        due_date TEXT,
        due_time TEXT,
        status TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT,
        data_type TEXT,
        message TEXT,
        posted_date TEXT,
        posted_time TEXT,
        status TEXT
    );
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT,
                group_name TEXT,
                assignment_name TEXT,
                score REAL,
                points_possible REAL
            );
        ''')

    conn.commit()

    cursor.execute(f'SELECT COUNT(*) FROM {"grades"}')
    row_count = cursor.fetchone()[0]

    conn.close()


    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        cursor.execute(f"DELETE FROM {table[0]};")

    conn.commit()
    conn.close()


    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chatResponse TEXT,
        userQuery TEXT
    );
    ''')

    conn.commit()
    conn.close()

    if (row_count<1):
        GetCourseDetail.get_course_assignments(filtered_courses, canvas_url, headers)
        GetCourseDetail.get_course_announcements(filtered_courses, canvas_url, headers)
        GetCourseDetail.get_course_grades(filtered_courses, canvas_url, headers)

@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    #OpenAI API Key
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    data = request.get_json()
    userPrompt = data['message']


    systemContent2 = '''You are an educational assistant chatbot. 
        Use the following data to answer user query. Please format the answer in an easy to read way. Avoid overuse of asteriks and symbols. 
        For example instead of 1. **Homework Set 3** - **Due Date:** February 27, 2024 at 22:00:00 UTC - **Status:** it would be better to write
        Homework Set 3 is due on Feb 27, 2024 at 22:00:00 UTC. Here are the user's assignments by course: \n'''

    database_path = 'canvas_data.db'
    table_name = "assignments"

    conn = sqlite3.connect(database_path)

    cur = conn.cursor()

    sql_query = f'SELECT * FROM {table_name}'

    cur.execute(sql_query)

    rows = cur.fetchall()

    formatted_results = ""

    for row in rows:
        concatenated_row = ' '.join(map(str, row)) 
        formatted_results += concatenated_row + "\n"

    conn.commit()
    conn.close()

    systemContent2 = systemContent2 + "Course Data_Type Name Due_Date Due_Time Status" + formatted_results 

    
    table_name = "announcements"

    conn = sqlite3.connect(database_path)

    cur = conn.cursor()

    sql_query = f'SELECT * FROM {table_name}'

    cur.execute(sql_query)

    rows = cur.fetchall()

    formatted_results = ""

    for row in rows:
        concatenated_row = ' '.join(map(str, row)) 
        formatted_results += concatenated_row + "\n"
    
    conn.commit()
    conn.close()

    systemContent2 = systemContent2 + "Here are the user's announcements by course:" + "Course Data_Type Message Posted_Date Posted_Time Status" + formatted_results 

    table_name = "grades"

    conn = sqlite3.connect(database_path)

    cur = conn.cursor()

    sql_query = f'SELECT * FROM {table_name}'

    cur.execute(sql_query)

    rows = cur.fetchall()

    formatted_results = ""

    for row in rows:
        concatenated_row = ' '.join(map(str, row)) 
        formatted_results += concatenated_row + "\n"
    
    conn.commit()
    conn.close()

    systemContent2 = systemContent2 + "Here is the user's grade data by course:" + "course_name group_name group_weight assignment_name points_recieved points_possible" +formatted_results
    
    systemContent2 = systemContent2 + '''If the user asks for their score/grade, simply compute points_recieved divided bypoints_possible. Follow
    the same answer format for similiar queries: If a user asks: "What grade did i recieve on pSet1 for FODL, you should return 80.0/80.0. 
    If the user asks for assignments, you must give them assignments. If they ask for announcements, you must give them announcements. 
    If the user does not need information about their courses, simply answer their general questions. When a user asks for the most
    recent assignment sort by the due date. For announcements, sort by the post date and'''

    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute(f'SELECT {"chatResponse"} FROM {"responses"}')

    rows = cursor.fetchall()

    chatResponses = '\n'.join([str(row[0]) for row in rows])

    print(chatResponses)

    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute(f'SELECT {"userQuery"} FROM {"responses"}')

    rows = cursor.fetchall()

    userQueries = '\n'.join([str(row[0]) for row in rows])

    systemContent2 = systemContent2 + "This is the current time:" + str(datetime.now(ZoneInfo("America/New_York"))) + ''' use this 
    to help you answer queries (especially those regarding most recent things).''' + '''\n Here are previous user queries: ''' + userQueries + ''' 
    use this to help you answer queries.''' + ''' \n Here are your previous responses:''' + chatResponses + " use this to help you answer queries."

    chatResponse2 = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": systemContent2},
            {"role": "user", "content": userPrompt}
        ]
    )

    chatResponseFinal2 = chatResponse2.choices[0].message.content

    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO responses (chatResponse, userQuery) VALUES (? , ?)", (chatResponseFinal2, userPrompt))

    conn.commit()
    conn.close()

    return jsonify({"response": chatResponseFinal2})


if __name__ == '__main__':
    app.run(debug=True,port=6524)