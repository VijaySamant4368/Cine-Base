@echo off

mkdir templates
mkdir assets
mkdir static

:: Add the following to the app.py file

echo from flask import Flask, render_template, request, redirect, url_for > ./app.py
echo. >> ./app.py
echo app = Flask(__name__) >> ./app.py
echo. >> ./app.py
echo @app.route('/') >> ./app.py
echo def home(): >> ./app.py
echo     return render_template('index.html') >> ./app.py
echo. >> ./app.py
echo @app.route('/submit', methods=['POST']) >> ./app.py
echo def submit(): >> ./app.py
echo     # Handle form submission >> ./app.py
echo     name = request.form.get('name') >> ./app.py
echo     return redirect(url_for('home')) >> ./app.py
echo. >> ./app.py
echo if __name__ == '__main__': >> ./app.py
echo     app.run(debug=True) >> ./app.py
echo. >> ./app.py

:: Add the following to the utils.py file

nul > ./utils.py

:: Add the following to the requirements.txt file
echo Flask==2.0.2 > ./requirements.txt

cd templates

:: Add the following to the index.html file
echo ^<!DOCTYPE html^> > ./index.html
echo ^<html lang="en"^> >> ./index.html
echo ^<head^>   >> ./index.html
echo     ^<meta charset="UTF-8"^>   >> ./index.html
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>   >> ./index.html
echp     ^<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"^>  >> ./index.html
echo     ^<title^>Flask App^</title^>   >> ./index.html
echo ^</head^>  >> ./index.html
echo ^<body^>   >> ./index.html
echo     ^<h1^>Welcome to Flask^</h1^>  >> ./index.html
echo     ^<form method="POST" action="{{ url_for('submit') }}"^>    >> ./index.html
echo         ^<label for="name"^>Enter your name:^</label^> >> ./index.html
echo         ^<input type="text" id="name" name="name"^>    >> ./index.html
echo         ^<button type="submit"^>Submit^</button^>  >> ./index.html
echo     ^</form^>  >> ./index.html
echo     ^<script src="{{ url_for('static', filename='js/script.js') }}"^>^</script^>
echo ^</body^>  >> ./index.html
echo ^</html^>  >> ./index.html


cd ../static
mkdir js
mkdir css
cd css
nul > ./style.css

:: Add the following to the style.css file
echo body { >> style.css
echo     font-family: Arial, sans-serif; >> style.css
echo } >> style.css
echo.  >> style.css
echo h1 { >> style.css
echo     color: blue; >> style.css
echo } >> style.css


cd ../js
nul > ./script.js
echo document.addEventListener('DOMContentLoaded', function() { >> script.js
echo     console.log('JavaScript loaded!'); >> script.js
echo }); >> script.js
