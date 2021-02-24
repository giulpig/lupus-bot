echo Insert commit commment
read comment
git add .
git commit -m $comment
git push heroku master

