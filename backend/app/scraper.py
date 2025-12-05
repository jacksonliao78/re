import selenium 
from api.jobs import SearchQuery, Job


#job sites we are searching from
search_sites = [ 
    'https://www.linkedin.com/jobs/search/?keywords=',
    'https://www.indeed.com/jobs?q=',

]


def scrape( query: SearchQuery ) -> list[ Job ]:



    # for some query we want to scrape 
    ...