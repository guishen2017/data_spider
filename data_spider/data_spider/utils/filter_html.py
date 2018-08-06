'''filte html tags'''
import re

def filte(html):
    """
    filte tags
    :param html: Html
    :return:
    """
    reg = re.compile('<[^>]*>')
    content = reg.sub('', html).replace('\n', '')
    return content
