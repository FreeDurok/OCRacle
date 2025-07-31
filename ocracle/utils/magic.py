from ocracle.config.config import MAGIC_SIGNATURES

def match_magic(path: str) -> bool:
    """
    Return True if the file matches a known magic signature.
    """
    try:
        with open(path, "rb") as f:
            header = f.read(8)
        return any(header.startswith(sig) for sig in MAGIC_SIGNATURES)
    except Exception:
        return False


def detect_type(path: str) -> str:
    """
    Detect the file type based on magic bytes.
    Returns the type (pdf, png, jpg, etc.) or 'unknown'.
    """
    try:
        with open(path, "rb") as f:
            header = f.read(8)
        for sig, ftype in MAGIC_SIGNATURES.items():
            if header.startswith(sig):
                return ftype
    except Exception:
        pass
    return "unknown"
