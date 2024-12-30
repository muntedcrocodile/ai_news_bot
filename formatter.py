
TEMPLATE = """
Author: {}\\
Published on: {}

AI Summary:\\
{}


[I'm a bot and I'm open source](https://github.com/muntedcrocodile/ai_news_bot)
"""

from datetime import datetime

def fix_paragraph_formatting(paragraph):
    # Remove space before full stop
    paragraph = paragraph.replace(" .", ".")

    # Capitalize the first letter of each sentence
    sentences = paragraph.split(". ")
    fixed_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()  # Remove leading and trailing whitespace
        if sentence:  # If sentence is not empty
            sentence = sentence[0].upper() + sentence[1:]  # Capitalize first letter
        fixed_sentences.append(sentence)
    fixed_paragraph = ". ".join(fixed_sentences)

    return fixed_paragraph


def make_body(summary, author, publish_date):
    return TEMPLATE.format(author, publish_date.strftime("%d/%m/%Y | %H:%M:%S"), fix_paragraph_formatting(summary))



