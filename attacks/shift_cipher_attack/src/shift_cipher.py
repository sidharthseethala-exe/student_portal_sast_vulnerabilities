def encrypt(text, key):
    result = ""

    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a') # ord gives num value
            result += chr((ord(ch) - base + key) % 26 + base)
        else:
            result += ch # if space

    return result


def decrypt(text, key):
    return encrypt(text, -key)
    
    
    
    # 
