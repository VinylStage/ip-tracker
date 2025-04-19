from config import setup_logging
setup_logging()

import logging
import os

def deduplicate_ip_list(file_path: str):
    with open(file_path, 'r') as f:
        original_ips = [line.strip() for line in f if line.strip()]

    unique_ips = sorted(set(original_ips))

    logging.info(f"중복 제거 전 IP 개수: {len(original_ips)}")
    logging.info(f"중복 제거 후 고유 IP 개수: {len(unique_ips)}")

    dedup_file_path = f"{file_path}.dedup"

    with open(file_path, 'w') as f:
        for ip in original_ips:
            f.write(ip + "\n")

    with open(dedup_file_path, 'w') as f:
        for ip in unique_ips:
            f.write(ip + "\n")

    logging.info(f"중복 제거된 IP 목록 저장 완료: {dedup_file_path}")
