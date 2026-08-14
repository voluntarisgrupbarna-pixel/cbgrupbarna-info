#!/usr/bin/env python3
"""Generador de codis QR en SVG, sense dependencies externes.

S'usa per als materials impresos del club (cartells, samarretes, taulell del
pavello). Genera un SVG vectorial: escala be a qualsevol mida d'impressio.

  python3 scripts/qr.py "https://cbgrupbarna.info/opina" opina/qr.svg

Executar-lo sense arguments passa la bateria de validacions (vectors coneguts
de l'estandard ISO/IEC 18004 + descodificacio de la propia matriu).
"""

import sys

# ---------------------------------------------------------------- GF(256) ---
EXP = [0] * 512
LOG = [0] * 256
_x = 1
for _i in range(255):
    EXP[_i] = _x
    LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    EXP[_i] = EXP[_i - 255]


def gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return EXP[LOG[a] + LOG[b]]


def rs_generator(n):
    poly = [1]
    for i in range(n):
        poly = poly_mul(poly, [1, EXP[i]])
    return poly


def poly_mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] ^= gf_mul(a, b)
    return out


def rs_encode(data, n_ec):
    """Retorna els n_ec codewords de corrreccio d'errors de `data`."""
    gen = rs_generator(n_ec)
    rem = list(data) + [0] * n_ec
    for i in range(len(data)):
        coef = rem[i]
        if coef == 0:
            continue
        for j, g in enumerate(gen):
            rem[i + j] ^= gf_mul(g, coef)
    return rem[len(data):]


# ------------------------------------------------------------ taules QR ----
# Codewords totals per versio (1-10).
TOTAL_CW = {1: 26, 2: 44, 3: 70, 4: 100, 5: 134, 6: 172, 7: 196, 8: 242, 9: 292, 10: 346}

# (ec_per_bloc, [(n_blocs, data_cw_per_bloc), ...])
BLOCKS = {
    (1, 'L'): (7, [(1, 19)]),   (1, 'M'): (10, [(1, 16)]),
    (1, 'Q'): (13, [(1, 13)]),  (1, 'H'): (17, [(1, 9)]),
    (2, 'L'): (10, [(1, 34)]),  (2, 'M'): (16, [(1, 28)]),
    (2, 'Q'): (22, [(1, 22)]),  (2, 'H'): (28, [(1, 16)]),
    (3, 'L'): (15, [(1, 55)]),  (3, 'M'): (26, [(1, 44)]),
    (3, 'Q'): (18, [(2, 17)]),  (3, 'H'): (22, [(2, 13)]),
    (4, 'L'): (20, [(1, 80)]),  (4, 'M'): (18, [(2, 32)]),
    (4, 'Q'): (26, [(2, 24)]),  (4, 'H'): (16, [(4, 9)]),
    (5, 'L'): (26, [(1, 108)]), (5, 'M'): (24, [(2, 43)]),
    (5, 'Q'): (18, [(2, 15), (2, 16)]), (5, 'H'): (22, [(2, 11), (2, 12)]),
    (6, 'L'): (18, [(2, 68)]),  (6, 'M'): (16, [(4, 27)]),
    (6, 'Q'): (24, [(4, 19)]),  (6, 'H'): (28, [(4, 15)]),
    (7, 'L'): (20, [(2, 78)]),  (7, 'M'): (18, [(4, 31)]),
    (7, 'Q'): (18, [(2, 14), (4, 15)]), (7, 'H'): (26, [(4, 13), (1, 14)]),
    (8, 'L'): (24, [(2, 97)]),  (8, 'M'): (22, [(2, 38), (2, 39)]),
    (8, 'Q'): (22, [(4, 18), (2, 19)]), (8, 'H'): (26, [(4, 14), (2, 15)]),
    (9, 'L'): (30, [(2, 116)]), (9, 'M'): (22, [(3, 36), (2, 37)]),
    (9, 'Q'): (20, [(4, 16), (4, 17)]), (9, 'H'): (24, [(4, 12), (4, 13)]),
    (10, 'L'): (18, [(2, 68), (2, 69)]), (10, 'M'): (26, [(4, 43), (1, 44)]),
    (10, 'Q'): (24, [(6, 19), (2, 20)]), (10, 'H'): (28, [(6, 15), (2, 16)]),
}

ALIGN = {
    1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30],
    6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50],
}

REMAINDER = {1: 0, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 0, 8: 0, 9: 0, 10: 0}

EC_INDICATOR = {'L': 0b01, 'M': 0b00, 'Q': 0b11, 'H': 0b10}


def _self_check_tables():
    for (ver, lvl), (ec, groups) in BLOCKS.items():
        blocs = sum(n for n, _ in groups)
        data = sum(n * d for n, d in groups)
        assert data + ec * blocs == TOTAL_CW[ver], (ver, lvl)


_self_check_tables()


def data_capacity(version, level):
    ec, groups = BLOCKS[(version, level)]
    return sum(n * d for n, d in groups)


# ------------------------------------------------------------- codificar ---
def encode_data(text, version, level):
    payload = text.encode('utf-8')
    count_bits = 8 if version <= 9 else 16
    bits = []

    def put(value, n):
        for i in range(n - 1, -1, -1):
            bits.append((value >> i) & 1)

    put(0b0100, 4)               # mode byte
    put(len(payload), count_bits)
    for b in payload:
        put(b, 8)

    capacity = data_capacity(version, level) * 8
    if len(bits) > capacity:
        raise ValueError('dades massa llargues per a la versio')

    put(0, min(4, capacity - len(bits)))        # terminador
    while len(bits) % 8:
        bits.append(0)
    pad = [0xEC, 0x11]
    i = 0
    while len(bits) < capacity:
        put(pad[i % 2], 8)
        i += 1

    return [int(''.join(str(b) for b in bits[i:i + 8]), 2) for i in range(0, len(bits), 8)]


def interleave(codewords, version, level):
    ec_len, groups = BLOCKS[(version, level)]
    blocks, ec_blocks, pos = [], [], 0
    for n, size in groups:
        for _ in range(n):
            block = codewords[pos:pos + size]
            pos += size
            blocks.append(block)
            ec_blocks.append(rs_encode(block, ec_len))

    out = []
    for i in range(max(len(b) for b in blocks)):
        for b in blocks:
            if i < len(b):
                out.append(b[i])
    for i in range(ec_len):
        for b in ec_blocks:
            out.append(b[i])
    return out


def choose_version(text, level):
    payload_bits = 4 + 8 + len(text.encode('utf-8')) * 8
    for version in range(1, 11):
        count_bits = 8 if version <= 9 else 16
        need = 4 + count_bits + len(text.encode('utf-8')) * 8
        if need <= data_capacity(version, level) * 8:
            return version
    raise ValueError('text massa llarg (max versio 10)')


# --------------------------------------------------------------- matriu ----
FINDER = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]


def build_function_patterns(version):
    size = version * 4 + 17
    matrix = [[None] * size for _ in range(size)]
    reserved = [[False] * size for _ in range(size)]

    def place_finder(row, col):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr, cc = row + r, col + c
                if 0 <= rr < size and 0 <= cc < size:
                    inside = 0 <= r < 7 and 0 <= c < 7
                    matrix[rr][cc] = FINDER[r][c] if inside else 0
                    reserved[rr][cc] = True

    place_finder(0, 0)
    place_finder(0, size - 7)
    place_finder(size - 7, 0)

    # timing
    for i in range(size):
        if matrix[6][i] is None:
            matrix[6][i] = 1 - (i % 2)
            reserved[6][i] = True
        if matrix[i][6] is None:
            matrix[i][6] = 1 - (i % 2)
            reserved[i][6] = True

    # alineament
    coords = ALIGN[version]
    for r in coords:
        for c in coords:
            if reserved[r][c]:
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    val = 1 if max(abs(dr), abs(dc)) != 1 else 0
                    matrix[r + dr][c + dc] = val
                    reserved[r + dr][c + dc] = True

    # modul fosc + reserva de format
    matrix[size - 8][8] = 1
    reserved[size - 8][8] = True
    for i in range(9):
        if not reserved[8][i]:
            reserved[8][i] = True
            matrix[8][i] = 0
        if not reserved[i][8]:
            reserved[i][8] = True
            matrix[i][8] = 0
    for i in range(8):
        if not reserved[8][size - 1 - i]:
            reserved[8][size - 1 - i] = True
            matrix[8][size - 1 - i] = 0
        if not reserved[size - 1 - i][8]:
            reserved[size - 1 - i][8] = True
            matrix[size - 1 - i][8] = 0

    # informacio de versio (v7+)
    if version >= 7:
        bits = version_info_bits(version)
        for i in range(18):
            bit = (bits >> i) & 1
            r, c = i // 3, i % 3
            matrix[size - 11 + c][r] = bit
            reserved[size - 11 + c][r] = True
            matrix[r][size - 11 + c] = bit
            reserved[r][size - 11 + c] = True

    return matrix, reserved, size


def data_positions(size, reserved):
    """Recorregut en zig-zag, de baix a dalt, columnes de dues en dues."""
    positions = []
    col = size - 1
    upward = True
    while col > 0:
        if col == 6:          # la columna de timing no compta
            col -= 1
        rows = range(size - 1, -1, -1) if upward else range(size)
        for row in rows:
            for c in (col, col - 1):
                if not reserved[row][c]:
                    positions.append((row, c))
        upward = not upward
        col -= 2
    return positions


MASKS = [
    lambda r, c: (r + c) % 2 == 0,
    lambda r, c: r % 2 == 0,
    lambda r, c: c % 3 == 0,
    lambda r, c: (r + c) % 3 == 0,
    lambda r, c: (r // 2 + c // 3) % 2 == 0,
    lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
    lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
    lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
]


def bch_format(data5):
    value = data5 << 10
    for i in range(4, -1, -1):
        if value & (1 << (i + 10)):
            value ^= 0x537 << i
    return ((data5 << 10) | value) ^ 0x5412


def version_info_bits(version):
    value = version << 12
    for i in range(5, -1, -1):
        if value & (1 << (i + 12)):
            value ^= 0x1F25 << i
    return (version << 12) | value


def place_format(matrix, size, level, mask):
    bits = bch_format((EC_INDICATOR[level] << 3) | mask)
    for i in range(15):
        bit = (bits >> i) & 1
        # copia 1: tira vertical sota el localitzador superior esquerre + tira
        # horitzontal a la seva dreta
        if i < 6:
            matrix[i][8] = bit
        elif i == 6:
            matrix[7][8] = bit
        elif i == 7:
            matrix[8][8] = bit
        elif i == 8:
            matrix[8][7] = bit
        else:
            matrix[8][14 - i] = bit
        # copia 2: tira horitzontal a la dreta + tira vertical a baix a
        # l'esquerra (sense tocar el modul fosc de la fila size-8)
        if i < 8:
            matrix[8][size - 1 - i] = bit
        else:
            matrix[size - 15 + i][8] = bit


def penalty(matrix, size):
    score = 0
    # regla 1: series de 5 o mes
    for line in list(matrix) + [list(col) for col in zip(*matrix)]:
        run, prev = 1, line[0]
        for v in line[1:]:
            if v == prev:
                run += 1
            else:
                if run >= 5:
                    score += 3 + (run - 5)
                run, prev = 1, v
        if run >= 5:
            score += 3 + (run - 5)
    # regla 2: blocs 2x2
    for r in range(size - 1):
        for c in range(size - 1):
            v = matrix[r][c]
            if v == matrix[r][c + 1] == matrix[r + 1][c] == matrix[r + 1][c + 1]:
                score += 3
    # regla 3: patrons 1:1:3:1:1 amb zona clara
    pat_a = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    pat_b = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]
    for line in list(matrix) + [list(col) for col in zip(*matrix)]:
        for i in range(size - 10):
            window = line[i:i + 11]
            if window == pat_a or window == pat_b:
                score += 40
    # regla 4: proporcio de moduls foscos
    dark = sum(sum(row) for row in matrix)
    ratio = dark * 100 // (size * size)
    score += 10 * (min(abs(ratio - 50), abs((dark * 100 + size * size - 1) // (size * size) - 50)) // 5)
    return score


def make_matrix(text, level='Q', version=None):
    version = version or choose_version(text, level)
    codewords = interleave(encode_data(text, version, level), version, level)

    bits = []
    for cw in codewords:
        for i in range(7, -1, -1):
            bits.append((cw >> i) & 1)
    bits += [0] * REMAINDER[version]

    base, reserved, size = build_function_patterns(version)
    positions = data_positions(size, reserved)
    assert len(positions) == len(bits), (len(positions), len(bits))

    best = None
    for mask in range(8):
        matrix = [row[:] for row in base]
        for (r, c), bit in zip(positions, bits):
            matrix[r][c] = bit ^ (1 if MASKS[mask](r, c) else 0)
        place_format(matrix, size, level, mask)
        score = penalty(matrix, size)
        if best is None or score < best[0]:
            best = (score, mask, matrix)

    return best[2], size, version, best[1]


# ---------------------------------------------------- descodificar (test) ---
def decode_matrix(matrix, size, version, level, mask):
    """Llegeix la matriu i retorna el text. Serveix de validacio de l'encoder."""
    _, reserved, _ = build_function_patterns(version)
    positions = data_positions(size, reserved)
    bits = [matrix[r][c] ^ (1 if MASKS[mask](r, c) else 0) for r, c in positions]
    codewords = [int(''.join(str(b) for b in bits[i:i + 8]), 2)
                 for i in range(0, len(bits) - REMAINDER[version], 8)]

    ec_len, groups = BLOCKS[(version, level)]
    sizes = []
    for n, sz in groups:
        sizes += [sz] * n
    blocks = [[] for _ in sizes]
    idx = 0
    for i in range(max(sizes)):
        for b, sz in enumerate(sizes):
            if i < sz:
                blocks[b].append(codewords[idx])
                idx += 1
    data = [cw for b in blocks for cw in b]

    stream = ''.join(f'{cw:08b}' for cw in data)
    assert stream[:4] == '0100', 'mode inesperat'
    length = int(stream[4:12], 2)
    payload = bytes(int(stream[12 + i * 8:20 + i * 8], 2) for i in range(length))
    return payload.decode('utf-8')


# ------------------------------------------------------------------ SVG ----
def to_svg(matrix, size, quiet=4, module=8, dark='#0A0A0A', light='#FFFFFF'):
    total = (size + quiet * 2) * module
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{total}" '
        f'viewBox="0 0 {total} {total}" shape-rendering="crispEdges" role="img" '
        f'aria-label="Codi QR">',
        f'<rect width="{total}" height="{total}" fill="{light}"/>',
        f'<path fill="{dark}" d="',
    ]
    path = []
    for r in range(size):
        c = 0
        while c < size:
            if matrix[r][c]:
                run = 0
                while c + run < size and matrix[r][c + run]:
                    run += 1
                x = (c + quiet) * module
                y = (r + quiet) * module
                path.append(f'M{x} {y}h{run * module}v{module}h-{run * module}z')
                c += run
            else:
                c += 1
    parts.append(''.join(path))
    parts.append('"/></svg>\n')
    return ''.join(parts)


# ----------------------------------------------------------------- tests ---
def run_tests():
    # 1. Camp de Galois: x^8 = x^4+x^3+x^2+1 amb el polinomi 0x11D.
    assert EXP[8] == 0x1D and EXP[0] == 1 and LOG[1] == 0
    assert all(gf_mul(a, EXP[255 - LOG[a]]) == 1 for a in range(1, 256))

    # 2. Reed-Solomon: la paraula codi sencera ha de ser divisible pel generador,
    #    es a dir, tots els sindromes s'anul·len a alpha^0..alpha^(n-1).
    for n_ec in (7, 10, 13, 18, 26):
        data = [(i * 37 + 11) % 256 for i in range(20)]
        word = data + rs_encode(data, n_ec)
        for i in range(n_ec):
            acc = 0
            for cw in word:
                acc = gf_mul(acc, EXP[i]) ^ cw
            assert acc == 0, f'sindrome no nul (ec={n_ec}, i={i})'

    # 2. Format info: valors tabulats de l'estandard.
    assert bch_format((EC_INDICATOR['L'] << 3) | 0) == 0b111011111000100
    assert bch_format((EC_INDICATOR['M'] << 3) | 0) == 0b101010000010010
    #    i la distancia minima del codi BCH(15,5) ha de ser 7.
    words = [bch_format(v) for v in range(32)]
    assert min(bin(a ^ b).count('1') for i, a in enumerate(words)
               for b in words[i + 1:]) == 7

    # 3. Informacio de versio: valors tabulats.
    assert version_info_bits(7) == 0x07C94
    assert version_info_bits(10) == 0x0A4D3

    # 4. Anada i tornada: codificar i tornar a llegir la matriu.
    for txt, lvl in [('https://cbgrupbarna.info/opina', 'Q'),
                     ('https://cbgrupbarna.info/', 'H'),
                     ('CB GRUP BARNA 1965 · El Clot, Barcelona', 'M'),
                     ('x' * 100, 'L')]:
        matrix, size, version, mask = make_matrix(txt, lvl)
        assert decode_matrix(matrix, size, version, lvl, mask) == txt, txt
        # patrons de localitzacio als tres angles
        for (r0, c0) in [(0, 0), (0, size - 7), (size - 7, 0)]:
            for r in range(7):
                for c in range(7):
                    assert matrix[r0 + r][c0 + c] == FINDER[r][c], 'finder trencat'
        assert matrix[size - 8][8] == 1, 'modul fosc absent'
        for i in range(8, size - 8):
            assert matrix[6][i] == 1 - (i % 2), 'timing trencat'

    print('QR: totes les validacions OK')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_tests()
        sys.exit(0)
    text = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else 'qr.svg'
    level = sys.argv[3] if len(sys.argv) > 3 else 'Q'
    run_tests()
    matrix, size, version, mask = make_matrix(text, level)
    assert decode_matrix(matrix, size, version, level, mask) == text
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(to_svg(matrix, size))
    print(f'{out}: v{version}-{level}, mask {mask}, {size}x{size} moduls · {text}')
