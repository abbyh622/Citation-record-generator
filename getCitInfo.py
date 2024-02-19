import os
import tls_client
import time
import tqdm


# if this file is returning a 403 error, this part is probably why
# at the time of writing this, this library is able to trick the bot detection on the T&F website but changes in the 
# security provider's system could make this stop working
# if 403 error occurs, check the source of the tls-client library for notes (https://pypi.org/project/tls-client/)
session = tls_client.Session(
    client_identifier="chrome120",
    random_tls_extension_order=True
)

os.chdir('./temp')
# make temp folder to store html files
htmlVault = os.path.join(os.getcwd(), 'htmls_temp')
os.makedirs(htmlVault)

inputFileName = 'cit_links.txt'     # output from getAllArticles

# get number of lines (articles)
with open(inputFileName, "r") as inputFile:
    numLines = sum(1 for line in inputFile)


# loop through each line w/ tqdm to show progress bar
with open(inputFileName, 'r') as inputFile:
    lines = inputFile.readlines()     # delete this line
    for line in tqdm.tqdm(lines, total = len(lines)):  # change lines to inputFile, total to numLines
        url = line.strip()

        # get webpage 
        content = session.get(url)
        status = content.status_code 
        if status >= 400:
            if status == 403:       # this shouldnt happen if getAllArticles.py was successful
                msg = f'403 Forbidden status code received for {url}'   
            else: 
                msg = f'Error: received status code {status} for URL {url}'
            raise Exception(msg)
        
        # make unique file names
        filename = url.split('/')[-1].replace('.', '-')
        filepath = os.path.join(htmlVault, filename)

        # save html
        with open(filepath, 'wb') as file:
            file.write(content.content)

        time.sleep(1)   # slow down !!!!!!!

