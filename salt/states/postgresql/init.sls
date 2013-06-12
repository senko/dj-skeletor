postgresql:
    pkg.installed:
        - pkgs:
            - postgresql-9.1
            - postgresql-contrib-9.1
            - postgresql-doc-9.1
            - postgresql-server-dev-9.1
    service:
        - running
        - require:
            - pkg: postgresql
        - watch:
            - file: /etc/postgresql/9.1/main/pg_ident.conf
            - file: /etc/postgresql/9.1/main/pg_hba.conf

/etc/postgresql/9.1/main/pg_ident.conf:
    file.managed:
        - source: salt://postgresql/pg_ident.conf
        - template: jinja
        - require:
            - pkg: postgresql

/etc/postgresql/9.1/main/pg_hba.conf:
    file.managed:
        - source: salt://postgresql/pg_hba.conf
        - template: jinja
        - require:
            - pkg: postgresql
