ssh ssh -o StrictHostKeyChecking=no  $USER@$IP <<SSH

cd workplace/adoptab

git pull --rebase origin main

SSH