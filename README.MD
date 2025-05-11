# Screen OCR Translator (Korean to English)

This is a Python desktop tool that allows you to select a portion of your screen containing Korean text, extract the text using OCR, and then translate it into English. The Korean text is also copied to your clipboard, with the English translation and a romanized version (when possible) printed to the console. Due to some proprietary Windows APIs, this tool is only compatible with Windows.

## Features

- Select a screen region with your mouse
- Extract Korean (or English) text using [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- Translate Korean to English locally using the [Helsinki-NLP MarianMT model](https://huggingface.co/Helsinki-NLP/opus-mt-ko-en)
- Romanize Korean text for pronunciation reference
- Automatically copy Korean text to clipboard
- Reuse selection region or reselect on demand
- Simple keyboard shortcuts for quick use

## Requirements

- Python 3.8 or higher
- The following Python packages:

```bash
pip install easyocr transformers pillow keyboard korean_romanizer pyperclip
