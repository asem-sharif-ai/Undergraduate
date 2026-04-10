def RC4(key: str, data: str, output_format: str = 'bytes') -> str | bytes:
    data, key = data.encode('utf-8'), key.encode('utf-8')
    
    j, S = 0, list(range(256))
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    output = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        output.append(byte ^ K)

    if output_format == 'Decimal':
        return ' '.join(str(b) for b in output)
    elif output_format == 'Octal':
        return ' '.join(oct(b) for b in output)
    elif output_format == 'Hexadecimal':
        return output.hex()
    elif output_format == 'Binary':
        return ' '.join(bin(b)[2:] for b in output)
    else:
        return bytes(output)