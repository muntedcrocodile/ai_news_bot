
TEMPLATE = """
Author: {}\\
Published on: {}

AI Summary:\\
{}


Original: {} words
Summary: {} words
Percent reduction: {}

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


def make_body(text, summary, author, publish_date):

    summary = summary.replace("SKIP ADVERTISEMENT", "")

    original_length = len(text.split())
    summary_length = len(summary.split())
    percent_reduction = ((original_length - summary_length) / original_length) * 100
    percent_reduction = f"{percent_reduction:.2f}%"

    return TEMPLATE.format(author, publish_date.strftime("%d/%m/%Y | %H:%M:%S"), fix_paragraph_formatting(summary), original_length, summary_length, percent_reduction)



