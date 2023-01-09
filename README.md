# NASA API

## Installation:

- Create new dir and change your current dir to `project`:
```
mkdir proejct
cd project 
```
- Clone repository to `project` dir: 
```bash
git clone git@github.com:djeck1432/nasa_api.git
```
- If you want to run it out of docker, set up env environment:
```bash
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
```

## How to run
- Run docker build:
```bash
docker build -t nasa_image .
```
- Run docker image:
```bash
docker run -p 8000:8000 nasa_image
```
- Run without docker:
```bash
python manage.py runserver
```
## Set up ENV variables
1. In root folder:
```bash
touch .env 
```
2. Follow this [link](https://api.nasa.gov/) to sign up and create `api_key`
3. Add nasa `api key` to credentials via command
```bash
echo NASA_API_KEY=<your_api_key> >> .env
```

## How to run test

1. Go to root folder, where `manage.py` located
2. Run next command:
```bash
python manage.py test
```

## Test endpoint:
Once you run docker image, you can reach `objects` endpoint:
`http://0.0.0.0:8000/api/objects/?start_date=2022-01-10&end_date=2022-01-15`