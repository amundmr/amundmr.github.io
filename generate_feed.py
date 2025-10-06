from feedgen.feed import FeedGenerator
import os
from datetime import datetime
import pytz
from bs4 import BeautifulSoup

TZ = pytz.timezone("Europe/Oslo")
DOMAIN = "https://raniseth.com/"
BLOG_PATH = "blog"
ATOM_FILE = "atom.xml"

# Set up a feed
fg = FeedGenerator()
fg.id(DOMAIN)
fg.title('Raniseth')
fg.author( {'name':'Amund Raniseth'} )
fg.link( href=DOMAIN + ATOM_FILE, rel='self' )
fg.link( href=DOMAIN, rel='alternate' )

# Find all blogposts
blogposts = [x for x in os.listdir(BLOG_PATH) if x.endswith(".html")]
blogposts.remove("template.html")

# Add blogposts to feed
for bp in blogposts:

    # Find date of article (defaults to 00:00 at night)
    yr, mth, day = bp.split("-")[:3]
    date = datetime(int(yr), int(mth), int(day))
    date = TZ.localize(date) # Required by feedgen

    # Find title and author from html
    with open(os.path.join(BLOG_PATH, bp), 'r') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    title = title = soup.title.string
    author = soup.find('meta', attrs={'name': 'author'})
    author_content = author['content']

    link = DOMAIN + BLOG_PATH + "/" + bp 

    fe = fg.add_entry()
    fe.id(link)
    fe.title(title)
    fe.link(href=link, rel='alternate')
    fe.author(name=author_content)
    fe.published(date)

fg.atom_file(ATOM_FILE, pretty=True) # Write the ATOM feed to a file
