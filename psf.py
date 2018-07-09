"""https://git.kernel.org/pub/scm/linux/kernel/git/legion/kbd.git/tree/src/psf.h"""

import struct

PSF1_MAGIC		= b'\x36\x04'
PSF1_MODE512		= 0x01
PSF1_MODEHASTAB		= 0x02
PSF1_MODEHASSEQ		= 0x04
PSF1_MAXMODE		= 0x05
PSF1_SEPARATOR		= 0xFFFF
PSF1_STARTSEQ		= 0xFFFE

PSF2_MAGIC		= b'\x72\xb5\x4a\x86'
"""32-bit magic 0x864ab572: int.to_bytes(0x864ab572,32/8,'little')"""
PSF2_HAS_UNICODE_TABLE	= True
PSF2_MAXVERSION		= 0
PSF2_SEPARATOR		= 0xFF
PSF2_STARTSEQ		= 0xFE

PSF1_MAGIC_OK		= lambda x: x[:len(PSF1_MAGIC)]==PSF1_MAGIC
PSF2_MAGIC_OK		= lambda x: x[:len(PSF2_MAGIC)]==PSF2_MAGIC

psf1_header_struct = '<2sBB'
psf2_header_struct = '<4siiiiiii'
"""The integers here are little endian 4-byte integers."""
