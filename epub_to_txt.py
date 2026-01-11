import argparse
import shutil
import tempfile
import zipfile
from glob import glob
from pathlib import Path

from epub2txt import epub2txt

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

# epub file list
parser = argparse.ArgumentParser(
    description="Batch convert .epub files to .txt using epub2txt."
)
parser.add_argument(
    "-i", "--input-folder",
    default="/Users/knpob/Downloads",
    help="Folder containing input EPUB files (default: %(default)s).",
)
args = parser.parse_args()

path = Path(args.input_folder).expanduser()

# glob returns both files and directories; Apple Books may provide .epub directories.
epub_ls = sorted(Path(p) for p in glob(str(path / "*.epub")))
print(f"found {len(epub_ls)} epub entries to convert")

# process each epub file
for epub_path in epub_ls:
    temp_to_delete = None
    try:
        src = epub_path
        if epub_path.is_dir():
            src, temp_to_delete = package_epub_dir(epub_path)

        output_path = epub_path.with_suffix(".txt")
        text = epub2txt(str(src))  # returns full text as a string

        output_path.write_text(text, encoding="utf-8")
        print(f"converted {epub_path} to {output_path}")

    except Exception as e:
        print(f"failed to convert {epub_path}: {e}")

    finally:
        if temp_to_delete is not None:
            shutil.rmtree(temp_to_delete, ignore_errors=True)