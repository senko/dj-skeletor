postgresql_dbuser:
  postgres_user.present:
    - runas: postgres
    - name: {{ pillar['postgresql-dbuser'] }}
    - password: {{ pillar['postgresql-dbpass'] }}
    - require:
      - service: postgresql

sunrise_db:
  postgres_database.present:
    - runas: postgres
    - name: {{ pillar['postgresql-dbname'] }}
    - owner: {{ pillar['postgresql-dbuser'] }}
    - require:
      - postgres_user: {{ pillar['postgresql-dbuser'] }}
      - service: postgresql
