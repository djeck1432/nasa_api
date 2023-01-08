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
- Run docker-compose:
```
docker-compose up -d
```
- Stop docker-compose:
```bash
docker-compose down
```

## How to run test

1. Go to root folder, where `manage.py` located
2. Run next command:
```bash
python manage.py test
```