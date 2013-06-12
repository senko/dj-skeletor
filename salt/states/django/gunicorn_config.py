bind = "127.0.0.1:{{ pillar['app-port'] }}"
workers = {{ pillar['django-gunicorn-workers'] }}
accesslog = "logs/access.txt"
errorlog = "logs/error.txt"
pidfile = "gunicorn_pid.txt"
loglevel = "info"
daemon = False
