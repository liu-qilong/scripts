# require imagemagick
# init
export file_path="input/file.pdf"
export output_folder="auto"
export width=800

# parse options
while getopts "f:o:n:w" opt; do
    case $opt in
        f) file_path=$OPTARG ;;
        o) output_folder=$OPTARG ;;
        w) width=$OPTARG ;;
        \?) echo "Usage: $0 -f <pdf-path> -o <output-folder> -w <width-in-pixels>. If -o is auto, the output folder will be the same as the input folder."
            exit 1 ;;
    esac
done

# parse file path
export input_folder="${file_path%/*}"
export file_name="${file_path##*/}"
export file_name="${file_name%.*}"

if [ "$output_folder" == "auto" ]; then
    output_folder=$input_folder
fi

# convert pdf to png images
magick convert -density 300 "$input_folder/$file_name.pdf" -resize "$width""x" "$output_folder/$file_name.png"