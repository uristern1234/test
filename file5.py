import requests
import io

def send_to_cuckoo(raw_exe, pasteid):
    cuckoo_ip = conf["post_process"]["post_b64"]["cuckoo"]["api_host"]
    cuckoo_port = conf["post_process"]["post_b64"]["cuckoo"]["api_port"]
    cuckoo_host = 'http://{0}:{1}'.format(cuckoo_ip, cuckoo_port)
    submit_file_url = '{0}/tasks/create/file'.format(cuckoo_host)
    files = {'file': ('{0}.exe'.format(pasteid), io.BytesIO(raw_exe))}
    submit_file = requests.post(submit_file_url, files=files).json()
    task_id = None
    try:
        task_id = submit_file['task_id']
    except KeyError:
        try:
            task_id = submit_file['task_ids'][0]
        except KeyError:
            logger.error(submit_file)

    return task_id