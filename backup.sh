export destination='/Volumes/BACKUP'

# colors
export green='\033[0;32m'
export red='\033[0;31m'
export nocolor='\033[0m'

# backup local drive files
export source_local='/Users/knpob/Territory'

for folder in 'Marx' 'Kolmo' 'Nietzsche' 'Humboldt'
do
    export src="$source_local/$folder"
    export des="$destination/Territory"
    echo "backup $green$src$nocolor >> $green$des$nocolor"
    rsync -av --delete --exclude '*-nosync' "$src" "$des"
done

# backup cloud drive files
export source_cloud='/Users/knpob/Library/Mobile Documents/com~apple~CloudDocs/Territory'

for folder in 'Achilles' 'Odyssey'
do
    export src="$source_cloud/$folder"
    export des="$destination/Territory"
    echo "backup $green$src$nocolor >> $green$des$nocolor"
    rsync -av --delete --exclude '*-nosync' "$src" "$des"
done

# backup obsidian vaults
export source_obsidian='/Users/knpob/Library/Mobile Documents/iCloud~md~obsidian/Documents'
export src="$source_obsidian/"
export des="$destination/Obsidian"
echo "backup $green$src$nocolor >> $green$des$nocolor"
rsync -av --delete --exclude '*-nosync' "$src" "$des"