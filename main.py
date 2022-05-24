import requests
import ast
import time
import random
import numpy as np
from matplotlib import cm
from pyvox.models import Color
from pyvox.models import Vox
from pyvox.writer import VoxWriter
from pyvox.parser import VoxParser

color_list = [cm.inferno,
              cm.viridis,
              cm.plasma,
              cm.magma,
              cm.cividis,
              cm.Greys,
              cm.Purples,
              cm.Blues,
              cm.Greens,
              cm.Oranges,
              cm.Reds,
              cm.YlOrBr,
              cm.YlOrRd,
              cm.OrRd,
              cm.PuRd,
              cm.RdPu,
              cm.BuPu,
              cm.GnBu,
              cm.PuBu,
              cm.YlGnBu,
              cm.PuBuGn,
              cm.BuGn,
              cm.YlGn,
              cm.binary,
              cm.gist_yarg,
              cm.gist_gray,
              cm.gray,
              cm.bone,
              cm.pink,
              cm.spring,
              cm.summer,
              cm.autumn,
              cm.winter,
              cm.cool,
              cm.Wistia,
              cm.hot,
              cm.afmhot,
              cm.gist_heat,
              cm.copper,
              cm.PiYG,
              cm.PRGn,
              cm.BrBG,
              cm.PuOr,
              cm.RdGy,
              cm.RdBu,
              cm.RdYlBu,
              cm.RdYlGn,
              cm.Spectral,
              cm.coolwarm,
              cm.bwr,
              cm.seismic,
              cm.twilight,
              cm.twilight_shifted,
              cm.hsv,
              cm.flag,
              cm.prism,
              cm.ocean,
              cm.gist_earth,
              cm.terrain,
              cm.gist_stern,
              cm.gnuplot,
              cm.gnuplot2,
              cm.CMRmap,
              cm.cubehelix,
              cm.brg,
              cm.gist_rainbow,
              cm.rainbow,
              cm.jet,
              cm.turbo,
              cm.nipy_spectral,
              cm.gist_ncar]


def convert_positive_int(n):
    if n < 0:
        return -n
    else:
        return n


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


def log_txt(fn, bn, bh):
    f = open(fn, 'a')
    f.write(str(bn) + ' ' + bh + '\n')
    f.close()
    print(str(bn) + ': ' + bh)


def write_voxel(n, h):
    random.seed(h)
    vox_size = 100
    vox_array = np.zeros((vox_size, vox_size, vox_size), dtype='B')
    for i in range(0, 100000):
        rn1 = random.randrange(0, vox_size)
        rn2 = random.randrange(0, vox_size)
        rn3 = random.randrange(0, vox_size)
        rn4 = random.randrange(1, 256)
        vox_array[rn1][rn2][rn3] = rn4
    rn = random.randrange(0, 71)
    rand_color_list = color_list[rn]
    pal = [Color(*[int(255*x) for x in rand_color_list(i/256)]) for i in range(256)]
    vox = Vox.from_dense(vox_array)
    vox.palette = pal
    fn = '.\\op\\' + str(n) + '.vox'
    VoxWriter(fn, vox).write()


def write_voxel_rose(n, h):
    random.seed(h)
    a = VoxParser(".\\rose_model\\rose_202005201728.vox").parse()
    b = a.to_dense()
    rn1 = random.randrange(1, 78)
    rn2 = random.randrange(178, 256)
    for x in range(0, len(b)):
        for y in range(0, len(b[x])):
            for z in range(0, len(b[x][y])):
                if b[x][y][z] == 216:
                    b[x][y][z] = random.randrange(rn1, rn1 + 50)
                if b[x][y][z] == 226:
                    b[x][y][z] = random.randrange(rn2 - 50, rn2)
                else:
                    if random.randrange(1, 10000) == 1:
                        b[x][y][z] = random.randrange(1, 256)
    color_number = random.randrange(0, 71)
    color = color_list[color_number]
    pal = [Color(*[int(255*x) for x in color(i/256)]) for i in range(256)]
    vox = Vox.from_dense(b)
    vox.palette = pal
    fn = '.\\op\\' + str(n) + '.vox'
    VoxWriter(fn, vox).write()


def main_loop():
    # hash variables
    block_number_int = int(get_blocknumber(), 16)
    block_hash = get_hash(hex(block_number_int))
    log_file_name = '.\\op\\' + str(block_number_int) + ".txt"
    log_txt(log_file_name, block_number_int, block_hash)
    write_voxel_rose(block_number_int, block_hash)

    while True:
        time.sleep(10)
        latest_block_number_int = int(get_blocknumber(), 16)
        if latest_block_number_int > block_number_int:
            block_number_int = block_number_int + 1
            block_hash = get_hash(hex(block_number_int))
            log_txt(log_file_name, block_number_int, block_hash)
            write_voxel_rose(block_number_int, block_hash)


main_loop()
# write_voxel(14545511, '0x0568aca073f67f5604919c1a709686ff9a1d60f50ed991081b87b21fb36f99e7')
