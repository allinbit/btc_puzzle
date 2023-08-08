import hashlib
import ecdsa
import random
from multiprocessing import Process, Event

def binary_to_hex(bin_string):
    return hex(int(bin_string, 2))[2:].zfill(len(bin_string) // 4)

def worker(num_zeros, num_ones, stop_event):

    target_hash = "20d45a6a762535700ce9e0b216e31994335db8a5"

    while True:
        if stop_event.is_set():
            break

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
            print(private_key_hex)
            print("hash160:", hashed_compressed_public_key)
            print("Target hash found!")

            stop_event.set()
            break

def main():
    num_processes = 4
    processes = []
    stop_event = Event()

    for _ in range(num_processes):
        process = Process(target=worker, args=(31, 35, stop_event))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    if stop_event.is_set():
        for process in processes:
            process.terminate()

if __name__ == '__main__':
    main()
