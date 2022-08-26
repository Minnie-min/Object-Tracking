import cv2
import numpy as np
import sys

# open video file
video_path = 'hockey.mp4'
cap = cv2.VideoCapture(video_path)
if cap is None:
  print("video load failed")
  sys.exit()


#####################모바일용으로 저장##########################
output_size = (375, 667)

# initialize writing video
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)

# 동영상이 제대로 로드되면 True 반환, 아니면 exit
if not cap.isOpened():
  exit 

#Tracker 설정
tracker = cv2.TrackerCSRT_create()

# ROI(Region of Interest), 트랙킹할 오브젝트를 설정
ret, img = cap.read() # 동영상의 첫 번째 프레임을 읽어와
cv2.namedWindow('Select Object')
cv2.imshow('Select Object', img)

rect = cv2.selectROI('Select Object', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Object')

# Initialize Tracker
tracker.init(img, rect)

while True:
  ret, img = cap.read()

  # 비디오를 잘못 읽거나, 비디오가 끝나면 ret 변수가 False가 됨. 그때 exit
  if not ret:
    exit()

  success, box = tracker.update(img) # img에서 rect로 설정한 오브젝트와 비슷한 물제의 위치를 찾아서 반환하며 업데이트

  left, top, w, h = [int(v) for v in box]

  center_x = left+w/2
  center_y = top+h/2

  result_top = int(center_y - output_size[1]/2)
  result_bottom = int(center_y + output_size[1]/2)
  result_left = int(center_x + output_size[0]/2)
  result_right = int(center_x + output_size[0]/2)


  cv2.rectangle(img, pt1=(left,top), pt2=(left+w, top+h), color=(255,255,255), thickness=3)

  cv2.imshow('img', img)
  

  if cv2.waitKey(1) == ord('q'): # q 버튼을 누르면 강제 종료
    break
