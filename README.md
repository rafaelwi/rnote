# RNote Compiled Document Format
RNote is a simple, compiled document format intended for taking bullet-point notes.

![An example document](https://github.com/rafaelwi/rnote/raw/master/media/DEMO_OCT_4_2020.png "An example document")

## Features
- Easy to learn and use syntax designed for taking notes quickly
- Customizable document themes and templates
- Seventeen different page sizes to choose from
- Bold, underline, italicize, and strikethrough your text
- Insert images and tables with ease
- Simple command-line interface for generating your documents quickly

## Setup
1. Clone the repo<br>
```git clone https://github.com/rafaelwi/rnote```
2. CD into the `rnote` directory and create a new pipenv<br>
```pipenv install```<br>
This will install the necessary libraries  for RNote to work
3. Open up your favourite text editor and begin writing documents. [Take a look at the format spec sheet to learn the syntax.](https://github.com/rafaelwi/rnote/blob/master/spec.md)<br>
4. When you're done writing your document, simply enter the rnote directory and run the processor to generate your document into a PDF<br>
```python3 processor.py -i INPUT_FILE.rnote -o OUTPUT_FILE.pdf```

Contgratulations! If all has gone well, you have successfully created your first RNote document!
