# require imagemagick
# init
export input_folder="input/"
export output_path="output/combined.pdf"

# parse options
while getopts "p:o:" opt; do
    case $opt in
        p) input_folder=$OPTARG ;;
        o) output_path=$OPTARG ;;
        \?) echo "Usage: $0 -p <input-folder/> -o <output-path.pdf>"
            exit 1 ;;
    esac
done

# find image files
files=$(find "$input_folder" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \))

if [ -z "$files" ]; then
    echo "no .png or .jpg files found in the input folder"
    exit 1
fi

# convert files to PDF
convert $files "$output_path"