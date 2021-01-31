import os
import time
from django.conf import settings
from django.template import loader
from utils.goods import get_categories,get_contents

def generate_static_index_html():
    """
        生成静态的主页html文件
        """
    print('%s: generate_static_index_html' % time.ctime())

    categories=get_categories()
    contents = get_contents()

    context = {
        'categories':categories,
        'contents':contents
    }


    # 获取首页模板文件
    template = loader.get_template('index.html')
    # 渲染首页html字符串
    html_text = template.render(context)
    # 将首页html字符串写入到指定目录，命名'index.html'
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)