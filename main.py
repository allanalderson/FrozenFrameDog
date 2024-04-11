import cv2
import pyautogui
import threading
import time
print()
print("NOTE:   ENSURE NDI WEBCAM 1 IS IN SET TO 480p30 BEFORE RUNNING THIS CODE.\n")
####################
difference_threshold = 5000 # Default 5000   Keep value below 20000
retrigger_holdoff = 31 # seconds.
frame_distance = 15 #  (30 = 1sec at 30fps) Higher values are more forgiving of dropous
show_diff_window = False  # True or False
####################

frame_count = 0
frame_loss = False
cap = cv2.VideoCapture(0) # 0 is NDI webcam 1
ret, frame1 = cap.read()
time.sleep(1)
ret, frame2 = cap.read()
time.sleep(2)

def reset_frame_loss():
	global frame_loss
	time.sleep(retrigger_holdoff)
	frame_loss = False


while True:
	ret, frame2 = cap.read()
	if not ret:
		print("NO VIDEO.    NDI WEBCAM NOT CONFIGURED?")
		break
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	frame_count += 1
	if frame_count % frame_distance == 0:
		diff = cv2.absdiff(frame1, frame2)
		pixel_difference_count = cv2.countNonZero(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY))
		#print(pixel_difference_count)
		diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
		frame1 = frame2
		if show_diff_window:
			enhanced_diff = cv2.equalizeHist(diff_gray)
			cv2.imshow(' Difference       (use q to exit)', enhanced_diff)
		if pixel_difference_count < difference_threshold and frame_loss == False:
			frame_loss = True
			print("Frame Loss")
			pyautogui.typewrite("2")
			threading.Thread(target=reset_frame_loss).start()
cap.release()
cv2.destroyAllWindows()
