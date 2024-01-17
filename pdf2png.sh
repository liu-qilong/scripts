# to use this script, make sure that you have installed imagemagick
# and place the pdf file in temp/

read -p "enter the name of the file (without extension): " file
read -p "enter pixel width of the output (default=800): " width
width=${width:-800}

convert -density 300 "temp/$file.pdf" -resize "$width""x" "temp/temp.png"
convert temp/temp*.png -append "temp/$file.png"
rm temp/temp-*.png