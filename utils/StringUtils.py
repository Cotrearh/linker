import re

stoplist = {
    "и",
    "или",
    "с",
    "к",
    "в",
    "на",
    "до",
    "за",
    ",",
    ".",
    ":",
    ";",
    "(",
    ")",
    "[",
    "]",
    "-",
    "),",
    "при",
    "не",
    "по"
}

stoplist_list = [
    "и",
    "или",
    "с",
    "к",
    "в",
    "на",
    "до",
    "за",
    ",",
    ".",
    ":",
    ";",
    "(",
    ")",
    "[",
    "]",
    "-",
    "),",
    "при",
    "не",
    "по"
]

stoplist_non_chars = [
    ",",
    ".",
    ":",
    ";"
]

postfix_set_4 = {
    "оями",
    "иями",
}

postfix_set_3 = {
    "ами",
    "его",
    "ему",
    "ери",
    "ими",
    "иям",
    "иях",
    "овь",
    "ого",
    "оев",
    "ому",
    "оям",
    "оях",
    "ыми",
    "ями",
}

postfix_set_2 = {
    "ам",
    "ах",
    "ая",
    "ев",
    "ей",
    "ем",
    "ею",
    "ея",
    "ии",
    "ий",
    "им",
    "их",
    "ию",
    "ие",
    "ия",
    "ми",
    "ов",
    "ое",
    "ой",
    "ом",
    "ою",
    "ую",
    "ые",
    "ый",
    "ым",
    "ых",
    "ьв",
    "юю",
    "ям",
    "ях",
    "яя",
    "ём",
}

postfix_set_1 = {
    "а",
    "е",
    "и",
    "й",
    "о",
    "у",
    "ы",
    "ь",
    "я",
}


def slicer(prep_str):
    prep_len = len(prep_str)

    if prep_len >= 7:
        prep_slice = prep_str[-4:]
        if prep_slice in postfix_set_4:
            return prep_str[:-4]

    if prep_len >= 6:
        prep_slice = prep_str[-3:]
        if prep_slice in postfix_set_3:
            return prep_str[:-3]

    if prep_len >= 5:
        prep_slice = prep_str[-2:]
        if prep_slice in postfix_set_2:
            return prep_str[:-2]

    if prep_len >= 4:
        prep_slice = prep_str[-1:]
        if prep_slice in postfix_set_1:
            return prep_str[:-1]

    return prep_str


def stem_str(str):
    str = str.lower()
    str = re.sub(r'[^a-zA-Zа-яА-Я0-9 \t]', '', str)
    words = re.split("[ \t]+", str)
    words = [slicer(x) for x in words if x not in stoplist]
    res = ''.join(words)
    return res


def remove_all_tags(str):
    res = re.sub(r'<.*>', '', str)
    res = res.replace('&nbsp;', '')
    return res


def toInitialHtmlFormat(html):
    html = html.replace('\n', '')
    for t in re.findall(r'<span[^>]*>.*?</span>', html):
        newt = re.sub(r'(^(.*?)(?=<p))|((</*[^ap>]*>))|((</*span[^>]*>))', '', t)
        span_only = re.findall(r'<span.*?>', t)[0]
        if 'super' in span_only:
            newt = '<SUP>' + newt + '</SUP>'
        if 'sub' in span_only:
            newt = '<SUB>' + newt + '</SUB>'
        if 'font-weight' in span_only:
            newt = '<B>' + newt + '</B>'
        if 'italic' in span_only:
            newt = '<I>' + newt + '</I>'
        if 'underline' in span_only:
            newt = '<U>' + newt + '</U>'
        html = html.replace(t, newt)

    html = html.replace('<a href', '<A href')
    html = html.replace('</a>', '</A>')
    html = re.sub(r'</I> +<I>', ' ', html)
    html = re.sub(r'</I><I>', '', html)
    html = re.sub(r'</U> +<U>', ' ', html)
    html = re.sub(r'</U><U>', '', html)
    html = re.sub(r'</B> +<B>', ' ', html)
    html = re.sub(r'</B><B>', '', html)
    html = re.sub(r'</SUP> +<SUP>', ' ', html)
    html = re.sub(r'</SUP><SUP>', '', html)
    html = re.sub(r'</SUB> +<SUB>', ' ', html)
    html = re.sub(r'</SUB><SUB>', '', html)

    for t in re.findall(r'><U>[^U]*</U></A>', html):
        newt = t.replace('</U>', '').replace('<U>', '')
        html = html.replace(t, newt)

    res = re.sub(r'(^(.*?)(?=<p))|((</*[^ApUIB>]*>))|((</*span[^>]*>))', '', html)  # Очистка от лишних тегов
    res = re.sub(r'(?<=<p)[^>]*(?=>)', '', res)  # Очистка тега <p> от лишней информации

    res = res.replace(' />', '>')
    res = res.strip()
    res = re.sub(r'</p><p>$', '', res)
    res = res.replace('</p><p></p><p>', '</p><p>&nbsp;</p><p>')
    res = re.sub(r'^<p>', '', res)
    res = re.sub(r'</p>$', '', res)
    return res


def delete_uuid_from_definition(uuid, definition):
    links = re.findall(r'<[Aa][^>]*' + uuid.__str__() + '[^>]*>(?:.*?)<\/[Aa]>', definition)
    for l in links:
        new_l = re.sub(r'<\/*[Aa][^>]*>', '', l)
        definition = re.sub(l, new_l, definition)
    return definition
