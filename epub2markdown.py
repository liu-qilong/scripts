"""
Batch convert .epub files to .txt or .md format

Install required packages:
python -m pip install ebooklib beautifulsoup4 lxml
"""

import argparse
import shutil
import tempfile
import zipfile
from glob import glob
from pathlib import Path

from epub2txt import epub2txt

# NEW: for Markdown conversion
from ebooklib import epub
from bs4 import BeautifulSoup

def package_epub_dir(epub_dir: Path) -> tuple[Path, Path]:
    """
    Turn an Apple Books-style .epub *directory* into a standard .epub *file* (zip).
    Returns (epub_file_path, temp_folder_to_delete).
    """
    temp_root = Path(tempfile.mkdtemp(prefix="epub_pack_"))
    out_epub = temp_root / epub_dir.name  # keep .epub suffix in name

    with zipfile.ZipFile(out_epub, "w") as zf:
        # EPUB spec: 'mimetype' should be first and uncompressed if present.
        mimetype = epub_dir / "mimetype"
        if mimetype.is_file():
            zf.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)

        for p in sorted(epub_dir.rglob("*")):
            if p.is_dir():
                continue
            arcname = p.relative_to(epub_dir).as_posix()
            if arcname == "mimetype":
                continue
            zf.write(p, arcname, compress_type=zipfile.ZIP_DEFLATED)

    return out_epub, temp_root

def _html_to_markdown(html_bytes: bytes) -> str:
    soup = BeautifulSoup(html_bytes, "lxml")
    body = soup.body or soup

    out: list[str] = []
    blocks = body.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "pre"],
        recursive=True,
    )

    for el in blocks:
        name = el.name.lower()
        text = el.get_text(" ", strip=True)

        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(name[1])
            if text:
                out.append(f'{"#" * level} {text}\n')
        elif name == "p":
            if text:
                out.append(text + "\n")
        elif name == "li":
            if text:
                out.append(f"- {text}\n")
        elif name == "blockquote":
            if text:
                out.append("\n".join(["> " + line for line in text.splitlines()]) + "\n")
        elif name == "pre":
            code = el.get_text("\n", strip=False).rstrip()
            if code:
                out.append("```text\n" + code + "\n```\n")

    # ensure blank lines between blocks
    md = "\n".join(s.strip() for s in out if s.strip())
    return md.strip() + "\n"

def epub_to_markdown(epub_path: Path) -> str:
    book = epub.read_epub(str(epub_path))

    # Preserve reading order via spine
    spine_ids = []
    for item in book.spine:
        # item is typically (idref, linear)
        idref = item[0] if isinstance(item, (tuple, list)) else item
        if idref and idref != "nav":
            spine_ids.append(idref)

    parts: list[str] = []
    seen = set()

    for idref in spine_ids:
        it = book.get_item_with_id(idref)
        if not it:
            continue
        # Avoid duplicates
        if it.get_name() in seen:
            continue
        seen.add(it.get_name())

        parts.append(_html_to_markdown(it.get_content()))

    return "\n".join(p for p in parts if p.strip()).strip() + "\n"

parser = argparse.ArgumentParser(
    description="Batch convert .epub files to .txt or .md."
)
parser.add_argument(
    "-i", "--input-folder",
    default="/Users/knpob/Downloads",
    help="Folder containing input EPUB files (default: %(default)s).",
)
parser.add_argument(
    "-f", "--format",
    choices=["txt", "md"],
    default="md",
    help="Output format (default: %(default)s).",
)
args = parser.parse_args()

path = Path(args.input_folder).expanduser()

epub_ls = sorted(Path(p) for p in glob(str(path / "*.epub")))
print(f"found {len(epub_ls)} epub entries to convert")

for epub_path in epub_ls:
    temp_to_delete = None
    try:
        src = epub_path
        if epub_path.is_dir():
            src, temp_to_delete = package_epub_dir(epub_path)

        if args.format == "md":
            output_path = epub_path.with_suffix(".md")
            md = epub_to_markdown(src)
            output_path.write_text(md, encoding="utf-8")
        else:
            output_path = epub_path.with_suffix(".txt")
            text = epub2txt(str(src))
            output_path.write_text(text, encoding="utf-8")

        print(f"converted {epub_path} to {output_path}")

    except Exception as e:
        print(f"failed to convert {epub_path}: {e}")

    finally:
        if temp_to_delete is not None:
            shutil.rmtree(temp_to_delete, ignore_errors=True)