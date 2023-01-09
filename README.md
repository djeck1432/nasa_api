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
- Run docker build:
```bash
docker build -t nasa_image .
```
- Run docker image:
```bash
docker run -p 8000:8000 nasa_image
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