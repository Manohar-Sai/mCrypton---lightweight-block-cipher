# mCrypton S-box
sbox = [[4, 15, 3, 8, 13, 10, 12, 0, 11, 5, 7, 14, 2, 6, 1, 9],
        [1, 12, 7, 10, 6, 13, 5, 3, 15, 11, 2, 0, 8, 4, 9, 14],
        [7, 14, 12, 2, 0, 9, 13, 10, 3, 15, 5, 8, 6, 4, 11, 1],
        [11, 0, 10, 7, 13, 6, 4, 2, 12, 14, 3, 9, 1, 5, 15, 8]]


def su0(u0):
    """This function does a nibble wise substitution for the first 16 bits of user key where each nibble is 4bits"""
    u = [int(str(u0)[2], 16), int(str(u0)[3], 16), int(str(u0)[4], 16), int(str(u0)[5], 16)]
    su = []
    for k in range(4):
        su.append(str(sbox[k][u[k]]))
    return hex(int(''.join(su), 16))


def updated_key(key1):
    """This function updates the user key for the next round key"""
    z = [key1[5], key1[6], key1[7]]
    a = bin(int(key1[0], 16))
    stx = str(a)[2:]
    while len(stx) < 16:
        stx = '0' + stx
    stx = stx[3:] + stx[0:3]
    z.append(hex(int(stx, 2)))
    z.append(key1[1])
    z.append(key1[2])
    z.append(key1[3])
    y = bin(int(key1[4], 16))
    stx = str(y)[2:]
    while len(stx) < 16:
        stx = '0' + stx
    stx = stx[8:] + stx[0:8]
    z.append(hex(int(stx, 2)))
    return z


def main():
    """Main function processes all round keys"""
    round_constant1 = [0b0001, 0b0010, 0b0100, 0b1000,
                       0b0011, 0b0110, 0b1100, 0b1011,
                       0b0101, 0b1010, 0b0111, 0b1110,
                       0b1111, 0b0000, 0b0000, 0b0000]
    round_constant = []
    round_keys = []
    for i in range(13):
        x = round_constant1[i] << 12
        round_constant.append(hex(x))

    # user key 128-bit given by user in hex decimal in list where each element is 1 byte
    U1 = ['7a', '4c', '7c', 'cf', '30', '4c', 'be', '27', '96', '67', '6f', '5f', '0f', 'bb', '6d', '58']
    try:
        if len(U1) > 16:
            raise ValueError
    except ValueError:
        print('Invalid Input!!')
        exit(0)
    U = []
    for i in U1:
        U.append(i[0])
        U.append(i[1])
    U.reverse()
    key = []
    for i in range(8):
        x = []
        for j in range(4):
            try:
                x.append(U.pop())
            except IndexError:
                print('Invalid user key')
                exit(0)
        key.append(hex(int(''.join(x), 16)))
    M = [0xf000, 0x0f00, 0x00f0, 0x000f]
    print('Round constants : ')
    print(round_constant)
    print()
    print('Initial 128-bit user key :')
    print(key)
    print()
    print('Updated 128-bit user key : ')
    for i in range(13):
        T1 = int(su0(key[0]), 16) ^ int(round_constant[i], 16)
        T = []
        for j in range(4):
            T.append(T1 & M[j])
        x = []
        for j in range(4):
            x.append(hex(int(key[j + 1], 16) ^ T[j]))
        round_keys.append(x)
        if i > 0:
            print(key)
        key = updated_key(key)
    print()
    print('Round keys : ')
    for r in round_keys:
        print(r)
    t =[]
    for i in round_keys:
        for j in i:
            t.append(j)
    with open('Roundkeys.txt', 'w') as file1:
        file1.write(' '.join(t))


if __name__ == '__main__':
    main()
