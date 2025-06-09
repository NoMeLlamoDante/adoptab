ssh -o StrictHostKeyChecking=no  $USER@$IP <<SSH

cd workplace/adoptab

git pull --rebase origin main

source env/bin/activate

python3 manage.py collectstatic --noinput

SSH