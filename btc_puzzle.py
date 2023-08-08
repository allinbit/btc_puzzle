import hashlib
import ecdsa
import random
import threading

lock = threading.Lock()
found = False

def binary_to_hex(bin_string):
    return hex(int(bin_string, 2))[2:].zfill(len(bin_string) // 4)

def worker(num_zeros, num_ones):
    global found

    target_hash = "20d45a6a762535700ce9e0b216e31994335db8a5"

    while not found:
        bits = ['0'] * num_zeros + ['1'] * (num_ones - 1)
        random.shuffle(bits)

        bits.insert(0, '1')
        private_key_bin = ''.join(bits)

        private_key_bin = '0' * (256 - 66) + private_key_bin
        private_key_hex = binary_to_hex(private_key_bin)

        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
        public_key = sk.get_verifying_key().to_string().hex()

        compressed_public_key = '02' + public_key[0:64] if int(public_key[-2:], 16) % 2 == 0 else '03' + public_key[0:64]
        compressed_public_key_bytes = bytes.fromhex(compressed_public_key)

        ripemd160_hash = hashlib.new('ripemd160')
        ripemd160_hash.update(hashlib.sha256(compressed_public_key_bytes).digest())
        hashed_compressed_public_key = ripemd160_hash.digest().hex()

        if hashed_compressed_public_key == target_hash:
            with lock:
                if not found:
                    found = True
                    print(private_key_hex)
                    print("hash160:", hashed_compressed_public_key)
                    print("Target hash found!")

num_threads = 8
threads = []

for _ in range(num_threads):
    t = threading.Thread(target=worker, args=(31, 35))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
