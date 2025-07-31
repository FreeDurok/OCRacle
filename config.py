# Magic byte signatures: header bytes -> logical file type
# Only files that match these signatures will be analyzed
MAGIC_SIGNATURES = {
    b"\x25PDF": "pdf",               # PDF
    b"\x89PNG": "png",               # PNG
    b"\xFF\xD8\xFF": "jpg",          # JPEG
    b"\x49\x49\x2A\x00": "tiff",     # TIFF little endian
    b"\x4D\x4D\x00\x2A": "tiff",     # TIFF big endian
}