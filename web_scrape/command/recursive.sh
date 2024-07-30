python3 web_scrape/code/recursive/recursive.py \
    --base_url "http://internationaloffice.hanu.vn/" \
    --root_url "http://internationaloffice.hanu.vn/#" \
    --max_depth 3 \
    --scrape_threshold 100 \
    --output_filename 'web_scrape/data/hanu/documents_content.csv'