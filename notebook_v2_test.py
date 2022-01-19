#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from notebook_v1 import *
from notebook_v2 import *

class Question15(unittest.TestCase):
    def test_build_code_cell(self):
        code_cell = CodeCell("b777420a", ['print("Hello world!")'], 1)
        self.assertEqual('b777420a', code_cell.id)
        self.assertEqual(1, code_cell.execution_count)
        self.assertEqual(
        ['print("Hello world!")']
            , code_cell.source)

    def test_build_markdown_cell(self):
        markdown_cell = MarkdownCell("a9541506", [
            "Hello world!\n",
            "============\n",
            "Print `Hello world!`:"
        ])
        self.assertEqual('a9541506', markdown_cell.id)
        self.assertEqual(
        ['Hello world!\n', '============\n', 'Print `Hello world!`:'],
             markdown_cell.source)

    def test_build_notebook(self):
        version = "4.5"
        cells = [
            MarkdownCell("a9541506", [
                "Hello world!",
                "============",
                "Print `Hello world!`:"
            ]),
            CodeCell("b777420a", ['print("Hello world!")'], 1),
        ]
        nb = Notebook(version, cells)
        self.assertEqual("4.5", nb.version)
        self.assertIsInstance(nb.cells, list)
        self.assertIsInstance(nb.cells[0], MarkdownCell)
        self.assertIsInstance(nb.cells[1], CodeCell)

class Question16(unittest.TestCase):
    def test_load_hello_world(self):
        nbl = NotebookLoader("samples/hello-world.ipynb")
        nb = nbl.load()
        self.assertEqual("4.5", nb.version)
        self.assertEqual("a9541506", nb.cells[0].id)
        self.assertEqual("b777420a", nb.cells[1].id)
        self.assertEqual("a23ab5ac", nb.cells[2].id)

class Question17(unittest.TestCase):
    def test_markdownizer(self):
        nb = NotebookLoader("samples/hello-world.ipynb").load()
        nb2 = Markdownizer(nb).markdownize()
        self.assertIsInstance(nb2.cells[0], MarkdownCell)
        self.assertIsInstance(nb2.cells[1], MarkdownCell)
        self.assertIsInstance(nb2.cells[2], MarkdownCell)

class Question18(unittest.TestCase):
    def test_markdownlesser(self):
        nb = NotebookLoader("samples/hello-world.ipynb").load()
        nb2 = MarkdownLesser(nb).remove_markdown_cells()
        self.assertEqual(1, len(nb2.cells))
        self.assertIsInstance(nb2.cells[0], CodeCell)

class Question19(unittest.TestCase):
    def test_py_percent_loader(self):
        nb = NotebookLoader("samples/hello-world.ipynb").load()
        PyPercentSerializer(nb).to_file("samples/hello-world-py-percent.py")
        nb2 = PyPercentLoader("samples/hello-world-py-percent.py").load()
        self.assertEqual("4.5", nb2.version)

        self.assertIsInstance(nb2.cells[0], MarkdownCell)
        first_source = [line.strip() for line in nb2.cells[0].source]
        self.assertEqual(["Hello world!", "============", "Print `Hello world!`:"], first_source)
        self.assertIsInstance(nb2.cells[1], CodeCell)
        self.assertIsInstance(nb2.cells[2], MarkdownCell)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
