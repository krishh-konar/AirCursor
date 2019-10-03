#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import cv2
import numpy as np
import utilities


def main():
    detector = utilities.Detector()
    mouse = utilities.Mouse()

    lower_skin_thresh, upper_skin_thresh = detector.caliberate_hsv_values()
    if np.array_equal(lower_skin_thresh, np.array([0, 0, 0], dtype=int)) and \
            np.array_equal(upper_skin_thresh, np.array([0, 0, 0], dtype=int)):
        # default values for detection
        lower_skin_thresh = np.array([0, 78, 103], dtype=int)
        upper_skin_thresh = np.array([35, 125, 170], dtype=int)

    video_feed = cv2.VideoCapture(0)
    print(pyautogui.size())
    print(video_feed.read()[1].shape)

    while True:
        _, screen = video_feed.read()
        screen = cv2.flip(screen, 1)
        screen_hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        # thresholding the HSV values
        thresh_screen_hsv = cv2.inRange(screen_hsv, lower_skin_thresh, upper_skin_thresh)

        # Blurring the threshold image
        # blurred_threshold = cv2.blur(thresh_screen_hsv, ksize=(3,3))
        # blurred_threshold = cv2.GaussianBlur(thresh_screen_hsv, (5,5), 0)
        blurred_threshold = cv2.bilateralFilter(thresh_screen_hsv, 8, 200, 200)
        blurred_threshold_final = cv2.medianBlur(blurred_threshold, ksize=5)

        #cv2.imshow("Video Feed", screen_hsv)
        # cv2.imshow("final", blurred_threshold_final)

        contours, _ = cv2.findContours(blurred_threshold_final.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        biggest_contour = max(contours, key=lambda x: cv2.contourArea(x))

        hand = np.zeros(shape = blurred_threshold_final.shape)
        cv2.drawContours(hand, [biggest_contour], 0, (255, 255, 255), 2)

        # pinpointing cursor location for movement
        mouse.move_cursor(biggest_contour)
        cv2.imshow("Hand", hand)

        #break out of the loop (exit program)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the web-cam
    video_feed.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
