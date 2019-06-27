import matplotlib.pyplot as plt
import numpy as np
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
    def show(self,img_input,landmarks_input,scale=3,wait_time=0):

        landmarks = copy.deepcopy(landmarks_input.reshape(-1,2))
        img = copy.deepcopy(img_input)
        img = cv2.resize(img,(img.shape[1]*scale,img.shape[0]*scale))

        if landmarks is not  None:
            landmarks = scale * landmarks
            landmarks[:,0] = landmarks[:,0]
            landmarks[:,1] = landmarks[:,1]
            for i in range(0, landmarks.shape[0], 1):
                pt = (int(landmarks[i, 0]),int(landmarks[i, 1]))
                cv2.circle(img, pt, 3, (255, 255, 0), -1)

        cv2.namedWindow("test", 0)

        cv2.imshow("test", img)
        key = cv2.waitKey(wait_time)