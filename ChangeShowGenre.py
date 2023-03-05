import urllib
import http.client
import json
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
from plexapi.myplex import MyPlexDevice

PLEX_URL = ""
PLEX_TOKEN = ""
sectionNum = ""
currenttitle = ""
genreTags = ""

def fetchPlexApi(path='', method='GET', getFormPlextv=False, token=PLEX_TOKEN, params=None):
    """a helper function that fetches data from and put data to the plex server"""
    headers = {'X-Plex-Token': token,
               'Accept': 'application/json'}
    if getFormPlextv:
        url = 'plex.tv'
        connection = http.client.HTTPSConnection(url)
    else:
        url = PLEX_URL.rstrip('/').replace('http://', '')
        connection = http.client.HTTPConnection(url)
    try:
        if method.upper() == 'GET':
            pass
        elif method.upper() == 'POST':
            headers.update(
                {'Content-type': 'application/x-www-form-urlencoded'})
            pass
        elif method.upper() == 'PUT':
            pass
        elif method.upper() == 'DELETE':
            pass
        else:
            print("Invalid request method provided: {method}".format(
                method=method))
            connection.close()
            return

        connection.request(method.upper(), path, params, headers)
        response = connection.getresponse()
        r = response.read()
        contentType = response.getheader('Content-Type')
        status = response.status
        connection.close()

        if response and len(r):
            if 'application/json' in contentType:
                return json.loads(r)
            elif 'application/xml' in contentType:
                return contentType.parse(r)
            else:
                return r
        else:
            return r

    except Exception as e:
        connection.close()
        print("Error fetching from Plex API: {err}".format(err=e))


def updategenre(rating, genre):
    for tag in genre:
        try:
            enggenre = tag["tag"]
            enggenre = urllib.parse.quote(enggenre.encode('utf-8'))
            zhQuery = genreTags[tag["tag"]]
            zhQuery = urllib.parse.quote(zhQuery.encode('utf-8'))
            data = fetchPlexApi("/library/sections/"+sectionNum+"/all?type=2&id="+rating +
                                "&genre%5B2%5D.tag.tag="+zhQuery+"&genre%5B%5D.tag.tag-="+enggenre+"&", "PUT", token=PLEX_TOKEN)
            print("\t","ChangeGenre：", currenttitle, tag["tag"], "->", genreTags[tag["tag"]])
        except:
            pass


def getgenre(rating):
    url = "/library/metadata/"+rating+"?checkFiles=1"
    metadata = fetchPlexApi(url, token=PLEX_TOKEN)
    container = metadata["MediaContainer"]
    elements = container["Metadata"]
    for show in elements:
        genre = show["Genre"]
        updategenre(rating, genre)


def loopThroughAllShows():
    global PLEX_URL, PLEX_TOKEN, sectionNum,currenttitle
    toDo = True
    start = 0
    size = 100
    while toDo:
        if len(sectionNum):
            url = "/library/sections/" + sectionNum + \
                "/all?type=2&X-Plex-Container-Start=%i&X-Plex-Container-Size=%i" % (
                    start, size)
            metadata = fetchPlexApi(url, token=PLEX_TOKEN)
            container = metadata["MediaContainer"]
            elements = container["Metadata"]
            totalSize = container["totalSize"]
            offset = container["offset"]
            size = container["size"]
            start = start + size
            if totalSize-offset-size == 0:
                toDo = False
            for show in elements:
                mediaType = show["type"]
                if mediaType != "show":
                    continue
                if "Genre" not in show:
                    continue
                key = show["ratingKey"]
                currenttitle = show["title"]
                # print(title)
                getgenre(key)

def ChangeShowGenre(URL, TOKEN, TAGS):
    global PLEX_URL, PLEX_TOKEN, genreTags, sectionNum
    PLEX_URL = URL
    PLEX_TOKEN = TOKEN
    genreTags = TAGS
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    for section in plex.library.sections():
        # 筛选出类型为剧集，语言为中文或 None 的资料库
        if section.type == 'show' and (section.language == 'zh-CN' or section.language == 'xn'):
            print("准备处理 剧集　 Genre，    库：", section.key, section.type,
                  section.title, section.language)
            sectionNum = str(section.key)
            # run at startup
            loopThroughAllShows()
