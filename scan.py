import sys
from pathlib import Path


jpeg_files = list()
png_files = list()
jpg_files = list()
txt_files = list()
docx_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": jpeg_files,
    "JPG": jpg_files,
    "PNG": png_files,
    "TXT": txt_files,
    "DOCX": docx_files,
    "ZIP": archives,
    "RAR": archives
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("JPEG", "JPG", "PNG", "TXT", "DOCX", "OTHER", "ARCHIVE"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                extensions.add(extension)
                container = registered_extensions[extension]
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


def scan_result():
    print(f"jpeg: {jpeg_files}\n")
    print(f"jpg: {jpg_files}\n")
    print(f"png: {png_files}\n")
    print(f"txt: {txt_files}\n")
    print(f"docx: {docx_files}\n")
    print(f"archives: {archives}\n")
    print(f"unknown: {others}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    scan_result()

    

