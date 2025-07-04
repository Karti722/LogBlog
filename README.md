# Getting started developer guide
# In the terminal, do the following:
1) clone this repo from github
2) Navigate to the root of the project, create a python virtual env called logenv("python -m venv logvenv")
3) Add the venv to the .gitignore
4) Navigate to the backend root directory and pip install dependencies after navigating to the root backend folder through requirements.txt
5) add a .env file in this directory for supabase connection
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
6) Run this command ("python manage.py runserver")
7) Congratulations, you finished the backend setup! 
# On a separate terminal do the following:
1) Navigate to the frontend folder and type "npm i" to install dependencies
2) Add a .env file for supabase on client side:
REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here
1) Run this command ("npm run dev") 

