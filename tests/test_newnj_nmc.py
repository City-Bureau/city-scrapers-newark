import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL, TENTATIVE
from freezegun import freeze_time

from city_scrapers.spiders.newnj_nmc import NewnjSpider

freezer = freeze_time("2024-04-10")
freezer.start()

with open(
    join(dirname(__file__), "files", "newnj_nmc.json"), "r", encoding="utf-8"
) as f:  # noqa
    test_response = json.load(f)

spider = NewnjSpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Municipal Council"


def test_description():
    assert (
        parsed_items[0]["description"] == ""
    )  # Assuming description isn't provided directly  # noqa


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 4, 10, 12, 30)


def test_end():
    # Assuming the end time is not calculated and thus not provided
    assert parsed_items[0]["end"] is None


def test_time_notes():
    # Assuming no specific time notes provided
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    # You'll need to adjust the expected ID based on how your spider generates it
    assert parsed_items[0]["id"].startswith("newnj_nmc")


def test_status():
    # Assuming status needs to be assumed or calculated somehow
    assert parsed_items[0]["status"] == TENTATIVE


def test_location():
    assert parsed_items[0]["location"] == {
        "address": "City Hall, 920 Broad Street, Newark, NJ 07102",
        "name": "Municipal Council Chamber",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://newark.legistar.com/MeetingDetail.aspx?ID=1189588&GUID=C695B36D-A796-47DD-8140-118B4FFBA77F&Options=info|&Search="  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://newark.legistar.com/View.ashx?M=A&ID=1189588&GUID=C695B36D-A796-47DD-8140-118B4FFBA77F",  # noqa
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
