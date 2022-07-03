def extract_texts_from_toppage(url):
    toppage = get_page(url)                         # トップページを読む
    anchors = extract_anchors(toppage, url)         # トップページのリンクを抽出

    all_texts = []
    print('Loading page: ', end='', file=sys.stdout, flush=True)
    for link in anchors:
        print('.', end='', file=sys.stderr, flush=True)
        html = get_page(link)
        if html is None:
            continue

        texts = extract_texts(html)                 # テキストを抽出
        all_texts.extend(texts)

    return all_texts

