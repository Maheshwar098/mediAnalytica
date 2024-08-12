# MediAnalytica

A website designed to connect patients with corresponding medical staff intelligently leveraging ML

### Setup

```
git clone https://github.com/Maheshwar098/mediAnalytica.git
cd mediAnalytica
python -m venv .venv
venv/Scripts/Activate
pip install -r requirements.txt
python manage.py createsuperuser
```

### ReRun Training Pipeline on new Data 
```
cd mediAnalytica
venv/Scripts/Activate
python train/train.py
```

### Run Server
```
cd mediAnalytica
venv/Scripts/Activate
python manage.py runserver
```
