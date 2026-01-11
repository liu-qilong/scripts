# fish shell script to convert folder-like epub files from Apple Books to isolated epub file and then to markdown using pandoc
# input title without extension
title=$1
mv $title.epub temp
cd temp
zip -rX ../$title.epub mimetype META-INF OEBPS
cd ..
pandoc $title.epub -t markdown -o $title.md
rm -rf temp