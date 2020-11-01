# SARAMARA WEBSITE TECH SPEC

- OWNER : HAJUNE LEE
- LAST UPDATE : 2020-11-01

## 요약 (Summary)

- 가장 먼저 테크 스펙을 세 줄 내외로 정리합니다. 테크 스펙의 제안 전체에 대해 누가/무엇을/언제/어디서/왜를 간략하면서도 명확하게 적습니다.
- ex) Bottom Navigation 영역(하단 탭)을 유저가 원하는 순서로 커스텀할 수 있게 합니다.
  서버에 순서 정렬 및 저장 API를 요청할 수 없으므로, 순서를 로컬에 저장하고 불러옵니다.

## 배경 (Background)

- 프로젝트의 Context를 적습니다. 왜 이 기능을 만드는지, 동기는 무엇인지, 어떤 사용자 문제를 해결하려 하는지, 이전에 이런 시도가 있었는지, 있었다면 해결이 되었는지 등을 포함합니다.
  ex) 다양한 탭을 사용하는 유저는 Segment에 따라 하단 탭의 노출 수와 사용 빈도가 다릅니다. 예를 들어, 20대와 30대의 추천 탭 노출 수 사이는 월 n만 정도입니다.
  이러한 유저의 Segment에 맞춰 하단 탭 순서를 유저가 직접 커스텀할 수 있다면 뱅크샐러드가 개인화되었다고 인지할 수 있을 것입니다.

## 목표 (Goals)

- 예상 결과들을 Bullet Point 형태로 나열합니다. 이 목표들과 측정 가능한 임팩트들을 이용해 추후 이 프로젝트의 성공 여부를 평가합니다.
  ex) o Bottom Navigation의 순서를 유저가 편집할 수 있게 한다.
  o 앱을 껐다 켰을 시에도 유저가 편집한 순서대로 하단 탭을 보이게 한다.

## 목표가 아닌 것 (Non-Goals)

- 목표가 아닌 것은 프로젝트에 연관되어 있으나 의도적으로 하지 않거나 해결하지 않으려 하는 것을 말합니다.
- 목표가 아닌 것을 정하면 프로젝트 범위를 더 명확하게 할 수 있고, 이 기능도 붙이자, 저 기능도 붙이자 하는 것을 막을 수 있습니다.
- 목표처럼 목표가 아닌 것도 Bullet Point 형태로 읽기 쉽게 적어 독자가 직관적으로 이해할 수 있도록 합니다.
- 목표가 아닌 것을 세부적으로 잘 적으면 프로젝트 범위를 넓게 보려 하는 독자들의 폭주를 막을 수 있습니다.
  ex) o 사용하지 않는 탭의 삭제 기능 등 ‘순서 편집’ 외 하단 탭에 관련한 추가적인 기능 개발
  o 순서 정렬 및 저장 API 개발

## 계획 (Plan)

- 테크 스펙에서 가장 긴 파트 입니다.
- 준비한 모든 리서치, 준비 내용들을 여기에 씁니다.
- 어떻게 기술적, 엔지니어링적으로 접근할지 상세히 묘사합니다.
- 만약 어떤 부분을 어떻게 할지 확실히 결정하지 못한 상태라면 어떤 것들을 고려하고 있는지 목록화해서 적습니다.
- 그렇게 하면 이 문서 리뷰어들이 올바른 결정을 내리도록 도움을 주게 됩니다.
- 얼마나 기술적으로 깊게 써야 하는지는 이 테크 스펙의 목적과 독자들에 따라 정합니다.
- 작성자는 생산적인 제안을 받을 수 있도록 충분히 상세하게 계획을 적습니다.
- 이 섹션은 프로젝트가 다른 시스템들과 어떻게 상호작용하는지 그림이나 다이어그램을 포함하기 좋은 지점입니다.
- 사용자와 시스템 간의 시퀀스 다이어그램, 서비스와 API 간의 데이터 흐름 다이어그램, 데이터베이스 ERD 등을 포함하면 독자의 이해를 한층 높일 수 있습니다.
- 또한 이 테크 스펙이 로우 레벨 까지 다뤄야 한다면 HTTP 응답 코드, JSON 요청 / 응답 포맷, 에러 명세 등까지 모두 다뤄져야 합니다.

## 이외 고려 사항들 (Other Considerations)

- 고려했었으나 하지 않기로 결정된 사항들을 적습니다.
- 이렇게 함으로써 이전에 논의되었던 주제가 다시 나오지 않도록 할 수 있고, 이미 논의되었던 내용이더라도 리뷰어들이 다시 살펴볼 수 있습니다.
  ex) 앱 데이터 초기화 시에는 사용자가 커스텀했던 리스트를 모두 날리기로 했었으나,
  기존 로직에서 앱 데이터 초기화 시에 로컬 관련 추가 핸들링이 없어 이 기능에서도 앱 데이터 초기화 때에 리스트를 날리는 등 추가적인 기능 구현을 하지 않기로 함.

## 마일스톤 (Milestones)

- 프로젝트를 제 시간에 맞추기 위해 테크 스펙의 내용을 바탕으로 추정한 마일스톤을 공유합니다.
- 실험 계획, 배포 날짜를 포함해 최대한 자세히 적습니다.
  ex) ~ 9/25: BPL 컴포넌트 개발
  9/28 ~ 9/29: 실험 변수 추가, 로컬 변수 추가
  9/30 ~ 10/4: 추석 연휴!
  10/5: 하단 탭 확장 가능한 구조로 리팩토링
  10/6 ~ 10/8: 비즈니스 로직 구현
  10/12 ~ 10/20: 사용자 이벤트 부착 및 미진한 내용 보충
  10/20: 2.45.0 코드 프리즈 (이때까지 내부 기능 테스트, 이벤트 로깅 테스트)
  10/21 ~ 10/23: 2.45.0 릴리즈 QA
  11/4: 2.45.0 Rollout
