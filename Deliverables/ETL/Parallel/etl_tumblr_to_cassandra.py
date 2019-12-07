import pytumblr
# pip install pytumblr -- if not already installed
import re, string
# regex to exclude html tag
import datetime as dt


# Authenticate via OAuth
# We only need the consumer key to call "posts" function
client = pytumblr.TumblrRestClient('nAvaCgNT6dVls4dxKYnWyM1as57L0aSAkSXAayRCPEtNxJSQjr')

# ### cassandra table create statement
# added 'last_update' column for possible scenario of "training only using the blogs updated in the last 2 years"

# CREATE TABLE tumblr_data (
# 	website TEXT,
# 	last_update TIMESTAMP,
# 	title_font TEXT,
# 	body_font TEXT,
# 	back_color TEXT,
# 	text_color TEXT,
# 	link_color TEXT,
# 	title_text TEXT,
# 	body_text TEXT,
# 	PRIMARY KEY (website)
# );

# ### tumblr data pattern:
# 1) only pick 'text' type post => 'posts': [{'type': 'text'~~~}~~~]
# 2) fonts and colors are the same for all posts since they are under 'blog' attribute
#    but they need body contents. If body is empty, 'trail' will be empty
# 3) title and/or body can be empty (if title is empty, 'title': None, whereas 'comment': '' when body is empty)

# website = {'blog': {~~~'url': 'THIS'~~~}~~~}
# last_update = first in 'posts': [{~~~'date': 'THIS'~~~}~~~]
# title_font = first in 'posts': [~~~{~~~'trail': [{'blog': {~~~'theme': {~~~'title_font': 'THIS'~~~}~~~}}]~~~}~~~]
# body_font = first in 'posts': [~~~{~~~'trail': [{'blog': {~~~'theme': {~~~'body_font': 'THIS'~~~}~~~}}]~~~}~~~]
# back_color = first in 'posts': [~~~{~~~'trail': [{'blog': {~~~'theme': {~~~'background_color': 'THIS'~~~}~~~}}]~~~}~~~]
# text_color = first in 'posts': [~~~{~~~'trail': [{'blog': {~~~'theme': {~~~'title_color': 'THIS'~~~}~~~}}]~~~}~~~]
# link_color = first in 'posts': [~~~{~~~'trail': [{'blog': {~~~'theme': {~~~'link_color': 'THIS'~~~}~~~}}]~~~}~~~]
# title_text = append for every post in 'posts': [~~~{~~~'title': 'THIS'~~~}~~~]
# body_text = append for every post in 'posts': [~~~{~~~'reblog': {'comment': 'THIS'~~~}~~~}~~~]

# exclude html tags, punctuation, and extra whitespaces

def reformat_text(data):
    html = re.compile(r'<.*?>')
    temp = html.sub(' ', data)
    special = re.compile(r'[%s\s]+' % re.escape(string.punctuation))
    temp2 = special.sub(' ', temp)
    wspace = re.compile('\s{2,}')
    return wspace.sub(' ', temp2)

def make_json(blogname):
    print(blogname)
    # Make the request
    # Use minkim25.tumblr.com for test
    data = client.posts(blogname + '.tumblr.com')
    
    #To be modified later
    #Filters out all blogs without 'blog' or 'posts' elements
    try:
        website = data['blog']['url']
        last_update = data['posts'][0]['date'][:19]
    except:
        print('Warning: blog or posts or date or url is null')
        return {}
    
    last_update = dt.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
    trail_flag = 0
    
    # Initialization
    title_text = ""
    body_text = ""
    title_font = ""
    body_font = ""
    back_color = ""
    text_color = ""
    link_color = ""   
    
    for post in data['posts']:
        if post['type'] == 'text':
            if trail_flag == 0 and post['trail'] != []:
                theme = post['trail'][0]['blog']['theme']
                title_font = theme['title_font']
                body_font = theme['body_font']
                back_color = theme['background_color']
                text_color = theme['title_color']
                link_color = theme['link_color']
                trail_flag = 1
            if post['title'] != None:
                title_text = title_text + ' ' + post['title']
                title_text = reformat_text(title_text)
            if post['reblog']['comment'] != '':
                body_text = body_text + ' ' + post['reblog']['comment']
                body_text = reformat_text(body_text)
        elif post['type'] == 'photo':
            if trail_flag == 0 and post['trail'] != []:
                theme = post['trail'][0]['blog']['theme']
                title_font = theme['title_font']
                body_font = theme['body_font']
                back_color = theme['background_color']
                text_color = theme['title_color']
                link_color = theme['link_color']
                trail_flag = 1
            title_text = ''
            if post['reblog']['comment'] != '':
                body_text = body_text + ' ' + post['reblog']['comment']
                body_text = reformat_text(body_text)
            
    result = {'website': website, 'last_update': last_update, 'title_font': title_font, 'body_font': body_font, \
              'back_color': back_color, 'text_color': text_color, 'link_color': link_color, \
              'title_text': title_text, 'body_text': body_text}
    return result