# Break-Google-reCAPTCHA
구글 리캡챠 뚫기

Weights file : https://drive.google.com/drive/folders/1q5EodHEguUeu3u3dXC0qABd5YEyjPHS8?usp=sharing


#설명

# ./cfg, ./data

yolov4 train할 때 필요한 설정 파일들

# ./recaptcha

deathlyface()에 있는 dataset의 일부에 모델을 돌려본 것



# ./darknet

linux에서 build한 yolov4실행파일

# ./201113YOLOv4OIDv6Training.ipynb

yolov4 build, train, test하는 코드


# ./captcha*.avi

셀레니움으로 구글 리캡챠를 뚫는 과정을 담은 영상


# ./chart_*.png

각 class별로 학습을 돌렸을 때 loss랑 mAP값을 차트로 나타낸 것, _숫자가 붙으면 같은 training에서 끊겨져서 한번더 돌린거고, 그냥 숫자가 붙으면 새로 training했다는 뜻.

parkingmeter의 경우 일부가 사라졌다

# ./predictions_*.jpg

테스트할 이미지들에 모델을 돌려본 결과



# 그외 모든 ./*.jpg, ./*.png

테스트할 이미지
