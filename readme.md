# 부스 프로젝트 Repository

스노우 카메라와 유사하지만, 유저가 직접 스티커나 마스크등을 만들고 설정 가능한 프로그램을 제작하였습니다.

일단 여긴 done sticker 및 save폴더가 없기 때문에 따로 만드셔야 하고 컴파일 된 소스 용량이 만만치 않기 때문에 exe로 바꾸신다면 pyInstaller로 직접 진행하셔야 합니다.

### 소스코드 간단한 설명
소스는
1. main -> 메인 화면
2. Camera -> 촬영 및 웹캠 캡쳐, 스티커 적용
3. config -> 설정창
4. confirm -> 마스크 적용 창
5. bringImage -> 마스크 가져오는거
6. definederror -> 사용자 정의 에러
7. draw_sticker -> 스티커를 그리는 소스
8. drawImage -> 이미지 그리기
9. myutility -> pixmap으로 변환하는 함수 밖으로 뺀거
10. sticker_apply -> 스티커 적용
