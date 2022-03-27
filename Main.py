import requests
import ast
import time
import pyautogui


def get_json_result(a, b):  # input request from server
    t = a.text
    d = ast.literal_eval(t)
    r = d[b]
    return r


def get_blocknumber():
    h = {"Content-Type": "application/json"}  # infura api data
    u = "https://mainnet.infura.io/v3/df9c2fdd407e45be990e5a698b63c7e4"  # infura api data
    d = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
    r = requests.post(u, data=d, headers=h)
    n = get_json_result(r, "result")
    return n


def get_hash(a):
    h = {"Content-Type": "application/json"}  # infura api data
    u = "https://mainnet.infura.io/v3/df9c2fdd407e45be990e5a698b63c7e4"  # infura api data
    d = '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":[' + '"' + a + '"' + ',false' + '],"id":1}'
    r = requests.post(u, data=d, headers=h)
    rs = get_json_result(r, "result")
    hh = rs["hash"]
    return hh


def write_voxel():
    data = int('0xd4ee953f53e9c89033631e8327a0153b70076d7560eb107c5b39c8fdd8428c63', 16)

    # pyautogui.write('fxxk Python !', interval=0.3)
    # pyautogui.press('enter')

    print(data)


time.sleep(5)
write_voxel()


# initial variables
block_number = get_blocknumber()
block_number_int = int(block_number, 16)
block_number_str = str(block_number_int)
block_hash = get_hash(block_number)
file_name = block_number_str + '.txt'
file_open = open(file_name, 'a')
file_open.write(block_number_str + ' ' + block_hash + '\n')
file_open.close()
print(block_number_str + ' ' + block_hash + '\n')

while True:
    time.sleep(10)
    latest_block_number = int(get_blocknumber(), 16)
    if latest_block_number > block_number_int:
        block_number_int = block_number_int + 1
        block_number_str = str(block_number_int)
        block_hash = get_hash(hex(block_number_int))
        file_open = open(file_name, 'a')
        file_open.write(block_number_str + ' ' + block_hash + '\n')
        file_open.close()
        print(block_number_str + ' ' + block_hash + '\n')

