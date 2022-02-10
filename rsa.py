from math import gcd
import base64
import random


def lcm(p, q):
    '''
    最小公倍数を求める。
    '''
    return (p * q) // gcd(p, q)


def generate_keys(p, q):
    '''
    与えられた 2 つの素数 p, q から秘密鍵と公開鍵を生成する。
    '''
    N = p * q
    L = lcm(p - 1, q - 1)

    for i in range(2, L):
        if gcd(i, L) == 1:
            E = i
            break

    for i in range(2, L):
        if (E * i) % L == 1:
            D = i
            break

    return (E, N), (D, N)


def encrypt(plain_text, public_key):
    '''
    公開鍵 public_key を使って平文 plain_text を暗号化する。
    '''
    E, N = public_key
    plain_integers = [ord(char) for char in plain_text]
    encrypted_integers = [pow(i, E, N) for i in plain_integers]
    encrypted_text = ''.join(chr(i) for i in encrypted_integers)

    # encode with base64
    text = base64.b64encode(encrypted_text.encode("utf-8")).decode()

    return text


def decrypt(encrypted_text, private_key):
    '''
    秘密鍵 private_key を使って暗号文 encrypted_text を復号する。
    '''
    # use base64 to decode
    encrypted_text = base64.b64decode(encrypted_text).decode("utf-8")

    D, N = private_key
    encrypted_integers = [ord(char) for char in encrypted_text]
    decrypted_intergers = [pow(i, D, N) for i in encrypted_integers]
    decrypted_text = ''.join(chr(i) for i in decrypted_intergers)

    return decrypted_text


def sanitize(encrypted_text):
    '''
    UnicodeEncodeError が置きないようにする。
    '''
    return encrypted_text.encode('utf-8', 'replace').decode('utf-8')

def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)
    return prime_list


if __name__ == '__main__':
    print("ようこそ！")
    primes = primesInRange(100, 1000)
    s1 = random.choice(primes)
    s2 = random.choice(primes)
    print("鍵を生成します...")
    public_key, private_key = generate_keys(int(s1), int(s2))
    print("鍵を生成しました")
    print("公開鍵:", public_key)
    print("秘密鍵:", private_key)
    print("公開鍵をお相手に渡してください。")
    print("お相手の公開鍵を入力してください")
    p1 = input("公開鍵の一つ目の数字:")
    p2 = input("公開鍵の二つ目の数字:")
    aite = (int(p1), int(p2))

    print("対話モードに入ります")
    print("文章の暗号化とお相手の文章の復号化を交互におこないます")
    while(True):
        text = input("[暗号化]文章を入力してください:")
        try:
            print(encrypt(text, aite))
        except:
            print("エラーが発生しました。続行します。")
        text = input("[復号化]文章を入力してください:")
        try:
            print(decrypt(text, private_key))
        except:
            print("エラーが発生しました。続行します。")