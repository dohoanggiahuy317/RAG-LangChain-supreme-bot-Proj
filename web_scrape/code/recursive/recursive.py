import argparse
import logging
from langchain_community.document_loaders import RecursiveUrlLoader
import pandas as pd
from utils.parser import extract_title_and_text_from_html # type: ignore
from utils.scrape_preprocessing import create_output_file, get_processed_url # type: ignore
from collections import Counter


def url_check(curr_url, processed_urls):
    # Skip already processed URLs
    if curr_url.strip("#").strip("/") in processed_urls or curr_url in processed_urls:
        logging.info(f"Skipping already processed URL: {curr_url}")
        return True
    
    # Skip PDF URLs
    if curr_url.lower().endswith('.pdf'):
        logging.info(f"Skipping PDF URL: {curr_url}")
        return True
    
    return False


def write_data(page, output_filename):
    new_df = pd.DataFrame(page)
    new_df.to_csv(output_filename, mode='a', index=False, header=False)
    
    # Reset the page dictionary and counter
    page = {'url': [], 'title': [], 'text': []}
    return page



def root_parsing(base_url, loader, processed_urls, output_filename, logging, scrape_threshold):
    """
    Parse documents from the loader and save the extracted data to the CSV file.

    Args:
    loader (RecursiveUrlLoader): The loader to fetch documents.
    processed_urls (set): The set of URLs that have already been processed.
    output_filename (str): The path to the output CSV file.
    """
    logging.info(f"Starting to scrape.")
    
    # Initialize containers for page data and counters
    page = {'url': [], 'title': [], 'text': []}
    fail_urls = set()
    counter, total = 0, 0

    try: 
        # Iterate over the documents from the loader
        for doc in loader.lazy_load():
            curr_url = doc.metadata['source']
            url_set = set(list(curr_url))
            
            # check url
            if url_check(curr_url, processed_urls) and not curr_url.startswith(base_url) and url_set["/"] <= 5:
                continue

            # Extract title and cleaned text from the document
            title, cleaned_text = extract_title_and_text_from_html(doc.page_content)


            # Append the extracted data to the page dictionary
            page['url'].append(curr_url)
            page['title'].append(title)
            page["text"].append(cleaned_text)
            
            processed_urls.add(curr_url)
            counter += 1
            

            # Save in batches of 2 for demonstration purposes
            if counter >= 2:
                page = write_data(page, output_filename)
                total += 2
                logging.info(f"Processed and saved {counter} documents (total {total} documents)")
                counter = 0

            if total >= scrape_threshold:
                break

    except Exception as e:
        fail_urls.add(doc.metadata['source'])
        logging.error(f"Error processing URL {doc.metadata['source']}: {e}")


    # Save the rest
    page = write_data(page, output_filename)
    logging.info(f"Processed and saved {counter} documents (total {total} documents)")
    total += len(page["url"])

    # Done parsing
    logging.info(f"Processed total {total} documents")
    
    return fail_urls, processed_urls


def main():
    """
    Main function to set up logging, initialize the loader, and start parsing.
    """

    parser = argparse.ArgumentParser(description='Scrap content from a link')
    parser.add_argument('--base_url', type=str, help='link of the root url')
    parser.add_argument('--root_url', type=str, help='link of the root url')
    parser.add_argument('--max_depth', type=int, help='depth threshold', default=2)
    parser.add_argument('--scrape_threshold', type=int, help='stoping threshold', default=float("INF"))
    parser.add_argument('--output_filename', type=str, help='path to content file in csv')
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Output filename
    create_output_file(args.output_filename)

    # Get the set of processed URLs
    processed_urls = get_processed_url(args.output_filename)
    
    # Initialize the document loader
    loader = RecursiveUrlLoader(
            url = args.root_url,
            max_depth = int(args.max_depth),
            prevent_outside = True,
            base_url=args.base_url,
            continue_on_failure = True)
    
    # Start parsing the documents
    fail_urls, processed_urls = root_parsing(args.base_url, loader, processed_urls, args.output_filename, logging, args.scrape_threshold)

    logging.info(f"Failed total {len(fail_urls)} documents. Start scraping again")

    for fail_url in fail_urls:
        f_loader = RecursiveUrlLoader(
            url = fail_url,
            max_depth = int(args.max_depth),
            prevent_outside = True,
            continue_on_failure = False)
        root_parsing(args.base_url, f_loader, processed_urls, args.output_filename, logging, args.scrape_threshold - len(processed_urls))


# Run the main function
if __name__ == "__main__":   
    main()