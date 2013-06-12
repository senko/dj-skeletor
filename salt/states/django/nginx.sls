include:
    - django
    - nginx

/etc/nginx/sites-available/default:
    file.managed:
        - name: /etc/nginx/sites-available/default
        - source: salt://django/nginx.conf
        - template: jinja
        - require:
            - pkg: nginx
