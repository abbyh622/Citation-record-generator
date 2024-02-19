import tls_client
from bs4 import BeautifulSoup
import os


# if this file is returning a 403 error, this part is probably why
# at the time of writing this, this library is able to trick the bot detection on the T&F website but changes in the 
# security provider's system could make this stop working
# if 403 error occurs, check the source of the tls-client library for notes (https://pypi.org/project/tls-client/)
session = tls_client.Session(
    client_identifier="chrome120",
    random_tls_extension_order=True
)


# make temp folder 
tempDir = './temp'
if not os.path.exists(tempDir):
    os.mkdir(tempDir)


# at the time of writing this, JNg has 877 articles published online
# this url links to an empty search within JNg with the page set to display 1200 items to account for future publications 
# if you're still using this when JNg has over 1200 articles, just change '1200' at the end of the url to a bigger number
#
# i know this is a weird way to do this but it avoids the javascript stuff on the page that lists all vols/issues 
# and i simply don't want to deal with that so i'm doing it this way
url = 'https://www.tandfonline.com/action/doSearch?AllField=&SeriesKey=ineg20&subjectTitle=&startPage=&pageSize=1200'

print('finding articles...')

# getting webpage 
content = session.get(url)
status = content.status_code 

if status >= 400:
    if status == 403:
        msg = f'403 Forbidden status code received for URL {url}, see program documentation'
    else: 
        msg = f'Error: received status code {status} for URL {url}'
    raise Exception(msg)

soup = BeautifulSoup(content.content, 'html.parser')

# find all elements with the class hlFld-Title
articles = soup.select('.searchResultItem')

# get the href from only the first a element of each article, second is journal link
links = [article.select_one('a')['href'] for article in articles]

os.chdir('./temp')
file_name = "extracted_links.txt"

# write links to a file
with open(file_name, "w") as file:
    for link in links:
        file.write(link + "\n")

print(f'{len(links)} articles found')


# generate citation page urls
inputFileName = "extracted_links.txt"
outputFileName = "cit_links.txt"
prefix = 'https://www.tandfonline.com'

print()
print('generating links to citation pages...')

with open(inputFileName, "r") as inputFile:
    lines = inputFile.readlines()

# do replacements and store updated lines
updatedLines = [prefix + line.replace('/doi/full/', '/doi/citedby/').replace('/doi/abs/', '/doi/citedby/') for line in lines]

# write updated lines to output file
with open(outputFileName, "w") as outputFile:
    outputFile.writelines(updatedLines)

print('citation page links generated')
print()
