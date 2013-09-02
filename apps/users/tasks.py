from celery import task
from project.utilities import send_email as project_send_email

@task
def send_email(*args, **kwargs):
    project_send_email(*args, **kwargs)
