# To Do List App

This application allows users to manage tasks, and create or join work teams in which specific tasks can be assigned to each member of the team.


## Features
#### Auth Module
  - Login/Register
  - Logout
  
#### Tasks Module
 - Add a task
 - Edit a task
 - Mark a task as completed
 - Remove a task
 
#### Team Module
 - Create a team
 - Join a team (with a valid code)
 - Assign task (Just the team user admin have this feature)
 - Leave a team (If team user admin leave the team, assigns admin role to the last user who joined the team; if no user remains in the team, it is removed.
 
## Technologies
  - Django
  - Javascript
  - Bootstrap

## Run app
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
## Why this app satisfies the requirements
Unlike the other projects, this final project involves more API services, in addition to having a more elaborate front end. It also has the characteristic of a single page application, thanks to the use of javascript, thus improving the user experience. Finally the application is fully responsive to mobile devices.

## Deployed App
- <https://todolistharv.herokuapp.com/>
 

