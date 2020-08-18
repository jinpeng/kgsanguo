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

def thtml2text(thtml):
    # print(thtml.decode('utf-8'))
    output = []
    soup = BeautifulSoup(thtml.decode('utf-8'), 'html.parser')
    captions = soup.find_all('h1', class_='chapterCaption1')
    for caption in captions:
        # print(caption.text)
        output.append(caption.text)
    paragraphs = soup.find_all("p", class_="bodyContent")
    for paragraph in paragraphs:
        # print(paragraph.text)
        output.append(paragraph.text)
    return '\n'.join(output)
  
'''
    TODO: 1. Fix some chapter caption loss.
          2. Split chapter caption into 3 segements.
          3. Convert rare characters from images to text.
'''
if __name__ == '__main__':
    chapters = epub2thtml("../data/raw/sgyy.epub")
    # print(len(chapters))
    count = 0
    for chapter in chapters:
        # skip first 3 chapters
        if count >= 3:
            text = thtml2text(chapter)
            with open("../data/text/ch{:03d}.txt".format(count-2), 'w') as f:
                f.write(text)
        count += 1