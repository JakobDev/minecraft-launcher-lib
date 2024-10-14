# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import subprocess
import importlib
import pathlib
import inspect
import shutil
import sys
import os

sys.path.insert(0, os.path.abspath('..'))

import minecraft_launcher_lib  # noqa: E402

# -- Project information -----------------------------------------------------

project = 'minecraft-launcher-lib'
copyright = '2019-2024, JakobDev'
author = 'JakobDev'

# The full version, including alpha/beta/rc tags
with open(pathlib.Path(__file__).parent.parent / "minecraft_launcher_lib" / "version.txt", "r", encoding="utf-8") as f:
    release = f.read().strip()

master_doc = 'index'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.coverage", "sphinx.ext.napoleon", "sphinx.ext.linkcode", "sphinx.ext.extlinks"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_extra_path = ["robots.txt"]

html_css_files = ["custom.css"]

autodoc_member_order = "bysource"
autodoc_typehints = "both"
add_module_names = False

default_dark_mode = False

html_theme_options = {
    "style_external_links": True
}

if os.environ.get("READTHEDOCS_CANONICAL_URL") is not None:
    html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

try:
    commit = subprocess.run(["git", "log", "-n1", "--pretty=format:%H"], check=True, capture_output=True).stdout.decode("utf-8").strip()
except Exception as ex:
    print(ex, file=sys.stderr)
    commit = None


if commit is not None:
    extlinks = {"repolink": (f"https://codeberg.org/JakobDev/minecraft-launcher-lib/src/commit/{commit}/%s", "repofile %s")}
else:
    extlinks = {"repolink": ("https://codeberg.org/JakobDev/minecraft-launcher-lib/src/branch/master/%s", "repofile %s")}


def linkcode_resolve(domain: str, info: dict[str, str]):
    if domain != "py":
        return None

    if "." in info["fullname"]:
        return None

    if commit is None:
        return None

    module_name = info["module"].removeprefix("minecraft_launcher_lib.")

    obj = getattr(getattr(minecraft_launcher_lib, module_name), info["fullname"])
    source_line = inspect.getsourcelines(obj)[1]

    return f"https://codeberg.org/JakobDev/minecraft-launcher-lib/src/commit/{commit}/minecraft_launcher_lib/{module_name}.py#L{source_line}"


def add_optional_extension(name: str) -> None:
    try:
        importlib.import_module(name)
        extensions.append(name)
    except ModuleNotFoundError:
        print(f"Optional module {name} was not found", file=sys.stderr)


add_optional_extension("sphinx_reredirects")
add_optional_extension("notfound.extension")
add_optional_extension("sphinx_rtd_dark_mode")
add_optional_extension("sphinx_copybutton")
add_optional_extension("sphinxext.opengraph")

redirects = {
    "command": "modules/command.html",
    "exceptions": "modules/exceptions.html",
    "fabric": "modules/fabric.html",
    "forge": "modules/forge.html",
    "install": "modules/install.html",
    "microsoft_account": "modules/microsoft_account.html",
    "natives": "modules/natives.html",
    "runtime": "modules/runtime.html",
    "utils": "modules/utils.html",
    "develop/making_a_merge_request": "making_a_pull_request.html"
}


def write_module_file(in_path: pathlib.Path, out_dir: pathlib.Path) -> None:
    with open(os.path.join(out_dir, in_path.stem + ".rst"), "w", encoding="utf-8") as f:
        f.write(".. This File ia autogenerated. Do not edit.\n\n")
        f.write(in_path.stem + "\n")
        f.write("==========================\n")
        f.write(f".. automodule:: minecraft_launcher_lib.{in_path.stem}\n")
        f.write("  :show-inheritance:\n")
        f.write("  :undoc-members:\n")
        f.write("  :members:\n")
        f.write(f"\n\n:repolink:`View the source code of this module <minecraft_launcher_lib/{in_path.name}>`\n")


def write_modules() -> None:
    MODULE_ORDER = ("command", "install", "natives", "microsoft_account", "utils", "news", "java_utils", "forge", "fabric", "quilt", "runtime", "vanilla_launcher", "mrpack", "exceptions", "types", "microsoft_types")
    modules_path = pathlib.Path(__file__).parent.parent / "minecraft_launcher_lib"
    modules_doc_dir = pathlib.Path(__file__).parent / "modules"

    try:
        shutil.rmtree(modules_doc_dir)
    except Exception:
        pass

    try:
        os.mkdir(modules_doc_dir)
    except FileExistsError:
        pass

    with open(os.path.join(modules_doc_dir, "index.rst"), "w", encoding="utf-8") as f:
        f.write(".. This File is autogenerated. Do not edit.\n\n")
        f.write("Modules\n==================================================\n\n")
        f.write(".. toctree::\n    :maxdepth: 2\n\n")

        for module in MODULE_ORDER:
            write_module_file((modules_path / f"{module}.py"), modules_doc_dir)
            f.write(f"    {module}\n")

        for path in modules_path.iterdir():
            if path.stem in MODULE_ORDER:
                continue

            if not path.name.endswith(".py") or path.name.startswith("_"):
                continue
            write_module_file(path, modules_doc_dir)
            f.write(f"    {path.stem}\n")


def write_examples_file(in_path: pathlib.Path, out_dir: pathlib.Path) -> None:
    with open(in_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    with open(os.path.join(out_dir, in_path.name[:-3] + ".rst"), "w", encoding="utf-8") as f:
        f.write(".. This File is autogenerated. Do not edit.\n\n")
        f.write(in_path.name[:-3] + "\n")
        f.write("==========================\n")
        f.write("\n.. code:: python\n\n")
        for i in file_content.splitlines():
            f.write("    " + i + "\n")
        f.write(f"\n\n:repolink:`View this example on Codeberg <examples/{in_path.name}>`")


def write_examples() -> None:
    examples_path = pathlib.Path(__file__).parent.parent / "examples"
    examples_doc_dir = pathlib.Path(__file__).parent / "examples"

    try:
        os.mkdir(examples_doc_dir)
    except FileExistsError:
        pass

    with open(os.path.join(examples_doc_dir, "index.rst"), "w", encoding="utf-8") as f:
        f.write(".. This File is autogenerated. Do not edit.\n\n")
        f.write("Examples\n==================================================\n\n")
        f.write(".. toctree::\n    :maxdepth: 2\n\n")
        for i in examples_path.iterdir():
            if not i.name.endswith(".py"):
                continue
            write_examples_file(i, examples_doc_dir)
            f.write("    " + i.name[:-3] + "\n")


write_modules()
write_examples()
