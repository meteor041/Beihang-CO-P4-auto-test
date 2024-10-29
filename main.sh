python GenerateInstuction.py
java -jar Mars_perfect.jar mc CompactDataAtZero a dump .text HexText ./docs/code.txt nc instruction.asm
java -jar Mars_perfect.jar mc CompactDataAtZero nc instruction.asm > ./result/right_ans.txt
cd docs
iverilog -o wave.exe -y ./ tb_mips.v
vvp -n wave.exe -lxt2 > ../result/your_ans.txt
cd ../
python compare.py >> ./result/diff.txt