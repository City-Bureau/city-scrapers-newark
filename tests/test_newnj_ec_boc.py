from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, PASSED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.newnj_ec_boc import NewnjEcBoCSpider

test_response = file_response(
    join(dirname(__file__), "files", "newnj_ec_boc.html"),
    url="https://ecfnj.com/cms/18/Meeting-Schedule-2024",
)
spider = NewnjEcBoCSpider()

freezer = freeze_time(datetime(2024, 5, 17, 8, 56))
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]
parsed_item = parsed_items[0]
freezer.stop()


def test_title():
    assert parsed_item["title"] == "Board of County Commissioners"


def test_description():
    assert parsed_item["description"] == ""


def test_start():
    assert parsed_item["start"] == datetime(2024, 1, 2, 17, 0)


def test_end():
    assert parsed_item["end"] is None


def test_time_notes():
    assert parsed_item["time_notes"] == ""


def test_id():
    assert (
        parsed_item["id"] == "newnj_ec_boc/202401021700/x/board_of_county_commissioners"
    )


def test_status():
    assert parsed_item["status"] == PASSED


def test_location():
    assert parsed_item["location"] == {
        "name": "Essex County Board of County Commissioners – Room Chambers",
        "address": "Essex County Board of County Commissioners, 5th Floor, Room 506, Hall of Records, Newark, New Jersey",  # noqa
    }


def test_source():
    assert parsed_item["source"] == "https://ecfnj.com/cms/18/Meeting-Schedule-2024"


def test_links():
    assert parsed_item["links"] == [
        {
            "title": "Meeting materials",
            "href": "https://essexcountynj.new.swagit.com/views/390",
        }
    ]


def test_classification():
    assert parsed_item["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
