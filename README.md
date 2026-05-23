# Auto Decryptool

Python obfuscation decoder. Strips multiple layers of encoding/encryption from malware and obfuscated scripts recursively until readable code is recovered.

## Features

- 16 decode methods (base64, zlib, AES, DES, RC4, XOR, marshal, emoji, caesar, hex, berserker)
- Recursive unwrapping with plain text detection
- One-liner pipe mode
- File mode with layer breakdown

## Install

```bash
pip install pycryptodome

## Usage

```bash
# Interactive menu
python3 A-DECRYPTOOL.py

# Direct file
python3 A-DECRYPTOOL.py encoded.py

# Pipe mode
cat encoded.py | python3 A-DECRYPTOOL.py -p

# File flag mode
python3 A-DECRYPTOOL.py -f encoded.py
