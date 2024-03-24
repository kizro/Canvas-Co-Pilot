# Functions used to fetch course details and writing to text files
import requests
from datetime import datetime, timedelta


def get_course_assignments(filtered_courses, canvas_url, headers):
    with open('Assignments.txt', 'w') as file:
        for course in filtered_courses:
            course_id = course.get("id", "No ID")
            course_name = course.get("name", "No Name")

            # Initialize variables for pagination
            assignments = []
            assignments_url = f'{canvas_url}/api/v1/courses/{course_id}/assignments'

            # Fetch all pages of assignments for the course
            while assignments_url:
                assignments_response = requests.get(assignments_url, headers=headers)
                if assignments_response.status_code == 200:
                    assignments.extend(assignments_response.json())
                    # Check for the 'next' link in the response headers to get the URL for the next page
                    assignments_url = assignments_response.links.get('next', {}).get('url')
                else:
                    file.write(f'Failed to retrieve assignments for course {course_name}. Status code: {assignments_response.status_code}\n')
                    break  # Exit the loop if there's an error

            # Write assignments to the file
            file.write(f'Course: {course_name} (ID: {course_id})\n')
            if not assignments:
                file.write("  - This course doesn't have any assignments yet.\n")
            else:
                for assignment in assignments:
                    due_at = assignment.get('due_at', 'No due date')
                    if due_at:
                        due_date, due_time = due_at.split('T')  # Split due_at into date and time
                        due_date_time = datetime.strptime(due_at, '%Y-%m-%dT%H:%M:%SZ')
                        current_time = datetime.utcnow()
                        if current_time > due_date_time:
                            due_status = "Past due"
                            remaining_time = "N/A"
                        else:
                            due_status = "Active"
                            remaining_delta = due_date_time - current_time
                            days = remaining_delta.days
                            hours, remainder = divmod(remaining_delta.seconds, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            remaining_time = f"{days} days, {hours} hours, {minutes} minutes"
                    else:
                        due_date = "No due date"
                        due_time = "No due time"
                        due_status = "No due date"
                        remaining_time = "N/A"

                    file.write(f"  - Assignment: {assignment['name']} | Due Date: {due_date} | Due Time: {due_time} | Status: {due_status} | Remaining Time: {remaining_time}\n")



def get_course_announcements(filtered_courses, canvas_url, headers):
    with open('Announcements.txt', 'w') as file:
        for course in filtered_courses:
            course_id = course.get("id", "No ID")
            course_name = course.get("name", "No Name")

            # Initialize variables for pagination
            announcements = []
            announcements_url = f'{canvas_url}/api/v1/courses/{course_id}/discussion_topics?only_announcements=true'

            # Fetch all pages of announcements for the course
            while announcements_url:
                announcements_response = requests.get(announcements_url, headers=headers)
                if announcements_response.status_code == 200:
                    announcements.extend(announcements_response.json())
                    # Check for the 'next' link in the response headers to get the URL for the next page
                    announcements_url = announcements_response.links.get('next', {}).get('url')
                else:
                    file.write(f'Failed to retrieve announcements for course {course_name}. Status code: {announcements_response.status_code}\n')
                    break  # Exit the loop if there's an error

            # Write announcements to the file
            file.write(f'Course: {course_name} (ID: {course_id})\n')
            if not announcements:
                file.write("  - This course doesn't have any announcements yet.\n")
            else:
                for announcement in announcements:
                    posted_at = announcement.get('posted_at', 'No posting date')
                    if posted_at:
                        post_date, post_time = posted_at.split('T')  # Split posted_at into date and time
                    else:
                        post_date = "No posting date"
                        post_time = "No posting time"

                    # Check if the announcement is new or read
                    read_state = announcement.get('read_state', 'unknown')
                    if read_state == 'unread':
                        status = 'Unread'
                    else:
                        status = 'Read'

                    file.write(f"  - Announcement: {announcement['title']} | Posted Date: {post_date} | Posted Time: {post_time} | Status: {status}\n")


def clear_files():
    filenames = [
        'Assignments.txt',
        'Announcements.txt',
    ]
    for filename in filenames:
        with open(filename, 'w') as file:
            file.write('')  # Write an empty string to clear the file