import json
import re
from config import setup_logging
import logging

setup_logging()

def extract_ips_from_log(input_file: str, output_file: str):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    logging.info(f"IP 추출 시작: {input_file} → {output_file}")
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            try:
                log_data = json.loads(line)
                log_text = log_data.get("log", "")
                if re.search(r'^\d{4}/\d{2}/\d{2}', log_text):
                    logging.debug("날짜 로그 스킵됨")
                    continue
                ips = ip_pattern.findall(log_text)
                if ips:
                    logging.info(f"IP 추출됨: {ips}")
                else:
                    logging.debug("해당 라인에서 IP 없음")
                for ip in ips:
                    outfile.write(ip + "\n")
            except json.JSONDecodeError:
                logging.warning("잘못된 JSON 라인, 무시됨")
                continue

    logging.info("IP 추출 완료")
