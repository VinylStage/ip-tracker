from config import setup_logging
setup_logging()

import logging
import requests
import time
import json

def trace_ip_locations(ip_file: str, output_file: str):
    with open(ip_file, 'r') as f, open(output_file, 'w') as out:
        for ip in f:
            ip = ip.strip()
            if not ip:
                continue
            logging.info(f"IP 요청 시작: {ip}")
            try:
                res = requests.get(f"https://ipwho.is/{ip}", timeout=5)
                if res.status_code == 200:
                    info = res.json()
                    if not info.get("success", False):
                        logging.warning(f"요청 실패: {ip} → 응답 실패 플래그")
                        continue
                    parsed = {
                        "ip": info.get("ip"),
                        "continent": info.get("continent"),
                        "country": info.get("country"),
                        "region": info.get("region"),
                        "city": info.get("city"),
                        "latitude": info.get("latitude"),
                        "longitude": info.get("longitude"),
                        "org": info.get("connection", {}).get("org"),
                        "timezone": info.get("timezone", {}).get("id")
                    }
                    out.write(json.dumps(parsed) + "\n")
                    logging.info(f"응답 수신: {ip} → {parsed['country']}, {parsed['region']}, 좌표: ({parsed['latitude']}, {parsed['longitude']})")
                else:
                    logging.warning(f"요청 실패: {ip} → 상태 코드 {res.status_code}")
            except requests.RequestException as e:
                logging.warning(f"요청 예외 발생: {ip} → {e}")
            time.sleep(1)

    logging.info(f"위치 추적 완료: {output_file}")
