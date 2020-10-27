# Mask_Detection
아래 모델들을 사용해서 Mask_Detection 처리

### 사용 모델
1. facenet : 얼굴을 찾는 모델
  facenet = cv2.dnn.readNet('models/deploy.prototxt', 'models/res10_300x300_ssd_iter_140000.caffemodel')
2. model : 마스크 검출 모델**mobile net 기반의 전이학습으로 모델 제작**   

  model = load_model('models/mask_detector.model')
  

### 실행하기
1. 가상환경 구성
2. pip install -r requirements.txt  로 모듈 설치하기(tensorflow 2.2버전 이상필요) - **물론 image.ipynb는 코랩에서 돌려보기 추천**
3. image.ipynb, video.py, cam.py 실행해보기

### 레퍼런스
https://github.com/kairess/mask-detection

https://github.com/prajnasb/observations

https://www.pyimagesearch.com/2020/05/04/covid-19-face-mask-detector-with-opencv-keras-tensorflow-and-deep-learning/
