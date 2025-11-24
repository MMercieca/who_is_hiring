import argparse
import scraper
from analyzers import find_careers_page, job_extractor, find_job_listings, find_company_website
def parse_arguments():
    parser = argparse.ArgumentParser(description="Find job openings for a specific company.")
    
    parser.add_argument(
        "fields", 
        type=str, 
        nargs='+', 
        help="The name of the company to search for (e.g. 'TechSmith' or 'Home Depot')"
    )
    
    return parser.parse_args()

def read_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            target_company = line.strip()
            search_company(target_company)

def search_company(target_company):
    company_website = find_company_website(target_company)
    print(f"Info --- Company website: {company_website}")
    company_website_content = scraper.get_html_content(company_website)
    company_website_links = scraper.extract_links(company_website_content, company_website)

    broad_career_page = find_job_listings(company_website_links)

    if not broad_career_page:
        print("Info --- Could not find a career page.")
        return
    print(f"Info --- The careers page is likely here: {broad_career_page}")
    print("Info --- Downloading job listing page...")
    careers_page_content = scraper.get_html_content(broad_career_page)
    careers_page_links = scraper.extract_links(careers_page_content, broad_career_page)
    
    # Find the page that has the postings
    jobs_page = find_job_listings(careers_page_links)
    print(f"Info --- Job openings page: {jobs_page}")
    
    # Download jobs postings
    jobs_page_content = scraper.get_html_content(jobs_page)
    jobs_links = scraper.extract_links(jobs_page_content, jobs_page)

    # Use AI to filter down to just the job postings
    jobs = job_extractor.extract_jobs_from_links(jobs_links, jobs_page)

    print(f"Info --- Found {len(jobs)} potential job postings:")
    print(f"\"{target_company}\",\"careers page\",\"{jobs_page}\"")
    for job in jobs:
        print(f"\"{target_company}\",\"{job['title']}\",\"{job['url']}\"")

def main():
    args = parse_arguments()
    if args.fields[0] == "file":
        read_from_file(args.fields[1])
    else:
        target_company = " ".join(args.fields)
        search_company(target_company)

# This is the standard boilerplate to run the script
if __name__ == "__main__":
    main()