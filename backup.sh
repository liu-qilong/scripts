export drive_path='/Volumes/BACKUP'
export icloud_path='/Users/knpob/Library/Mobile Documents/com~apple~CloudDocs/Territory'
export local_path='/Users/knpob/Territory'
export obsidian_path='/Users/knpob/Library/Mobile Documents/iCloud~md~obsidian/Documents'

# colors
export green='\033[0;32m'
export red='\033[0;31m'
export nocolor='\033[0m'

# backup local drive files
for folder in 'Marx' 'Kolmo' 'Nietzsche' 'Humboldt'
do
    export src="$local_path/$folder"
    export des="$drive_path/Territory"
    echo "backup $green$src$nocolor >> $green$des$nocolor"
    rsync -av --delete --exclude '*-nosync' "$src" "$des"
done

# backup cloud drive files
for folder in 'Achilles' 'Odyssey'
do
    export src="$icloud_path/$folder"
    export des="$drive_path/Territory"
    echo "backup $green$src$nocolor >> $green$des$nocolor"
    rsync -av --delete --exclude '*-nosync' "$src" "$des"
done

# backup obsidian vaults
export src="$obsidian_path/"
export des="$drive_path/Obsidian"
echo "backup $green$src$nocolor >> $green$des$nocolor"
rsync -av --delete --exclude '*-nosync' "$src" "$des"