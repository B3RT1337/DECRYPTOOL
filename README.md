# Auto Decryptool

Python obfuscation decoder. Strips multiple layers of encoding/encryption from malware and obfuscated scripts recursively until readable code is recovered.

## Features

- 16 decode methods (base64, zlib, AES, DES, RC4, XOR, marshal, emoji, caesar, hex, berserker)
- Recursive unwrapping with plain text detection
- One-liner pipe mode
- File mode with layer breakdown

## Install

```
pip3 install pycryptodome
```
# Interactive menu
```
python3 A-DECRYPTOOL.py
```
# Direct file
```
python3 A-DECRYPTOOL.py Encrypted_code.py
```
# Pipe mode
```
cat Encrypted_code.py | python3 A-DECRYPTOOL.py -p
```
# File flag mode
```
python3 A-DECRYPTOOL.py -f Encrypted_code.py
```
