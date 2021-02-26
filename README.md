# Identrics API Development
## Installation

### Prerequisites
Python version >=3.7.4 installed. Check can be performed by running ```python --version``` in terminal.

### Dependencies
To be able to develop and run the Flask application, the dependencies from the ```requirements.txt``` need to be installed either on the system installation of Python, or on a virtual environment:

---- Jupyter Notebook Functionality
```bash
pip install -r requirementsNotebook.txt
```

---- API Functionality
```bash
pip install -r requirementsApi.txt
```

## Running
To serve the Flask application, go to the folder containing ```api.py``` and run:
```bash
python api.py
```

## Application Overview
![ContextDiagram]

## API Usage
### Get Character Info
URL: <b><i><your_host>/api/character/info?name=<character_name></i></b>\
Example: http://127.0.0.1:5000/api/character/info?name=Dante \
Returns: 
- <i>Successful</i> : JSON object containing character info, 200 
- <i>Unsuccessful</i> : JSON object containing error message, 400/404 

### Get Main Characters
URL: <b><i><your_host>/api/character/main</i></b>\
Example: http://127.0.0.1:5000/api/character/main \
Returns: 
- <i>Successful</i> : JSON object containing main characters (rank 1) info, 200 

### Get Support Characters
URL: <b><i><your_host>/api/character/support</i></b>\
Example: http://127.0.0.1:5000/api/character/support \
Returns: 
- <i>Successful</i> : JSON object containing support characters (rank 2) info, 200 

### Get Episode Characters
URL: <b><i><your_host>/api/character/episode</i></b>\
Example: http://127.0.0.1:5000/api/character/episode \
Returns: 
- <i>Successful</i> : JSON object containing episode characters (rank 3) info, 200 

### Get Character Mentions
URL: <b><i><your_host>/api/character/mentions?name=<character_name></i></b>\
Example: http://127.0.0.1:5000/api/character/mentions?name=Dante \
Returns: 
- <i>Successful</i> : JSON object containing all sentences where the character's name is mentioned, 200. If no name is specified in the url, the API returns a JSON object containing all sentences in which main characters (rank 1) are mentioned.
- <i>Unsuccessful</i> : JSON object containing error message, 404 

### Get Characters Comentions
URL:  
<b><i><your_host>/api/character/comentions?name_a=<character_name>&name_b=<character_name></i></b>\
Example: http://127.0.0.1:5000/api/character/comentions?name_a=Dante&name_b=Charles \
Returns: 
- <i>Successful</i> : JSON object containing all sentences where the characters are mentioned together, if there are any, 200 
- <i>Unsuccessful</i> : JSON object containing error message, 400/404 


## Bonus API Usage
### Get Book Information Using ISBN
URL: <b><i><your_host>/api/book/info?isbn=<isbn_number></i></b>\
Example: http://127.0.0.1:5000/api/book/info?isbn=0142437344 \
Returns: 
- <i>Successful</i> : JSON object containing book info, 200 
- <i>Unsuccessful</i> : JSON object containing error message, 400/404 


[ContextDiagram]: context_diagram.jpg
