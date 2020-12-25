from os.path import abspath, dirname, join

from markdown import markdown
from markdown_include.include import MarkdownInclude

markdown_include = MarkdownInclude(
    configs={
        'inheritHeadingDepth': True,
        'base_path': './docs/',
    },
)
docs_path = dirname(abspath(__file__))
root_path = abspath(join(docs_path, '../'))
year_path = abspath(join(docs_path, '../src/years/2020/'))

with open(join(docs_path, 'index.md'), 'r') as rf:
    with open(join(root_path, 'README.md'), 'w') as wf:
        wf.writelines(markdown(rf.read(), extensions=[markdown_include]))

with open(join(docs_path, 'year.md'), 'r') as rf:
    with open(join(year_path, 'README.md'), 'w') as wf:
        wf.writelines(markdown(rf.read(), extensions=[markdown_include]))
