# to use this script, make sure that you have installed imagemagick

if [ -d "temp" ]; then
    echo "Warning: temp/ folder already exists. Please remove it before running the script."
    exit 1
fi

mkdir temp
read -p "Enter the name of the file (without extension): " file
convert -density 300 "$file.pdf" -resize 800x "temp/$file.png"
rm -r temp