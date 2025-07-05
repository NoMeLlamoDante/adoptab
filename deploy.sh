ssh -o StrictHostKeyChecking=no  $USER@$IP <<SSH

cd workplace/adoptab

git pull --rebase origin main

source env/bin/activate

pip install -r requirements.txt 

python3 manage.py collectstatic --noinput

systemctl restart nginx
systemctl restart gunicorn

SSH