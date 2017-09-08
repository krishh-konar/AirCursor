#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import cv2
import numpy as np


def nothing(x):
    pass


def main():
    video_feed = cv2.VideoCapture(0)
    fgbg = cv2.BackgroundSubtractorMOG(history=500,nmixtures=50,backgroundRatio=.85,noiseSigma=15)

    # Palm-HSV Calibration (Pt.1)
    # ---------------------------
    # Enable the snippet below to enable a colorbar to manually caliberate HSV values to
    # detect palm.

    '''
    # defining colorbar windows to dynamically control HSV values
    Colorbar_window = 'Colorbars'
    cv2.namedWindow(Colorbar_window)
    cv2.createTrackbar("Hue_Low", Colorbar_window, 0, 179, nothing)
    cv2.createTrackbar("Hue_High", Colorbar_window, 0, 179, nothing)
    cv2.createTrackbar("Saturation_Low", Colorbar_window, 0, 255, nothing)
    cv2.createTrackbar("Saturation_High", Colorbar_window, 0, 255, nothing)
    cv2.createTrackbar("Value_Low", Colorbar_window, 0, 255, nothing)
    cv2.createTrackbar("Value_High", Colorbar_window, 0, 255, nothing)
    '''

    while True:

        _, screen = video_feed.read()
        screen = cv2.flip(screen, 1)
        screen_hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        # gray_screen = cv2.cvtColor(screen,cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray Feed", gray_screen)
        # fg_image = fgbg.apply(gray_screen)
        # cv2.imshow("BG reductionFeed", fg_image)


        # Palm-HSV Calibration (Pt. 2)
        # ----------------------------
        # Enable the snippet below to enable a colorbar to manually caliberate HSV values to
        # detect palm.
        '''
        # read trackbar positions for each trackbar
        Hue_Low = cv2.getTrackbarPos("Hue_Low", Colorbar_window)
        Hue_High = cv2.getTrackbarPos("Hue_High", Colorbar_window)
        Saturation_Low = cv2.getTrackbarPos("Saturation_Low", Colorbar_window)
        Saturation_High = cv2.getTrackbarPos("Saturation_High", Colorbar_window)
        Value_Low = cv2.getTrackbarPos("Value_Low", Colorbar_window)
        Value_High = cv2.getTrackbarPos("Value_High", Colorbar_window)

        lower_skin = np.array([Hue_Low, Saturation_Low, Value_Low], dtype=int)
        upper_skin = np.array([Hue_High, Saturation_High, Value_High])
        '''

        # Default HSV values for Palm Detection
        Hue_Low, Saturation_Low, Value_Low = 0, 53, 148
        Hue_High, Saturation_High, Value_High = 46, 101, 240

        lower_skin = np.array([Hue_Low, Saturation_Low, Value_Low], dtype=int)
        upper_skin = np.array([Hue_High, Saturation_High, Value_High])

        # print lower_skin, upper_skin

        # thresholding the HSV values
        thresh_screen_hsv = cv2.inRange(screen_hsv, lower_skin, upper_skin)

        # Blurring the threshold image
        # blurred_threshold = cv2.blur(thresh_screen_hsv, ksize=(3,3))
        # blurred_threshold = cv2.GaussianBlur(thresh_screen_hsv, (5,5), 0)
        blurred_threshold = cv2.bilateralFilter(thresh_screen_hsv, 8, 200, 200)
        blurred_threshold_final = cv2.medianBlur(blurred_threshold, ksize=5)

        #cv2.imshow("Video Feed", screen_hsv)
        cv2.imshow("threshold feed", thresh_screen_hsv)
        cv2.imshow("blurred threshold", blurred_threshold)
        cv2.imshow("final", blurred_threshold_final)




        #break out of the loop (exit program)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the web-cam
    video_feed.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
