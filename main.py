

import requests
from bs4 import BeautifulSoup

# استبدل هذا بعنوان الصفحة المراد https://shoot-yalla.io
url = 'https://drama-live.tv'#p/tomorrow-matches.html'#https://2kooralive.live-kooora.com https://drama-live.tv https://www.koralivs.comاستبدل برابط الصفحة الفعلية

#url1 = f"https://en.logodownload.org/?s=Vicenza"

response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
# استخراج البيانات من الصفحة
# هنا يمكنك استخدام BeautifulSoup للبحث عن العناصر المراد استخراجها
# مثال: استخراج العناصر التي تحتوي على النص "مرحبًا"

# تحليل المحتوى باستخدام BeautifulSoup
#article_soup = BeautifulSoup(html_content, 'html.parser')
# استخراج العناصر التي تحتوي على النص "مرحبًا"
#
match_matchflex = soup.find_all(id='matchTable')
#match_containers = soup.find_all(class_='blog-post hentry index-post')#albaflex matchTable

match_event = soup.find_all(class_='posts-thumb post-thumb')




for match_container in match_event:

    #a_event = match_container.find('a')

    #match_event = match_container.find_all('div', class_='match-event') #.prettify()
  # استخراج النص من العنصر المحدد



    #match_date = match_container.find('div', class_='match-date').text

    if match_container :

      related_posts = soup.find_all('div', class_='post-info')

      if related_posts:
          for post in related_posts:
              post.extract()


    



    html_content = f"""

   <html>


<style>
.match-event {{
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}}
.team-name {{
  font-weight: bold;
}}
.team-logo img {{
  width: 70px;
  height: 70px;
}}
</style>



{match_event}


    </html>
    """

  # حفظ محتوى المقالة في ملف بصيغة HTML بناءً على عنوانها
with open('match.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

        print("تم إنشاء ملف match.html بنجاح.")




import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# قراءة محتوى ملف output.html
with open('match.html') as file:
    content = file.read()

# إنشاء كائن Beautiful Soup لتحليل المحتوى
l_soup = BeautifulSoup(content, 'html.parser')

# استخراج العناصر <a> واستخراج روابطها
links = l_soup.find_all('a')
urls = []  # قائمة لتخزين روابط الـ href
for i, link in enumerate(links):
    url = link.get('href')
    urls.append(url)

# حلقة لتقسيم كل رابط إلى اسم الموقع والمسار
for i, url in enumerate(urls):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    path_parts = path.split('/')
    last = path_parts[3]
    last_part_url = path_parts[-1]
    last_part = path_parts[-1].split('-vs-')
    home = last_part[0]
    url_html = f"""
    
    <title> {last_part_url}</title>
    <title2>{last}{home}</title2>
    <style>
    .iframe-container {{
    position: relative;
    width: 100%;
    height: 100%; /* ارتفاع العنصر iframe */
    overflow: hidden; /* لإخفاء المحتوى الزائد */
    }}

    .iframe-container iframe {{
    position: fixed;
    top: -100px; /* قم بضبط هذا الرقم بناءً على ارتفاع العنصر العلوي الذي تريد تغطيته 
      allow="autoplay" allowfullscreen="allowfullscreen" frameborder="0" id="player" loading="lazy" sandbox="allow-same-origin allow-scripts" scrolling="no" 
      */
    left: 0;
    width: 100%;
    height: 100%;
    }}
    </style>
    <div class="iframe-container">

    <iframe src="https://1xnews.online{path}" style="min-height: 1250px; width: 100%;" title="{last_part_url}">
    </iframe>
     </div>

    """
    with open(f'hd{i+1}.html', 'w') as file:
        file.write(url_html)
    print(f"تم إنشاء ملف hd{i+1}.html بنجاح.")






import requests
from bs4 import BeautifulSoup
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery

# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = 'client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/blogger'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials don't exist in the storage location, run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

def get_blogger_service():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://blogger.googleapis.com/$discovery/rest?version=v3')
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discovery_url)
    return service

def get_existing_page(service, blog_id, article_title):
    pages = service.pages()
    response = pages.list(blogId=blog_id).execute()
    items = response.get('items', [])
    for item in items:
        if item['title'] == article_title:
            return item
    return None

def post_to_blogger(payload):
    service = get_blogger_service()
    blog_id = '4141346273346273464'  # استبدل بمعرف المدونة الخاصة بك
    article_title = payload['title']
    
    existing_page = get_existing_page(service, blog_id, payload['title'])
    if existing_page:
        # تحديث المقال الموجود
        updated_page = service.pages().update(blogId=blog_id, pageId=existing_page['id'], body=payload).execute()
        print('تم تحديث المقال:', updated_page['title'])
    else:
        # إنشاء مقال جديد
        new_page = service.pages().insert(blogId=blog_id, body=payload).execute()
        #new_page = service.pages().update(blogId=blog_id, pageId=existing_page['id'], body=payload).execute()
        print('تم إنشاء مقال جديد:', new_page['title'])

def build_html(article_title, article_soup):
    html_code = f"""
    
    {article_soup}
    """
    return html_code

def scrape_and_publish():
    for i in range(2):  # تحديد encoding='ISO-8859-1' عدد المقالات المراد نشرها<meta charset="UTF-8">
        file_name = f"hd{i+1}.html"
        with open(file_name, 'r') as file:
            article_content = file.read()
            article_soup = BeautifulSoup(article_content, 'html.parser')

            article_title = article_soup.find('title2').text.strip()

            html_code = build_html(article_title, article_soup)

            payload = {
                "content": html_code,
                "title": article_title,
                'customMetaData': 'This is meta data'
            }

            post_to_blogger(payload)
            print(f"تم إنشاء {file_name} بنجاح")
            print(f"تم إنشاء {article_title} بنجاح")

# استدعاء الدالة
scrape_and_publish()

import requests
from bs4 import BeautifulSoup
import urllib.parse

match_events = ''

for i in range(5):  # استبدل n بعدد الملفات المطلوبة
    with open(f"hd{i+12}.html", 'r') as file:
        html_content = file.read()

    article_soup = BeautifulSoup(html_content, 'html.parser')

    #result_now = article_soup.find('a')
    #title_now = result_now.get('title')#.text.strip()
    #if len(title_now) < 2:
      #continue
    #result_now = title_now[0]#.text.strip()
    #title_team = title_now[1]#.text.strip()
    #title_team2 = title_now[2]
    #print(f"{title_now}")
    title2 = article_soup.find('title2')#.text.split()
    #title_now = title2.get('title').text.strip()


    #if len(title2) < 2:
        #continue

    #home_team2 = title2[0]#.text
    #away_team2 = title2[1]#.text
    print(f"{title2}")



    #albaplayer_name = article_soup.find(class_='albaplayer_name')
    #albaplayer_server = article_soup.find(class_='albaplayer_server-body')
    title = article_soup.find('title').text.split('-vs-')


    if len(title) < 2:
        continue

    home_team = title[0]
    away_team = title[1]
    print(f"{home_team} vs {away_team}")

#https://www.google.com/search?hl=en&q=pngwing+{away_team}+png
    url1 = f"https://www.google.com/search?hl=en&q=flag+{away_team}+png"

    response1 = requests.get(url1)

    soup1 = BeautifulSoup(response1.content, "html.parser")

    div1 = soup1.find('div' , class_='idg8be')
    if div1 is not None:
        a_links1 = div1.find_all('a', class_='BVG0Nb OxTOff')

        matches1 = {}
        for i, a_link1 in enumerate(a_links1):
            if i >= 2:
                break  # توقف بعد استخراج رابطين فقط
            article_url1 = a_link1['href']
            if article_url1 is not None and article_url1.startswith('https://'):
                article_response1 = requests.get(article_url1)
                article_content1 = article_response1.text
                article_soup1 = BeautifulSoup(article_content1, 'html.parser')
                image_element1 = article_soup1.find('img', id='il_fi')['src']
                matches1[article_url1] = image_element1
                print(f"img: {image_element1}")


           # image_elements_html1 = ""
           # image_elements_html2 = ""
            #for i, (article_url1, image_element1) in enumerate(matches1.items()):
               # if i >= 2:
                   # break
                #if i == 0:
                #    image_elements_html1 += f"<img alt='{home_team}' height='70' src='{image_element1}' title='{home_team}' width='70' />\n"
               # elif i == 1:
                #    image_elements_html2 += f"<img alt='{home_team}' height='70' src='{image_element1}' title='{home_team}' width='70' />\n"



                away_elements_html1 = ""
                for article_url1, image_element1 in matches1.items():
                   away_elements_html1 += f"""
                <img alt="" height="70" src="{image_element1}" title="" width="70" />

                    """
    else:
        print("العنصر غير موجود")
              # image_elements_html2 += f"""
              # <img alt="{away_team}" height="70" src="{image_element1}" title="{away_team}" width="70" />

              # """

    url = f"https://www.google.com/search?hl=en&q=Circular+flag+{home_team}png"


    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    div = soup.find('div' , class_='idg8be')
    if div1 is not None:
        a_links = div.find_all('a', class_='BVG0Nb OxTOff')

        matches = {}
        for i, a_link in enumerate(a_links):
            if i >= 2:
                break  # توقف بعد استخراج رابطين فقط
            article_url = a_link['href']
            if article_url is not None and article_url.startswith('https://'):
                article_response = requests.get(article_url)
                article_content = article_response.text
                article_soup = BeautifulSoup(article_content, 'html.parser')
                image_element = article_soup.find('img', id='il_fi')['src']
                matches[article_url] = image_element
            #print(f"img: {image_element}")
            #away_elements_html1 = ""
            #away_elements_html2 = ""
           # for i, (article_url1, image_element1) in enumerate(matches1.items()):
               # if i >= 2:
                #    break
               # if i == 0:
                  #  away_elements_html1 += f"<img alt='{away_team}' height='70' src='{image_element1}' title='{away_team}' width='70' />\n"
                #elif i == 1:
                  #  away_elements_html2 += f"<img alt='{away_team}' height='70' src='{image_element1}' title='{away_team}' width='70' />\n"



                home_elements_html = ""

                for article_url, image_element in matches.items():

                  home_elements_html += f"""<img alt="" height="70" src="{image_element}" title="" width="70" />"""
                  print(f"img: {image_element}")
    else:
        print("العنصر غير موجود")





    match_event_html = f"""

        <div class="match-event">
        {title2}
            <a href="" title="">
                <div class="first-team">
                    <div class="team-logo">
              {home_elements_html}
                    </div>
                    <div class="team-name">
                    {away_team}
                    </div>

                </div>
                <div class="match-time">
                    <div class="match-timing">

                        <div id="result-now"></div>
                        <div id="match-hour"></div>

                    </div>
                </div>
                <div class="left-team">
                    <div class="team-logo">
                        {away_elements_html1}
                    </div>
                    <div class="team-name">
                    {home_team}
                    </div>

                </div>

            </a>

            
        </div>
    """

    match_events += match_event_html 

html_output = '''
<!DOCTYPE html>

<html lang="en-US">
<head>
<style>
.match-event {{
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
}}
.team-name {{
    font-weight: bold;
}}
.team-logo img {{
    width: 70px;
    height: 70px;
}}
</style>
</head>
<body>
{content}
</body>
</html>
'''

html_output = html_output.format(content=match_events)

with open("result.html", 'w', encoding='utf-8') as file:
    file.write(html_output)
    print("تم إنشاء ملف result.html بنجاح")
#else:
   #print("فشل في تحميل النسخه من الصورة الثانيه")

print("تم إنشاء ملف result.html بنجاح")

from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import imghdr

with open('result.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# تحليل المحتوى باستخدام BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

match_articles = soup.find_all(class_='match-event')

# فتح الصورة الخلفية


# تحليل المقالات وكتابتها في ملفات HTML منفصلة
for i, article in enumerate(match_articles):
    background = Image.open("pp.jpeg")
    background_width, background_height = background.size
    # تحليل رابط الصورة الخلفية
    first_team = article.find(class_='first-team')
    team_logo_images = first_team.find_all('img')
    team_logo_image_urls = [img['src'] for img in team_logo_images]

    # طباعة الروابط بشكل منفصل
  
    # طباعة الروابط بشكل منفصل
    for url_away, url_home in zip(team_logo_image_urls, team_logo_image_urls[1:]):
        print(f"url_away: {url_away}")
        

    left_team = article.find(class_='left-team')
    team_logo_images = left_team.find_all('img')
    team_logo_image_urls = [img['src'] for img in team_logo_images]
    # طباعة الروابط بشكل منفصل
    for url_away2, url_home2 in zip(team_logo_image_urls, team_logo_image_urls[1:]):
        print(f"url_away2: {url_away2}")
        

    # فتح الصورتين الشفافتين
    logo1_url = f"{url_away}"
    logo2_url = f"{url_away2}"
    
    response_logo1 = requests.get(logo1_url)
    response_logo2 = requests.get(logo2_url)

    # التحقق من أن الاستجابة صحيحة ونوع المحتوى هو صورة
    if response_logo1.status_code == 200 and response_logo1.headers["Content-Type"].startswith("image"):
        logo11 = Image.open(BytesIO(response_logo1.content))
        logo11_resized = logo11.resize((300, 300))
    else:
        print("فشل في تحميل الصورة الأولى")
        default_image_path = f"{url_home}"
        response_logo11 = requests.get(default_image_path)
        #print(f"default_image_path1: {default_image_path}")
        if response_logo11.status_code == 200 and response_logo11.headers["Content-Type"].startswith("image"):
           response_logo11 = Image.open(BytesIO(response_logo11.content))
           logo11_resized = response_logo11.resize((300, 300))
        else:
           print("فشل في تحميل النسخه من الصورة الأولى")

    if response_logo2.status_code == 200 and response_logo2.headers["Content-Type"].startswith("image"):
        #image_type = imghdr.what(None, h=response_logo2.content)
    
    #if image_type:
        # نوع الملف معروف، يمكن فتحه
      logo22 = Image.open(BytesIO(response_logo2.content))
      logo22_resized = logo22.resize((300, 300))
    else:
        print("نوع الملف غير معروف")
    #else:
           #print("فشل في تحميل الصورة الثانية")
        #logo22 = Image.open(BytesIO(response_logo2.content))
        #logo22_resized = logo22.resize((250, 250))
    #else:
       # print("فشل في تحميل الصورة الثانية")
        default_image_path = f"{url_home2}"
        response_logo22 = requests.get(default_image_path)
        print(f"default_image_path2: {response_logo22}")
        if response_logo22.status_code == 200 and response_logo22.headers["Content-Type"].startswith("image"):
           response_logo22 = Image.open(BytesIO(response_logo22.content))
           logo22_resized = response_logo22.resize((300, 300))
        else:
           print("فشل في تحميل النسخه من الصورة الثانيه")

    if logo22_resized.mode != "RGBA":
        logo22_resized = logo22_resized.convert("RGBA")

    if logo11_resized.mode != "RGBA":
        logo11_resized = logo11_resized.convert("RGBA")
    # إنشاء صورة جديدة
    result = Image.new("RGBA", (background_width, background_height))

    # وضع الصورة الخلفية في الصورة الناتجة
    result.paste(background, (0, 0))

    # وضع الصورة الأولى في الصورة الناتجة
    result.paste(logo11_resized, (int(background_width * 0.10) - int(logo11_resized.width * 0.10), int(background_height * 0.50)), mask=logo11_resized.split()[3])

    #                         رفع + تنزبل                            وضع الصورة الثانية في الصورة الناتجة
    result.paste(logo22_resized, (int(background_width * 0.75) - int(logo22_resized.width * 0.2), int(background_height * 0.50)), mask=logo22_resized.split()[3])

    # حفظ الصورة الناتجة
    result.save(f"ppua{i+12}.png")
    print("تم حفظ الصورة بنجاح!")


import requests
from bs4 import BeautifulSoup
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import base64

# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = 'client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/blogger'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials don't exist in the storage location, run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

def get_blogger_service():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://blogger.googleapis.com/$discovery/rest?version=v3')
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discovery_url)
    return service

def get_existing_page(service, blog_id, article_title):
    pages = service.pages()
    response = pages.list(blogId=blog_id).execute()
    items = response.get('items', [])
    for item in items:
        if item['title'] == article_title:
            return item
    return None

def post_to_blogger(payload):
    service = get_blogger_service()
    blog_id = '4141346273346273464'  # استبدل بمعرف المدونة الخاصة بك
    article_title = payload['title']
    
    existing_page = get_existing_page(service, blog_id, payload['title'])
    if existing_page:
        # تحديث المقال الموجود
        updated_page = service.pages().update(blogId=blog_id, pageId=existing_page['id'], body=payload).execute()
        print('تم تحديث المقال:', updated_page['title'])
    else:
        # إنشاء مقال جديد
        new_page = service.pages().insert(blogId=blog_id, body=payload).execute()
        print('تم إنشاء مقال جديد:', new_page['title'])

def build_html(article_title, article_soup, image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    html_code = f"""
    <img src="data:image/jpeg;base64,{encoded_image}" alt="صورة المقالة" width: 100%; />
    {article_soup}
    """
    return html_code

def scrape_and_publish():
    for i in range(1):
        file_name = f"hdh{i+12}.html"
        image_path = f"ppua{i+12}.png"  # استبدل بمسار الصورة المحلية الخاصة بك
        with open(file_name, 'r') as file:
            article_content = file.read()
            article_soup = BeautifulSoup(article_content, 'html.parser')

            article_title = article_soup.find('title2').text.strip()

            html_code = build_html(article_title, article_soup, image_path)

            payload = {
                "content": html_code,
                "title": article_title,
                'customMetaData': 'This is meta data'
            }

            post_to_blogger(payload)
            print(f"تم إنشاء {file_name} بنجاح")
            print(f"تم إنشاء {article_title} بنجاح")
            print(f"تم إنشاء {image_path} بنجاح")

# استدعاء الدالة
scrape_and_publish()