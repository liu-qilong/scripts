drive_path='/Volumes/BACKUP'
local_path='/Users/knpob/Territory'
icloud_path='/Users/knpob/Documents'
app_path='/Users/knpob/Library/Mobile Documents'

# colors
green='\033[0;32m'
red='\033[0;31m'
nocolor='\033[0m'

# backup local drive files
for folder in 'Marx' 'Kolmo' 'Humboldt'
do
    src="$local_path/$folder"
    des="$drive_path/Territory"
    echo "backup $green$src$nocolor >> $green$des$nocolor"
    rsync -av --delete --exclude '*-nosync' "$src" "$des"
done

# backup cloud drive files
for folder in 'Achilles' 'Odyssey' 'Nietzsche' 
do
    src="$icloud_path/$folder"
    des="$drive_path/Territory"
    echo "backup $green$src$nocolor >> $green$des$nocolor"
    rsync -av --delete --exclude '*-nosync' "$src" "$des"
done

# backup app data
for folder in "iCloud~md~obsidian" "iCloud~com~apple~iBooks" "iCloud~is~workflow~my~workflows"
do
    src="$app_path/$folder/Documents/"
    des="$drive_path/App/$folder"
    echo "backup $green$src$nocolor >> $green$des$nocolor"
    rsync -av --delete --exclude '*-nosync' "$src" "$des"
done