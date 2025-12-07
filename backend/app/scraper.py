from models import SearchQuery, Job
from jobspy import scrape_jobs
from pandas import DataFrame


#job sites we are searching from



def scrape( query: SearchQuery ) -> list[ Job ]:

    if( query is None ): return []

    type = query.type
    level = query.level # list

    jobs = []

    for lev in level:
        res = scrape_jobs( site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"], search_term= type, job_type= lev, results_wanted=10 )

        print(f"Found {len(res)} jobs")

        print(res.head())
        for thing in res:
            print(thing)
        jobs.append( res )
    print(jobs)
        



    # for some query we want to scrape 

    # for each job, we also need to put it into a db so that we dno't get it again?
    ...


def clean_scraped_job( job ) -> Job:
    #here we need to parse the important bits
    ...


testQuery = SearchQuery( type = "Software Engineer", level=["internship", "fulltime"])
scrape( testQuery )