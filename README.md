Obsidian is a free note-taking app and in older versions when you move stuff around the links don't get updated, so this is a way to update the links to what they should be. To run it you need to open your notes and clone it into your notes, and then run it. It edits your notes, so you should make sure to take a backup first if you decide to use it. 

from inside your notebook

```shell
git init
git add .
git commit -m "backup"
```

```shell
git clone https://github.com/haydenrear/obsidian-link-fixer.git link-fixer
cd link-fixer
python3  
```
