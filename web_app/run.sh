uwsgi --http 0.0.0.0:8000 -w app:app  --processes 4 --threads 2