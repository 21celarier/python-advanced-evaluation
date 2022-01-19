#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import numpy as np

from notebook_v0 import *

def strip_last_lines(s):
    while s and s.endswith("\n"):
        s = s[:-1]
    return s

class Question1(unittest.TestCase):
    def test_load_ipynb_minimal(self):
        ipynb = load_ipynb("samples/minimal.ipynb")
        self.assertEqual(
            {
                "cells": [],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5,
            },
            ipynb,
        )

    def test_load_ipynb_hello_world(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        self.assertEqual(
            {
                "cells": [
                    {
                        "cell_type": "markdown",
                        "id": "a9541506",
                        "metadata": {},
                        "source": [
                            "Hello world!\n",
                            "============\n",
                            "Print `Hello world!`:",
                        ],
                    },
                    {
                        "cell_type": "code",
                        "execution_count": 1,
                        "id": "b777420a",
                        "metadata": {},
                        "outputs": [
                            {
                                "name": "stdout",
                                "output_type": "stream",
                                "text": ["Hello world!\n"],
                            }
                        ],
                        "source": ['print("Hello world!")'],
                    },
                    {
                        "cell_type": "markdown",
                        "id": "a23ab5ac",
                        "metadata": {},
                        "source": ["Goodbye! 👋"],
                    },
                ],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5,
            },
            ipynb,
        )

    def test_save_ipynb_minimal(self):
        ipynb = load_ipynb("samples/minimal.ipynb")
        self.assertIsNotNone(ipynb)
        save_ipynb(ipynb, "samples/minimal-save-load.ipynb")
        try:
            ipynb_saved = load_ipynb("samples/minimal-save-load.ipynb")
            self.assertIsNotNone(ipynb_saved)
            self.assertEqual(ipynb, ipynb_saved)
        finally:
            os.remove("samples/minimal-save-load.ipynb")

    def test_save_ipynb_hello_world(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        self.assertIsNotNone(ipynb)
        save_ipynb(ipynb, "samples/hello-world-save-load.ipynb")
        try:
            ipynb_saved = load_ipynb("samples/hello-world-save-load.ipynb")
            self.assertIsNotNone(ipynb_saved)
            self.assertEqual(ipynb, ipynb_saved)
        finally:
            os.remove("samples/hello-world-save-load.ipynb")

class Question2(unittest.TestCase):
    def test_get_format_version_minimal(self):
        ipynb = load_ipynb("samples/minimal.ipynb")
        self.assertEqual("4.5", get_format_version(ipynb))

    def test_get_format_version_hello_world(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        self.assertEqual("4.5", get_format_version(ipynb))

    def test_get_metadata(self):
        ipynb = load_ipynb("samples/metadata.ipynb")
        self.assertEqual(
            {
                "celltoolbar": "Edit Metadata",
                "kernelspec": {
                    "display_name": "Python 3 (ipykernel)",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {
                    "codemirror_mode": {"name": "ipython", "version": 3},
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.9.7",
                },
            },
            get_metadata(ipynb),
        )

    def test_get_cells_minimal(self):
        ipynb = load_ipynb("samples/minimal.ipynb")
        self.assertEqual([], get_cells(ipynb))

    def test_get_cells_hello_world(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        self.assertEqual(
            [
                {
                    "cell_type": "markdown",
                    "id": "a9541506",
                    "metadata": {},
                    "source": [
                        "Hello world!\n",
                        "============\n",
                        "Print `Hello world!`:",
                    ],
                },
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "id": "b777420a",
                    "metadata": {},
                    "outputs": [
                        {
                            "name": "stdout",
                            "output_type": "stream",
                            "text": ["Hello world!\n"],
                        }
                    ],
                    "source": ['print("Hello world!")'],
                },
                {
                    "cell_type": "markdown",
                    "id": "a23ab5ac",
                    "metadata": {},
                    "source": ["Goodbye! 👋"],
                },
            ],
            get_cells(ipynb),
        )

class Question3(unittest.TestCase):
    def test_to_percent_hello_world(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        self.assertEqual(
            r"""# %% [markdown]
# Hello world!
# ============
# Print `Hello world!`:

# %%
print("Hello world!")

# %% [markdown]
# Goodbye! 👋""",
            strip_last_lines(to_percent(ipynb)),
        )

    def test_to_starboard_text(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(to_starboard(ipynb))
        self.assertEqual(
            r"""# %% [markdown]
Hello world!
============
Print `Hello world!`:
# %% [python]
print("Hello world!")
# %% [markdown]
Goodbye! 👋""",
            strip_last_lines(to_starboard(ipynb)),
        )

class Question4(unittest.TestCase):
    def test_to_starboard_html(self):
        self.maxDiff = None
        ipynb = load_ipynb("samples/hello-world.ipynb")
        begin_with = """<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Starboard Notebook</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <link rel="icon" href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/favicon.ico">
        <link href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.css" rel="stylesheet">
    </head>
    <body>
        <script>
            window.initialNotebookContent = '"""
        starboard_code = '# %% [markdown]\\nHello world!\\n============\\nPrint `Hello world!`:\\n# %% [python]\\nprint("Hello world!")\\n# %% [markdown]\\nGoodbye! 👋'
        ends_with = """'
            window.starboardArtifactsUrl = `https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/`;
        </script>
        <script src="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.js"></script>
    </body>
</html>"""
        html = to_starboard(ipynb, html=True)
        self.assertIn(begin_with, html)
        self.assertIn(starboard_code, html)
        self.assertIn(ends_with, html)

class Question5(unittest.TestCase):
    def test_clear_output(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        clear_outputs(ipynb)
        self.assertEqual(
            {
                "cells": [
                    {
                        "cell_type": "markdown",
                        "id": "a9541506",
                        "metadata": {},
                        "source": [
                            "Hello world!\n",
                            "============\n",
                            "Print `Hello world!`:",
                        ],
                    },
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "id": "b777420a",
                        "metadata": {},
                        "outputs": [],
                        "source": ['print("Hello world!")'],
                    },
                    {
                        "cell_type": "markdown",
                        "id": "a23ab5ac",
                        "metadata": {},
                        "source": ["Goodbye! 👋"],
                    },
                ],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5,
            },
            ipynb,
        )

        for cell in get_cells(ipynb):
            if cell["cell_type"] == "code":
                self.assertEqual(None, cell["execution_count"])
                self.assertEqual([], cell["outputs"])

class Question6(unittest.TestCase):
    def test_get_streams(self):
        ipynb = load_ipynb("samples/streams.ipynb")
        self.assertEqual("👋 Hello world! 🌍\n", get_stream(ipynb))
        self.assertEqual(
            "🔥 This is fine. 🔥 (https://gunshowcomic.com/648)\n",
            get_stream(ipynb, stdout=False, stderr=True),
        )
        self.assertEqual(
            r"""👋 Hello world! 🌍
🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
""",
            get_stream(ipynb, stdout=True, stderr=True),
        )

class Question7(unittest.TestCase):
    def test_exceptions_hello_world(self):
        ipynb = load_ipynb("samples/hello-world.ipynb")
        self.assertEqual([], get_exceptions(ipynb))

    def test_exceptions_errors(self):
        ipynb = load_ipynb("samples/errors.ipynb")
        errors = get_exceptions(ipynb)
        self.assertEqual(len(errors), 2)
        for error in errors:
            self.assertIsInstance(error, Exception)
        self.assertEqual(
            "TypeError(\"unsupported operand type(s) for +: 'int' and 'str'\")",
            repr(errors[0]),
        )
        self.assertEqual("Warning('🌧️  light rain')", repr(errors[1]))

class Question8(unittest.TestCase):
    def test_get_images(self):
        ipynb = load_ipynb("samples/images.ipynb")
        images = get_images(ipynb)
        self.assertIsInstance(images, list)
        for image in images:
            self.assertIsInstance(image, np.ndarray)

        grace_hopper_image = images[0]
        self.assertEqual((600, 512, 3), grace_hopper_image.shape)
        self.assertEqual(np.uint8, grace_hopper_image.dtype)


if __name__ == "__main__":
    unittest.main()
