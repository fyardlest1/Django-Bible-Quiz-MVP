#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py migrate --no-input
python manage.py collectstatic --no-input


chmod +x build.sh
git add build.sh && git commit -m "Add Render build script"
git push
