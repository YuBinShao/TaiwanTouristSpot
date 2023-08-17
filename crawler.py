import sqlite3
from bs4 import BeautifulSoup
import re
import urllib.request 
import urllib.parse
def main():
    baseurl = "https://www.taiwan.net.tw/m1.aspx?sNo=0000064&page="
    datalist = getdata(baseurl)

def askURL(url):
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

}
    request = urllib.request.Request(url)
    html=""
    try :
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except :
        print('error')
    return html

rechar = re.compile(r'<a href=.*? title="#(.*?)">') #特色
retitle = re.compile(r'<a "="" class="card-link" href=.*? title="(.*?)">') #景點
renum = re.compile(r'<span class="sr-only">瀏覽人次：</span>(.*?)</p>')
reimgsrc = re.compile(r'<img .*? class="lazyload" data-src="(.*?)" src="images/white.jpg"/>')
reconsrc = re.compile(r'<a "="" class="card-link" href="(.*?)" title')

def getdata(baseurl):
    datalist = []
    idx = 1
    for i in range(0,63):
        url = baseurl + str(i+1)
        
        
        html = askURL(url)
        
        soup = BeautifulSoup(html,"html.parser")
        for i in soup.find_all("div",class_="card"):
            i=str(i)
            
            title = re.findall(retitle,i)[0]
            
            char = re.findall(rechar,i)

            num = re.findall(renum,i)[0]

            slug = 'attraction' + str(idx)
            print(slug)
            imgsrc = re.findall(reimgsrc,i)[0]
            consrc = re.findall(reconsrc,i)[0].replace('amp;','')
            consrc = 'https://www.taiwan.net.tw/' + consrc
            #print(idx)
            
            print(title)

            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()

            for ele in char:
                sql = '''insert into mysite_characteristic(character,scene_id) values('{}','{}')'''.format(ele,idx)
                cur.execute(sql)
            
            
            sql = '''insert into mysite_scene(name,hot,img,content_id,slug) values('{}','{}','{}','{}','{}')'''.format(title,num,imgsrc,idx,slug) 
            
            cur.execute(sql)
            conn.commit()
            cur.close()

            getcontent(consrc,idx)
            idx += 1
       

recontent = re.compile(r'</noscript>.*?(<p>.*</p>).*?<a class="morebtn more-read"',re.S)
rephone = re.compile(r'<a class="tel-link phone" href="tel:(.*?)">')
readdress =  re.compile(r'<a class="tel-link address".*?title="點選開啟新視窗">(.*?)</a>')


def getcontent(url,idx):
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    content = ""
    for i in soup.find_all("div",class_="content"):
        i=str(i)
        #print(i)   

        content = re.findall(recontent,i)
        if len(content) != 0:
            content = re.sub(r'[\'\n\r]','',content[0])
            #content = content.replace('\'','')
        else:
            content =  re.findall(re.compile(r'</noscript>.*?(<div>.*</div>).*?<a class="morebtn more-read"',re.S),i)
            content = re.sub(r'[\'\n\r]','',content[0])
            

        phone = re.findall(rephone,i)

        if len(phone) == 0:
            phone = 'No phone'
        else:
            phone = phone[0]
        address = re.findall(readdress,i)[0]
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        sql = '''insert into mysite_content(text,phone,address) values('{}','{}','{}')'''.format(content,phone,address) 
        #print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()

        
    

if __name__ == "__main__":
    main()

