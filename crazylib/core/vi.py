import matplotlib.pyplot as plt
import numpy as np
import copy

def DrawLine(y,flag,ymin,ymax):
    x = np.linspace(0, y.shape[0], y.shape[0])
    plt.plot(x, y)
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.ylim((ymin,ymax))
    plt.title(flag)
    plt.show()




class Visualizer():
    def __init__(self):

        pass
    def show(self,img_input,landmarks_input,scale=3,wait_time=0,draw_flag="num",flag="test"):
        import cv2
        landmarks = copy.deepcopy(landmarks_input.reshape(-1,2))
        img = copy.deepcopy(img_input)
        img = cv2.resize(img,(img.shape[1]*scale,img.shape[0]*scale))

        if landmarks is not  None:
            landmarks = scale * landmarks
            landmarks[:,0] = landmarks[:,0]
            landmarks[:,1] = landmarks[:,1]
            for i in range(0, landmarks.shape[0], 1):
                pt = (int(landmarks[i, 0]),int(landmarks[i, 1]))

                if draw_flag=="num":
                    cv2.putText(img,str(i), pt, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.circle(img, pt, 3, (255, 255, 0), -1)

        cv2.namedWindow(flag, 0)

        cv2.imshow(flag, img)
        key = cv2.waitKey(wait_time)