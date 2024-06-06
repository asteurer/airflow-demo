import pandas as pd
from paramiko import AutoAddPolicy, SSHClient

from example.config import SFTP_HOST, SFTP_PORT, username, password


def read_from_sftp(sftp_file_path):
    client = SSHClient()
    try:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname=SFTP_HOST, port=SFTP_PORT, username=username, password=password)

        with client.open_sftp() as sftp:
            with sftp.file(sftp_file_path, "r") as f:
                df = pd.read_excel(f)
                return df
    finally:
        client.close()
