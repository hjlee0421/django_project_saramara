![alt text](https://github.com/hjlee0421/django_project_saramara/blob/master/saramara_github.jpg?raw=true)

# SARAMARA WEBSITE TECH SPEC

- OWNER : HAJUNE LEE
- LAST UPDATE : 2021-01-23
- Website를 개발하는 이유?
- 멈춰있는 데이터 (csv, json)을 분석해서 결과물을 보고서로 작성하는 일을 하면서,
  보고서가 아닌 실제 서비스에 적용시킬 수 있는 환경에서 데이터 분석을 해보고 싶었다.
  하지만, 웹 혹은 앱에 대해서 frontend & backend 에 대해서 지식이 있는가? 에 대한 대답에는 대답하지 못했다.
  공부를 통해서 이러한 지식을 습득할 수 있지민, 지식을 습득하는 가장 좋은 방법은 직접 해보는것이라고 생각했다.
  부족하지만, 꾸준하게 발전시키면서 frontend & backend 개발자들과 가장 효율적으로 일할 수 있는 Data Scientist가 되고싶다.

## 요약 (Summary)

- 누가 : 상품을 구매할지 말지 고민하는 예비 고객
- 언제 : 상품을 인지하고, 구매를 고민하는 시점
- 어디서 : 사라마라 커뮤니티 사이트에서
- 무엇을 : 고민하는 상품에 대한 타인의 의견을
- 어떻게 : 성별/연령대별 사라/마라 의견을 듣고 고민을 해결
- 왜 : 내가 잘 모르는 상품에 대해서 타인의 의견을 듣고 결정하는 습관을 이용하여, 고민을 해결해주는 역할을 하기 위해서
- tech : python django framework 을 기본 베이스로 활용하여, html/css/javascript를 이용하여 사이트를 구축하며, 서버부분은 추후에 AWS를 활용할 예정.

## 배경 (Background)

- 상품을 구매할지 말지에 대한 고민은 모두에게 발생
- 이러한 불편을 타인의 의견을 통해서 해결하기도 하는데, 해당 의견이 남자인지 여자인지, 연령대는 어떻게 되는지에 대한 정보가 없는 문제 존재
- 타인의 의견을 범주(성별/연령)화 하여, 고객의 고민을 해결
- 이전에 "사라마라 해주세요" 라는 제목으로 각 상품별 커뮤니티에 글이 많이 존재하지만, 의견을 주는 상대에 대한 정보가 전무하다는 단점이 존재
- 따라서 의견이 통일되지 않을때 해당 의견에 대한 추가정보에 대한 요구 존재

## 목표 (Goals)

- 모바일상에서 카카오톡 연동을 통해 빠른 회원가입 및 로그인이 가능
- 살지 말지 고민하는 상품의 이미지, 링크, 가격등을 편리하게 업로드 가능
- 성별/연령대 가 오픈된 타인의 구매에 대한 찬반 의견을 수렴 가능
- 전체 사라/마라 의견과 함께 추가적인 성별/연령대별 의견 확인 가능

## 목표가 아닌 것 (Non-Goals)

- 카카오톡 친구기능 추가하여 추가적인 프로모션
- ajax, react, vue 등 최신의 javascript 활용
- point 시스템 적용하여, 커뮤니티 활동 활성화 유인
- app 개발하여 배포

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

- Backend 는 Django Framework 와 AWS 의 EC2, S3, RDSe, Elastic Beanstalk를 활용하여 구성한다.
- Frontend 는 HTML, CSS, JQUERY 를 활용하여 구성 한 후, 추후에 frontend에 React를 사용하게 되면, DRF와 함께 업데이트 하기로 한다.
- Website 는 총 6개의 페이지로 구성된다. (메인페이지, 질문페이지, 상세페이지, 수정페이지, 마이페이지, 유저정보변경페이지)
- views.py 에 들어갈 view 들은 모두 Class Based View 로 작성한다.
- 모든 페이지에서 해당페이지를 보여주는 API call 은 GET을 사용하고, 해당페이의 정보가 작성/수정 되는경우 POST를 사용한다.
- 단, 예외적으로 메인페이지에서 조건검색을 할때에는 GET을 사용한다.

## 이외 고려 사항들 (Other Considerations)

- 사라마라 투표부분을 ajax 혹은 Django REST Framework 활용할까 했으나, 우선은 사이트의 오픈이 먼저여서 추후에 v2 에 적용하는것으로 변경
- 이버주 인기글 top3 를 상단에 띄우는것을 고려했었으나, 이것 또한 v2에 적용하는게 좋을것으로 얘기되어 v2 에 적용하는것으로 변경
- 대댓글 기능 & 댓글에 대해서 좋아요/싫어요 기능이 있으면 좋을것 같으나, 이것도 우선 v2 에 적용하는것으로 변경

## 마일스톤 (Milestones)

- ~ 20/12/31 : User, Post, Comment 모델 CRUD 완성하기
- 21/01/01 ~ 20/01/31 : Post 모델에 연결된 Image 모델 CRUD 추가하기
- 21/02/01 ~ 20/02/28 : Comment 모델에 대댓글 기능 CRUD 추가하기 & AWS 진행
