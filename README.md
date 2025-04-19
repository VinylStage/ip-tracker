# Nginx 로그 기반 IP 추적 및 통계(v0.1.0)

이 프로젝트는 Nginx 로그 파일에서 IP 주소를 추적하고, 위치 정보를 분석하여 통계 데이터를 생성하는 도구입니다. 이를 통해 네트워크 트래픽의 지리적 분포와 조직별 요청 수를 파악할 수 있습니다.

## 📑 목차

- [Nginx 로그 기반 IP 추적 및 통계(v0.1.0)](#nginx-로그-기반-ip-추적-및-통계v010)
  - [📑 목차](#-목차)
  - [⚙️ 동작 프로세스](#️-동작-프로세스)
  - [🧪 사용법](#-사용법)
  - [🗂 생성되는 파일 목록](#-생성되는-파일-목록)
  - [📊 분석 결과 예시](#-분석-결과-예시)

---

## ⚙️ 동작 프로세스

1. 로그에서 IP 추출

    - `extract_ips_from_log.py`

2. 중복 IP주소 제거 및 분리기록

    - `deduplicate_ip_list.py`

3. `ipwho.is`에 요청하여 정보 추출

    - `trace_ip_locations.py`

4. 기록된 정보를 토대로 `stats_summary.csv`에 통계 기록

   - `analyze_and_output_stats.py`
   - 국가, 지역, 조직, 대륙별 요청수 순위 통계

---

## 🧪 사용법

1. 가상환경 설정

```bash
python3 -m venv venv
```

or

```bash
poetry shell
```

2. 기본 패키지 설치

이 프로젝트에서는 `poetry`를 사용하는 것이 권장됩니다. 하지만 `pip`도 지원됩니다.

- `poetry`를 사용하는 경우:

```bash
pip install -r requirements.txt
```

or

```bash
poetry install
```

3. 로그파일 준비

```bash
mkdir -p data
```

- `data` 디렉토리 하위에 `raw_log.json` 이름으로 엔진엑스 컨테이너 로그 저장 (JSON Lines 형식으로 저장)

- `data` 디렉토리 하위에 `raw_log.json` 이름으로 엔진엑스 컨테이너 로그 저장
- 현재로써는 도커 컨테이너에서 추출한 엔진엑스 컨테이너의 raw 로그만 취급

>예시

```json
{"log":"2025/04/10 07:43:36 [notice] 1#1: start worker process 9\n","stream":"stderr","time":"2025-04-10T07:43:36.00728926Z"}
{"log":"175.209.248.172 - - [10/Apr/2025:07:46:30 +0000] \"GET /docs HTTP/1.1\" 200 938 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0\" \"-\"\n","stream":"stdout","time":"2025-04-10T07:46:30.630969002Z"}
# ↑ 여기서 IP "175.209.248.172" 이 추출됩니다
```

4. 프로그램 실행

- windows 혹은 기타 alias 설정된 환경

```bash
python main.py
```

- unix 환경

```bash
python3 main.py
```

---

## 🗂 생성되는 파일 목록

- `data/ip_list.txt`: 로그에서 추출된 IP 리스트 (중복 포함, 중간 출력 파일로 최종 중복 제거된 목록은 아님). 이 파일은 추출된 모든 IP 주소를 포함합니다.
- `data/ip_list.txt.dedup`: 중복 제거된 고유 IP 목록. 분석에 사용될 고유 IP 주소만 포함합니다.
- `data/ip_info.jsonl`: 각 IP에 대한 위치 정보 (JSON Lines 형식). IP 주소별로 위치 데이터를 저장합니다.
- `data/stats_summary.txt`: 사람이 읽기 쉬운 통계 요약. 주요 통계 데이터를 텍스트 형식으로 제공합니다.
- `data/stats_summary.csv`: 정렬 및 시각화에 용이한 통계 테이블 (CSV 포맷). 통계 데이터를 테이블 형식으로 저장하여 분석 및 시각화에 적합합니다.

---

## 📊 분석 결과 예시

`data/stats_summary.csv` 예시:

```Plain Text
category,value,count
country,KR,127
region,Seoul,58
continent,Asia,180
org,SK Broadband,76
```
