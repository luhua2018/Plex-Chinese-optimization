

import Config
import ChangeMovieTitleSort
import ChangeShowTitleSort
import ChangeMovieGenre
import ChangeShowGenre
import ChangeAlbumTitleSort
import ChangeArtistTitleSort

if __name__ == '__main__':
    print("")
    print("说明：本脚本的作用和使用方法")
    print("\t 1.本脚本会修改电影、剧集、音乐专辑和音乐艺术家的排序标题(TitleSort)为汉语拼音缩写。")
    # 对汉字的判定是Unicode编码范围在u4E00-u9FFF之间且在Python的pinyin库中能查到拼音的文字，其他范围的文字将保持原样。
    print("\t 2.本脚本会修改电影、剧集的类型(Grnre)为中文，类型的中英文对应的字典可在Config.py中自行扩充。")
    print("\t 3.运行此脚本需要Plex服务器的URL和Token，请在Config.py中填写。")
    print("\t 4.运行此脚本需要Python3环境并安装plexapi与pypinyin两个库。")
    print("")
    print("警告：可能会引起错误的情况：")
    print("\t 1.存在空的资料库。")
    print("\t 2.项目的标题或其他标签中含有特殊字符(命名时请尽量较少符号的使用)。")
    print("\t 3.在运行该脚本时Plex还未完成对资料库的扫描。")
    print("\t 4.服务器的URL或Token内容或格式不正确。")
    print("")
    print("🐸 很惭愧，就做了一点微小的工作，谢谢大家。\r\n")
    print("")
    input("按回车键继续...")
    print("")
    # 所有的操作都是基于 ChangeMovieTitleSort.py 和 ChangeMovieGenre.py 修改而来，如需修改代码请优先参考这两个文件
    ChangeMovieTitleSort.ChangeMovieTitleSort(Config.PLEX_URL,Config.PLEX_TOKEN)
    ChangeShowTitleSort.ChangeShowTitleSort(Config.PLEX_URL,Config.PLEX_TOKEN)
    ChangeMovieGenre.ChangeMovieGenre(Config.PLEX_URL,Config.PLEX_TOKEN)
    ChangeShowGenre.ChangeShowGenre(Config.PLEX_URL,Config.PLEX_TOKEN)
    ChangeAlbumTitleSort.ChangeAlbumTitleSort(Config.PLEX_URL,Config.PLEX_TOKEN)
    ChangeArtistTitleSort.ChangeArtistTitleSort(Config.PLEX_URL,Config.PLEX_TOKEN)

