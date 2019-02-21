# cookbookpy
Simple script to render static html for a personal cook book
## Requirements
Built for Python 3.6.5. 
Needs the modules [Jinja2](http://jinja.pocoo.org/) and [Markdown](https://python-markdown.github.io/) to be installed. 
## Usage
```python
from cookbookpy import Generator
source_content_dir = 'path/to/dir'
destination_content_dir = 'path/to/dir'
template_dir = 'path/to/dir'
language = 'en'
Generator(source_content_dir, destination_content_dir, template_dir, language)
```