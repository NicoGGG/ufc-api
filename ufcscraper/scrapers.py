from bs4 import BeautifulSoup

from ufcscraper.models import Fighter


def get_fighter_photo_url(page, fighter: dict):
    try:
        photo_url = page.json()["response"]["results"][0]["data"]["c_photo"]["url"]
    except Exception:
        print(
            f"No photo found for fighter {fighter['fighter_id']} ({fighter['first_name']} {fighter['last_name']})"
        )
        photo_url = (
            "https://www.ufc.com/themes/custom/ufc/assets/img/no-profile-image.png"
        )
    return photo_url


def convert_to_int(s):
    try:
        return int(s)
    except ValueError:
        return 0  # or return 0, or any default value


def scrap_fights_from_event(event_fights_html, event_id):
    fight_list = []
    soup = BeautifulSoup(event_fights_html, "html.parser")
    table = soup.find("table", class_="b-fight-details__table")
    rows_body = table.find("tbody")  # type: ignore
    rows = rows_body.find_all("tr")  # type: ignore
    for row in rows:
        fight_link = row["data-link"]
        fight_id = fight_link.split("/")[-1]
        cells = row.find_all("td")
        if len(cells) > 0:
            fighters = cells[1].find_all("p")
            fighter1_id = fighters[0].find("a")["href"].split("/")[-1]
            fighter2_id = fighters[1].find("a")["href"].split("/")[-1]
            # Belt and bonus are not always present but they are always in the same cell as weight class
            weight_class = cells[6].text.strip()
            belt_and_bonus = [
                x["src"].split("/")[-1].split(".")[0] for x in cells[6].find_all("img")
            ]
            belt = "belt" in belt_and_bonus
            bonus = next((x.capitalize() for x in belt_and_bonus if x != "belt"), None)
            method = cells[7].text.strip().split("\n")[0]
            round = convert_to_int(cells[8].text.strip())
            time = cells[9].text.strip()
            wl = cells[0].find_all("i", class_="b-flag__text")
            wl_fighter1 = None
            wl_fighter2 = None
            if wl and len(wl) > 1:
                wl_fighter1 = wl[0].text.strip().upper()
                wl_fighter2 = wl[1].text.strip().upper()
            elif wl and len(wl) > 0:
                wl_fighter1 = "W" if wl[0].text.strip() == "win" else "L"
                wl_fighter2 = "L" if wl_fighter1 == "W" else "W"
            fight = {
                "event": event_id,
                "fight_id": fight_id,
                "fight_link": fight_link,
                "fighter1": fighter1_id,
                "fighter2": fighter2_id,
                "weight_class": weight_class,
                "method": method,
                "round": round,
                "time": time,
                "belt": belt,
                "bonus": bonus,
                "wl_fighter1": wl_fighter1,
                "wl_fighter2": wl_fighter2,
            }
            fight_list.append(fight)
    return fight_list
