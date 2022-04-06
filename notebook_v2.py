#!/usr/bin/env python
# -*- coding: utf-8 -*-

# +
"""
an object-oriented version of the notebook toolbox
"""
import json
from notebook_v0 import get_format_version, get_cells

# zzz voyez le corrigé et les commentaires communs
# pour voir comment on pouvait éviter
# d'importer ces deux classes ici

from notebook_v1 import CodeCell as CodeCell_1
from notebook_v1 import MarkdownCell as MarkdownCell_1


# -

class CodeCell:
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.
        execution_count (int): The execution count of the cell.

    Attributes:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.
        execution_count (int): The execution count of the cell.

    Usage:

        >>> code_cell = CodeCell("b777420a", ['print("Hello world!")'], 1)
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    def __init__(self, id, source, execution_count):
        self.id = id
        self.source = source
        self.execution_count = execution_count


# +
class MarkdownCell:
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.

    Attributes:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell("a9541506", [
        ...     "Hello world!",
        ...     "============",
        ...     "Print `Hello world!`:"
        ... ])
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!', '============', 'Print `Hello world!`:']
    """

    def __init__(self, id, source):
        self.id = id
        self.source = source


# zzz
#markdown_cell = MarkdownCell(
#    "a9541506", ["Hello world!", "============", "Print `Hello world!`:"])
#markdown_cell.source


# -

class Notebook:
    r"""A Jupyter Notebook

    Args:
        version (str): The version of the notebook format.
        cells (list): The cells of the notebook (either CodeCell or MarkdownCell).

    Attributes:
        version (str): The version of the notebook format.
        cells (list): The cells of the notebook (either CodeCell or MarkdownCell).

    Usage:

        >>> version = "4.5"
        >>> cells = [
        ...     MarkdownCell("a9541506", [
        ...         "Hello world!",
        ...         "============",
        ...         "Print `Hello world!`:"
        ...     ]),
        ...     CodeCell("b777420a", ['print("Hello world!")'], 1),
        ... ]
        >>> nb = Notebook(version, cells)
        >>> nb.version
        '4.5'
        >>> isinstance(nb.cells, list)
        True
        >>> isinstance(nb.cells[0], MarkdownCell)
        True
        >>> isinstance(nb.cells[1], CodeCell)
        True
    """

    def __init__(self, version, cells):
        self.version = version
        self.cells = cells

    def __iter__(self):
        r"""Iterate the cells of the notebook.
        """
        return iter(self.cells)


class NotebookLoader:
    r"""Loads a Jupyter Notebook from a file

    Args:
        filename (str): The name of the file to load.

    Usage:
            >>> nbl = NotebookLoader("samples/hello-world.ipynb")
            >>> nb = nbl.load()
            >>> nb.version
            '4.5'
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
    """

    def __init__(self, filename):
        self.filename = filename

    def load(self):
        r"""Loads a Notebook instance from the file.
        """
        # zzz ça aurait été habile de réutiliser load_ipynb
        with open(self.filename, 'r') as f:
            string = f.read()
            dic = json.loads(string)
            cells = []
            for cell in dic['cells']:
                if cell['cell_type'] == 'markdown':
                    # pas hyper lisible, je me suis creusé les méninges 
                    # un moment avant de comprendre
                    # on aurait pu écrire
                    # v1 = MarkdownCell_1(cell)
                    # cells.append(MarkdownCell(v1.id, v1.source))
                    # en tous cas moi j'aurais mieux compris...
                    cells.append(MarkdownCell(MarkdownCell_1(
                        cell).id, MarkdownCell_1(cell).source))
                else:
                    cells.append(CodeCell(CodeCell_1(cell).id, CodeCell_1(
                        cell).source, CodeCell_1(cell).execution_count))
        return Notebook(get_format_version(dic), cells)


# +
class Markdownizer:
    r"""Transforms a notebook to a pure markdown notebook.

    Args:
        notebook (Notebook): The notebook to transform.

    Usage:

        >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
        >>> nb2 = Markdownizer(nb).markdownize()
        >>> nb2.version
        '4.5'
        >>> for cell in nb2:
        ...     print(cell.id)
        a9541506
        b777420a
        a23ab5ac
        >>> isinstance(nb2.cells[1], MarkdownCell)
        True
        >>> Serializer(nb2).to_file("samples/hello-world-markdown.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    # zzz
    # ATTENTION ici vous modifiez le notebook en-place
    # alors que l'énoncé demandait
    # > nous générons un nouveau notebook
    def markdownize(self):
        r"""Transforms the notebook to a pure markdown notebook.
        """
        # zzz
        # en plus ici vous modifiez self.notebook.cells
        # dans une boucle sur .. self.notebook.cells
        # (puisque l'itérateur fonctionne comme cela)
        # ce qui est une pratique interdite car dangereuse
        # voyez le corrigé !
        for indice, cell in enumerate(self.notebook):
            if isinstance(cell, CodeCell):
                cell.source = ['``` python', f'{cell.source}', '```']
                self.notebook.cells[indice] = MarkdownCell(
                    cell.id, cell.source)

        return self.notebook


# zzz
# nb = NotebookLoader("samples/hello-world.ipynb").load()
# nb2 = Markdownizer(nb).markdownize()
# nb2.version
# for cell in nb2:
#     print(cell.id)

# isinstance(nb2.cells[1], MarkdownCell)

# -


class MarkdownLesser:
    r"""Removes markdown cells from a notebook.

    Args:
        notebook (Notebook): The notebook to transform.

    Usage:

            >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
            >>> nb2 = MarkdownLesser(nb).remove_markdown_cells()
            >>> print(Outliner(nb2).outline())
            Jupyter Notebook v4.5
            └─▶ Code cell #b777420a (1)
                | print("Hello world!")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    # zzz
    # mêmes remarques, modification en place et modification
    # du sujet de la boucle
    def remove_markdown_cells(self):
        r"""Removes markdown cells from the notebook.

        Returns:
            Notebook: a Notebook instance with only code cells
        """
        # zzz idem modification sujet de la boucle
        for indice, cell in enumerate(self.notebook):
            if isinstance(cell, MarkdownCell):
                del self.notebook.cells[indice]
        return self.notebook

# zzz
# nb = NotebookLoader("samples/hello-world.ipynb").load()
# nb2 = MarkdownLesser(nb).remove_markdown_cells()


# +
class PyPercentLoader:
    r"""Loads a Jupyter Notebook from a py-percent file.

    Args:
        filename (str): The name of the file to load.
        version (str): The version of the notebook format (defaults to '4.5').

    Usage:

            >>> # Step 1 - Load the notebook and save it as a py-percent file
            >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
            >>> PyPercentSerializer(nb).to_file("samples/hello-world-py-percent.py")
            >>> # Step 2 - Load the py-percent file
            >>> nb2 = PyPercentLoader("samples/hello-world-py-percent.py").load()
            >>> nb.version
            '4.5'
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
    """

    def __init__(self, filename, version="4.5"):
        self.filename = filename
        self.version = version

    # zzz effectivement celle-ci était un peu plus compliquée...
    def load(self):
        r"""Loads a Notebook instance from the py-percent file.
        """
        with open(filename, 'r') as f:
            string = f.read()


# zzz
# nb = NotebookLoader("samples/hello-world.ipynb").load()
