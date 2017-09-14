#!/usr/bin/env python


import pyautogui
import cv2
import numpy as np


class Detector:

    colorbar_window = 'Colorbars'

    def __int__(self):
        pass

    def nothing(self, x):
        pass

    def caliberate_hsv_values(self):

        video_feed = cv2.VideoCapture(0)

        # Palm-HSV Calibration (Pt.1)
        # ---------------------------
        # Enable the snippet below to enable a colorbar to manually caliberate HSV values to
        # detect palm.

        # defining colorbar windows to dynamically control HSV values

        cv2.namedWindow(self.colorbar_window)
        cv2.createTrackbar("Hue_Low", self.colorbar_window, 0, 179, self.nothing)
        cv2.createTrackbar("Hue_High", self.colorbar_window, 0, 179, self.nothing)
        cv2.createTrackbar("Saturation_Low", self.colorbar_window, 0, 255, self.nothing)
        cv2.createTrackbar("Saturation_High", self.colorbar_window, 0, 255, self.nothing)
        cv2.createTrackbar("Value_Low", self.colorbar_window, 0, 255, self.nothing)
        cv2.createTrackbar("Value_High", self.colorbar_window, 0, 255, self.nothing)

        while True:
            _, screen = video_feed.read()
            screen = cv2.flip(screen, 1)
            screen_hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

            # Palm-HSV Calibration (Pt. 2)
            # ----------------------------
            # Enable the snippet below to enable a colorbar to manually caliberate HSV values to
            # detect palm.

            # read trackbar positions for each trackbar
            Hue_Low = cv2.getTrackbarPos("Hue_Low", self.colorbar_window)
            Hue_High = cv2.getTrackbarPos("Hue_High", self.colorbar_window)
            Saturation_Low = cv2.getTrackbarPos("Saturation_Low", self.colorbar_window)
            Saturation_High = cv2.getTrackbarPos("Saturation_High", self.colorbar_window)
            Value_Low = cv2.getTrackbarPos("Value_Low", self.colorbar_window)
            Value_High = cv2.getTrackbarPos("Value_High", self.colorbar_window)

            lower_skin_thresh = np.array([Hue_Low, Saturation_Low, Value_Low], dtype=int)
            upper_skin_thresh = np.array([Hue_High, Saturation_High, Value_High], dtype=int)

            thresh_screen_hsv = cv2.inRange(screen_hsv, lower_skin_thresh, upper_skin_thresh)

            # Blurring the threshold image
            # blurred_threshold = cv2.blur(thresh_screen_hsv, ksize=(3,3))
            # blurred_threshold = cv2.GaussianBlur(thresh_screen_hsv, (5,5), 0)
            blurred_threshold = cv2.bilateralFilter(thresh_screen_hsv, 8, 200, 200)
            blurred_threshold_final = cv2.medianBlur(blurred_threshold, ksize=5)

            # cv2.imshow("Video Feed", screen_hsv)
            #cv2.imshow("threshold feed", thresh_screen_hsv)
            cv2.imshow("final", blurred_threshold_final)

            #cv2.imshow("img", thresh_screen_hsv)

            # break out of the loop (exit program)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release the web-cam
        video_feed.release()
        cv2.destroyAllWindows()

        return lower_skin_thresh, upper_skin_thresh


class Mouse:
    screen_resolution = pyautogui.size()
    video_feed = cv2.VideoCapture(0)
    cam_resolution = video_feed.read()[1]
    # print cam_resolution
    video_feed.release()
    cv2.destroyAllWindows()

    def __int__(self):
        pass

    def move_cursor(self, hand_contour):
        moment = cv2.moments(hand_contour)
        centre_x = int(moment['m10'] / moment['m00'])
        centre_y = int(moment['m01'] / moment['m00'])
        pointer_x = int((centre_x * self.screen_resolution[0]) / self.cam_resolution.shape[1])
        pointer_y = int((centre_y * self.screen_resolution[1]) / self.cam_resolution.shape[0])
        # cv2.circle(hand, (centre_x, centre_y), 7, (255, 255, 255), -1)
        pyautogui.moveTo(pointer_x, pointer_y, 0.1)
        # cv2.imshow("Hand", hand)
        return