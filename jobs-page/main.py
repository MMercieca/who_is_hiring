import argparse
import search_tools
import scraper
from analyzers import find_careers_page, job_extractor

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
    # Step 1: Find the main website
    website = search_tools.find_company_website(target_company)
    if not website:
        print("Info --- Could not find company website.")
        return
    print(f"Info --- Found Website: {website}")

    # Step 2: Find the broad career page via Google
    broad_career_page = search_tools.find_initial_career_page(website)
    if not broad_career_page:
        print("Info --- Could not find a career page via Google.")
        return
    print(f"Info --- Initial Career Page: {broad_career_page}")

    # Step 3: Download that page
    html_content = scraper.get_html_content(broad_career_page)
    
    # Step 4: Extract links
    page_links = scraper.extract_links(html_content, website)
    
    # Step 5: Use AI to find the specific job board link
    final_link = find_careers_page(page_links)
    
    print("Info ---", "-" * 30)
    print(f"Info --- The detailed job list is likely here: {final_link}")
    print("Info ---", "-" * 30)

    # 4. Extract Job Titles and URLs
    print("Info --- Downloading job listing page...")
    listings_html = scraper.get_html_content(final_link)
    
    # Get all raw links from that page
    raw_links = scraper.extract_links(listings_html, website)
    
    # Use AI to filter down to just the job postings
    jobs = job_extractor.extract_jobs_from_links(raw_links)

    print(f"Info --- Found {len(jobs)} potential job postings:")
    print(f"\"{target_company}\",\"careers page\",\"{final_link}\"")
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