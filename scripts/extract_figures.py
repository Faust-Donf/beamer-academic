#!/usr/bin/env python3
"""
Extract figures from thesis files (PDF, DOCX, or LaTeX project).
Output: materials/figures/fig_001.png, fig_002.png, ...

Usage:
    python3 extract_figures.py thesis.pdf
    python3 extract_figures.py thesis.docx
    python3 extract_figures.py thesis.tex
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

OUTPUT_DIR = "materials/figures"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_from_pdf(pdf_path):
    """Extract embedded images from PDF using pdfimages (poppler)."""
    ensure_output_dir()

    # Try pdfimages first (best quality, extracts embedded images directly)
    if shutil.which("pdfimages"):
        prefix = os.path.join(OUTPUT_DIR, "raw")
        subprocess.run(
            ["pdfimages", "-all", pdf_path, prefix],
            capture_output=True,
        )
        # Rename extracted files to fig_001, fig_002, ...
        raw_files = sorted(Path(OUTPUT_DIR).glob("raw-*"))
        count = 0
        for f in raw_files:
            # Skip tiny images (likely icons/bullets, < 5KB)
            if f.stat().st_size < 5000:
                f.unlink()
                continue
            count += 1
            ext = f.suffix
            new_name = f"fig_{count:03d}{ext}"
            f.rename(Path(OUTPUT_DIR) / new_name)
        print(f"✅ Extracted {count} figures from PDF (pdfimages)")
        return count

    # Fallback: try PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(pdf_path)
        count = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images(full=True)
            for img_idx, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                if base_image["size"] < 5000:  # skip tiny images
                    continue
                count += 1
                ext = base_image["ext"]
                img_path = os.path.join(OUTPUT_DIR, f"fig_{count:03d}.{ext}")
                with open(img_path, "wb") as f:
                    f.write(base_image["image"])
        print(f"✅ Extracted {count} figures from PDF (PyMuPDF)")
        return count
    except ImportError:
        pass

    print("❌ No PDF extraction tool available.")
    print("   Install one of: poppler (brew install poppler) or PyMuPDF (pip install pymupdf)")
    return 0


def extract_from_docx(docx_path):
    """Extract embedded images from Word document."""
    ensure_output_dir()

    # Method 1: python-docx
    try:
        from docx import Document
        from docx.opc.constants import RELATIONSHIP_TYPE as RT

        doc = Document(docx_path)
        count = 0
        for rel in doc.part.rels.values():
            if "image" in rel.reltype:
                count += 1
                image_data = rel.target_part.blob
                # Detect extension from content type
                content_type = rel.target_part.content_type
                ext_map = {
                    "image/png": ".png",
                    "image/jpeg": ".jpg",
                    "image/gif": ".gif",
                    "image/tiff": ".tiff",
                    "image/x-emf": ".emf",
                    "image/x-wmf": ".wmf",
                }
                ext = ext_map.get(content_type, ".png")
                img_path = os.path.join(OUTPUT_DIR, f"fig_{count:03d}{ext}")
                with open(img_path, "wb") as f:
                    f.write(image_data)
        print(f"✅ Extracted {count} figures from DOCX (python-docx)")
        return count
    except ImportError:
        pass

    # Method 2: unzip (docx is a zip file)
    import zipfile

    if not zipfile.is_zipfile(docx_path):
        print("❌ File is not a valid DOCX")
        return 0

    count = 0
    with zipfile.ZipFile(docx_path, "r") as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                count += 1
                ext = Path(name).suffix
                img_path = os.path.join(OUTPUT_DIR, f"fig_{count:03d}{ext}")
                with z.open(name) as src, open(img_path, "wb") as dst:
                    dst.write(src.read())
    print(f"✅ Extracted {count} figures from DOCX (unzip)")
    return count


def extract_from_tex(tex_path):
    """Find figures referenced in LaTeX source and copy them."""
    ensure_output_dir()

    import re

    tex_dir = Path(tex_path).parent

    # Read all .tex files in the directory (main + included)
    tex_files = list(tex_dir.glob("**/*.tex"))
    image_paths = []

    for tf in tex_files:
        content = tf.read_text(errors="ignore")
        # Match \includegraphics[...]{path} or \includegraphics{path}
        matches = re.findall(r"\\includegraphics(?:\[.*?\])?\{([^}]+)\}", content)
        image_paths.extend(matches)

    # Also check \graphicspath
    main_content = Path(tex_path).read_text(errors="ignore")
    gp_match = re.findall(r"\\graphicspath\{(.+?)\}", main_content)
    search_dirs = [tex_dir]
    for gp in gp_match:
        # Parse {dir1/}{dir2/} format
        dirs = re.findall(r"\{([^}]+)\}", gp)
        for d in dirs:
            candidate = tex_dir / d
            if candidate.is_dir():
                search_dirs.append(candidate)

    # Resolve and copy images
    count = 0
    seen = set()
    common_exts = ["", ".png", ".jpg", ".jpeg", ".pdf", ".eps", ".svg"]

    for img_ref in image_paths:
        if img_ref in seen:
            continue
        seen.add(img_ref)

        # Try to find the actual file
        found = None
        for search_dir in search_dirs:
            for ext in common_exts:
                candidate = search_dir / (img_ref + ext)
                if candidate.is_file():
                    found = candidate
                    break
            if found:
                break

        if found:
            count += 1
            new_name = f"fig_{count:03d}{found.suffix}"
            shutil.copy2(found, Path(OUTPUT_DIR) / new_name)

    print(f"✅ Found and copied {count} figures from LaTeX project")
    if count < len(seen):
        print(f"   ⚠️ {len(seen) - count} image references could not be resolved")
    return count


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_figures.py <thesis.pdf|thesis.docx|thesis.tex>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    ext = Path(input_file).suffix.lower()

    if ext == ".pdf":
        n = extract_from_pdf(input_file)
    elif ext in (".docx", ".doc"):
        n = extract_from_docx(input_file)
    elif ext == ".tex":
        n = extract_from_tex(input_file)
    else:
        print(f"❌ Unsupported file type: {ext}")
        print("   Supported: .pdf, .docx, .tex")
        sys.exit(1)

    if n == 0:
        print("\n⚠️ No figures extracted. Check if the file contains images.")
    else:
        print(f"\n📁 Output: {OUTPUT_DIR}/ ({n} files)")
        # List extracted files
        for f in sorted(Path(OUTPUT_DIR).iterdir()):
            size_kb = f.stat().st_size / 1024
            print(f"   {f.name} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
