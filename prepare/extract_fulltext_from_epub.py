import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

# <h1 class="chapterCaption"><a id="CHP14"></a>第十三回<br/>李傕郭汜大交兵<br/>杨奉董承双救驾</h1>
# <h1 class="chapterCaption1"><a id="CHP19"></a>第十八回<br/>贾文和料敌决胜<br/>夏侯惇拔矢啖睛<sup><a class="duokan-footnote" href="#jz_1_172" id="jzyy_1_172"><img alt="" src="../Images/note.png"/></a></sup></h1>
def split_chapter_caption(h1_element):
    output = []
    for child in h1_element.children:
        if child.string != None:
            # print(child.string)
            output.append(child.string)
    return '，'.join(output) + "。"

def load_rare_chars(filepath):
    d = {}
    with open(filepath, 'r') as f:
        for line in f:
            (key, value) = line.split()
            d[key] = value
    return d

# <span class="rareFont"><img src="../Images/image01005.gif" alt=""/></span>
def convert_rare_characters(chapter, rare_chars_dict):
    rare_chars = chapter.find_all('span', class_='rareFont')
    for rare_char in rare_chars:
        for child in rare_char.children:
            image_path = child['src']
            image_name = os.path.basename(image_path)
            rare_char.replace_with(rare_chars_dict[image_name])


def thtml2text(thtml, rare_chars_dict):
    # print(thtml.decode('utf-8'))
    output = []
    soup = BeautifulSoup(thtml.decode('utf-8'), 'html.parser')
    convert_rare_characters(soup, rare_chars_dict)
    captions = soup.find_all('h1')
    for caption in captions:
        splitted_caption  = split_chapter_caption(caption)
        # print(splitted_caption)
        output.append(splitted_caption)
    paragraphs = soup.find_all('p', class_='bodyContent')
    for paragraph in paragraphs:
        # print(paragraph.text)
        output.append(paragraph.text)
    return '\n'.join(output)
  
if __name__ == '__main__':
    # load rare characters dictionary
    rare_chars_dict = load_rare_chars("../data/raw/rare_characters.txt")
    chapters = epub2thtml("../data/raw/sgyy.epub")
    # print(len(chapters))
    count = 0
    for chapter in chapters:
        # skip first 3 chapters
        if count >= 3:
            text = thtml2text(chapter, rare_chars_dict)
            with open("../data/text/ch{:03d}.txt".format(count-2), 'w') as f:
                f.write(text)
        count += 1