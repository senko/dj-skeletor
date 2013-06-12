gunicorn:
    service:
        - running
        - require:
            - virtualenv: django-env
            - pkg: django-deps
            - user: {{ pillar['app-user'] }}
        - watch:
            - file: {{ pillar['app-root'] }}/gunicorn_config.py
            - file: /etc/init/gunicorn.conf

{{ pillar['app-root'] }}/gunicorn_config.py:
    file.managed:
        - runas: {{ pillar['app-user'] }}
        - source: salt://django/gunicorn_config.py
        - template: jinja
        - require:
            - user: {{ pillar['app-user'] }}

{{ pillar['app-root'] }}/logs:
    file.directory:
        - user: {{ pillar['app-user'] }}
        - makedirs: True
        - require:
            - user: {{ pillar['app-user'] }}

/etc/init/gunicorn.conf:
    file.managed:
        - source: salt://django/gunicorn.conf
        - template: jinja
