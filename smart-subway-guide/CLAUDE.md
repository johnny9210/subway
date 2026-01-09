# Smart Subway Boarding Guide - Claude Code Instructions

> "뛰지 않아도 되는 안심 탑승 안내" - NFC 결제 시점 기반 실시간 탑승 안내 시스템

## Project Structure

```
smart-subway-guide/
├── apps/
│   ├── mobile/          # Flutter 앱 (Dart)
│   └── backend/         # FastAPI 백엔드 (Python)
├── infrastructure/      # Docker 설정
├── docs/               # 문서
└── shared/             # 공유 리소스
```

---

## Bash Commands

### Backend (Python/FastAPI)

```bash
# 가상환경 활성화 (IMPORTANT: 항상 먼저 실행)
cd apps/backend && source .venv/bin/activate

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 테스트 실행
pytest

# 테스트 + 커버리지
pytest --cov=app --cov-report=term-missing

# 린트 체크
ruff check app/

# 린트 자동 수정
ruff check app/ --fix

# 타입 체크
mypy app/

# 의존성 설치
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Mobile (Flutter/Dart)

```bash
# 의존성 설치
cd apps/mobile && flutter pub get

# 코드 생성 (freezed, riverpod 등)
flutter pub run build_runner build --delete-conflicting-outputs

# 앱 실행
flutter run

# 테스트 실행
flutter test

# 분석 (lint)
flutter analyze

# 빌드 (릴리즈)
flutter build apk --release
flutter build ios --release
```

### Docker

```bash
# 컨테이너 실행 (PostgreSQL, Redis)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 컨테이너 중지
docker-compose down
```

---

## Code Style

### Python (Backend)

- Python 3.11+ 필수
- ruff 린터 사용 (pyproject.toml 참조)
- 100자 라인 제한
- isort로 import 정렬 (first-party: `app`)
- mypy strict 타입 체크
- async/await 패턴 사용 (FastAPI)
- Pydantic 모델로 데이터 검증

```python
# Good: 타입 힌트 + async
async def get_travel_time(station_id: str) -> TravelTimeResponse:
    ...

# Bad: 타입 힌트 없음
def get_travel_time(station_id):
    ...
```

### Flutter (Mobile)

- Dart 3.2+ / Flutter 3.16+
- Riverpod 상태 관리 사용
- freezed로 불변 모델 생성
- 기능별 폴더 구조 (features/)

```dart
// Good: Riverpod + freezed 패턴
@freezed
class Station with _$Station {
  const factory Station({
    required String id,
    required String name,
  }) = _Station;
}

// UI에서는 ref.watch() 사용
final stations = ref.watch(stationsProvider);
```

---

## Core Files

### Backend
- `app/main.py` - FastAPI 앱 진입점
- `app/config.py` - 환경 설정
- `app/api/v1/router.py` - API 라우터
- `app/domain/stations/` - 역 관련 비즈니스 로직
- `app/infrastructure/` - DB, 캐시, 외부 API 연동

### Mobile
- `lib/main.dart` - 앱 진입점
- `lib/app/app.dart` - MaterialApp 설정
- `lib/app/routes.dart` - 라우팅
- `lib/features/` - 기능별 모듈
- `lib/features/boarding/` - 탑승 안내 핵심 기능

---

## Testing

### Backend 테스트

```bash
# 전체 테스트
pytest

# 특정 파일 테스트
pytest tests/test_stations.py

# 특정 테스트만
pytest tests/test_stations.py::test_get_nearby_stations -v

# 커버리지 리포트
pytest --cov=app --cov-report=html
```

- `tests/conftest.py`에 공통 fixtures 정의
- async 테스트는 `@pytest.mark.asyncio` 사용
- httpx.AsyncClient로 API 테스트

### Mobile 테스트

```bash
# 전체 테스트
flutter test

# 특정 파일
flutter test test/features/boarding_test.dart

# 커버리지
flutter test --coverage
```

- mocktail 사용하여 mock 생성
- Widget 테스트는 `testWidgets()` 사용

---

## API Endpoints

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/v1/health` | 서버 상태 확인 |
| POST | `/api/v1/auth/token` | JWT 토큰 발급 |
| GET | `/api/v1/stations/{id}/travel-time` | 평균 소요시간 조회 |
| GET | `/api/v1/stations/{id}/arrivals` | 실시간 열차 도착 정보 |
| GET | `/api/v1/stations/nearby` | 주변 역 검색 (GPS) |
| POST | `/api/v1/travel-logs` | 소요시간 데이터 업로드 |

API 문서: http://localhost:8000/docs (Swagger UI)

---

## Environment Variables

Backend `.env` 파일 필수 (`.env.example` 참조):

```bash
# 필수
KAKAO_REST_API_KEY=<카카오 API 키>
DATABASE_URL=postgresql://user:pass@localhost:5432/subway
REDIS_URL=redis://localhost:6379

# 선택
SECRET_KEY=<JWT 시크릿>
DEBUG=true
```

IMPORTANT: `.env` 파일은 절대 커밋하지 마세요!

---

## Git Workflow

### Branch Naming

```
feature/기능명     # 새 기능
fix/버그명        # 버그 수정
refactor/대상    # 리팩토링
docs/문서명       # 문서 수정
```

### Commit Message

```
feat: 주변역 검색 API 추가
fix: NFC 태그 인식 오류 수정
refactor: 상태 관리 로직 개선
docs: API 문서 업데이트
```

### Workflow

1. `main` 브랜치에서 feature 브랜치 생성
2. 작업 완료 후 PR 생성
3. 코드 리뷰 후 squash merge
4. feature 브랜치 삭제

---

## Known Issues & Warnings

### iOS NFC 제한
- iOS는 앱이 실행 중일 때만 NFC 감지 가능 (백그라운드 불가)
- `Info.plist`에 NFCReaderUsageDescription 필수

### BLE 비콘
- Android 12+ 에서 BLUETOOTH_SCAN, BLUETOOTH_CONNECT 권한 필요
- 비콘 스캔은 배터리 소모가 큼 - 지오펜싱과 함께 사용 권장

### 공공 API
- 일일 호출 제한 있음 - 반드시 캐싱 사용
- 공공 API 응답 지연 시 캐시 폴백 적용됨

### 한글 인코딩
- 역 이름 등 한글 데이터 처리 시 UTF-8 인코딩 확인

---

## Development Tips

1. **typecheck 먼저**: 코드 변경 후 항상 `ruff check` + `mypy` 실행
2. **테스트 단위 실행**: 전체 테스트보다 단일 테스트 파일로 빠른 피드백
3. **API 문서 확인**: `/docs` 엔드포인트에서 Swagger UI로 API 테스트
4. **build_runner**: Flutter 모델 변경 시 `build_runner` 재실행 필요
5. **환경 분리**: 개발/스테이징/프로덕션 환경별 `.env` 파일 관리

---

## References

- [PRD 문서](../Guide.md) - 상세 요구사항
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Flutter 공식 문서](https://docs.flutter.dev/)
- [Riverpod 문서](https://riverpod.dev/)
