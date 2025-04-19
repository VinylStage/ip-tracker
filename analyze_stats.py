from config import setup_logging
setup_logging()

import logging
import json
from collections import Counter
import csv

def analyze_and_output_stats(ip_list_path: str, info_path: str, output_file: str):
    logging.info(f"통계 분석 시작: {ip_list_path} + {info_path}")

    ip_counter = Counter()
    with open(ip_list_path, 'r') as f:
        for line in f:
            ip = line.strip()
            if ip:
                ip_counter[ip] += 1

    ip_info_map = {}
    with open(info_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                ip_info_map[data["ip"]] = data
            except json.JSONDecodeError:
                logging.warning("IP 정보 파싱 오류 발생")
                continue

    countries = Counter()
    regions = Counter()
    orgs = Counter()
    continents = Counter()

    for ip, count in ip_counter.items():
        info = ip_info_map.get(ip)
        if not info:
            continue
        countries[info.get("country", "Unknown")] += count
        regions[info.get("region", "Unknown")] += count
        orgs[info.get("org", "Unknown")] += count
        continents[info.get("continent", "Unknown")] += count

    with open(output_file, 'w') as out:
        out.write("Top 10 IPs:\n")
        for ip, count in ip_counter.most_common(10):
            out.write(f"{ip}: {count} times\n")
        logging.info("Top 10 IP 통계 작성 완료")

        out.write("\nCountry Stats:\n")
        for country, count in countries.most_common():
            out.write(f"{country}: {count}\n")
        logging.info("국가별 통계 작성 완료")

        out.write("\nRegion Stats:\n")
        for region, count in regions.most_common():
            out.write(f"{region}: {count}\n")
        logging.info("지역별 통계 작성 완료")

        out.write("\nOrg Stats:\n")
        for org, count in orgs.most_common():
            out.write(f"{org}: {count}\n")
        logging.info("조직별 통계 작성 완료")

        out.write("\nContinent Stats:\n")
        for cont, count in continents.most_common():
            out.write(f"{cont}: {count}\n")
        logging.info("대륙별 통계 작성 완료")

    with open("data/stats_summary.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["type", "value", "count"])

        for country, count in countries.most_common():
            writer.writerow(["country", country, count])
        for region, count in regions.most_common():
            writer.writerow(["region", region, count])
        for org, count in orgs.most_common():
            writer.writerow(["org", org, count])
        for continent, count in continents.most_common():
            writer.writerow(["continent", continent, count])

    logging.info("CSV 통계 파일 저장 완료: data/stats_summary.csv")
    logging.info(f"통계 분석 완료: {output_file}")
