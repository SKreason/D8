from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def censor(text):
    if isinstance(text,str):
        censor_list = list(open(f'{settings.BASE_DIR}/news/templatetags/censor_list.txt', encoding='UTF-8').read().split())
        # with open(f'{settings.BASE_DIR}/news/templatetags/censor_list.txt', encoding="utf-8") as f: #проверка пути
        in_text = list(text.split())
        text_clear = []
        for word in in_text:
            word_l = word.lower()
            word_cl = ""
            for i in word_l:
                punct_mark = ""
                simv_mark = "!?,.:;()@#$%^&*+-/<>"
                if i in simv_mark:
                    punct_mark = i
                    word_cl
                else:
                    word_cl = word_cl + i
            if word_cl in censor_list:
                text_clear.append(word[0] + "*" * (len(word) - 2) + punct_mark)
            else:
                text_clear.append(word)
        return " ".join(text_clear)
    else:
        raise ValueError("Применение не к строковым значениям")


