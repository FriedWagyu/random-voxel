import requests
import ast


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


number = get_blocknumber()

print(str(int(number,16)) + ' ' + get_hash(number))
