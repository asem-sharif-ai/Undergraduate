# Cryptography Tool

> A dark-themed desktop application for exploring core cryptographic algorithms - encrypt, decrypt, hash, and stream-cipher any text input through a clean GUI. No code required.

---

## Demo

| | |
|---|---|
| ![](Demo/1.jpg) | ![](Demo/2.jpg) |

| | |
|---|---|
| ![](Demo/3.jpg) | ![](Demo/4.jpg) |

| | |
|---|---|
| ![](Demo/5.jpg) | ![](Demo/6.jpg) |

| | |
|---|---|
| ![](Demo/7.jpg) | ![](Demo/8.jpg) |

![](Demo/9.jpg)

---

## Overview

Cryptography Tool was built as a practical companion for the Information Security course at the Faculty of Artificial Intelligence, Menoufia University. The goal was simple: make it easy to experiment with real cryptographic algorithms without writing a single line of code.

Type or import any text, pick an algorithm, configure its parameters, and get the output immediately. Ciphers and keys can be saved to JSON and reloaded later - so you can encrypt in one session and decrypt in another.

The project is split into two layers:

- **Methods** - the backend engine, implementing each algorithm as a standalone module
- **GUI** - the frontend, a single-window customtkinter interface with swappable method panels and dual text boxes

---

## How It Works

```
Import or Type Input → Select Method → Configure → Apply → Read Output → Export
```

The left side holds two text boxes - input on top, output on bottom. The right side is a swappable panel that changes based on the selected method. Navigate between methods using the arrow buttons or scroll wheel, and the panel updates instantly.

---

## Methods

### Symmetric Encryption

Supports **AES** and **DES** - switchable from the same panel.

| Parameter | Options |
|-----------|---------|
| Key Size | 16 / 24 / 32 bytes (AES) · 8 bytes fixed (DES) |
| Mode | CBC · CFB · OFB |

A random key and IV are generated automatically when the key size or mode changes. Keys and IVs are displayed in Base64 and can be saved to `.json` and reloaded for decryption.

### Asymmetric Encryption

Implements **RSA** with PKCS1-OAEP padding.

| Parameter | Options |
|-----------|---------|
| Key Size | 1024 · 2048 · 3072 · 4096 bits |

Public and private keys are generated automatically when the slider moves. Both keys are displayed in truncated PEM format and can be saved to `.json` and reloaded.

### Stream Cipher

Implements **RC4** - a pure Python keystream cipher.

| Parameter | Options |
|-----------|---------|
| Key | Any string |
| Output Format | Decimal · Octal · Hexadecimal · Binary · Bytes |

The key is entered as plain text. Output format controls how the ciphertext byte stream is rendered. RC4 is symmetric - applying it twice with the same key recovers the original text.

### Hashing

Supports **MD5** and **SHA3-256**.

Input text is hashed and the hex digest is written to the output box. The input text, method, and hash can be exported together as a `.json` file for record-keeping.

---

## Session Management

| Action | Effect |
|--------|--------|
| Import File | Load a `.txt` file into the input box |
| Export | Save the current output to `.txt` or the cipher to `.json` |
| Save Cipher / Key | Write the current key material to `.json` |
| Load Cipher / Key | Restore key material from a previously saved `.json` |
| Reset Session | Destroy and rebuild the entire UI - fresh start |

---

## File Formats

**Symmetric cipher file:**
```json
{
    "Method": "AES",
    "Key": "<base64>",
    "IV": "<base64>",
    "Len": 24,
    "Mode": "CBC"
}
```

**Asymmetric cipher file:**
```json
{
    "Key_Size": 2048,
    "Public_Key": "-----BEGIN PUBLIC KEY-----\n...",
    "Private_Key": "-----BEGIN RSA PRIVATE KEY-----\n..."
}
```

**Hash output file:**
```json
{
    "Input": "hello world",
    "Method": "MD5",
    "Hash": "5eb63bbbe01eeed093cb22bb8f5acdc3"
}
```

---

## Installation

```bash
pip install customtkinter pycryptodome
```

## Run

```bash
python App.py
```

---

## Project Structure

```
Cryptography Tool/
│
├── App.py                        # Entry point
├── Main.py                       # App window, method switching, IO logic
│
├── Tool/
│   ├── GUI/
│   │   ├── SymmetricFrame.py     # AES / DES panel
│   │   ├── AsymmetricFrame.py    # RSA panel
│   │   ├── StreamFrame.py        # RC4 panel
│   │   └── HashFrame.py          # MD5 / SHA3 panel
│   └── Methods/
│       ├── Symmetric.py          # AES / DES encrypt & decrypt
│       ├── Asymmetric.py         # RSA key generation, encrypt & decrypt
│       ├── Stream.py             # RC4 implementation
│       └── Hash.py               # MD5 / SHA3 hashing
│
└── Demo/
    ├── 1.jpg  ...  9.jpg
```

---

## Course

**Information Security**
Faculty of Artificial Intelligence, Menoufia University - Year 3