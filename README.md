
## Installation

```bash
git clone git@github.com:iroman-d/VacationManager.git
```

Inside project directory create virtual environment

```bash
virtalenv venv
```
activate virtual environment
```bash 
source venv/bin/activate
```
install requirements
```bash 
pip install -r requirements.txt
```
## Development
create migrations 
```bash 
python manage.py makemigrations
```
run migrations 
```bash 
python manage.py migrate
```
run server
 ```bash 
python manage.py runserver
```
