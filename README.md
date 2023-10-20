# UFC API Scrapper
## Overview

Using a combination of celery, requests and beautiful soup, the application scrape various website and API to try and recreate the content of ufcstats.com. You can then access this content in your own apps either by making another django app in the project if you want to make a django app, or externally using the django_rest API built in this project.

> **Warning**
Obviously this project will take some maintenance as the UFC website can change at any time, and the API can change as well. This project is not affiliated with the UFC in any way, and is not endorsed by them. It is simply a (dirty) way to try and recreate a UFC API to build apps with.
I will do my best to keep it up to date, if you encounter any issue using the project or if you have any suggestion, please open an issue on this github repository.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine to be able to run your own UFC API.

### Prerequisites
- Python 3.10+
- A message broker like RabbitMQ or Redis

### Installation
1. Clone the repository:
```bash
git clone https://github.com/NicoGGG/ufc-api-scrapper.git
```
2. Navigate to the project directory:
```bash
cd ufc-api-scrapper
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
4. Apply the migrations:
```bash
python manage.py migrate
```

### Running the Application

#### API

1. Start the Django development server:
```bash
python manage.py runserver
```
2. The application is now running and you can access the API at http://localhost:8000/.

#### Scraper
To scrape UFC data, execute a celery worker
```bash
celery -A ufcapi worker -B -l INFO
```

To customize the cron schedule, edit the `beat_schedule` variable in `ufcapi/celery.py`.
You can leave the celery worker running in the background, it will automatically scrape the data at the specified interval. This will ensure that the data is always up to date with the UFC website, and also ensure that it will retry every now and then if the scraping fails for some reason.

> **Note** 
The first time you run the scraper, you should scrape the fighters first in order to be able to scrape the fights.

> **Warning**
This can take a while, as the scraper needs to make a lot of requests to the UFC stats website and various API with rate limits.
