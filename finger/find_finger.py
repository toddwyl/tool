#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : ManWingloeng


# from imutils.video.webcamvideostream import WebcamVideoStream
import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt


# frame_read = cv2.imread("/media/todd/38714CA0C89E958E/147/yl_tmp/readingbook/data/all_nail/test/01.jpg")


# frame=cv2.blur(frame,(11,11))

def find_hand(frame):
    # frame = imutils.resize(frame, width=500, height=500)
    img = frame.copy()
    # frame = cv2.GaussianBlur(frame, (15, 15), 0)
    # frame = cv2.bilateralFilter(frame, 9, 75, 100)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    YCrCb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    YCrCb_frame = cv2.GaussianBlur(YCrCb_frame, (9, 9), 0)
    YCrCb_frame = cv2.GaussianBlur(YCrCb_frame, (3, 3), 0)
    cv2.imshow("YCrCb_frame", YCrCb_frame)
    print(frame.shape[:2])
    # mask = cv2.inRange(YCrCb_frame, np.array([0, 135, 97]), np.array([255, 177, 127]))#140 170 100 120
    mask = cv2.inRange(YCrCb_frame, np.array([0, 140, 100]), np.array([255, 175, 120]))
    # skinEllipse = np.zeros(shape=(256, 256))
    # skinEllipse = skinEllipse.astype(np.int32)
    # skinEllipse = cv2.ellipse(skinEllipse, (109.38, 152.02), (23.4, 15.2), 43, 0, 360, (255, 255, 255), -1)
    cv2.imshow("mask", mask)
    # mask = cv2.inRange(YCrCb_frame, np.array([0, 140, 100]), np.array([255, 170, 120]))
    # cv2.imshow("mask", mask)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # res = cv2.GaussianBlur(res, (15, 15), 0)
    # res = cv2.bilateralFilter(res, 9, 75, 100)
    res = cv2.dilate(res, (15, 15), iterations=4)
    res = cv2.erode(res, (15, 15), iterations=3)
    res = cv2.dilate(res, (15, 15), iterations=1)

    # res = cv2.GaussianBlur(res, (15, 15), 0)
    #     cv2.imshow("res", res)
    ret, bin_mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # ret, bin_mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
    # init_mask = bin_mask.copy()
    # cv2.imshow("init_mask", init_mask)

    # mask_frame=frame[:,:,1:]
    # mask=np.ones(shape=mask_frame.shape)
    # msk_lower=np.array([136, 100]) #140,100 136
    # msk_upper=np.array([175, 120]) #175,120
    # print("mask: ",mask.shape)
    # print("mask_frame: ",mask_                    frame.shape)
    # np.putmask(mask, mask_frame<msk_lower, 0.)
    # np.putmask(mask, mask_frame>msk_upper, 0.)

    # mask=mask[:,:,0]*mask[:,:,1]
    # print(mask.shape)

    # kernelf = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelf, iterations=1)
    # mask = cv2.dilate(mask, kernelf, iterations=1)
    # mask = cv2.erode(mask, kernelf, iterations=1)



    bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, (11, 11))
    watershed_mask = bin_mask.copy()
    bin_mask = cv2.dilate(bin_mask, (15, 15), iterations=4)
    bin_mask = cv2.erode(bin_mask, (15, 15), iterations=2)

    # bin_mask = cv2.medianBlur(bin_mask, 3)

    ### watershed
    # kernel = np.ones((3, 3), np.uint8)
    # fg = cv2.erode(watershed_mask, kernel, iterations=3)
    # # cv2.imshow("fg", fg)
    # bg = cv2.dilate(watershed_mask, kernel, iterations=4)
    # bg = cv2.dilate(bg, (15, 15), iterations=4)
    # cv2.imshow("bg", bg)
    # ret, bg_bin = cv2.threshold(bg, 1, 128, cv2.THRESH_BINARY_INV)
    # cv2.imshow("bg_bin", bg_bin)

    # markers = fg + bg_bin
    # cv2.imshow("markers", markers)

    # markers = markers.astype(np.int32)
    # markers = cv2.watershed(img, markers)
    # img[markers == -1] = [255, 0, 0]
    # cv2.imshow("water_img", img)q

    _, contours, _ = cv2.findContours(bin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cmax = max(contours, key=cv2.contourArea)

    # epsilon = 0.000001*cv2.arcLength(cmax,True)
    # cmax = cv2.approxPolyDP(cmax,epsilon,True)
    cv2.drawContours(frame, [cmax], 0, (55, 55, 251), 1)  # red
    cv2.drawContours(img, [cmax], 0, (55, 55, 251), 1)  # red
    return img, bin_mask, res, cmax


def gravity(image, gray, contours):
    # print("countours 0",contours)
    only_hand = np.zeros(shape=gray.shape)
    # save_zeros = save_zeros.astype(np.int32)
    cv2.drawContours(only_hand, [contours], 0, 255, cv2.FILLED)
    #     cv2.imshow("only_hand", only_hand)
    moments = cv2.moments(contours)
    m00 = moments['m00']

    c_x, c_y = None, None
    if m00 != 0:
        c_x = int(moments['m10'] / m00)  # Take X coordinate
        c_y = int(moments['m01'] / m00)  # Take Y coordinate
    print("c_x: {},c_y: {}".format(c_x, c_y))
    ctr = (-1, -1)
    if c_x != None and c_y != None:
        ctr = (c_x, c_y)
        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 5, (255, 255, 255), -1)
    index = 0
    cnt = 0
    dis_sum = 0.
    size_of_contours = len(contours)
    # Threshold_update = 140
    Threshold_update = int(0.07 * size_of_contours)
    print("size_of_contours", size_of_contours)
    print("Threshold", Threshold_update)
    finger_Candidate = list()
    distances = list()
    for id, point in enumerate(contours):
        point = point[0]
        dis = (point[0] - c_x) ** 2 + (point[1] - c_y) ** 2
        distances.append(dis)
        dis_sum += dis
    ave_dis_sum = dis_sum / size_of_contours
    finger_dis = ave_dis_sum * 1.2
    ## smooth the distances with five steps (i-2,i-1,i,i+1,i+2) --> i
    L_of_distances = len(distances)
    distances_smooth = list()
    for x, h in enumerate(distances):
        if x < 2:
            dis_ave = h
        if x + 2 == L_of_distances:
            break
        else:
            dis_ave = (distances[x - 2] + distances[x - 1] + distances[x] + distances[x + 1] + distances[x + 2]) / 5.
        distances_smooth.append(dis_ave)

    mx = 0.
    update = False
    angel = Curvature(contours, 20)
    print("cosPI/6:", np.cos(np.pi / 6))
    for i, h in enumerate(distances_smooth):

        point = contours[i][0]
        if h > mx:
            mx = h
            index = i
            update = True
        else:
            update = False
        if update is False:
            cnt += 1
            if cnt > Threshold_update:

                # if distances_smooth[index] >= finger_dis and -0.7 <angel[index]:

                # angel[index] > np.cos(np.pi / 6)
                import math
                # if distances_smooth[index] >= finger_dis:

                # acos math domain
                if -1 <= angel[index] <= 1:
                    if distances_smooth[index] >= finger_dis and 20 < 180 * math.acos(angel[index]) / math.pi < 90:
                        cnt = 0
                        mx = 0
                        mx_point = contours[index][0]
                        print("angel index:", index, "|angel:", angel[index], "|theta:",
                              180 * math.acos(angel[index]) / math.pi,
                              "|mx_point:", mx_point)
                        finger_Candidate.append(mx_point)
                        cv2.circle(image, (mx_point[0], mx_point[1]), 9, (0, 255, 255), -1)

    # plt.bar(np.arange(len(distances)), distances)
    # plt.show()
    # plt.bar(np.arange(len(distances_smooth)), distances_smooth)
    # plt.show()
    print("finger_Candidate", finger_Candidate)
    print("distances", distances)

    # cv2.imshow("gravity", image)


def derived_gravity(image, gray, contours):
    only_hand = np.zeros(shape=gray.shape)
    cv2.drawContours(only_hand, [contours], 0, 255, cv2.FILLED)
    # cv2.imshow("only_hand", only_hand)
    moments = cv2.moments(contours)
    m00 = moments['m00']

    c_x, c_y = None, None
    if m00 != 0:
        c_x = int(moments['m10'] / m00)  # Take X coordinate
        c_y = int(moments['m01'] / m00)  # Take Y coordinate
    print("c_x: {},c_y: {}".format(c_x, c_y))
    ctr = (-1, -1)
    if c_x != None and c_y != None:
        ctr = (c_x, c_y)
        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 5, (255, 255, 255), -1)
    dis_sum = 0.
    size_of_contours = len(contours)
    print("size_of_contours", size_of_contours)
    finger_Candidate = list()
    distances = list()
    for id, point in enumerate(contours):
        point = point[0]
        dis = (point[0] - c_x) ** 2 + (point[1] - c_y) ** 2
        distances.append(dis)
        dis_sum += dis
    ave_dis_sum = dis_sum / size_of_contours
    finger_dis = ave_dis_sum * 1.6

    ## smooth the distances with five steps (i-2,i-1,i,i+1,i+2) --> i


    def smooth_array(A):
        smooth = list()
        L_of_A = len(A)
        for x, h in enumerate(A):
            if x < 2:
                ave = h
            if x + 2 == L_of_A:
                break
            else:
                ave = (A[x - 2] + A[x - 1] + A[x] + A[x + 1] + A[x + 2]) / 5.
                smooth.append(ave)

        return smooth

    distances_smooth = smooth_array(distances)
    dif_distances_smooth = list()
    for i, h in enumerate(distances_smooth):
        if i == 1:
            continue
        if i == 2:
            dif = distances_smooth[i] - distances_smooth[i - 1]
            dif_distances_smooth.append(dif)
            dif_distances_smooth.append(dif)
        else:
            dif = distances_smooth[i] - distances_smooth[i - 1]
            dif_distances_smooth.append(dif)
    dif_dis = smooth_array(dif_distances_smooth)
    for i, sub in enumerate(dif_dis):
        if i < 2:
            continue
        if i + 3 >= len(dif_dis):
            break
        if dif_dis[i - 2] > 0 and dif_dis[i - 1] > 0 and dif_dis[i] >= 0 and dif_dis[i + 1] <= 0 and dif_dis[
                    i + 2] < 0 and dif_dis[i + 3] < 0:
            mx_point = contours[i][0]
            if distances_smooth[i] > finger_dis:
                finger_Candidate.append(mx_point)
                cv2.circle(image, (mx_point[0], mx_point[1]), 9, (0, 255, 255), -1)
    # plt.bar(np.arange(len(distances)), distances)
    # plt.show()
    # plt.bar(np.arange(len(distances_smooth)), distances_smooth)
    # plt.show()
    print("finger_Candidate", finger_Candidate)
    print("distances", distances)


def Curvature(contours, step):
    size_of_contours = len(contours)
    L_of_contours = len(contours)
    angel = [-1] * L_of_contours
    for id, point in enumerate(contours):
        if id < step and id + step < L_of_contours:
            p = point[0]
            p_pre = contours[L_of_contours - step][0]
            p_nxt = contours[id + step][0]
        if id + step >= size_of_contours:
            p = point[0]
            p_pre = contours[id - step][0]
            p_nxt = contours[id + step - L_of_contours][0]
        else:
            p = point[0]
            p_pre = contours[id - step][0]
            p_nxt = contours[id + step][0]
        p2p_pre = p - p_pre
        p2p_nxt = p - p_nxt
        dot_p = np.dot(p2p_pre, p2p_nxt.T)
        cos_p = dot_p / (np.linalg.norm(p2p_pre) * np.linalg.norm(p2p_nxt))
        angel[id] = cos_p
    # for i, a in enumerate(angel[:step]):
    #     angel[i] = angel[step]
    print(angel)
    return angel
    # print("angel:", angel)
    # if -20 < angel < 20:
    #     cross = np.cross(p2p_pre, p2p_nxt)
    #     print("cross!!!!!!:", cross)
    #     if cross > 0:
    #         finger_Candidate.append(point)
    #         print("point:", p)
    #         cv2.circle(image, (p[0], p[1]), 9, (0, 255, 255), -1)
    #
    #         # cv2.circle(bin_mask, (point[0], point[1]), 9, (0, 255, 255), -1)

# img, bin_mask, cmax = find_hand(frame_read)
# derived_gravity(img, bin_mask, cmax)
# Curvature(img, bin_mask, cmax, 5)
# gray = bin_mask.copy()
# gravity(img, gray, cmax)
# cv2.namedWindow("img_deal")
# cv2.namedWindow("img")
# cv2.namedWindow("gray")
# cv2.namedWindow("BGR")
# cv2.namedWindow("Ycbcr")
# cv2.imshow("img", img)
# cv2.imshow("img_deal", frame)
# cv2.imshow("gray", gray)

# cv2.imshow("BGR",mask_frame_BGR)
# cv2.imshow("Ycbcr",mask_frame_gray)
# if cv2.waitKey(0) & 0xFF == ord("q"):
#     cv2.destroyAllWindows()

# cv2.waitKey(0)