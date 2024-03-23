import requests

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

    # Print each course
    for course in filtered_courses:
        course_id = course.get("id", "No ID")
        course_name = course.get("name", "No Name")
        enrollment_term_id = course.get("enrollment_term_id", "No Term ID")
        print(f'Course ID: {course_id}, Name: {course_name}, TermID: {enrollment_term_id}')

else:
    print(f'Failed to retrieve courses. Status code: {response.status_code}')
