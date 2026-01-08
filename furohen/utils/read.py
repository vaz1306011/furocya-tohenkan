import logging
import re
from pathlib import Path
from typing import Optional

from pycparser.c_ast import Decl, FileAST, FuncDef
from pycparser.c_parser import CParser

logger = logging.getLogger(__name__)


def read_file(file_path: Path) -> Optional[str]:
    try:
        raw = file_path.read_bytes()
        for encoding in ("utf-8", "cp932", "shift_jis"):
            try:
                content = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                content = None
        if content is None:
            raise UnicodeDecodeError("unknown", b"", 0, 0, "decode failed")

        file_list = []
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            line = re.sub(r"//.*", "", line)
            file_list.append(line)
        return "\n".join(file_list)

    except Exception as e:
        logger.warning(f"Error reading file {file_path}: {e}")
        return None


def read_code(code: str) -> list[FuncDef]:
    parser = CParser()
    ast: FileAST = parser.parse(code)
    return ast.ext
