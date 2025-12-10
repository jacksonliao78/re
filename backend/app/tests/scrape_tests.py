from app.scraper import scrape
import pytest
from unittest.mock import patch
from app.models import Job
from app.models import SearchQuery

@pytest.fixture
def sample_query():
    return SearchQuery(
        type="Software Engineer", 
        level=["intern", "full-time"]
        )

@pytest.fixture
def sample_return():
    return [
        {"title": "Junior Software Engineer", "company": "ABC"},
        {"title": "Entry Level Developer", "company": "XYZ"},
    ]

def test_once_per_keyword(sample_query, sample_return):
    """
    Ensure that scrape is called once for each keyword in query.level.
    """

    with patch( "app.scraper.scrape", return_value=sample_return ) as mock_scrape:
        jobs = scrape(sample_query)

        # Called once per level keyword
        assert mock_scrape.call_count == len(sample_query.level)

        # scrape() should return the collected job objects
        assert len(jobs) == len(sample_query.level)

        # Each element should contain the fake jobs returned
        for batch in jobs:
            assert list(batch) == sample_return


def test_empty():
    """
    If level list is empty, ensure no scrape calls occur.
    """
    query = SearchQuery(type="any", level=[])

    with patch("app.scraper.scrape") as mock_scrape:
        jobs = scrape(query)

        assert mock_scrape.call_count == 0
        assert jobs == []


