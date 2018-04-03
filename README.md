# tok41.github.io
tok41's weblog

## About
- ブログ

## Branch
- master : ブログの本体。ローカルマシンからghp-importでcommitしてpushする
```
$ ghp-import output
$ git push https://github.com/{username}/{username}.github.io.git gh-pages:master
```
- source : ブログのソース管理用のbranch
```
$ git add .
$ git commit -m 'first commit’
$ git push https://github.com/{username}/{username}.github.io.git source:source
```
