from models import SearchQuery, Job
from jobspy import scrape_jobs
from pandas import DataFrame
import pandas as pd




async def scrape( query: SearchQuery ) -> list[ Job ]:

    print()

    if( query is None ): return []

    type = query.type
    level = query.level # list

    jobs = []

    for lev in level:
        res = scrape_jobs( site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"], search_term= type, job_type= lev, results_wanted=10 )

        jobs.extend( clean_scraped_jobs( res ) )

    return jobs


def clean_scraped_jobs( jobs: DataFrame ) -> list[ Job ]:

    formatted = []

    for _, job in jobs.iterrows():

        title = job['title']
        position_level = job['job_type'] if not pd.isna(job["job_type"]) else None
        description = job['description']
        company = job['company'] if not pd.isna(job["company"]) else None
        location = job['location'] if not pd.isna(job['location']) else None
        url = job['job_url']
        
        if not ( pd.isna(job["description"]) ):
            cleaned = Job( title = title, 
                       position_level= position_level if position_level is not None else "", 
                       description= description,
                       company= company if company is not None else "",
                       location=location if location is not None else "",
                       url = url)
            formatted.append( cleaned )
      
    return formatted


#testQuery = SearchQuery( type = "Software Engineer", level=["internship", "fulltime"])
#scrape( testQuery )