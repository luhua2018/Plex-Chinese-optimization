# python 3
# pip install plexapi
# pip install pypinyin
# 更多中文插件请访问plexmedia.cn

import urllib
import http.client
import json
import sys
import pypinyin
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
from plexapi.myplex import MyPlexDevice

PLEX_URL = ""
PLEX_TOKEN = ""
sectionNum = ""


def fetchPlexApi(path='', method='GET', getFormPlextv=False, token=PLEX_TOKEN, params=None):
    """a helper function that fetches data from and put data to the plex server"""
    # print(path)
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


def updateSortTitle(rating, item):
    sortQuery = urllib.parse.quote(item.encode('utf-8'))
    data = fetchPlexApi("/library/sections/"+sectionNum+"/all?type=9&id=%s&titleSort.value=%s&" %
                        (rating, sortQuery), "PUT", token=PLEX_TOKEN)


def uniqify(seq):
    # Not order preserving
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()

# 判断是否包含中文字符


def check_contain_chinese(check_str):
    for ch in check_str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def changepinyin(title):
    a = pypinyin.pinyin(title, style=pypinyin.FIRST_LETTER)
    b = []
    for i in range(len(a)):
        b.append(str(a[i][0]).upper())
    c = ''.join(b)
    return c


def loopThroughAllAlbums():
    global PLEX_URL, PLEX_TOKEN, sectionNum
    toDo = True
    start = 0
    size = 100
    while toDo:
        if len(sectionNum):
            url = "/library/sections/" + sectionNum + \
                "/all?type=9&X-Plex-Container-Start=%i&X-Plex-Container-Size=%i" % (
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
            #    print(toDo)
            # loop through all elements
            for music in elements:
                mediaType = music["type"]
                if mediaType != "album":
                    continue
                # 存在 TitleSort 且不包含中文字符的话跳出本次循环，否则就会继续执行修改 TitleSort
                if ('titleSort' in music) and (check_contain_chinese(music["titleSort"]) == False):
                    continue
                # 创建处理后的 TitleSort
                key = music["ratingKey"]
                title = music["title"]
                SortTitle = changepinyin(title)
                print("\t", "ChangeTitleSort：", title, "  ->  ", SortTitle)
                updateSortTitle(key, SortTitle)


def CheckAlbumTitleSort():
    global PLEX_URL, PLEX_TOKEN, sectionNum
    toDo = True
    start = 0
    size = 100
    while toDo:
        if len(sectionNum):
            url = "/library/sections/" + sectionNum + \
                "/all?type=9&X-Plex-Container-Start=%i&X-Plex-Container-Size=%i" % (
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
            for music in elements:
                mediaType = music["type"]
                if mediaType != "album":
                    continue
                # 若没有 TitleSort，则尝试加一个空格并重新写入
                if 'titleSort' not in music:
                    key = music["ratingKey"]
                    title = music["title"]
                    SortTitle = changepinyin(title) + ' '
                    print("\t", "ChangeTitleSort(Retry)：", title, "  ->  ", SortTitle)
                    updateSortTitle(key, SortTitle)


def ChangeAlbumTitleSort(URL, TOKEN):
    global PLEX_URL, PLEX_TOKEN, sectionNum
    PLEX_URL = URL
    PLEX_TOKEN = TOKEN
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    for section in plex.library.sections():
        # 筛选出类型为音乐，语言为中文或 None 的资料库
        # 在 Plex 中音乐库这一大类的类型就被称为 "artist", 与 "show、movie" 同级
        if section.type == 'artist' and (section.language == 'zh-CN' or section.language == 'xn'):
            print("准备处理 专辑　 TitleSort，库：", section.key, section.type,
                  section.title, section.language)
            sectionNum = str(section.key)
            # run at startup
            loopThroughAllAlbums()
            # 在音乐库中遇到过少数专辑或艺术家写入 TitleSort 失败的情况，此时加一个空格并重试写入可以成功。其它类型的资料库中暂未发现类似问题
            CheckAlbumTitleSort()
