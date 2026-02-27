import os, requests, json
from time import sleep
from bs4 import BeautifulSoup
# from rich.console import Console
# from time import sleep

LINK = 'https://www.cifraclub.com.br'
OUT_FOLDER = 'extracted'

def extractPageContent(content, isVersion=False):
    soup = BeautifulSoup(content, 'html.parser') if isinstance(content, str) else content

    tab = [x.get_text() for x in soup.select('div.cifra_cnt pre')]

    if isVersion:
        return {
            "tab": tab
        }
    
    songName = soup.select_one('div.cifra .t1')
    author = soup.select_one('div.cifra .t3')
    versionName = soup.select_one('a.tab_more')
    name = f"{songName.text.lower()}@{author.text.lower()}" if songName and author else "unknown"

    return {
        "versioName": versionName.text if versionName else "",
        "author": author.text if author else "",
        "song_name": songName.text if songName else "",
        "file": name,
        "instrument": "",
        "tab": tab
    }

def main():
    outjson = dict() 
    link = 'https://www.cifraclub.com.br/red-hot-chili-peppers/cant-stop/'
    extractFolder = f"{OUT_FOLDER}/{link.replace(LINK, '')}"

    page = requests.get(link).text
    # soup = BeautifulSoup(page.text, 'html.parser')

    mainContent = BeautifulSoup(page, 'html.parser')
    versions = mainContent.select('a.vers-r.js-version')

    outjson['default'] = extractPageContent(mainContent)

    # WARN: could cause runtine errors
    versions = [str(x['href']) for x in versions if str(x['href']).endswith('.html')]

    for ver in versions:
        content = requests.get(LINK + ver).text
        outjson[ver] = extractPageContent(content, True)
        sleep(1)

    os.system(f"mkdir -p {extractFolder}")

    with open(f"{extractFolder}/{outjson['default']['file']}.json", "w") as f:
        json.dump(outjson, f, indent=2)

    pass

if __name__ == "__main__": 
    main()
