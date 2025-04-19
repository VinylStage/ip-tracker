from extract_ip import extract_ips_from_log
from deduplicate_ip import deduplicate_ip_list
from trace_location import trace_ip_locations
from analyze_stats import analyze_and_output_stats
from config import setup_logging
import logging
import csv

setup_logging()


# 실행 흐름
logging.info("Version 0.1.0")

logging.info("프로그램 시작")

extract_ips_from_log("data/raw_log.json", "data/ip_list.txt")

deduplicate_ip_list("data/ip_list.txt")

trace_ip_locations("data/ip_list.txt.dedup", "data/ip_info.jsonl")

analyze_and_output_stats("data/ip_list.txt", "data/ip_info.jsonl", "data/stats_summary.txt")

logging.info("프로그램 종료")
