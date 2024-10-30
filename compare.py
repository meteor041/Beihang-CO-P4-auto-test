# coding=gbk
#enoding=gbk
def main():
    right_ans_path = "./result/right_ans.txt"
    your_ans_path = "./result/your_ans.txt"
    with open(your_ans_path, "r") as f1, open(right_ans_path, "r") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        lines1 = [x for x in lines1 if x.startswith('@') and not '$ 0' in x]
        lines2 = [x for x in lines2 if x.startswith('@')]
        flag = False
        if len(lines1) > len(lines2):
            print("more results than we expect")
            lines2 += [""] * (len(lines1) - len(lines2))
        elif len(lines1) < len(lines2):
            print("less results than we expect")
            lines1 += [""] * (len(lines2) - len(lines1))
        else:
            flag = True
        for line1, line2 in zip(lines1, lines2):
            line1 = line1[:-len('\n')] if '\n' in line1 else line1
            line2 = line2[:-len('\n')] if '\n' in line2 else line2
            if line1 != line2:
                print("we got \"" + line1 + "\" but we expected \"" + line2+"\"")
                flag = False
        if flag:
            print("yes!!!")

if __name__ == '__main__':
    main()