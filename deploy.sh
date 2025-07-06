ssh -o StrictHostKeyChecking=no  $USER@$IP <<SSH
set -e

cd ~/workplace/adoptab

git reset --hard

git clean -fd

git pull --rebase origin main

source env/bin/activate

pip install -r requirements.txt

python3 manage.py collectstatic --noinput

sudo /usr/bin/systemctl restart nginx.service
sudo /usr/bin/systemctl restart gunicorn.service

SSH