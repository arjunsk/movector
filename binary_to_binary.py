import array
import binascii
import time

import numpy as np

vec_len = 3
num_inserts = 1


def run():
    for i in range(num_inserts):
        to_db_binary(np.random.rand(vec_len))


def to_db_binary(value, dim=None):
    if value is None:
        return value

    value = np.asarray(value, dtype='<f')

    if value.ndim != 1:
        raise ValueError('expected ndim to be 1')

    print(value)
    print(value.tolist())
    print(value.tobytes())
    print(str(list(value.tobytes())))
    print(binascii.b2a_hex(value.tobytes()))

    arr = array.array('f')
    arr.frombytes(value.tobytes())
    print(arr)

    print(np.frombuffer(value.tobytes(), dtype='<f'))


if __name__ == "__main__":
    start = time.time()
    run()
    duration = time.time() - start
    print(f"duration={duration}")
