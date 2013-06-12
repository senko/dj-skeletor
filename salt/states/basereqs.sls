base-reqs:
    pkg.installed:
        - pkgs:
            - vim-nox
            - git

{{ pillar['app-user'] }}:
    user.present:
        - fullname: Application User
        - shell: /bin/bash
        - home: /home/{{ pillar['app-user'] }}
        - createhome: True
