drive_path='/Volumes/BACKUP'
icloud_path='/Users/knpob/Documents'
local_path='/Users/knpob/Territory'
obsidian_path='/Users/knpob/Library/Mobile Documents/iCloud~md~obsidian/Documents'
notes_path='/Users/knpob/Desktop/notes'
beancount_path='/Users/knpob/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/beancount'

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

# backup notes
des="$drive_path/Desktop"
echo "backup $green$notes_path$nocolor >> $green$des$nocolor"
rsync -av --delete --exclude '*-nosync' "$notes_path" "$des"

# backup beancount
des="$drive_path/Desktop"
echo "backup $green$beancount_path$nocolor >> $green$des$nocolor"
rsync -av --delete --exclude '*-nosync' "$beancount_path" "$des"

# backup obsidian vaults
src="$obsidian_path/"
des="$drive_path/Obsidian"
echo "backup $green$src$nocolor >> $green$des$nocolor"
rsync -av --delete --exclude '*-nosync' "$src" "$des"