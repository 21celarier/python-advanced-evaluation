#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
an object-oriented version of the notebook toolbox
"""
from notebook_v0 import load_ipynb
import pprint
import json
import ast


class Cell:

    def __init__(self, ipynb):
        self.id = ipynb['id']
        self.source = ipynb['source']
        self.type = ipynb['cell_type']


class CodeCell(Cell):
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    def __init__(self, ipynb):
        super().__init__(ipynb)
        if self.type == "code":
            self.execution_count = ipynb['execution_count']


class MarkdownCell(Cell):
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    def __init__(self, ipynb):
        super().__init__(ipynb)


class Notebook:
    r"""A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """

    def __init__(self, ipynb):
        self.cells = []
        self.version = f'{ipynb["nbformat"]}' + \
            '.' + f'{ipynb["nbformat_minor"]}'
        for cell in ipynb['cells']:
            if cell['cell_type'] == 'markdown':
                self.cells.append(MarkdownCell(cell))
            else:
                self.cells.append(CodeCell(cell))

    @staticmethod
    def from_file(filename):
        r"""Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        with open(filename, 'r') as f:
            string = f.read()
            try:
                dic = json.loads(string)
            except:
                dic = ast.literal_eval(string)

        return Notebook(dic)

    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        return iter(self.cells)


# +
class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def to_py_percent(self):
        r"""Converts the notebook to a string in py-percent format.
        """
        text = ''
        for cell in self.notebook:
            if cell.type == 'markdown':
                text += '# %% [markdown]\n'
                for line in cell.source:
                    text += '# ' + line
                text += '\n\n'
            else:
                text += '# %%\n'
                for line in cell.source:
                    text += line
                text += '\n\n'
        text = text[:-2]
        return text

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        with open(filename, 'w+') as file:
            file.write(str(self.to_py_percent()))


class Serializer:
    r"""Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'metadata': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'metadata': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'metadata': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        dic = dict()
        dic['cells'] = []
        for cell in self.notebook:
            if isinstance(cell, MarkdownCell):
                dic['cells'].append(
                    {'cell_type': cell.type, 'id': cell.id, 'metadata': {}, 'source': cell.source})
            else:
                dic['cells'].append({'cell_type': cell.type, 'execution_count': cell.execution_count,
                                    'id': cell.id, 'metadata': {}, 'outputs': [], 'source': cell.source})
        dic['metadata'] = {}
        dic['nbformat'] = int(self.notebook.version[0])
        dic['nbformat_minor'] = int(self.notebook.version[-1])
        return dic

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        with open(filename, 'w+') as file:
            file.write(str(self.serialize()))


# -


class Outliner:
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def outline(self):
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        text = f'Jupyter Notebook v{self.notebook.version}\n'
        for cell in self.notebook:
            text += f'└─▶ {cell.type.capitalize()} cell #{cell.id}'
            if cell.type == 'code':
                text += f' ({cell.execution_count})'
            text += '\n'
            if len(cell.source) != 1:
                for indice, line in enumerate(cell.source):
                    if indice == 0:
                        text += '    ┌  '
                    elif indice == len(cell.source) - 1:
                        text += '    └  '
                    else:
                        text += '    │  '
                    text += line

            else:

                text += '    | ' + cell.source[0]
            text += '\n'
        return text[:-1]
nb = Notebook.from_file("samples/hello-world.ipynb")
ppp = PyPercentSerializer(nb)
# print(ppp.to_py_percent())
o = Outliner(nb)
# r"""Jupyter Notebook v4.5
# └─▶ Markdown cell #a9541506
#    ┌  Hello world!
#    │  ============
#    └  Print `Hello world!`:
# └─▶ Code cell #b777420a (1)
#    | print("Hello world!")
# └─▶ Markdown cell #a23ab5ac
#    | Goodbye! 👋""")
o.outline()
