django-deps:
    pkg.installed:
        - pkgs:
            - virtualenvwrapper
            - python-pip
            - python-dev
            - libfreetype6-dev
            - libjpeg-dev
            - liblcms1-dev
            - zlib1g-dev
            - libpq-dev
            - build-essential

django-env:
    virtualenv.managed:
        - name: {{ pillar['virtualenv-home'] }}
        - no_site_packages: True
        - runas:  {{ pillar['app-user'] }}
        - require:
            - pkg: django-deps
            - user: {{ pillar['app-user'] }}

/home/{{ pillar['app-user'] }}/.bashrc:
    file.managed:
        - runas: {{ pillar['app-user'] }}
        - source: salt://django/bashrc
        - template: jinja
        - require:
            - user: {{ pillar['app-user'] }}
            - pkg: django-deps

{% if not pillar.get('development') %}
app-code:
    git.latest:
        - runas: {{ pillar['app-user'] }}
        - name: {{ pillar['git-repo'] }}
        - target: {{ pillar['app-root'] }}
        - force: True
        - require:
            - user: {{ pillar['app-user'] }}
{% endif %}

{% if pillar.get('development') %}
update:
    cmd.run:
        - name: . ~/.bashrc && make dev-update
        - cwd: {{ pillar['app-root'] }}
        - user: {{ pillar['app-user'] }}
        - shell: /bin/bash
        - require:
            - file: /home/{{ pillar['app-user'] }}/.bashrc
            - user: {{ pillar['app-user'] }}
{% else %}
update:
    cmd.wait:
        - name: . ~/.bashrc && make prod-update
        - cwd: {{ pillar['app-root'] }}
        - user: {{ pillar['app-user'] }}
        - shell: /bin/bash
        - require:
            - file: /home/{{ pillar['app-user'] }}/.bashrc
            - user: {{ pillar['app-user'] }}
        - watch:
            - git: app-code
{% endif %}
