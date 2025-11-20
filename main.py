import argparse
import search_tools
import scraper
from analyzers import find_careers_page

def parse_arguments():
    parser = argparse.ArgumentParser(description="Find job openings for a specific company.")
    
    parser.add_argument(
        "company_name", 
        type=str, 
        nargs='+', 
        help="The name of the company to search for (e.g. 'TechSmith' or 'Home Depot')"
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    target_company = " ".join(args.company_name)
    
    # Step 1: Find the main website
    website = search_tools.find_company_website(target_company)
    if not website:
        print("Could not find company website.")
        return
    print(f"Found Website: {website}")

    # Step 2: Find the broad career page via Google
    broad_career_page = search_tools.find_initial_career_page(website)
    if not broad_career_page:
        print("Could not find a career page via Google.")
        return
    print(f"Initial Career Page: {broad_career_page}")

    # Step 3: Download that page
    html_content = scraper.get_html_content(broad_career_page)
    
    # Step 4: Extract links
    page_links = scraper.extract_links(html_content, website)
    
    # Step 5: Use AI to find the specific job board link
    final_link = find_careers_page(page_links)
    
    print("-" * 30)
    print(f"Final Result - The detailed job list is likely here: \n{final_link}")
    print("-" * 30)

# This is the standard boilerplate to run the script
if __name__ == "__main__":
    main()