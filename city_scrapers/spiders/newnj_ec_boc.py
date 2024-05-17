from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class NewnjEcBoCSpider(CityScrapersSpider):
    name = "newnj_ec_boc"
    agency = "Essex County Board Of County Commmissioners"
    timezone = "America/New_York"
    start_urls = ["https://ecfnj.com/cms/18/Meeting-Schedule-2024"]
    links = [
        {
            "title": "Meeting materials",
            "href": "https://essexcountynj.new.swagit.com/views/390",
        }
    ]
    location = {
        "name": "Essex County Board of County Commissioners – Room Chambers",
        "address": "Essex County Board of County Commissioners, 5th Floor, Room 506, Hall of Records, Newark, New Jersey",  # noqa
    }

    def parse(self, response):
        """This page has limited detail, so we only focus on the date and time.
        Note that the URL is targeting 2024 meetings because there is no
        generic URL for the meetings. The URL will likely need to be updated
        beyond 2024.
        """
        rows = response.css("table tbody tr")
        for row in rows:
            start = self._parse_start(row)
            if not start:
                continue

            meeting = Meeting(
                title="Board of County Commissioners",
                description="",
                classification=BOARD,
                start=start,
                end=None,
                time_notes="",
                all_day=False,
                location=self.location,
                links=self.links,
                source=response.url,
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        # get nodes
        date_str = item.css("td:nth-child(1)::text").get()
        time_str = item.css("td:nth-child(4)::text").get()
        if not date_str or not time_str:
            return None

        # clean up strings
        clean_date_str = date_str.replace(",", "").replace(".", "").strip()
        clean_time_str = time_str.replace(".", "").strip()
        if not clean_date_str or not clean_time_str:
            return None

        # Parse date and time
        try:
            date = datetime.strptime(clean_date_str, "%B %d %Y").date()
            time = datetime.strptime(clean_time_str, "%I:%M %p").time()
            start = datetime.combine(date, time)
        except ValueError:
            self.log(
                f"Failed to parse date or time: {clean_date_str} {clean_time_str}",  # noqa
                level="ERROR",
            )
        return start
