# Plex-Chinese-optimization

**修改Plex的电影、剧集、音乐专辑和音乐艺术家的排序标题(TitleSort)为汉语拼音缩写；修改电影、剧集的类型(Grnre)为中文。**

## 说明：本脚本的作用和使用方法

1. 本脚本会修改电影、剧集、音乐专辑和音乐艺术家的排序标题(TitleSort)为汉语拼音缩写（对汉字的判定是Unicode编码范围在u4E00-u9FFF之间且在Python的pinyin库中能查到拼音的文字，其他范围的文字将保持原样）。

2. 本脚本会修改电影、剧集的类型(Grnre)为中文，类型的中英文对应的字典可在Config.py中自行扩充。

3. 运行此脚本需要Plex服务器的URL和Token，请在Config.py中填写。

4. 运行此脚本需要Python3环境并安装plexapi与pypinyin两个库。
