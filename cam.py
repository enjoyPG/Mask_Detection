from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import winsound

# facenet : 얼굴을 찾는 모델
facenet = cv2.dnn.readNet('models/deploy.prototxt', 'models/res10_300x300_ssd_iter_140000.caffemodel')
# model : 마스크 검출 모델
model = load_model('models/mask_detector.model')

# 동영상 파일 읽기
# cap = cv2.VideoCapture('imgs/01.mp4')
# 실시간 웹캠 읽기
cap = cv2.VideoCapture(0)
i = 0

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    # 이미지의 높이와 너비 추출
    h, w = img.shape[:2]

    # 이미지 전처리
    # ref. https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/
    # facenet에서 blob이미지(4차원)를 input값으로 사용하였기에 테스트 이미지도 blob으로 만들어줌
    blob = cv2.dnn.blobFromImage(img, scalefactor=1., size=(300, 300), mean=(104., 177., 123.))

    # facenet의 input으로 위에서 만든 blob을 사용함
    facenet.setInput(blob)
    # facenet 결과 추론, 얼굴 추출 결과가 detections의 저장
    # 한 프레임 내의 여러 얼굴들을 받음
    dets = facenet.forward()

    result_img = img.copy()

    # 마스크를 찾용했는지 확인
    for i in range(dets.shape[2]):

        # 얼굴일 가능성 확인
        confidence = dets[0, 0, i, 2]
        # 얼굴일 가능성이 50%보다 낮을 경우 처리하지 않고 50%이상일 경우만 마스크 착용여부 확인
        if confidence < 0.5:
            continue

        # 바운딩 박스
        x1 = int(dets[0, 0, i, 3] * w)
        y1 = int(dets[0, 0, i, 4] * h)
        x2 = int(dets[0, 0, i, 5] * w)
        y2 = int(dets[0, 0, i, 6] * h)

        # 원본 이미지에서 얼굴영역 추출
        face = img[y1:y2, x1:x2]
        try:
            # 추출한 얼굴영역을 전처리
            # mobileNet pretrained 모델에 넣을 얼굴사진 제작 전처리
            face_input = cv2.resize(face, dsize=(224, 224))
            face_input = cv2.cvtColor(face_input, cv2.COLOR_BGR2RGB)
            # tensorflow에서 제공하는 mobileNet preprocessing input값 만들기
            face_input = preprocess_input(face_input)
            # (1,224,224,3)으로 만들기
            face_input = np.expand_dims(face_input, axis=0)

            # 마스크 검출 모델로 결과값 return (마스크 쓴 확률, 안 쓴 확률)
            mask, nomask = model.predict(face_input).squeeze()

            # 마스크를 꼈는지 안겼는지에 따라 라벨링해줌
            if mask > nomask:
                color = (0, 255, 0)
                label = 'Mask %d%%' % (mask * 100)
            else:
                color = (0, 0, 255)
                label = 'No Mask %d%%' % (nomask * 100)
                frequency = 2500  # Set Frequency To 2500 Hertz
                duration = 50  # Set Duration To 1000 ms == 1 second
                winsound.Beep(frequency, duration)

            # 화면에 얼굴부분과 마스크 유무를 출력해해줌
            cv2.rectangle(result_img, pt1=(x1, y1), pt2=(x2, y2), thickness=2, color=color, lineType=cv2.LINE_AA)
            cv2.putText(result_img, text=label, org=(x1, y1 - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
                        color=color, thickness=2, lineType=cv2.LINE_AA)
        except Exception as e:
            print(str(e))

    cv2.imshow('img',result_img)


    # q를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


