import cv2
import pyautogui
import threading
import time

print("FROZEN FRAME DIRECTOR\n")
print("NOTE:   ENSURE NDI WEBCAM 1 IS IN SET TO 480p30 BEFORE RUNNING THIS CODE.\n")
####################
overlay1_timer = 60 # seconds
frame_distance = 30  # (30 = 1sec at 30fps) Higher values are more forgiving of occasional freezes
show_diff_window = False  # True or False
difference_threshold = 5000  # Default 5000   Keep value below 20000 (480p)
retrigger_holdoff = 5  # seconds.
cap = cv2.VideoCapture(0)  # 0 is NDI webcam 1
####################
start_time = time.time()
frame_count = 0
frame_loss = False
ret, frame1 = cap.read()
time.sleep(1)
ret, frame2 = cap.read()
time.sleep(3)
no_overlays_rule = 0
overlay1_in_time = 0
print("Running!")
def overlay_function():
	if frame_loss == False: # Don't overlay during the adverts!
		print(" Overlay 3 In - F3 ")
		pyautogui.press('f3')     # press a function key
def rules_function():
	if frame_loss == True:
		print(" All Overlays OFF  - F12 ")
		pyautogui.press('f12')     # press a function key

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
		# print(pixel_difference_count)
		diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
		frame1 = frame2
		if show_diff_window:
			enhanced_diff = cv2.equalizeHist(diff_gray)
			cv2.imshow(' Difference       (use q to exit)', enhanced_diff)
		if pixel_difference_count < difference_threshold and frame_loss == False:
			frame_loss = True
			print(" Frame Loss \n")
			pyautogui.press('f2')     # press a function key
			threading.Thread(target=reset_frame_loss).start()
	current_time = time.time()
	if current_time - overlay1_in_time >= overlay1_timer:  # Seconds
		overlay_function()
		overlay1_in_time = current_time

	if current_time - no_overlays_rule >= .5:  # Seconds
		rules_function()
		no_overlays_rule = current_time

cap.release()
cv2.destroyAllWindows()
