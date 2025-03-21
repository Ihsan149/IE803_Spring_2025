import tensorflow as tf
import scipy.misc
import model
import cv2
from subprocess import call
from skimage.transform import resize
import PIL
from PIL import Image
import numpy as np
sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "save/model.ckpt")

img = cv2.imread('steering_wheel_image.jpg',0)
rows,cols = img.shape

smoothed_angle = 0

cap = cv2.VideoCapture(0)
while(cv2.waitKey(10) != ord('q')):
    ret, frame = cap.read()
    # image = scipy.misc.imresize(frame, [66, 200]) / 255.0

    # Convert frame to PIL Image
    pil_image = Image.fromarray(frame)

    # Resize the image
    resized_image = pil_image.resize((200, 66))  # PIL uses (width, height)

    # Convert resized image back to numpy array
    image = np.array(resized_image)

    # Normalize the pixel values
    image = image / 255.0


    degrees = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0] * 180 / scipy.pi
    call("clear")
    print("Predicted steering angle: " + str(degrees) + " degrees")
    cv2.imshow('frame', frame)
    #make smooth angle transitions by turning the steering wheel based on the difference of the current angle
    #and the predicted angle
    smoothed_angle += 0.2 * pow(abs((degrees - smoothed_angle)), 2.0 / 3.0) * (degrees - smoothed_angle) / abs(degrees - smoothed_angle)
    M = cv2.getRotationMatrix2D((cols/2,rows/2),-smoothed_angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    cv2.imshow("steering wheel", dst)

cap.release()
cv2.destroyAllWindows()
