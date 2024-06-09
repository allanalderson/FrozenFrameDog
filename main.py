import cv2
import pyautogui
import time

print("FROZEN FRAME DIRECTOR\n")
print("NOTE:   ENSURE NDI WEBCAM 1 IS IN SET TO 480p30 BEFORE RUNNING THIS CODE.\n")
####################
frame_distance = 15  # Typ: 15.  Minimum 5.  Higher values are more forgiving of occasional freezes
show_diff_window = False  # True or False
difference_threshold = 10000  # Default 10000   Keep value below 20000 (480p)
cap = cv2.VideoCapture(0)  # 0 is NDI webcam 1
####################
frame_count = 0
frame_loss = True
ret, frame1 = cap.read()
time.sleep(1)
print("Starting in 5 seconds. Put vmix to front.")
ret, frame2 = cap.read()
time.sleep(5)
print("Running!")



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
		# print(pixel_difference_count)
		diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
		frame1 = frame2
		if show_diff_window:
			enhanced_diff = cv2.equalizeHist(diff_gray)
			cv2.imshow(' Difference       (use q to exit)', enhanced_diff)
		if frame_loss == False:
			if pixel_difference_count < difference_threshold:
				pyautogui.press('f2')  # press a function key
				print("Frame Loss Detected. F2 sent.")
				frame_loss = True
		if frame_loss == True:
			if pixel_difference_count > difference_threshold:
				pyautogui.press('f1')  # press a function key
				print("Normal Video.  F1 sent.\n")
				frame_loss = False

cap.release()
cv2.destroyAllWindows()