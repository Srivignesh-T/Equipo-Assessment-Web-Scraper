import requests
from bs4 import BeautifulSoup
from csv import writer


# Function to fetch and parse HTML content from a given URL
def get_html_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/54.0.2840.71 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to fetch URL: {url}")
        return None


# Function to scrape data from a single page and write to CSV
def scrape_page(url, category, writer):
    # Fetch HTML content from the URL
    html_doc = get_html_content(url)
    if html_doc:
        # Extract code information from the HTML
        h1 = html_doc.find("h1")
        code = h1.text.strip()
        clickable_rows = html_doc.find_all(class_="clickable-row")
        # Iterate over clickable rows to extract detailed information
        for row in clickable_rows:
            td = row.find('td')
            href_tag = td.find('a')
            if href_tag:
                final_url = "https://www.hcpcsdata.com" + href_tag.attrs['href']
                # Fetch HTML content from the final URL
                last_page_html = get_html_content(final_url)
                if last_page_html:
                    # Extract detailed information from the last page HTML
                    span_tag = last_page_html.find_all('span')[6]
                    code_cls = last_page_html.find_all(class_='identifier16')[0]
                    h5 = last_page_html.find("h5")
                    td = last_page_html.find_all("td")[1]
                    short_description = td.text.strip()
                    long_description = h5.text.strip()
                    code = code_cls.string.strip()
                    group = 'HCPCS' + ' ' + span_tag.string.strip()
                    info = [group, category, code, long_description, short_description]
                    # Write extracted information to CSV
                    writer.writerow(info)
                    print(info)


# Main function to get Category URL and Name.
def main():
    url = "https://www.hcpcsdata.com/Codes"
    # Fetch HTML content from the main URL
    html_doc = get_html_content(url)
    if html_doc:
        with open('assignment.csv', 'w', encoding='utf8', newline="") as f:
            csv_writer = writer(f)
            header = ['group', 'category', 'code', 'long description', 'short description']
            csv_writer.writerow(header)

            table = html_doc.find_all(['table'])
            clickable_rows = table[0].find_all(class_="clickable-row")
            # Iterate over clickable rows to extract category URLs
            for row in clickable_rows:
                td = row.find('td')
                href_tag = td.find('a')
                if href_tag:
                    category_url = "https://www.hcpcsdata.com" + href_tag.attrs['href']
                    # Fetch HTML content from the category URL
                    category_html = get_html_content(category_url)
                    if category_html:
                        h5 = category_html.find_all("h5")[0]
                        category_name = h5.text.strip()
                        # Scrape data from the category page and write to CSV
                        scrape_page(category_url, category_name, csv_writer)


if __name__ == "__main__":
    main()
