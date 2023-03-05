# # 该文件仅在生成 Config.txt 时临时使用，真正的配置在 Config.txt 里

# import json

# # 服务器参数
# PLEX_URL = "http://127.0.0.1:32400"
# PLEX_TOKEN = "2wX1nS7oRp8pW7yH9qZz"

# # Genre 字典
# tags = {
#     "Action": "动作",
#     "Martial Arts": "武打",
#     "Adventure": "冒险",
#     "Animation": "动画",
#     "Anime": "日本动画",
#     "Comedy": "喜剧",
#     "Crime": "犯罪",
#     "Documentary": "纪录",
#     "Drama": "剧情",
#     "Family": "家庭",
#     "Fantasy": "奇幻",
#     "History": "历史",
#     "Horror": "恐怖",
#     "Music": "音乐",
#     "Mystery": "悬疑",
#     "Romance": "爱情",
#     "Science Fiction": "科幻",
#     "Sci-Fi & Fantasy": "科幻",
#     "Sport": "体育",
#     "Thriller": "惊悚",
#     "War": "战争",
#     "Western": "西部",
#     "Biography": "传记",
#     "Film-noir": "黑色",
#     "Musical": "音乐",
#     "Sci-Fi": "科幻",
#     "Tv Movie": "电视",
#     "Disaster": "灾难",
#     "Children": "儿童",
#     "Short": "短片",
#     "War & Politics": "战争/政治",
# }

# # 保存配置到TXT文档
# # 以UTF8编码打开文件
# with open('Config.txt', 'w', encoding='utf-8') as f:
#     # 将 tags 字典保存到文件，不将中文字符转换为Unicode编码，生成的JSON字符串中使用4个空格来缩进每一层
#     json.dump([PLEX_URL, PLEX_TOKEN, tags], f, ensure_ascii=False, indent=4)
