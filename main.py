from indeed import get_jobs
from repo import get_last_document, add_documents


def lambda_handler(event, context):
    last_doc = get_last_document()
    last_job_id = ''
    last_index = 0

    if last_doc is not None:
        last_job_id = last_doc['job_id']
        last_index = int(last_doc['doc_id'])

    indeed_jobs = get_jobs(last_index, last_job_id)

    if len(indeed_jobs) > 0:
        add_documents(indeed_jobs)

    return {
        "status": 200,
        "added_jobs": len(indeed_jobs)
    }
