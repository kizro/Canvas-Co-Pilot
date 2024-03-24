# Functions used to fetch course details and writing to text files
import requests
from datetime import datetime, timedelta
import sqlite3

def get_course_assignments(filtered_courses, canvas_url, headers):
    # Connect to the SQLite database
    conn = sqlite3.connect('canvas_data.db')
    cursor = conn.cursor()

    for course in filtered_courses:
        course_id = course.get("id", "No ID")
        course_name = course.get("name", "No Name")
        assignments = []
        assignments_url = f'{canvas_url}/api/v1/courses/{course_id}/assignments'

        while assignments_url:
            assignments_response = requests.get(assignments_url, headers=headers)
            if assignments_response.status_code == 200:
                assignments.extend(assignments_response.json())
                assignments_url = assignments_response.links.get('next', {}).get('url')
            else:
                break

        for assignment in assignments:
            due_at = assignment.get('due_at', 'No due date')
            due_date, due_time, due_status, remaining_time = "No due date", "No due time", "No due date", "N/A"
            if due_at:
                due_date, due_time = due_at.split('T')
                due_date_time = datetime.strptime(due_at, '%Y-%m-%dT%H:%M:%SZ')
                current_time = datetime.utcnow()
                if current_time > due_date_time:
                    due_status = "Past due"
                else:
                    due_status = "Active"
            # Insert into database
            cursor.execute("INSERT INTO assignments (course, data_type, name, due_date, due_time, status) VALUES (?, ?, ?, ?, ?, ?)",
                           (course_name, "Assignment", assignment['name'], due_date, due_time, due_status))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def get_course_announcements(filtered_courses, canvas_url, headers):
    # Connect to the SQLite database
    conn = sqlite3.connect('canvas_data.db')
    cursor = conn.cursor()

    for course in filtered_courses:
        course_id = course.get("id", "No ID")
        course_name = course.get("name", "No Name")
        announcements = []
        announcements_url = f'{canvas_url}/api/v1/courses/{course_id}/discussion_topics?only_announcements=true'

        while announcements_url:
            announcements_response = requests.get(announcements_url, headers=headers)
            if announcements_response.status_code == 200:
                announcements.extend(announcements_response.json())
                announcements_url = announcements_response.links.get('next', {}).get('url')
            else:
                # If you want to handle failed API calls differently, adjust here
                print(f'Failed to retrieve announcements for course {course_name}. Status code: {announcements_response.status_code}')
                break

        for announcement in announcements:
            posted_at = announcement.get('posted_at', 'No posting date')
            post_date, post_time = "No posting date", "No posting time"
            if posted_at:
                post_date, post_time = posted_at.split('T')  # Split posted_at into date and time
            read_state = announcement.get('read_state', 'unknown')
            status = 'Unread' if read_state == 'unread' else 'Read'

            # Insert into database
            cursor.execute("INSERT INTO announcements (course, data_type, message, posted_date, posted_time, status) VALUES (?, ?, ?, ?, ?, ?)",
                           (course_name, "Announcement", announcement['title'], post_date, post_time, status))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def clear_files():
    filenames = [
        'Assignments.txt',
        'Announcements.txt',
    ]
    for filename in filenames:
        with open(filename, 'w') as file:
            file.write('')  # Write an empty string to clear the file