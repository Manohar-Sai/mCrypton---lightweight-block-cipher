# mCrypton S-box
sbox = [[4, 15, 3, 8, 13, 10, 12, 0, 11, 5, 7, 14, 2, 6, 1, 9],
        [1, 12, 7, 10, 6, 13, 5, 3, 15, 11, 2, 0, 8, 4, 9, 14],
        [7, 14, 12, 2, 0, 9, 13, 10, 3, 15, 5, 8, 6, 4, 11, 1],
        [11, 0, 10, 7, 13, 6, 4, 2, 12, 14, 3, 9, 1, 5, 15, 8]]
# round_key produced by Key Scheduling algorithm
round_keys = []
with open('Roundkeys.txt', 'r') as file1:
    Round_keys = file1.read().split()
t = []
for i in range(13*4):
    t.append(Round_keys[i])
    if (i+1) % 4 == 0:
        round_keys.append(t)
        t = []
print(round_keys)
M = [0xe, 0xd, 0xb, 0x7]


def Non_linear_substitution(m):
    """Non-linear Substitution : Each element is called a nibble, nibble-wise substitution, using four 4-bit S-
boxes"""
    n = []
    for i in range(4):
        for j in range(4):
            try:
                n.append(hex(sbox[(i + j) % 4][int(m[i][j], 16)]))
            except IndexError:
                print('Invalid Input!!')
                exit(0)
    o = [n[0:4], n[4:8], n[8:12], n[12:]]
    return o


def Bit_permutation(m):
    """Bit Permutation : mixes column 0 to 3 by using given operation"""
    n = Col_to_row(m)
    b = []
    for i in range(4):
        a = n[i]
        c = []
        for j in range(4):
            c.append(hex((int(str(a[0]), 16) & M[(i + j + 0) % 4]) ^
                     (int(str(a[1]), 16) & M[(i + j + 1) % 4]) ^
                     (int(str(a[2]), 16) & M[(i + j + 2) % 4]) ^
                     (int(str(a[3]), 16) & M[(i + j + 3) % 4])))
        b.append(c)
    b = Col_to_row(b)
    return b


def Col_to_row(m):
    """Column-To-Row Transposition : moves the nibble in the position ( i , j ) to the
position ( j , i )"""
    n = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        for j in range(4):
            try:
                n[j][i] = m[i][j]
            except IndexError:
                print('Invalid Input!!')
                exit(0)
    return n


def Key_addition(m, p):
    """Key Addition : For a round key K r  ( K r [0], K r [1], K r [2], K r [3]) , it is a simple
bit-wise XOR operation."""
    n = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    key = round_keys[p]
    k = []
    for i in key:
        q = []
        s = str(i)[2:]
        while len(s) < 4:
            s = '0' + s
        for j in s:
            q.append(hex(int(j, 16)))
        k.append(q)
    for i in range(4):
        for j in range(4):
            n[i][j] = hex(int(m[i][j], 16) ^ int(k[i][j], 16))
    return n


def main():
    """Main function initializing and running 12 rounds"""
    # msgin = ['6', '3', '7', 'c', '7', '7', '7', 'b', 'f', '2', '6', 'b', '6', 'f', 'c', '5']
    # Taking input message from the user
    y = input('Enter your plain text in hex decimal of 64-bit giving 1 space between every 4bits :\n')
    msgin = y.split(' ')
    try:
        if len(msgin) > 16:
            raise ValueError
    except ValueError:
        print('Invalid Input!!')
        exit(0)
    msg = []
    su1 = []
    pi1 = []
    tu1 = []
    si1 = []
    x = []
    for i in range(16):
        try:
            x.append(hex(int(msgin[i], 16)))
        except ValueError:
            print('Invalid input!!')
            exit(0)
        if i > 0 and (i + 1) % 4 == 0:
            msg.append(x)
            x = []
    si = Key_addition(msg, 0)   # Addition transformation before 1st round
    si1.append(si)
    for i in range(12):     # 12 rounds
        su = Non_linear_substitution(si)
        su1.append(su1)
        pi = Bit_permutation(su)
        pi1.append(pi)
        tu = Col_to_row(pi)
        tu1.append(tu)
        si = Key_addition(tu, i + 1)
        si1.append(si)
    # final operation after final round
    fi_tu = Col_to_row(si)
    fi_pi = Bit_permutation(fi_tu)
    fi_tu2 = Col_to_row(fi_pi)
    print('encrypted message : ')
    for i in fi_tu2:
        print(i)


if __name__ == '__main__':
    main()
