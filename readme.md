# 부스 노동 결과 프로젝트

왜 git으로 옮겼는지 모르겠지만 어쨌든 스노우카메라 비슷한거 따라한거 옮겨놨어요!

일단 여긴 done sticker 및 save폴더가 없기 때문에 따로 만드셔야 하고 컴파일 된 소스 용량이 만만치 않기 때문에 PyInstaller로 
알아서 컴파일 하셔야 합니다.

### 발적화 주의할 것
소스는
1. main -> 다른거 부름
2. Camera -> 촬영 및 웹캠 캡쳐, 스티커 적용
3. compile -> Py2exe쓰다 망한거(퇴물)
4. config -> 설정창
5. confirm -> 마스크 적용 창
6. bringImage -> 마스크 가져오는거
7. definederror -> 사용자 정의 에러
8. draw_sticker -> 제곧내
9. drawImage -> 제곧내 * 2
10. myutility -> pixmap으로 변환하는 함수 밖으로뺀거
11. sticker_apply -> 스티커 적용 관련 제곧내 *3
12. 기타 파일들 -> 알아서 알아보세요(..?!)

그러합니다.