import time
import os
import signal

from cv2 import VideoCapture, imshow, imwrite, waitKey
from pynput import keyboard

DATA_DIR = 'data'
cam = VideoCapture(0)
PATIENT_ID = None
NUM_CAPTURES = 5
WAIT_TIME = 0.1

def make_dirs():
	if not os.path.exists(DATA_DIR):
		os.mkdir(DATA_DIR)

def get_new_patient():
	dir_prefix = 'patient_'
	i = 0
	while os.path.exists(os.path.join(DATA_DIR, dir_prefix + str(i))):
		i += 1
	os.mkdir(os.path.join(DATA_DIR, dir_prefix + str(i)))
	return i

def on_press(key):
	recognized_keys = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
	try:
		if key.char in recognized_keys:
			for j in range(NUM_CAPTURES):
				result, image = cam.read()
				if result:
					filename_prefix = 'pain_{}_img_'.format(key.char)
					i = 0
					img_dir = os.path.join(DATA_DIR, 'patient_{}'.format(PATIENT_ID))
					while os.path.exists(os.path.join(img_dir, filename_prefix + str(i) + '.png')):
						i += 1
					imwrite(os.path.join(img_dir, filename_prefix + str(i) + '.png'), image)
					if j == 0:
						print('...saving img...')
				else:
					print('Error with image capture. Please try again.')
				time.sleep(WAIT_TIME)
		else:
			print('unrecognized key press {}'.format(key))
	except AttributeError as e:
		return False

if __name__ == '__main__':
	make_dirs()
	PATIENT_ID = get_new_patient()
	print('Using patient id {}'.format(PATIENT_ID))
	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	listener.join()
	signal.SIGINT