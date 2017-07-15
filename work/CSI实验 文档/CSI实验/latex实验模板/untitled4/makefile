make clean:object.pdf
	cd ./文本_图片/pc;  mv object.pdf ../..
object.pdf:object.tex 
	cd ./文本_图片/pc;      pdflatex object.tex;     rm -f *.log *.aux  *.gz *.tex;
object.tex:doc.py
	python doc.py
