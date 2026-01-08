# Product Requirements Document (PRD)
## Smart Subway Boarding Guide System

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.1 |
| 작성일 | 2026년 1월 |
| 기술 스택 | Frontend: Flutter / Backend: Python (FastAPI) |
| 상태 | Draft |
| 변경 이력 | v1.1 - 보안/에러처리/테스트 전략 추가 |

---

## 1. 목적 및 배경

### 1.1 문제 정의

현재 지하철 이용 시 승객들은 개찰구 통과 후 승강장까지의 이동 시간과 열차 도착 시간을 직관적으로 파악하기 어렵습니다. 이로 인해 다음과 같은 문제가 발생합니다:

- 열차를 놓치지 않기 위해 불필요하게 뛰어가는 승객들로 인한 안전사고 위험
- 탑승 가능 여부를 판단할 수 없어 발생하는 심리적 스트레스
- 혼잡한 시간대 승강장 내 밀집 현상 가중

### 1.2 솔루션 개요

NFC 결제 시점과 BLE 비콘 기반 승강장 도착 시간 측정 시스템을 통해, 개찰구 통과 즉시 사용자에게 탑승 가능한 열차 정보를 실시간으로 제공합니다.

> **핵심 가치: "뛰지 않아도 되는 안심 탑승 안내"**

### 1.3 기대 효과

- 역 내 안전사고 감소 (뛰어가는 승객 감소)
- 사용자 스트레스 감소 및 이동 편의성 향상
- 빅데이터 기반 역별 이동 패턴 분석 인사이트 확보
- 스마트 시티 교통 인프라 데이터 기반 마련

---

## 2. 타겟 사용자

### 2.1 Primary Users

| 사용자 그룹 | 특성 | Pain Point |
|-------------|------|------------|
| 출퇴근 직장인 | 매일 정해진 시간에 지하철 이용, 시간 민감도 높음 | 출근 시간 열차 놓칠까 봐 항상 뛰어감 |
| 학생 | 등하교 시 지하철 이용, 스마트폰 활용도 높음 | 수업 시간에 맞춰 도착해야 하는 압박감 |
| 일반 시민 | 비정기적 지하철 이용, 역 구조 미숙지 | 낯선 역에서 승강장까지 시간 예측 불가 |

### 2.2 Secondary Users

- **교통 당국**: 역별 혼잡도 및 이동 패턴 데이터 활용
- **역 운영 관리자**: 실시간 승객 흐름 모니터링
- **도시 계획가**: 스마트 시티 교통 데이터 분석

---

## 3. 기능 요구사항 (Functional Requirements)

### 3.1 소요시간 측정 시스템

#### FR-001: NFC 결제 시점 기록
- 사용자가 개찰구 NFC 리더에 스마트폰 태그 시 결제 완료 타임스탬프(T_NFC) 자동 기록
- 역 ID 및 개찰구 위치 정보 함께 저장
- Android: NFC Intent Filter를 통한 앱 자동 실행
- iOS: 앱 실행 상태에서 NFC 이벤트 감지

#### FR-002: BLE 비콘 기반 승강장 진입 감지
- 승강장 진입 직전 또는 승강장 내 설치된 BLE 비콘 신호 감지
- 비콘 감지 시점 타임스탬프(T_Beacon) 기록
- 비콘 UUID/Major/Minor를 통한 역·승강장·방향 식별

#### FR-003: 이동 소요시간 계산 및 전송
- Δt = T_Beacon - T_NFC 계산
- 역 ID, 시간대, 요일 정보와 함께 서버 전송
- 전송 완료 후 백그라운드 앱 실행 정지 (배터리 최적화)

### 3.2 열차 정보 연동

#### FR-004: 실시간 열차 도착 정보 조회
- 공공 데이터 포털 API 연동 (도시철도 실시간 도착 정보 조회 서비스)
- 현재 역 기준 상행/하행(내선/외선) 양방향 열차 정보 조회
- 환승역의 경우 모든 호선의 승강장 정보 표시
- 열차 번호, 현재 위치, 도착 예정 시간, 종착역 정보 제공

### 3.3 사용자 인터페이스

#### FR-005: 탑승 안내 화면 표시
- NFC 태그 직후 자동 화면 표시
- 승강장까지 예상 소요시간 표시 (평균 + 혼잡도 보정)
- 탑승 가능/불가능 열차 구분 표시
- 여유 시간 계산 표시 (도착 예정 시간 - 소요 시간)
- 안내 메시지 제공 (예: "뛰지 마세요! 다다음 열차를 여유있게 탑승하세요")

#### FR-006: 방향/호선 선택
- 사용자 이동 방향 선택 UI 제공
- 환승역에서 호선별 승강장 선택 기능
- 자주 이용하는 방향 자동 학습 및 추천

---

## 4. 비기능 요구사항 (Non-Functional Requirements)

### 4.1 성능 요구사항

| ID | 구분 | 요구사항 | 상세 기준 |
|----|------|----------|-----------|
| NFR-001 | 성능 | 응답 속도 | NFC 태그 후 화면 표시까지 2초 이내 |
| NFR-002 | 성능 | API 응답 시간 | 열차 도착 정보 API 호출 후 500ms 이내 응답 |
| NFR-003 | 효율성 | 배터리 효율 | 비콘 스캔으로 인한 배터리 소모 시간당 1% 이하, 데이터 전송 완료 후 백그라운드 정지 |
| NFR-004 | 확장성 | 동시 사용자 | 피크 시간대 역당 1,000명 동시 요청 처리 |
| NFR-005 | 정확성 | 데이터 정확도 | 소요시간 예측 정확도 90% 이상 (±30초 오차 범위) |
| NFR-006 | 안정성 | 가용성 | 서버 가용성 99.9% (월간 다운타임 43분 이내) |
| NFR-007 | 호환성 | 플랫폼 호환성 | Android 8.0+, iOS 13.0+ 지원 |
| NFR-008 | 확장성 | 시스템 확장성 | 수도권 전체 역(약 700개) 확장 가능한 아키텍처 |
| NFR-009 | 접근성 | 접근성 | WCAG 2.1 AA 기준 준수, 고대비 모드/음성 안내 지원 |

### 4.2 보안 요구사항 (상세)

| ID | 구분 | 요구사항 | 상세 기준 |
|----|------|----------|-----------|
| SEC-001 | 통신 보안 | TLS 암호화 | 모든 API 통신 TLS 1.3 적용, 인증서 피닝 구현 |
| SEC-002 | 데이터 암호화 | 저장 데이터 암호화 | AES-256-GCM 방식, 민감 데이터 암호화 저장 |
| SEC-003 | 인증 | API 인증 | JWT 기반 인증, Access Token 유효기간 1시간, Refresh Token 7일 |
| SEC-004 | 인가 | 권한 관리 | RBAC 기반 권한 관리, 최소 권한 원칙 적용 |
| SEC-005 | 익명화 | 개인정보 익명화 | SHA-256 해싱 + 솔트, k-익명성(k≥5) 적용 |
| SEC-006 | 데이터 보관 | 보관 기간 정책 | 이동 로그 90일 보관 후 자동 삭제, 통계 데이터는 익명화 후 영구 보관 |
| SEC-007 | 개인정보 | 개인정보보호법 준수 | 위치정보법, GDPR 원칙 준수, 개인정보 처리방침 명시 |
| SEC-008 | 감사 | 보안 감사 로그 | 모든 인증 시도, 민감 데이터 접근 로그 기록, 1년 보관 |

#### 4.2.1 인증/인가 상세

```
인증 플로우:
1. 앱 최초 실행 → 디바이스 ID 기반 익명 사용자 생성
2. JWT Access Token 발급 (유효기간: 1시간)
3. Refresh Token으로 자동 갱신 (유효기간: 7일)
4. 토큰 만료 시 재인증 (디바이스 ID 기반)

토큰 구조:
- Access Token: { device_id_hash, issued_at, expires_at, scope }
- Refresh Token: { device_id_hash, issued_at, expires_at }
```

#### 4.2.2 데이터 익명화 정책

| 데이터 유형 | 익명화 방법 | 보관 기간 |
|-------------|-------------|-----------|
| 디바이스 ID | SHA-256 + 고정 솔트 | 영구 (해시값만) |
| 이동 로그 (T_NFC, T_Beacon) | k-익명성 적용, 시간 라운딩(5분 단위) | 90일 |
| 역별 통계 데이터 | 집계 데이터만 저장, 개인 식별 불가 | 영구 |
| 사용자 선호도 | 로컬 저장 (서버 미전송) | 앱 삭제 시 |

---

## 5. 에러 처리 시나리오

### 5.1 클라이언트 에러 처리

| ID | 에러 상황 | 감지 방법 | 사용자 화면 | 복구 방안 |
|----|-----------|-----------|-------------|-----------|
| ERR-001 | NFC 인식 실패 | NFC 타임아웃 (3초) | "NFC를 다시 태그해주세요" + 재시도 버튼 | 수동 역 선택 UI 제공 |
| ERR-002 | BLE 비콘 미감지 | 비콘 스캔 실패 (30초) | 무음 처리, 데이터 수집 스킵 | 다음 이용 시 재시도 |
| ERR-003 | 네트워크 오프라인 | 연결 상태 모니터링 | "오프라인 모드" 배지 표시 | 캐시된 평균 소요시간 표시 |
| ERR-004 | GPS/위치 권한 거부 | 권한 상태 확인 | "위치 권한 필요" 안내 | 권한 요청 다이얼로그 |
| ERR-005 | 블루투스 비활성화 | BT 상태 모니터링 | "블루투스를 켜주세요" 안내 | 시스템 설정 바로가기 |

### 5.2 서버 에러 처리

| ID | 에러 상황 | HTTP 코드 | 클라이언트 동작 | 복구 방안 |
|----|-----------|-----------|-----------------|-----------|
| ERR-101 | 서버 내부 오류 | 500 | 캐시 데이터 표시 + 재시도 | 지수 백오프 재시도 (최대 3회) |
| ERR-102 | 서비스 과부하 | 503 | "잠시 후 다시 시도" 안내 | 30초 후 자동 재시도 |
| ERR-103 | 인증 만료 | 401 | 자동 토큰 갱신 시도 | Refresh Token으로 재발급 |
| ERR-104 | 잘못된 요청 | 400 | 에러 로깅 (Sentry) | 앱 업데이트 안내 |
| ERR-105 | 역 정보 없음 | 404 | "지원되지 않는 역입니다" | 지원 역 목록 표시 |

### 5.3 외부 API 에러 처리

| ID | 에러 상황 | 감지 방법 | 폴백 전략 | 사용자 안내 |
|----|-----------|-----------|-----------|-------------|
| ERR-201 | 공공 API 응답 지연 | 타임아웃 (3초) | 마지막 캐시 데이터 사용 | "열차 정보 업데이트 중" |
| ERR-202 | 공공 API 장애 | 연속 3회 실패 | 캐시 + "정보 지연" 표시 | "실시간 정보 일시 중단" |
| ERR-203 | API 쿼터 초과 | 429 응답 | 캐시 전용 모드 전환 | 무음 처리 (사용자 영향 최소화) |
| ERR-204 | API 응답 파싱 실패 | JSON 파싱 에러 | 이전 유효 데이터 사용 | 무음 처리 + 로깅 |

### 5.4 오프라인 모드 동작

```
오프라인 모드 진입 조건:
- 네트워크 연결 불가 3초 이상
- 서버 응답 실패 3회 연속

오프라인 모드 기능:
1. 로컬 캐시된 평균 소요시간 표시 (캐시 시점 명시)
2. "오프라인 모드" 배지 상단 표시
3. 열차 실시간 정보 숨김 처리
4. 5초마다 네트워크 상태 확인
5. 연결 복구 시 자동 데이터 갱신

로컬 캐시 데이터:
- 최근 방문 10개역 평균 소요시간
- 마지막 조회 열차 시간표 (정적 데이터)
- 사용자 선호 방향 설정
```

---

## 6. 사용자 시나리오 (User Scenarios)

### 6.1 시나리오 1: 출근길 직장인

**페르소나**: 김민수 (32세, 판교 IT 기업 근무)
**상황**: 강남역에서 2호선 내선순환 탑승 예정
**시간**: 평일 오전 8시 30분 (출근 피크 시간)

#### Flow
1. 김민수가 강남역 개찰구에서 스마트폰 NFC로 결제
2. 앱이 자동 실행되며 T_NFC 기록
3. 화면에 즉시 표시: "2호선 내선순환 승강장까지 약 3분 20초"
4. 열차 정보 표시:
   - 다음 열차 1분 후 도착 (❌ 탑승 불가)
   - 다다음 열차 6분 후 도착 (✅ 2분 40초 여유)
5. 안내 메시지: **"뛰지 마세요! 다다음 열차를 여유있게 탑승하실 수 있습니다."**
6. 김민수는 걸어서 이동, 비콘 감지 후 Δt 데이터 서버 전송
7. 앱 백그라운드 정지

### 6.2 시나리오 2: 환승역 이용자

**페르소나**: 이지은 (25세, 대학원생)
**상황**: 신도림역에서 1호선 → 2호선 환승
**시간**: 평일 오후 2시 (비피크 시간)

#### Flow
1. 이지은이 신도림역에서 1호선 하차 후 2호선 환승 게이트 통과
2. 앱이 환승임을 인식, 2호선 양방향 승강장 정보 동시 표시
3. 화면: "신도림-외선 승강장 2분 10초 / 신도림-내선 승강장 2분 30초"
4. 이지은이 "외선순환" 선택
5. 해당 방향 열차 도착 정보 및 탑승 가능 여부 표시

### 6.3 시나리오 3: 처음 방문하는 역

**페르소나**: 박영호 (45세, 지방 출장 중인 영업사원)
**상황**: 처음 방문하는 여의도역에서 5호선 탑승
**특이사항**: 역 구조 미숙지, 시간 압박 있음

#### Flow
1. 박영호가 여의도역 개찰구 통과
2. 앱이 처음 방문 역임을 인식 (개인 이력 기반)
3. 해당 역의 평균 소요시간 데이터 기반 안내 (개인 데이터 없으므로)
4. "여의도역 5호선 승강장까지 평균 4분 소요" 표시
5. 방문 후 Δt 데이터 축적, 다음 방문 시 더 정확한 예측 제공

### 6.4 시나리오 4: 에러 상황 (네트워크 오프라인)

**페르소나**: 최수진 (28세, 프리랜서)
**상황**: 지하 심층부 역에서 네트워크 불안정
**특이사항**: 오프라인 상태

#### Flow
1. 최수진이 개찰구 NFC 태그 성공
2. 앱 실행되나 네트워크 연결 실패 감지
3. 화면 상단 "오프라인 모드" 배지 표시
4. 캐시된 평균 소요시간 표시: "약 2분 30초 (캐시 데이터)"
5. 열차 정보 영역: "실시간 정보를 불러올 수 없습니다"
6. 네트워크 복구 시 자동 갱신, 배지 제거

---

## 7. 성공 지표 (Success Metrics)

### 7.1 핵심 지표 (Key Metrics)

| ID | 지표 | 목표 | 측정 방법 |
|----|------|------|-----------|
| KPI-001 | 예측 정확도 | 90% 이상 | 실제 소요시간 vs 예측 비교 |
| KPI-002 | 일간 활성 사용자 (DAU) | 출시 6개월 후 10만 명 | 앱 분석 도구 |
| KPI-003 | 사용자 만족도 (NPS) | 40 이상 | 인앱 설문조사 |
| KPI-004 | 앱 실행률 | NFC 태그 시 80% 이상 자동 실행 | 이벤트 로그 분석 |
| KPI-005 | 데이터 수집량 | 역당 일 1,000건 이상 | 서버 로그 분석 |

### 7.2 보조 지표

- 앱 스토어 평점: 4.5점 이상 유지
- 이탈률: 앱 설치 후 1개월 내 삭제율 20% 이하
- 평균 세션 시간: 30초 이내 (빠른 정보 전달 목표)
- 역 내 안전사고 감소율: 파트너십 역 대상 전년 대비 15% 감소

### 7.3 기술 지표

| ID | 지표 | 목표 | 알림 임계값 |
|----|------|------|-------------|
| TECH-001 | API 응답 시간 (p95) | 500ms 이내 | > 800ms |
| TECH-002 | 에러율 | 0.1% 이하 | > 0.5% |
| TECH-003 | 서버 가용성 | 99.9% | < 99.5% |
| TECH-004 | 캐시 히트율 | 80% 이상 | < 60% |
| TECH-005 | 공공 API 성공률 | 99% 이상 | < 95% |

---

## 8. 우선순위 (Priority)

### 8.1 Must-Have (MVP) - P0

| 기능 | 비고 |
|------|------|
| NFC 태그 인식 및 앱 자동 실행 (Android) | 핵심 트리거 기능 |
| 실시간 열차 도착 정보 API 연동 | 공공 데이터 포털 API 활용 |
| 기본 탑승 안내 화면 UI | 소요시간 + 열차정보 표시 |
| 서버 평균 소요시간 데이터 제공 (초기값) | 사전 측정 데이터 기반 |
| 기본 에러 처리 (오프라인 모드) | 사용자 경험 보장 |
| JWT 인증 시스템 | 보안 기본 요소 |

### 8.2 Should-Have - P1

| 기능 | 비고 |
|------|------|
| BLE 비콘 기반 소요시간 측정 및 수집 | 정확도 향상을 위한 크라우드소싱 |
| 시간대/요일별 소요시간 분석 및 적용 | 피크/비피크 구분 |
| 환승역 다중 호선 지원 | 복합 환승역 대응 |
| iOS NFC 지원 (앱 실행 상태) | iOS 플랫폼 확장 |
| 상세 에러 처리 및 복구 로직 | 사용자 경험 개선 |
| 데이터 익명화 고도화 | k-익명성 적용 |

### 8.3 Nice-to-Have - P2

| 기능 | 비고 |
|------|------|
| 자주 가는 방향 자동 학습 및 추천 | 개인화 기능 |
| 혼잡도 보정 알고리즘 | 실시간 혼잡도 반영 |
| Apple Watch / Galaxy Watch 연동 | 웨어러블 확장 |
| 음성 안내 기능 | 접근성 강화 |
| 위젯 지원 (홈 화면) | 빠른 접근성 |

---

## 9. 제약사항 (Constraints)

### 9.1 기술적 제약

| ID | 제약사항 | 대응 방안 |
|----|----------|-----------|
| TC-001 | iOS 백그라운드 NFC 감지 불가 | 앱 실행 상태에서만 NFC 지원, 위젯/알림 활용 유도 |
| TC-002 | BLE 비콘 신호 콘크리트 감쇠 | 구역별 다중 비콘 설치, RSSI 기반 위치 보정 |
| TC-003 | 블루투스 스캔 배터리 소모 | 지오펜싱 기반 스캔 활성화, 데이터 전송 후 즉시 정지 |
| TC-004 | 공공 API 호출 제한 (일일 쿼터) | 캐싱 전략, 실시간 갱신 주기 최적화 (30초) |
| TC-005 | 다양한 스마트폰 NFC 성능 차이 | 주요 기종 대상 QA 테스트, 폴백 UI 제공 |

### 9.2 비즈니스 제약

| ID | 제약사항 | 대응 방안 |
|----|----------|-----------|
| BC-001 | 비콘 설치 시 역 관리 기관 협조 필요 | 서울교통공사, 코레일 등과 사전 MOU 체결 |
| BC-002 | 초기 데이터 부족 (Cold Start) | 사전 측정 데이터 수집, 베타 테스터 운영 |
| BC-003 | 개인정보보호법 준수 | 위치정보 익명화, 동의 절차 명확화, 법률 검토 |
| BC-004 | 기존 교통 앱과의 경쟁 | 차별화된 UX(자동 실행), 기존 앱 연동 API 제공 |

### 9.3 권한 요구사항

| 권한 | 용도 | 필수 여부 |
|------|------|-----------|
| 위치 (Fine Location) | BLE 비콘 스캔을 위한 권한 | 필수 (Android 12+) |
| 블루투스 | BLE 비콘 신호 감지 | 필수 |
| NFC | 개찰구 결제 태그 인식 | 필수 |
| 인터넷 | API 호출 및 데이터 전송 | 필수 |
| 백그라운드 실행 | 비콘 감지 및 데이터 전송 | 선택 (데이터 수집 참여 시) |

---

## 10. 기술 아키텍처 개요

### 10.1 시스템 구성

본 시스템은 모바일 클라이언트(Flutter), 백엔드 서버(Python/FastAPI), 외부 API 연동으로 구성됩니다.

| 계층 | 기술 스택 | 주요 역할 |
|------|-----------|-----------|
| Frontend | Flutter (Dart) | iOS/Android 크로스 플랫폼 앱, NFC/BLE 처리, UI 렌더링 |
| Backend | Python (FastAPI) | REST API 서버, 비즈니스 로직, 데이터 처리 |
| Database | PostgreSQL + Redis | 소요시간 데이터 저장, 캐싱 |
| External API | 공공 데이터 포털 | 실시간 열차 도착 정보 조회 |
| Infrastructure | AWS / GCP | 클라우드 호스팅, Auto Scaling, 모니터링 |

### 10.2 데이터 흐름

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  NFC 태그   │────▶│   Flutter   │────▶│   FastAPI   │
│  (개찰구)   │     │     App     │     │   Server    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  BLE 비콘   │     │  공공 API   │
                    │   (승강장)  │     │ (열차 정보) │
                    └─────────────┘     └─────────────┘
```

1. 사용자가 개찰구 NFC 태그 → 앱이 T_NFC 기록 및 서버에 역 정보 전송
2. 서버가 해당 역/시간대 평균 소요시간 + 실시간 열차 정보 응답
3. 앱이 탑승 가능 열차 계산 및 화면 표시
4. 사용자가 승강장 도착 → 비콘 감지 → T_Beacon 기록
5. Δt 계산 후 서버 전송 → 평균 소요시간 갱신
6. 앱 백그라운드 정지

### 10.3 데이터베이스 스키마

#### 10.3.1 ERD 개요

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│     stations     │     │    platforms     │     │   travel_times   │
├──────────────────┤     ├──────────────────┤     ├──────────────────┤
│ station_id (PK)  │────<│ platform_id (PK) │────<│ id (PK)          │
│ station_name     │     │ station_id (FK)  │     │ station_id (FK)  │
│ line_id          │     │ direction        │     │ platform_id (FK) │
│ latitude         │     │ line_id          │     │ gate_id          │
│ longitude        │     │ beacon_uuid      │     │ travel_seconds   │
│ created_at       │     │ beacon_major     │     │ day_type         │
└──────────────────┘     │ beacon_minor     │     │ time_slot        │
                         └──────────────────┘     │ recorded_at      │
                                                  │ device_hash      │
┌──────────────────┐     ┌──────────────────┐     └──────────────────┘
│  travel_stats    │     │   api_cache      │
├──────────────────┤     ├──────────────────┤
│ id (PK)          │     │ cache_key (PK)   │
│ station_id (FK)  │     │ cache_value      │
│ platform_id (FK) │     │ expires_at       │
│ day_type         │     │ created_at       │
│ time_slot        │     └──────────────────┘
│ avg_seconds      │
│ std_deviation    │
│ sample_count     │
│ updated_at       │
└──────────────────┘
```

#### 10.3.2 테이블 상세

**stations (역 정보)**
```sql
CREATE TABLE stations (
    station_id VARCHAR(10) PRIMARY KEY,  -- 예: 'ST_0222' (2호선 강남)
    station_name VARCHAR(50) NOT NULL,
    line_id VARCHAR(10) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_transfer BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_stations_line ON stations(line_id);
```

**platforms (승강장 정보)**
```sql
CREATE TABLE platforms (
    platform_id VARCHAR(20) PRIMARY KEY,  -- 예: 'PL_0222_IN' (강남 내선)
    station_id VARCHAR(10) REFERENCES stations(station_id),
    direction VARCHAR(20) NOT NULL,       -- 'inbound', 'outbound'
    line_id VARCHAR(10) NOT NULL,
    beacon_uuid UUID NOT NULL,
    beacon_major INTEGER NOT NULL,
    beacon_minor INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_platforms_station ON platforms(station_id);
CREATE INDEX idx_platforms_beacon ON platforms(beacon_uuid, beacon_major, beacon_minor);
```

**travel_times (이동 시간 로그)**
```sql
CREATE TABLE travel_times (
    id BIGSERIAL PRIMARY KEY,
    station_id VARCHAR(10) REFERENCES stations(station_id),
    platform_id VARCHAR(20) REFERENCES platforms(platform_id),
    gate_id VARCHAR(20),                  -- 개찰구 식별자
    travel_seconds INTEGER NOT NULL,      -- 실제 소요 시간 (초)
    day_type VARCHAR(10) NOT NULL,        -- 'weekday', 'saturday', 'sunday'
    time_slot VARCHAR(5) NOT NULL,        -- 'HH:MM' 형식 (5분 단위 라운딩)
    device_hash VARCHAR(64) NOT NULL,     -- SHA-256 해시된 디바이스 ID
    recorded_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_travel_times_lookup ON travel_times(station_id, platform_id, day_type, time_slot);
CREATE INDEX idx_travel_times_recorded ON travel_times(recorded_at);

-- 90일 이후 자동 삭제를 위한 파티셔닝 또는 배치 작업 설정
```

**travel_stats (통계 집계)**
```sql
CREATE TABLE travel_stats (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(10) REFERENCES stations(station_id),
    platform_id VARCHAR(20) REFERENCES platforms(platform_id),
    day_type VARCHAR(10) NOT NULL,
    time_slot VARCHAR(5) NOT NULL,
    avg_seconds DECIMAL(6, 2) NOT NULL,
    std_deviation DECIMAL(6, 2),
    sample_count INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(station_id, platform_id, day_type, time_slot)
);
CREATE INDEX idx_travel_stats_lookup ON travel_stats(station_id, platform_id, day_type, time_slot);
```

### 10.4 캐싱 전략

#### 10.4.1 Redis 캐시 구조

| 캐시 키 패턴 | TTL | 용도 | 무효화 조건 |
|-------------|-----|------|-------------|
| `arrival:{station_id}:{direction}` | 30초 | 실시간 열차 도착 정보 | TTL 만료 |
| `travel_avg:{station_id}:{platform_id}:{day_type}:{time_slot}` | 1시간 | 평균 소요시간 | 통계 업데이트 시 |
| `station:{station_id}` | 24시간 | 역 기본 정보 | 수동 갱신 |
| `platforms:{station_id}` | 24시간 | 역별 승강장 목록 | 수동 갱신 |
| `api_quota:daily` | 자정까지 | 공공 API 쿼터 카운터 | 자정 리셋 |

#### 10.4.2 캐시 무효화 정책

```python
# 캐시 무효화 전략
class CacheInvalidation:
    # 1. TTL 기반 자동 만료
    ARRIVAL_TTL = 30          # 실시간 정보: 30초
    TRAVEL_AVG_TTL = 3600     # 평균 소요시간: 1시간
    STATION_INFO_TTL = 86400  # 역 정보: 24시간

    # 2. 이벤트 기반 무효화
    async def on_travel_log_created(station_id, platform_id):
        # 새 데이터 100건 누적 시 통계 재계산 및 캐시 갱신
        if await get_pending_count(station_id) >= 100:
            await recalculate_stats(station_id, platform_id)
            await invalidate_travel_cache(station_id, platform_id)

    # 3. 수동 갱신 (관리자)
    async def manual_refresh(station_id):
        await invalidate_all_station_cache(station_id)
```

#### 10.4.3 캐시 히트/미스 처리

```
Cache-Aside 패턴:
1. 캐시 조회 (Redis)
2. 히트 → 캐시 데이터 반환
3. 미스 → DB 조회 → 캐시 저장 → 데이터 반환

Write-Through 패턴 (통계 데이터):
1. travel_times 테이블 INSERT
2. 비동기로 travel_stats 갱신
3. 캐시 업데이트
```

### 10.5 Flutter 주요 패키지

| 패키지 | 용도 |
|--------|------|
| `nfc_manager` | NFC 태그 읽기/쓰기 |
| `flutter_blue_plus` | BLE 비콘 스캔 |
| `dio` | HTTP 클라이언트 |
| `provider` / `riverpod` | 상태 관리 |
| `workmanager` | 백그라운드 작업 스케줄링 |
| `hive` | 로컬 데이터 저장 |
| `flutter_secure_storage` | 토큰 안전 저장 |
| `connectivity_plus` | 네트워크 상태 모니터링 |

### 10.6 Backend API Endpoints

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| POST | `/api/v1/auth/token` | JWT 토큰 발급 | - |
| POST | `/api/v1/auth/refresh` | 토큰 갱신 | Refresh Token |
| GET | `/api/v1/stations/{station_id}/travel-time` | 역별 평균 소요시간 조회 | Access Token |
| GET | `/api/v1/stations/{station_id}/arrivals` | 실시간 열차 도착 정보 조회 | Access Token |
| POST | `/api/v1/travel-logs` | 소요시간 데이터 업로드 | Access Token |
| GET | `/api/v1/stations/{station_id}/platforms` | 역 승강장 정보 조회 | Access Token |
| GET | `/api/v1/health` | 서버 상태 확인 | - |

---

## 11. 테스트 전략

### 11.1 테스트 피라미드

```
           ┌─────────┐
           │  E2E    │  10% - 핵심 사용자 플로우
          ─┼─────────┼─
         ┌─┴─────────┴─┐
         │ Integration │  30% - API, DB 연동
        ─┼─────────────┼─
       ┌─┴─────────────┴─┐
       │      Unit       │  60% - 비즈니스 로직
       └─────────────────┘
```

### 11.2 단위 테스트 (Unit Tests)

| 영역 | 테스트 대상 | 커버리지 목표 |
|------|-------------|---------------|
| Flutter | 소요시간 계산 로직, 탑승 가능 여부 판정, 상태 관리 | 80% |
| FastAPI | API 엔드포인트, 비즈니스 로직, 유틸리티 함수 | 85% |
| 공통 | 데이터 변환, 유효성 검증, 에러 처리 | 90% |

**Flutter 단위 테스트 예시**
```dart
// 탑승 가능 여부 판정 테스트
void main() {
  group('BoardingAvailabilityCalculator', () {
    test('충분한 여유 시간이 있으면 탑승 가능', () {
      final calculator = BoardingAvailabilityCalculator();
      final result = calculator.canBoard(
        travelTimeSeconds: 180,  // 3분
        trainArrivalSeconds: 300, // 5분 후 도착
      );
      expect(result.isAvailable, true);
      expect(result.marginSeconds, 120);
    });

    test('여유 시간이 부족하면 탑승 불가', () {
      final result = calculator.canBoard(
        travelTimeSeconds: 180,  // 3분
        trainArrivalSeconds: 120, // 2분 후 도착
      );
      expect(result.isAvailable, false);
    });
  });
}
```

### 11.3 통합 테스트 (Integration Tests)

| 테스트 시나리오 | 검증 항목 |
|-----------------|-----------|
| API → DB 연동 | 소요시간 저장/조회, 통계 계산 |
| API → Redis 연동 | 캐시 저장/조회/만료 |
| API → 공공 API 연동 | 열차 정보 조회, 에러 핸들링 |
| 인증 플로우 | 토큰 발급/갱신/검증 |

**FastAPI 통합 테스트 예시**
```python
# tests/test_travel_time_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_travel_time_success(client: AsyncClient, auth_token: str):
    response = await client.get(
        "/api/v1/stations/ST_0222/travel-time",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"platform_id": "PL_0222_IN", "day_type": "weekday", "time_slot": "08:30"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "avg_seconds" in data
    assert data["avg_seconds"] > 0

@pytest.mark.asyncio
async def test_get_travel_time_cache_hit(client: AsyncClient, auth_token: str, redis_mock):
    # 첫 번째 요청: DB 조회
    response1 = await client.get(...)
    # 두 번째 요청: 캐시 히트
    response2 = await client.get(...)
    assert redis_mock.get_call_count() == 2
    assert redis_mock.db_query_count() == 1  # DB는 1회만 조회
```

### 11.4 E2E 테스트 (End-to-End Tests)

| 시나리오 | 테스트 내용 | 도구 |
|----------|-------------|------|
| 정상 플로우 | NFC 태그 → 화면 표시 → 데이터 전송 | Flutter Integration Test |
| 오프라인 모드 | 네트워크 차단 → 캐시 표시 | Flutter Integration Test |
| 에러 복구 | 서버 에러 → 재시도 → 성공 | Flutter Integration Test |
| 다중 플랫폼 | Android/iOS 동작 일관성 | Firebase Test Lab |

### 11.5 성능 테스트

| 테스트 유형 | 도구 | 목표 |
|-------------|------|------|
| 부하 테스트 | k6, Locust | 역당 1,000 RPS 처리 |
| 스트레스 테스트 | k6 | 피크 대비 150% 부하 견딤 |
| 지속성 테스트 | k6 | 24시간 안정 운영 |

**k6 부하 테스트 스크립트 예시**
```javascript
// load_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 500 },   // 램프업
    { duration: '5m', target: 1000 },  // 피크
    { duration: '2m', target: 0 },     // 램프다운
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% 요청이 500ms 이내
    http_req_failed: ['rate<0.01'],    // 에러율 1% 이하
  },
};

export default function () {
  const res = http.get('https://api.example.com/api/v1/stations/ST_0222/arrivals');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### 11.6 품질 게이트

| 게이트 | 기준 | 차단 조건 |
|--------|------|-----------|
| 코드 커버리지 | 단위 테스트 80% 이상 | 미달 시 PR 머지 차단 |
| 정적 분석 | Critical 이슈 0건 | 발견 시 빌드 실패 |
| 보안 스캔 | High 취약점 0건 | 발견 시 배포 차단 |
| 성능 회귀 | p95 응답시간 ±10% | 초과 시 알림 |

---

## 12. 모니터링 및 알림

### 12.1 모니터링 아키텍처

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Flutter    │────▶│  Sentry     │     │  Grafana    │
│  (에러 로깅) │     │  (에러 추적) │     │  (대시보드)  │
└─────────────┘     └─────────────┘     └──────▲──────┘
                                               │
┌─────────────┐     ┌─────────────┐     ┌──────┴──────┐
│  FastAPI    │────▶│  Prometheus │────▶│ Alertmanager│
│  (메트릭)    │     │  (수집)     │     │  (알림)     │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 12.2 핵심 메트릭

| 카테고리 | 메트릭 | 알림 임계값 |
|----------|--------|-------------|
| 가용성 | 서버 업타임 | < 99.5% (5분 윈도우) |
| 응답 시간 | API p95 latency | > 800ms |
| 에러율 | HTTP 5xx 비율 | > 0.5% |
| 캐시 | Redis 히트율 | < 60% |
| 외부 API | 공공 API 성공률 | < 95% |
| 리소스 | CPU 사용률 | > 80% |
| 리소스 | 메모리 사용률 | > 85% |

### 12.3 알림 채널 및 에스컬레이션

| 심각도 | 조건 | 알림 채널 | 응답 시간 |
|--------|------|-----------|-----------|
| Critical | 서비스 다운, 에러율 > 5% | Slack + PagerDuty + SMS | 5분 |
| High | 성능 저하, 에러율 > 1% | Slack + PagerDuty | 15분 |
| Medium | 경고 임계값 초과 | Slack | 1시간 |
| Low | 정보성 알림 | 이메일 | 24시간 |

### 12.4 로깅 전략

| 로그 레벨 | 용도 | 보관 기간 |
|-----------|------|-----------|
| ERROR | 예외, 실패한 요청 | 90일 |
| WARN | 재시도, 폴백 사용 | 30일 |
| INFO | 주요 이벤트 (NFC 태그, API 호출) | 14일 |
| DEBUG | 상세 디버깅 (개발 환경만) | 1일 |

**구조화된 로그 형식**
```json
{
  "timestamp": "2026-01-15T08:30:45.123Z",
  "level": "INFO",
  "service": "subway-guide-api",
  "trace_id": "abc123",
  "station_id": "ST_0222",
  "event": "travel_time_requested",
  "response_time_ms": 45,
  "cache_hit": true
}
```

---

## 13. 로드맵 (Roadmap)

| Phase | 기간 | 주요 마일스톤 |
|-------|------|---------------|
| Phase 1 (MVP) | 1-3개월 | Android 앱 출시, 주요 10개역 지원, 기본 기능 구현, 모니터링 구축 |
| Phase 2 | 4-6개월 | iOS 지원, BLE 비콘 시스템 구축, 50개역 확장, 보안 고도화 |
| Phase 3 | 7-12개월 | 수도권 전역 확장, 개인화 기능, 웨어러블 연동, 성능 최적화 |

---

## 14. 부록

### 14.1 용어 정의

| 용어 | 정의 |
|------|------|
| T_NFC | NFC 태그 시점의 타임스탬프 |
| T_Beacon | BLE 비콘 감지 시점의 타임스탬프 |
| Δt | 소요 시간 (T_Beacon - T_NFC) |
| Cold Start | 초기 데이터 부족 상태 |
| k-익명성 | 최소 k명의 사용자와 구분 불가능하도록 하는 익명화 기법 |

### 14.2 참고 문서

- 공공 데이터 포털 API 가이드: https://www.data.go.kr/
- Flutter NFC Manager: https://pub.dev/packages/nfc_manager
- FastAPI 공식 문서: https://fastapi.tiangolo.com/
- WCAG 2.1 가이드라인: https://www.w3.org/WAI/WCAG21/quickref/

---

*— End of Document —*
