from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class NewnjSpider(LegistarSpider):
    name = "newnj_nmc"
    agency = "Newark Municipal Council"
    timezone = "America/New_York"
    start_urls = ["https://newark.legistar.com/Calendar.aspx"]
    default_location = {
        "address": "City Hall, 920 Broad Street, Newark, NJ 07102",
        "name": "Municipal Council Chamber",
    }

    def parse_legistar(self, events):
        """
        `parse_legistar` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for event in events:
            meeting = Meeting(
                title=event["Name"]["label"],
                description="",
                classification=CITY_COUNCIL,
                start=self.legistar_start(event),
                end=None,
                all_day=False,
                time_notes="",
                location=self.parse_location(event),
                links=self.legistar_links(event),
                source=event["Meeting Details"]["url"],
            )
            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)
            yield meeting

    def parse_location(self, event):
        """
        Parse or generate location.
        """
        location = event["Meeting Location"]
        if "Council Chamber" in location:
            return self.default_location
        return {
            "address": location,
            "name": "",
        }
