base:
    '*':
        - basereqs
        - django
        - django.nginx
{% if pillar.get('development') %}
{% else %}
        - django.gunicorn
{% endif %}
{% if pillar['postgresql-dbhost'] == 'localhost' %}
        - postgresql
        - postgresql.dbsetup
{% endif %}
