import uuid
from pathlib import Path

from furohen.core import make
from furohen.output import render
from furohen.utils import read_code, read_file

BASE_DIR = Path(__file__).resolve().parents[2]
WORK = BASE_DIR / "work"
WORK.mkdir(exist_ok=True)


async def convert_c_to_pdf(file):
    uid = uuid.uuid4().hex
    c_path = WORK / f"{uid}.c"
    pdf_path = WORK / uid
    name_path = WORK / f"{uid}.name"

    c_path.write_bytes(await file.read())
    code = read_file(c_path)
    if not code:
        raise ValueError("Failed to read C source")
    funcs = read_code(code)
    nodes = make(funcs)
    render(nodes[0], str(pdf_path), view=False)
    original_name = Path(file.filename or "flowchart").stem
    name_path.write_text(original_name, encoding="utf-8")

    return uid
