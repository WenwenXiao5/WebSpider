
import ssl
import sqlite3
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import urljoin
import urllib.error ###################################################
from bs4 import BeautifulSoup


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Create sqlite database:
conn = sqlite3.connect('spider2.sqlite')
cur = conn.cursor()

# Create tables in sqlite
cur.execute('''CREATE TABLE IF NOT EXISTS Pages
            (id INTEGER PRIMARY KEY, url TEXT UNIQUE, 
            html TEXT, error INTEGER, old_rank REAL, new_rank REAL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs
            (url TEXT UNIQUE)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Links
            (from_id INTEGER, to_id INTEGER)''')

# "WHERE html is NULL and error is NULL" just says where the url has not been parsed, 
# randomly select 1 record
cur.execute('''SELECT id,url FROM Pages WHERE html is NULL and error is NULL 
            ORDER BY RANDOM() LIMIT 1''')
idurl = cur.fetchone()
# Make sure we start from an empty sqlite
if idurl is not None:
    print('There is already something in the sqlite, remove and restart')
else:
    url = input('Enter the url link: ')
    if len(url) < 1:
        # url = 'http://www.dr-chuck.com/'
        url = 'http://python-data.dr-chuck.net/'
    # Clean up input the url
    if url.endswith ('/'):
        url = url[:-1]
    urll = url
    # ################################################################################
    if ( url.endswith('.htm') or url.endswith('.html') ) :
        pos = url.rfind('/') # "rfind" returns the index of last occurance
        urll = url[:pos]
    # ################################################################################
    
    if len(urll) > 1: ####################################################
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (?, NULL, 1.0)', (url,))
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES (?)', (urll,))
        conn.commit()

# Get the current webs
cur.execute('''SELECT url FROM Webs''')
webs = list()
for row in cur:
    # print(row)
    # print(type(row))   "row" is a tuple
    webs.append(str(row[0]))

print(webs)

many = 0
while True:
    if ( many < 1 ) :
        sval = input('How many pages:')
        if ( len(sval) < 1 ) : break
        many = int(sval)
    many = many - 1
 
    cur.execute('''SELECT id,url FROM Pages WHERE html is NULL and error is NULL 
                ORDER BY RANDOM() LIMIT 1''')
    try:
        row = cur.fetchone()
        # print row
        fromid = row[0]
        url = row[1]
    except:
        print('No unretrieved HTML pages found')
        many = 0 ##########################################################
        break

# ################################################################################
    # print(fromid, url, end=' ')   # means that the print function ends with a space (by default, it ends with a nline)

    # If we are retrieving this page, there should be no links from it
    cur.execute('DELETE from Links WHERE from_id=?', (fromid, ) )
# ################################################################################

    try:
        # Read the links inside of the url
        doc = urlopen(url, context=ctx)
        html = doc.read()
        # The getcode() method returns the HTTP status code that was sent with the response
        # 200 is a OK status code, 404 not found is not a OK status code
        if doc.getcode() != 200 :  
            print("Error on page: ",doc.getcode())
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (doc.getcode(), url) )

        if 'text/html' != doc.info().get_content_type() :
            print("Ignore non text/html page")
            cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
            conn.commit()
            continue

        # print('('+str(len(html))+')', end=' ') 

        # Parse the html
        soup = BeautifulSoup(html, "html.parser")
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except:
        print("Unable to retrieve or parse page")
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
        conn.commit()
        continue

    cur.execute('UPDATE Pages SET html = ? WHERE url = ?', (memoryview(html), url))
    conn.commit()

    # Retrieve all the anchor tag
    anchor = soup('a')
    # print(type(anchor))

    # keep track of the new url links added 
    numurl = 0

    for tag in anchor:
        href = tag.get('href', None)
        if href is None:
            continue
        hrefSplit = urlparse(href)
        scheme = hrefSplit.scheme
        if len(scheme) < 1:
            href = urljoin(url, href)
        # Clean the href
        ipos = href.find('#')
        if ( ipos > 1 ) : href = href[:ipos]
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ) : continue
        if ( href.endswith('/') ) : href = href[:-1]
        if len(href) < 1:
            continue

        # Check if the URL is in any of the webs
        found = False
        for web in webs:
            if ( href.startswith(web) ) :
                found = True
                break
        if not found : continue

        # Adding the new url obtained from the starturl page
        cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank) 
                    VALUES (?, NULL, 1.0)''',(href,) )
        numurl = numurl + 1
        conn.commit()

        cur.execute ('SELECT id FROM Pages WHERE url = ? LIMIT 1', (href,))
        try:
            row = cur.fetchone()
            toid = row[0]
        except:
            print('Could not retrieve id')
            continue

        cur.execute('''INSERT OR IGNORE INTO Links (from_id, to_id) 
                    VALUES (?,?)''', (fromid,toid))
        conn.commit()
        
    print (fromid, url, '('+str(len(html))+')', numurl )

cur.close()