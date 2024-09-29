# require imagemagick
# init
export input_folder="input"
export output_folder="output"
export file_name="file"
export width=800

# parse options
while getopts "p:o:n:w" opt; do
    case $opt in
        p) input_folder=$OPTARG ;;
        o) output_folder=$OPTARG ;;
        n) file_name=$OPTARG ;;
        w) width=$OPTARG ;;
        \?) echo "Usage: $0 -p <input-folder> -o <output-folder> -n <file-name-wo-extention> -w <width-in-pixels>"
            exit 1 ;;
    esac
done

# convert pdf to png images
convert -density 300 "$input_folder/$file_name.pdf" -resize "$width""x" "$output_folder/$file_name.png"