# Smart Subway Boarding Guide

> "뛰지 않아도 되는 안심 탑승 안내"

NFC 결제 시점과 BLE 비콘 기반 승강장 도착 시간 측정 시스템을 통해, 개찰구 통과 즉시 사용자에게 탑승 가능한 열차 정보를 실시간으로 제공합니다.

## 기술 스택

| 구분 | 기술 |
|------|------|
| Mobile App | Flutter (Dart) |
| Backend | Python (FastAPI) |
| Database | PostgreSQL + Redis |
| Infrastructure | Docker |

## 프로젝트 구조

```
smart-subway-guide/
├── apps/
│   ├── mobile/          # Flutter 앱
│   └── backend/         # FastAPI 백엔드
├── infrastructure/
│   └── docker/          # Docker 설정
├── docs/                # 문서
└── shared/              # 공유 리소스
```

## 시작하기

### 사전 요구사항

- Flutter 3.16+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### 로컬 개발 환경 설정

```bash
# 1. 저장소 클론
git clone <repository-url>
cd smart-subway-guide

# 2. Docker 컨테이너 실행 (DB, Redis)
docker-compose up -d

# 3. 백엔드 실행
cd apps/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Flutter 앱 실행
cd apps/mobile
flutter pub get
flutter run
```

## 문서

- [PRD (Product Requirements Document)](../Guide.md)
- [API 문서](docs/api/)
- [아키텍처 문서](docs/architecture/)

## 라이선스

Private - All rights reserved
