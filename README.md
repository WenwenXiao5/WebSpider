# WebSpider ###
This is a web spider with page rank algorithm and visualization tool.

This program can achieve three major tasks:
1. Crawl a web page and store the links within the webpage into a sqlite database
2. Run a page rank algorithm to determine the pages with highest importance
3. Output the results or use a visualization tool called d3.js to see the ralationships of web pages

# Notes ###
- This program utilizes some files from Dr Charles R. Severance's website: https://www.py4e.com/code3/pagerank.zip
  The "CocoSpider.py" and "CocoPrank.py" were wrote by myself, and other files were fully understood and used in this program.
- The program use BeautifulSoup to parse the html. Thus, you need to install BeautifulSoup in order to run this program.
  There are two ways to do it:
  1) Download the bs4 folder in this repository to the same location as the other files of this program
  2) Refer to https://pypi.org/project/beautifulsoup4/ (recommended method)
- You need to install the SQLite browser to view and modify the database:
  Refer to https://sqlitebrowser.org/dl/
- You need to remove the generate "spider2.sqlite" file if you want to re-run the spider program 
- Windows has difficulty in displaying UTF-8 characters
  in the console so for each console window you open, you may need
  to type the following command before running this code:

    chcp 65001

  http://stackoverflow.com/questions/388490/unicode-characters-in-windows-command-line-how

  Mac: rm spider.sqlite
  Mac: python3 spider.py

  Win: del spider.sqlite
  Win: spider.py
  
# Detailed Process ###
1. Crawl a web page and store the links within the webpage into a sqlite database
  a) Run CocoSpider.py:
      Mac: python3 CocoSpider.py 
      Win: CocoSpider.py
  b) Enter the url of the website you want to crawl
  c) Enter how many pages you want to crawl
  d) Hit "Return" to jump out of the command

  Now you have a spider2.sqlite database with all the web pages retrieved and the relationships between those webpages

  You can have multiple starting points in the same database - within the program these are called "webs".   
  The spider chooses randomly amongst all non-visited links across all the webs.

2. Run a page rank algorithm to determine the pages with highest importance
  a) Run CocoPrank.py:
      Mac: python3 CocoPrank.py 
      Win: CocoPrank.py
  b) Enter how many time you want to run the iteration
      You can run sprank.py as many times as you like and it will simply refine
      the page rank the more times you run it.  You can even run sprank.py a few times
      and then go spider a few more pages sith spider.py and then run sprank.py
      to converge the page ranks.

      For each iteration of the page rank algorithm it prints the average
      change per page of the page rank.   The network initially is quite 
      unbalanced and so the individual page ranks are changing wildly.
      But in a few short iterations, the page rank converges.  You 
      should run prank.py long enough that the page ranks converge.

    If you want to restart the Page Rank calculations without re-spidering the 
    web pages, you can use spreset.py

    Mac: python3 spreset.py 
    Win: spreset.py 

    All pages set to a rank of 1.0

3. Output the results or use a visualization tool called d3.js to see the ralationships of web pages
  a) If you want to just dump the content from the spider2.sqlite database:
    run spdump.py as follows:

    Mac: python3 spdump.py 
    Win: spdump.py

    This shows the number of incoming links, the old page rank, the new page
    rank, the id of the page, and the url of the page.  The spdump.py program
    only shows pages that have at least one incoming link to them.

  b) If you want to visualize the current top pages and the relationships between web pages:
    run spjson.py to write the pages out in JSON format to be viewed in a web browser

    Mac: python3 spjson.py 
    Win: spjson.py 

    Enter the number of nodes you want to see in the visualization tool.

    You can view this data by opening the file force.html in your web browser.  
    This shows an automatic layout of the nodes and links.  You can click and 
    drag any node and you can also double click on a node to find the URL
    that is represented by the node.

