#!/usr/bin/env python3
"""
AUTO DECRYPTOOL MADE BY B3RT1337
"""

import base64
import os
import re
import zlib
import sys
import subprocess
import time
import marshal
import hashlib
import bz2

try:
    from Crypto.Cipher import AES, DES, ARC4
    from Crypto.Util.Padding import unpad
    CRYPTO_AVAILABLE = True
except:
    CRYPTO_AVAILABLE = False

def fix_padding(data: str) -> str:
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data

def decode_base64(data: str) -> str:
    try:
        data = data.strip()
        data = fix_padding(data)
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except:
        return None

def decode_base64_reverse(data: str) -> str:
    try:
        reversed_data = data[::-1]
        reversed_data = fix_padding(reversed_data)
        return base64.b64decode(reversed_data).decode('utf-8', errors='ignore')
    except:
        return None

def decode_zlib_reverse(data: str) -> str:
    try:
        reversed_data = data[::-1]
        reversed_data = fix_padding(reversed_data)
        decoded = base64.b64decode(reversed_data)
        decompressed = zlib.decompress(decoded)
        return decompressed.decode('utf-8', errors='ignore')
    except:
        return None

def decode_zlib(data: str) -> str:
    try:
        data = fix_padding(data)
        decoded = base64.b64decode(data)
        decompressed = zlib.decompress(decoded)
        return decompressed.decode('utf-8', errors='ignore')
    except:
        return None

def decode_hex(data: str) -> str:
    try:
        return bytes.fromhex(data).decode('utf-8', errors='ignore')
    except:
        return None

def decode_bz2(data: str) -> str:
    try:
        return bz2.decompress(data.encode()).decode('utf-8', errors='ignore')
    except:
        return None

def decode_a85(data: str) -> str:
    try:
        return base64.a85decode(data).decode('utf-8', errors='ignore')
    except:
        return None

def decode_marshal(data: str) -> str:
    try:
        match = re.search(r"marshal\.loads\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)", data)
        if match:
            b64 = match.group(1)
            decoded = base64.b64decode(b64)
            code = marshal.loads(decoded)
            return code if isinstance(code, str) else None
    except:
        pass
    return None

def decode_compile_eval(data: str) -> str:
    try:
        match = re.search(r"eval\(compile\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\),.*?\)", data, re.DOTALL)
        if match:
            b64 = match.group(1)
            decoded = base64.b64decode(b64)
            return decoded.decode('utf-8', errors='ignore')
    except:
        pass
    return None

def decode_builtins_exec(data: str) -> str:
    try:
        match = re.search(r"__import__\(['\"]builtins['\"]\)\.exec\(['\"]([^'\"]+)['\"]\)", data)
        if match:
            return match.group(1)
    except:
        pass
    return None

def decode_emoji_obfuscation(data: str) -> str:
    try:
        match = re.search(r'for x in\s*["\']([^"\']+)["\']', data)
        if not match:
            return None
        emoji_str = match.group(1)
        mapping = {':D': 1, ':P': 2, ':S': 3, ':(': 4, '=)': 5, '=/': 6, ':/': 7, ':{': 8, ';)': 9, ':)': 0}
        map_match = re.search(r'\{([^}]+)\}', data)
        if map_match:
            pairs = re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*(\d+)", map_match.group(1))
            if pairs:
                mapping = {k: int(v) for k, v in pairs}
        parts = emoji_str.split('  ')
        result = []
        for part in parts:
            if not part.strip():
                continue
            emojis = part.split()
            num_str = ''.join(str(mapping[e]) for e in emojis if e in mapping)
            if num_str:
                try:
                    result.append(chr(int(num_str)))
                except:
                    pass
        decoded = ''.join(result)
        if decoded and len(decoded) > 5:
            return decoded
    except:
        pass
    return None

def decode_pymeomeo(data: str) -> str:
    try:
        match = re.search(r"a85decode\(b['\"]([^'\"]+)['\"]\)", data)
        if not match:
            return None
        a85_data = match.group(1).encode()
        b85 = base64.a85decode(a85_data)
        bz = bz2.decompress(b85)
        z = zlib.decompress(bz)
        code = marshal.loads(z)
        for const in code.co_consts:
            if isinstance(const, str) and len(const) > 50:
                if 'import' in const or 'def ' in const or 'print(' in const:
                    return const
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        exec(code)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        if output:
            return output
    except:
        pass
    return None

def decode_pyc(filepath: str) -> str:
    try:
        with open(filepath, 'rb') as f:
            header = f.read(16)
            code = marshal.load(f)
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        exec(code)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        if output:
            return output
    except:
        pass
    return None

def decode_aes(data: str) -> str:
    if not CRYPTO_AVAILABLE:
        return None
    try:
        match = re.search(r"AES\.new\(b['\"]([a-fA-F0-9]+)['\"],\s*AES\.MODE_CBC,\s*b['\"]([a-fA-F0-9]+)['\"]\)\.decrypt\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)", data)
        if match:
            key = bytes.fromhex(match.group(1))
            iv = bytes.fromhex(match.group(2))
            ct = base64.b64decode(match.group(3))
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(ct), AES.block_size)
            return decrypted.decode('utf-8', errors='ignore')
    except:
        pass
    return None

def decode_des(data: str) -> str:
    if not CRYPTO_AVAILABLE:
        return None
    try:
        match = re.search(r"DES\.new\(b['\"]([a-fA-F0-9]+)['\"],\s*DES\.MODE_CBC,\s*b['\"]([a-fA-F0-9]+)['\"]\)\.decrypt\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)", data)
        if match:
            key = bytes.fromhex(match.group(1))
            iv = bytes.fromhex(match.group(2))
            ct = base64.b64decode(match.group(3))
            cipher = DES.new(key, DES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(ct), DES.block_size)
            return decrypted.decode('utf-8', errors='ignore')
    except:
        pass
    return None

def decode_rc4(data: str) -> str:
    if not CRYPTO_AVAILABLE:
        return None
    try:
        match = re.search(r"ARC4\.new\(b['\"]([a-fA-F0-9]+)['\"]\)\.decrypt\(base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)", data)
        if match:
            key = bytes.fromhex(match.group(1))
            ct = base64.b64decode(match.group(2))
            cipher = ARC4.new(key)
            decrypted = cipher.decrypt(ct)
            return decrypted.decode('utf-8', errors='ignore')
    except:
        pass
    return None

def decode_xor(data: str) -> str:
    try:
        match = re.search(r"bytes\(\[ord\(c\)\s*\^\s*(\d+)\s*for\s+c\s+in\s+base64\.b64decode\(['\"]([A-Za-z0-9+/=]+)['\"]\)\.decode\(\)\]\)", data)
        if match:
            key = int(match.group(1))
            ct = base64.b64decode(match.group(2)).decode()
            return ''.join(chr(ord(c) ^ key) for c in ct)
    except:
        pass
    return None

def decode_caesar(data: str) -> str:
    try:
        match = re.search(r"['\"]([a-zA-Z]{10,})['\"]", data)
        if match:
            enc = match.group(1)
            for shift in range(1, 26):
                dec = ''.join(chr((ord(c) - ord('a') - shift) % 26 + ord('a')) if c.islower() else chr((ord(c) - ord('A') - shift) % 26 + ord('A')) if c.isupper() else c for c in enc)
                if 'import' in dec or 'def ' in dec or 'print' in dec:
                    return dec
    except:
        pass
    return None

def unberserker_decode(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
    try:
        s1 = re.search("if self.(.+?) in open", data).group(1)
        s1s = s1.replace("15", "12")
        s2 = re.findall("{(.+?)}", data)
        source = (data.replace(s1, s1s).replace("{" + s2[0] + "}", "print").replace(",{" + s2[1] + "}()", ""))
        with open('__tmp_decode.py', 'w', encoding='utf-8') as f:
            f.write(source)
        result = subprocess.run(["python3", "__tmp_decode.py"], capture_output=True, text=True)
        os.unlink('__tmp_decode.py')
        return result.stdout if result.stdout else None
    except:
        return None

def is_plain_text(content: str) -> bool:
    if not content or len(content) < 50:
        return False
    python_indicators = ['import ', 'from ', 'def ', 'class ', 'if __name__', 'print(', 'return ']
    obfuscation_patterns = [r"exec\(\(_\)\(b'", r"b'[A-Za-z0-9+/=]{30,}'", r"_sparkle", r"base64\.b64decode", r"zlib\.decompress", r"codecs\.decode", r"marshal\.loads", r":D :P", r"_ = lambda __ :"]
    has_python = any(i in content for i in python_indicators)
    has_obfuscation = any(re.search(p, content) for p in obfuscation_patterns)
    lines = content.split('\n')
    has_python_structure = any(l.strip().startswith(('import', 'from', 'def', 'class')) for l in lines[:20])
    return (has_python or has_python_structure) and not has_obfuscation

def decode_recursive(content: str, depth: int = 0, silent: bool = False) -> tuple:
    layers = []
    current = content
    max_depth = 50
    
    while depth < max_depth:
        if is_plain_text(current):
            if not silent:
                print(f"\033[92m[+]\033[0m Plain text at layer {depth}")
            break
        
        decoded = None
        method = None
        
        if not decoded and '_ = lambda __ :' in current:
            match = re.search(r"b'([A-Za-z0-9+/=]+)'", current)
            if match:
                b64 = match.group(1)
                test = decode_zlib_reverse(b64)
                if test:
                    decoded, method = test, "lambda_zlib_reverse"
                else:
                    test = decode_base64_reverse(b64)
                    if test:
                        decoded, method = test, "lambda_base64_reverse"
        
        
        if not decoded and 'exec((_)(b' in current:
            match = re.search(r"b'([A-Za-z0-9+/=]+)'", current)
            if match:
                b64 = match.group(1)
                test = decode_zlib_reverse(b64)
                if test:
                    decoded, method = test, "exec_zlib_reverse"
        
        
        if not decoded and 'codecs.decode' in current:
            match = re.search(r"codecs\.decode\(b'([a-fA-F0-9]+)'", current)
            if match:
                test = decode_hex(match.group(1))
                if test:
                    decoded, method = test, "hex_codecs"
        
        
        if not decoded and 'Berserker' in current:
            temp_file = f'__temp_{depth}.py'
            with open(temp_file, 'w') as f:
                f.write(current)
            test = unberserker_decode(temp_file)
            os.unlink(temp_file)
            if test:
                decoded, method = test, "unberserker"
        
        
        if not decoded and ':D :P' in current:
            test = decode_emoji_obfuscation(current)
            if test:
                decoded, method = test, "emoji"
        
        
        if not decoded and 'a85decode' in current:
            test = decode_pymeomeo(current)
            if test:
                decoded, method = test, "pymeomeo"
        
        
        if not decoded:
            match = re.search(r"b'([A-Za-z0-9+/=]{30,})'", current)
            if match:
                b64 = match.group(1)
                test = decode_zlib_reverse(b64)
                if test:
                    decoded, method = test, "zlib_reverse"
                else:
                    test = decode_base64_reverse(b64)
                    if test:
                        decoded, method = test, "base64_reverse"
        
        if not decoded:
            break
        
        layers.append({'depth': depth, 'method': method, 'length': len(decoded)})
        if not silent:
            print(f"\033[93m[Layer {depth}]\033[0m {method} -> {len(decoded)} chars")
        current = decoded
        depth += 1
    
    return current, layers

def auto_decrypt(content: str, is_file: bool = True) -> str:
    if is_file:
        print(f"\n\033[96m[+]\033[0m File: {content}")
        if os.path.exists(content) and open(content, 'rb').read(4) in [b'\x42\x0d\x0d\x0a', b'\x61\x0d\x0d\x0a', b'\xf3\x0d\x0d\x0a']:
            print("\033[96m[+]\033[0m Detected .pyc file, executing...")
            result = decode_pyc(content)
            if result:
                print("\033[92m[+]\033[0m Execution successful")
                return result
        with open(content, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        print(f"\033[96m[+]\033[0m Size: {len(data)} chars")
    else:
        data = content
        print(f"\n\033[96m[+]\033[0m Input length: {len(data)} chars")
    
    print("\033[96m[+]\033[0m Analyzing...")
    time.sleep(0.5)
    
    result, layers = decode_recursive(data)
    
    print(f"\n\033[92m[+]\033[0m Total layers decoded: {len(layers)}")
    if layers:
        print("\033[92m[+]\033[0m Methods used:")
        for layer in layers:
            print(f"    - Layer {layer['depth']}: {layer['method']}")
    
    return result

def show_menu():
    print("""
\033[96m╔══════════════════════════════════════════╗
║   AUTO DECRYPTOOL BY B3RT1337            ║
║   OFFICIAL ON GITHUB: B3RT1337/DECRYPTOOL║
╚══════════════════════════════════════════╝\033[0m
\033[97m1.\033[0m Decrypt file
\033[97m2.\033[0m Exit""")

def main():
    if len(sys.argv) > 1:
        result = auto_decrypt(sys.argv[1], is_file=True)
        print(f"\n\033[96m{'='*55}\033[0m")
        print("\033[97mDECRYPTED OUTPUT:\033[0m")
        print(f"\033[96m{'='*55}\033[0m")
        print(result)
        sys.exit(0)
    
    while True:
        show_menu()
        choice = input("\n\033[97mSelect (1-2):\033[0m ").strip()
        
        if choice == '2':
            print("\033[91m[+]\033[0m Exiting...")
            break
        
        if choice == '1':
            filepath = input("\033[97mFile path:\033[0m ").strip()
            if not os.path.exists(filepath):
                print(f"\033[91m[-]\033[0m File not found: {filepath}")
                input("\033[90mPress Enter...\033[0m")
                continue
            result = auto_decrypt(filepath, is_file=True)
        else:
            print("\033[91m[-]\033[0m Invalid choice")
            continue
        
        print(f"\n\033[96m{'='*55}\033[0m")
        print("\033[97mDECRYPTED OUTPUT:\033[0m")
        print(f"\033[96m{'='*55}\033[0m")
        
        if len(result) > 2000:
            print(result[:2000])
            print(f"\n\033[93m... (truncated, total {len(result)} chars)\033[0m")
        else:
            print(result)
        
        save = input("\n\033[97mSave to file? (y/n):\033[0m ").strip().lower()
        if save == 'y':
            outfile = input("\033[97mOutput filename:\033[0m ").strip()
            with open(outfile, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\033[92m[+]\033[0m Saved to {outfile}")
        
        input("\n\033[90mPress Enter to continue...\033[0m")

if __name__ == '__main__':
    main()
