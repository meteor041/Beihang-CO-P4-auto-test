# coding=gb2312
from random import *

number = 50
gpr = [0] * 32
mem = [0] * (2**10)

def print_add(f, use_ra):
    rt = randint(0, 31)
    rs = randint(0, 31)
    rd = randint(0, 31) if use_ra else randint(0, 30)
    if -2**31 <= gpr[rs] + gpr[rt] <= 2**31-1:  # 若溢出,则不打印这条指令
        gpr[rd] = gpr[rs] + gpr[rt] if rd != 0 else 0
        f.write('add ' + '$' + str(rd) + ',' +
                '$' + str(rs) + ',' +
                '$' + str(rt) + '\n')

def print_sub(f, use_ra):
    rt = randint(0, 31)
    rs = randint(0, 31)
    rd = randint(0, 31) if use_ra else randint(0, 31)
    if -2**31 <= gpr[rs] + gpr[rt] <= 2**31-1:  # 若溢出,则不打印这条指令
        gpr[rd] = gpr[rs] + gpr[rt] if rd != 0 else 0
        f.write('sub ' + '$' + str(rd) + ',' +
                '$' + str(rs) + ',' +
                '$' + str(rt) + '\n')

def print_ori(f, use_ra):
    rt = randint(0, 31) if use_ra else randint(0, 30)
    rs = randint(0, 31)
    imm = randint(0, 2**8-1)
    if rt != 0:
        gpr[rt] = gpr[rs] | imm
    f.write('ori ' + '$' + str(rt) + ',' +
            '$' + str(rs) + ',' +
            str(imm) + '\n')

def print_lw(f, use_ra):
    base = randint(0, 31) if use_ra else randint(0, 30)
    imm = randint(0, 2 ** 8)
    if base != 0:
        gpr[base] = imm
    f.write('ori ' + '$' + str(base) + ',' +
            '$0' + ',' +
            str(imm) + '\n')
    rt = randint(0, 31)
    offset = (randint(-200, 200) // 4) * 4 - (gpr[base] % 4)
    if 2**10 > offset + gpr[base] > 0:
        if rt != 0:
            gpr[rt] = mem[gpr[base] + offset]
        f.write('lw ' + '$' + str(rt) + ',' +
                str(offset) + '(' + '$' +
                str(base) + ')\n')

def print_sw(f, use_ra):
    base = randint(0, 31) if use_ra else randint(0, 30)
    imm = randint(0, 2 ** 8)
    if base != 0:
        gpr[base] = imm
    f.write('ori ' + '$' + str(base) + ',' +
            '$0' + ',' +
            str(imm) + '\n')
    rt = randint(0, 31) if use_ra else randint(0, 30)
    offset = (randint(-200, 200) // 4) * 4 - (gpr[base] % 4)
    if 2 ** 10 > offset + gpr[base] > 0:
        if rt != 0:
            gpr[rt] = mem[gpr[base] + offset]
        f.write('sw ' + '$' + str(rt) + ',' +
                str(offset) + '(' + '$' +
                str(base) + ')\n')

def ori(f, key, num):
    gpr[key] = num
    f.write('ori ' + '$' + str(key) + ',' +
            '$0' + ',' +
            str(num) + '\n')

def add(f, rd, rs, rt):
    gpr[rd] = gpr[rs] + gpr[rt]
    f.write('add ' + '$' + str(rd) + ',' +
                '$' + str(rs) + ',' +
                '$' + str(rt) + '\n')

def sub(f, rd, rs, rt):
    gpr[rd] = gpr[rs] - gpr[rt]
    f.write('sub ' + '$' + str(rd) + ',' +
                '$' + str(rs) + ',' +
                '$' + str(rt) + '\n')

label_ct = 0
def print_beq(f):
    global label_ct
    rs = randint(1, 31)  # 排除$0
    rt = randint(1, 31)
    while rt == rs:
        rt = randint(1, 31)  # rt != rs
    key1 = randint(1, 31)  # 中转
    while key1 == rt or key1 == rs:
        key1 = randint(1, 31)
    key2 = randint(1, 31)  # 中转
    while key2 == rt or key2 == rs or key2 == key1:
        key2 = randint(1, 31)


    mod = randint(0, 1)  # 跳转方向
    equal = randint(0, 1)  # 是否相等
    label = 'labelx'.replace("x", str(label_ct))
    label_ct += 1
    in_ct = randint(0, 20)  # 指令总数

    # 这里为了避免溢出,我们取一个较小的数而且它不能是0
    imm = randint(1, 2**10-1)
    ori(f, key1, imm)  # 将中转寄存器key1设为imm
    ori(f, key2, imm)

    if mod == 1:   # 向下跳转
        if equal == 1:  # 相等

            imm = randint(0, 2 ** 16 - 1)
            gpr[rt] = gpr[rs] = imm
            f.write('ori ' + '$' + str(rt) + ',' +
                    '$0' + ',' +
                    str(imm) + '\n')
            f.write('ori ' + '$' + str(rs) + ',' +
                    '$0' + ',' +
                    str(imm) + '\n')
        else:  # 不相等(极小概率相等)
            imm1 = randint(0, 2 ** 16 - 1)
            imm2 = randint(0, 2 ** 16 - 1)
            gpr[rt] = imm1
            gpr[rs] = imm2
            f.write('ori ' + '$' + str(rt) + ',' +
                    '$0' + ',' +
                    str(imm1) + '\n')
            f.write('ori ' + '$' + str(rs) + ',' +
                    '$0' + ',' +
                    str(imm2) + '\n')
        f.write('beq ' + '$' + str(rs) + ',' +
                '$' +str (rt) + ',' + label + '\n')
        run(f, in_ct, True)
        f.write(label + ':\n')
    else:
        # 向上跳转
        f.write(label + ':\n')
        run(f, in_ct, True)
        if equal == 1:  # 相等,这里处理死循环的可能
            sub(f, key1, key1, key2) # 第一次循环key1为0
            imm = randint(0, 2 ** 16 - 1)
            gpr[rt] = gpr[rs] = imm
            f.write('ori ' + '$' + str(rs) + ',' +
                    '$0' + ',' +
                    str(imm) + '\n')
            f.write('ori ' + '$' + str(rt) + ',' +
                    '$0' + ',' +
                    str(imm) + '\n')
            add(f, rt, rt, key1) # gpr[rt] = gpr[rt] + 0(key1)
        else:
            imm1 = randint(0, 2 ** 16 - 1)
            imm2 = randint(0, 2 ** 16 - 1)
            gpr[rt] = imm1
            gpr[rs] = imm2
            f.write('ori ' + '$' + str(rt) + ',' +
                    '$0' + ',' +
                    str(imm1) + '\n')
            f.write('ori ' + '$' + str(rs) + ',' +
                    '$0' + ',' +
                    str(imm2) + '\n')
        f.write('beq ' + '$' + str(rs) + ','
                '$' + str(rt) + ',' + label + '\n')

def print_lui(f, use_ra):
    rt = randint(0, 31) if use_ra else randint(0, 30)
    imm = randint(0, 2**16-1)
    if rt != 0:
        gpr[rt] = imm << 16
    f.write('lui' + ' $' + str(rt) +
            ',' + str(imm) + '\n')

def print_nop(f):
    f.write('nop\n')

def print_jal(f):
    global label_ct
    f.write("jal labelx\n".replace("x", str(label_ct)))
    run(f, randint(0,20), True)
    f.write("labelx:\n".replace("x", str(label_ct)))
    label_ct += 1

def run(f, ct, use_ra):
    op_set = ['add', 'sub', 'ori', 'lw', 'sw', 'lui', 'nop']
    for _ in range(ct):
        op = op_set[randint(0, len(op_set)-1)]
        if op == 'add':
            print_add(f, use_ra)
        elif op == 'sub':
            print_sub(f, use_ra)
        elif op == 'ori':
            print_ori(f, use_ra)
        elif op == 'lw':
            print_lw(f, use_ra)
        elif op == 'sw':
            print_sw(f, use_ra)
        elif op == 'lui':
            print_lui(f, use_ra)
        else:
            print_nop(f)

def main():
    op_set = ['add', 'sub', 'ori', 'lw', 'sw', 'beq', 'lui', 'nop', 'jal']
    path = 'instruction.asm'

    with open(path, "w") as f:
        for x in range(0, 32):
            ori(f, x, randint(0, 2 ** 16 - 1))
        for _ in range(number):
            op = op_set[randint(0, len(op_set) - 1)]
            if op == 'add':
                print_add(f, True)
            elif op == 'sub':
                print_sub(f, True)
            elif op == 'ori':
                print_ori(f, True)
            elif op == 'lw':
                print_lw(f, True)
            elif op == 'sw':
                print_sw(f, True)
            elif op == 'beq':
                print_beq(f)
            elif op == 'lui':
                print_lui(f, True)
            elif op == 'jal':
                print_jal(f)
            else:
                print_nop(f)
    # 接下来打印jr语句
        f.write("jal labelx\n".replace("x", str(label_ct)))
        run(f, randint(0, 20), False)
        f.write("jal End\n")
        run(f, randint(0, 20), False)
        f.write("labelx:\n".replace("x", str(label_ct)))
        run(f, randint(0, 20), False)
        f.write("jr $ra\n")
        # "结束"标签
        f.write("End:\n")



if __name__ == '__main__':
    main()
