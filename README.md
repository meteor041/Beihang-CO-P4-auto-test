# 北航计组P4自动化测试程序

[Beihang-CO-P4-auto-test](https://github.com/meteor041/Beihang-CO-P4-auto-test)

## 运行环境

1. `python 3.12`
2. `iverilog`

## 使用方式

1. 将源文件(.v结尾)放入docs文件夹

2. 运行自动生成代码文件:

   ```bash
   python GenerateInstuction.py
   ```
3. 利用Mars产生机器码以及正确答案
	```bash
	java -jar Mars_perfect.jar mc CompactDataAtZero a dump .text HexText ./docs/code.txt nc instruction.asm
	java -jar Mars_perfect.jar mc CompactDataAtZero nc instruction.asm > ./result/right_ans.txt
	```
4. `iverilog`运行源文件产生结果
	```bash
	cd docs
	iverilog -o wave.exe -y ./ tb_mips.v
	vvp -n wave.exe -lxt2 > ../result/your_ans.txt
	```
5. 对比结果
	```bash
	cd ../
	python compare.py > ./result/diff.txt
	```

## 结果分析

若正确,`./result/diff.txt`中会出现:

```
yes!!!
```

若有错误,会出现:

```
we got "..." but we expected "..."
...
we got "..." but we expected "..."
```

