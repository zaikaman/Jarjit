git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch app/resources/api_keys.json" \
--prune-empty --tag-name-filter cat -- --all 