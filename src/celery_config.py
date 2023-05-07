from helpers.project_envs import ProjectEnvs

broker_url = ProjectEnvs.CELERY_BROKER_URL

result_backend = ProjectEnvs.CELERY_RESULT_BACKEND_URL

task_serializer = 'json'  # Serializer used for task messages

result_serializer = 'json'  # Serializer used for result messages

accept_content = ['json']  # List of accepted content-types for task messages

worker_concurrency = 5  # Number of worker processes/threads to spawn

worker_redirect_stdouts_level = 'INFO'  # Logging level for Celery workers

task_ignore_result = False

task_track_started = True

imports = ('tasks.celery_alibaba_tasks',)  # List of modules to import when Celery starts up

task_soft_time_limit = None

task_time_limit = None
