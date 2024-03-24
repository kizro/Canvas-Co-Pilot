# Canvas-Co-Pilot
CanvasCoPilot acts as a 24/7 AI assistant for school. It tells about assignments, deadlines, announcements, grades, and quizzes. Users can also ask it general questions. It's designed to make student's lives easier by saving time managing and planning their day. For example, every morning, students could ask CanvasCoPilot what they should focus on and prioritize for that day based on upcoming assignments and deadlines.

## Installation
1. Install the requirements
`pip install -r requirements.txt`
2. Log in to Canvas and go to Account > Settings.
3. In the Approved Integrations section, click + New Access Token.
4. Enter "Canvas Copilot" in the Purpose field. Leave the Expires field blank for unlimited time. Click Generate Token and copy the provided token.
5. In command prompt or terminal, copy the source files to your local directory
`git clone https://github.com/kizro/Canvas-Co-Pilot.git`
6. Go to the project directory
`cd Canvas-Co-Pilot`
7. Create and open config.py, and paste the line `CANVAS_API_KEY = '[your access token]'`
8. In command prompt or terminal, run the code:
`python3 main.py`
9. Open Google Chrome, click Extensions on the upper right corner, then click Manage Extensions. In the Extensions page, click Load Unpacked, and then select the Extensions folder inside the Canvas-Co-Pilot folder.
10. Open Canvas and you will see Canvas-Co-Pilot on the right side of the screen. Click the circle to expand it.

## Features
Currently, this Canvas extension can answer users' questions about their Assignments, Quizzes, Announcements, or Grades. 

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Credits
Tiara Allard

Steven Qian

Saad Fayyaz

Matthew Nguyen
