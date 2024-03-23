import requests
import config 

# Your Canvas instance URL
canvas_url = 'https://canvas.its.virginia.edu/'  # Change this to your Canvas instance URL

# Your Canvas API access token
access_token = config.API_KEY  

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


# Open a text file to write the course and assignment information
with open('Course_Assignment.txt', 'w') as file:
    for course in filtered_courses:
        course_id = course.get("id", "No ID")
        course_name = course.get("name", "No Name")

        # Fetch assignments for the course
        assignments_endpoint = f'/api/v1/courses/{course_id}/assignments'
        assignments_url = f'{canvas_url}{assignments_endpoint}'

        assignments_response = requests.get(assignments_url, headers=headers)

        if assignments_response.status_code == 200:
            assignments = assignments_response.json()
            file.write(f'Course: {course_name} (ID: {course_id})\n')
            for assignment in assignments:
                file.write(f"  - Assignment: {assignment['name']}, Due: {assignment.get('due_at', 'No due date')}\n")
        else:
            file.write(f'Failed to retrieve assignments for course {course_name}. Status code: {assignments_response.status_code}\n')
