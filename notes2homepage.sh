notes_path='/Users/knpob/Library/Mobile Documents/iCloud~md~obsidian/Documents/DeepSpace'
homepage_path='/Users/knpob/Documents/Weber/homepage'

rsync -av --delete --exclude '*-private*' --exclude '.DS_Store' "$notes_path/blog" "$homepage_path/contents"
rsync -av --delete --exclude '*-private*' --exclude '.DS_Store' "$notes_path/note" "$homepage_path/contents"
rsync -av --delete --exclude '*-private*' --exclude '.DS_Store' "$notes_path/img" "$homepage_path/public"