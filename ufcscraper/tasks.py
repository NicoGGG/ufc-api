from celery import shared_task
from django.db import OperationalError
from ufcscraper.models import Event, Fighter, Fight
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

from ufcscraper.scrapers import get_fighter_photo_url, scrap_fights_from_event


# saving function for fights
@shared_task(serializer="json")
def save_all_fights_from_event(fights, event_id: str):
    for fight in fights:
        Fight.objects.update_or_create(
            fight_id=fight["fight_id"],
            defaults={
                "event": Event.objects.get(event_id=event_id),
                "link": fight["fight_link"],
                "fighter_one": Fighter.objects.get(fighter_id=fight["fighter1"]),
                "fighter_two": Fighter.objects.get(fighter_id=fight["fighter2"]),
                "weight_class": fight["weight_class"],
                "method": fight["method"],
                "round": fight["round"],
                "time": fight["time"],
                "belt": fight["belt"],
                "bonus": fight["bonus"],
                "wl_fighter_one": fight["wl_fighter1"],
                "wl_fighter_two": fight["wl_fighter2"],
            },
        )
    return print(f"Fights from event {event_id} saved")


# scraping function for fights in an event
@shared_task(
    bind=True,
    autoretry_for=(OperationalError, requests.RequestException),
    rate_limit="10/s",
    retry_kwargs={"max_retries": 5},
)
def scrape_ufc_event_fights(self, event_id: str):
    url = f"http://ufcstats.com/event-details/{event_id}"
    try:
        page = requests.get(url)
        if page.status_code != 200:
            print(
                f"Error scraping fights from event {event_id}. Error code: {page.status_code}"
            )
            raise requests.RequestException(
                f"Error scraping fights from event {event_id}. Status code: {page.status_code}"
            )
        fight_list = scrap_fights_from_event(page.content, event_id)
    except Exception as exc:
        raise self.retry(exc=exc)
    return save_all_fights_from_event(fight_list, event_id)


# saving function for events
@shared_task(serializer="json")
def save_events(events):
    for event in events:
        Event.objects.update_or_create(
            event_id=event["event_id"],
            defaults={
                "name": event["name"],
                "link": event["link"],
                "date": event["date"],
                "type": event["type"],
                "location": event["location"],
                "upcoming": event["upcoming"],
                "completed": event["completed"],
            },
        )
        print("Saving fights from event", event["event_id"])
        scrape_ufc_event_fights.delay(event["event_id"])  # type: ignore
    return print("Events saved")


# saving function for fighters
@shared_task(serializer="json")
def save_fighters(fighters):
    for fighter in fighters:
        Fighter.objects.update_or_create(
            fighter_id=fighter["fighter_id"],
            defaults={
                "first_name": fighter["first_name"],
                "last_name": fighter["last_name"],
                "nickname": fighter["nickname"],
                "link": fighter["link"],
                "height": fighter["height"],
                "weight": fighter["weight"],
                "reach": fighter["reach"],
                "stance": fighter["stance"],
                "belt": fighter["belt"],
                "win": fighter["win"],
                "loss": fighter["loss"],
                "draw": fighter["draw"],
                "photo_url": fighter["photo_url"],
            },
        )
    return print("Fighters saved")


# scraping function for fighters
@shared_task
def scrape_all_ufc_fighters():
    fighter_list = []
    chars = "abcdefghijklmnopqrstuvwxyz"
    for char in chars:
        url = f"http://ufcstats.com/statistics/fighters?char={char}&page=all"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", class_="b-statistics__table")
        rows_body = table.find("tbody")  # type: ignore
        rows = rows_body.find_all("tr")  # type: ignore
        # pop the first row because it is an empty line for some reason
        rows.pop(0)
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 0:
                first_name = cells[0].text.strip()
                last_name = cells[1].text.strip()
                nickname = cells[2].text.strip()
                link = cells[0].find("a")["href"]
                fighter_id = link.split("/")[-1]
                height = cells[3].text.strip()
                weight = cells[4].text.strip()
                reach = cells[5].text.strip()
                stance = cells[6].text.strip()
                win = cells[7].text.strip()
                loss = cells[8].text.strip()
                draw = cells[9].text.strip()
                belt = cells[10].find("img", class_="b-list__icon") is not None
                photo_page = requests.get(
                    f"https://liveapi.yext.com/v2/accounts/me/answers/vertical/query?experienceKey=answers-en&api_key=850a88aeb3c29599ce2db46832aa229f&v=20220511&version=PRODUCTION&locale=en&input={first_name}+{last_name}&verticalKey=athletes&limit=21&offset=0&retrieveFacets=true&facetFilters=%7B%7D&session_id=3ed6799e-6cad-46ea-9137-d9bd11417549&sessionTrackingEnabled=true&sortBys=%5B%5D&referrerPageUrl=https%3A%2F%2Fwww.ufc.com%2F&source=STANDARD&jsLibVersion=v1.14.3"
                )
                fighter = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "nickname": nickname,
                    "link": link,
                    "fighter_id": fighter_id,
                    "height": height,
                    "weight": weight,
                    "reach": reach,
                    "stance": stance,
                    "win": win,
                    "loss": loss,
                    "draw": draw,
                    "belt": belt,
                }
                photo_url = get_fighter_photo_url(photo_page, fighter)
                fighter["photo_url"] = photo_url
                fighter_list.append(fighter)
    return save_fighters(fighter_list)


# scraping function for events
@shared_task
def scrape_all_ufc_events():
    event_list = []
    url = "http://ufcstats.com/statistics/events/completed?page=all"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", class_="b-statistics__table-events")

    rows_body = table.find("tbody")  # type: ignore
    rows = rows_body.find_all("tr")  # type: ignore
    # pop the first row because it is an empty line for some reason
    rows.pop(0)
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            name = cells[0].find("a").text.strip()
            link = cells[0].find("a")["href"]
            event_id = link.split("/")[-1]
            date = cells[0].find("span", class_="b-statistics__date").text.strip()
            type = "Fight Night" if "Fight Night" in name else "UFC"
            location = cells[1].text.strip()
            upcoming = cells[0].find("img", class_="b-statistics__icon") is not None
            event = {
                "name": name,
                "link": link,
                "event_id": event_id,
                "date": datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d"),
                "type": type,
                "location": location,
                "upcoming": upcoming,
                "completed": True if not upcoming else False,
            }
            event_list.append(event)
    # sort by date to maintain a consistent order of event ids between the initial scraping and the following ones.
    event_list = sorted(event_list, key=lambda k: k["date"])
    return save_events(event_list)
