GIT CHEATSHEET

# SET UP
## initialise (creates folder .init)
git init

## set origin
git remote add origin <url>

## pull files down
git pull origin master




# AFTER CHANGES
## 1. add file to a commit
git add <filename>

## 2. commit
git commit -m "Message"

## 3. push it to github
git push -u origin master



# OTHER 
## ask for status
git status

## before changes/upload you often need to pull
git pull origin master
