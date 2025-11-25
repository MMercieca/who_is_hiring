import argparse
import scraper
from ask_ai import find_company_website, find_careers_page, find_job_listings, job_extractor
from ask_google import google_enabled, google_career_page

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
    # 1. Get company website
    company_website = find_company_website(target_company)
    print(f"Info --- Company website: {company_website}")
    print(f"\"{target_company}\",\"website\",\"{company_website}\"")

    # 2. Find careers page
    try:
        company_website_content = scraper.get_html_content(company_website)
        company_website_links = scraper.extract_links(company_website_content, company_website)
        career_page = find_careers_page(company_website_links)
    except:
        career_page = None

    if career_page == None and google_enabled():
        print("Info --- Career page not found with OpenAI. Using Google fallback.")
        google_career_page(target_company, company_website)

    print(f"Info --- The careers page is likely here: {career_page}")
    
    if career_page == None or company_website == None:
        print(f"Info --- could not find career page for {target_company}")
        return

    # 3. Find the page that has the listings
    careers_page_content = scraper.get_html_content(career_page)
    careers_page_links = scraper.extract_links(careers_page_content, career_page)
    jobs_page = find_job_listings(careers_page_links, career_page)
    print(f"Info --- Job openings page: {jobs_page}")
    
    # 4. Download jobs postings and display
    jobs_page_content = scraper.get_html_content(jobs_page)
    jobs_links = scraper.extract_links(jobs_page_content, jobs_page)
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