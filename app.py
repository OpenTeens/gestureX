#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PLUGINS:
- blackboard
- mouse
- keyboard


PLUGIN USAGE:
- plugin.blackboard
   - press 'p' to switch to the pen
   - press 'e' to switch to the eraser
   - press 'c' to clear the board

"""
import os

print("Loading Plugins ... ")

import csv
import copy
import argparse
import itertools
# 统计“可迭代序列”中每个元素的出现的次数
from collections import Counter
# 实现了两端都可以操作的队列，相当于双端队列
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier

# plug-in
import plugin.blackboard
import plugin.mouse
import plugin.keyboard
import plugin.UI
import plugin.stablediffusion
import plugin.text_pad

blackboard_fn_backup = blackboard_fn = plugin.blackboard.none

plugin.mouse.disable(True)
plugin.keyboard.disable(True)
plugin.blackboard.disable(True)
plugin.text_pad(True)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=1280)
    parser.add_argument("--height", help='cap height', type=int, default=720)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args


def main():
    print("Done.")  # opening plugins

    global blackboard_fn, blackboard_fn_backup

    # 参数解析 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    print("Opening Camera ... ")
    # 相机准备 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    print("Done.")
    # 模型载荷 #############################################################
    # STATIC_IMAGE_MODE:如果设置为 false，该解决方案会将输入图像视为视频流。它将尝试在第一个输入图像中检测手，并在成功检测后进一步定位手的地标。在随后的图像中，一旦检测到所有 max_num_hands 手并定位了相应的手的地标，它就会简单地跟踪这些地标，而不会调用另一个检测，直到它失去对任何一只手的跟踪。这减少了延迟，非常适合处理视频帧。如果设置为 true，则在每个输入图像上运行手部检测，非常适合处理一批静态的、可能不相关的图像。默认为false。
    # STATIC_IMAGE_MODE:如果设置为 false，该解决方案会将输入图像视为视频流。它将尝试在第一个输入图像中检测手，并在成功检测后进一步定位手的地标。在随后的图像中，一旦检测到所有 max_num_hands 手并定位了相应的手的地标，它就会简单地跟踪这些地标，而不会调用另一个检测，直到它失去对任何一只手的跟踪。这减少了延迟，非常适合处理视频帧。如果设置为 true，则在每个输入图像上运行手部检测，非常适合处理一批静态的、可能不相关的图像。默认为false。
    # MAX_NUM_HANDS：要检测的最多的手数量。默认为2。
    # MIN_DETECTION_CONFIDENCE：来自手部检测模型的最小置信值 ([0.0, 1.0])，用于将检测视为成功。默认为 0.5。
    # MIN_TRACKING_CONFIDENCE:来自地标跟踪模型的最小置信值 ([0.0, 1.0])，用于将手部地标视为成功跟踪，
    # 否则将在下一个输入图像上自动调用手部检测。将其设置为更高的值可以提高解决方案的稳健性，但代价是更高的延迟。如果 static_image_mode 为真，则忽这个参数略，手部检测将在每个图像上运行。默认为 0.5。

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    keypoint_classifier = KeyPointClassifier()

    point_history_classifier = PointHistoryClassifier()

    # 标签加载 ###########################################################
    with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]
    with open('model/point_history_classifier/point_history_classifier_label.csv', encoding='utf-8-sig') as f:
        point_history_classifier_labels = csv.reader(f)
        point_history_classifier_labels = [
            row[0] for row in point_history_classifier_labels
        ]

    # FPS测量模块 ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=10)

    # 历史坐标 #################################################################
    history_length = 16
    point_history = deque(maxlen=history_length)

    # 手势历史 ################################################
    finger_gesture_history = deque(maxlen=history_length)

    #  ########################################################################
    mode = 0
    mouse_pressed_down = False
    button_pressed_down = False
    pos = None
    if os.path.exists("result.png"):
        os.remove("result.png")
    while True:
        fps = cvFpsCalc.get()

        # 相机捕获 #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # 镜面显示
        debug_image = copy.deepcopy(image)

        # 按键处理(ESC：终止) #################################################
        key = cv.waitKey(10)

        if 49 <= key <= 58:
            plugin.blackboard.changeThickness(key)
        if key == 27:  # ESC
            break
        if key == 112:  # p for pen
            blackboard_fn_backup = blackboard_fn = plugin.blackboard.pen
        if key == 101:  # e for eraser
            blackboard_fn_backup = blackboard_fn = plugin.blackboard.erase
        if key == 99:  # c for clear
            plugin.blackboard.clear()
            plugin.stablediffusion.clear()
            blackboard_fn_backup = blackboard_fn = plugin.blackboard.none
        if key == 115:  # s for save
            plugin.blackboard.save()
        if key == 100:  # d for diffusion
            img, pos = plugin.blackboard.export(1)
            cv.imwrite("sd_input.png", img)
            plugin.stablediffusion.generate_image()
        number, mode = select_mode(key, mode)

        # 检测实施 #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        #  ####################################################################
        detected_hand = results.multi_hand_landmarks
        if detected_hand is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # 计算边界矩形
                # brect = calc_bounding_rect(debug_image, hand_landmarks)
                # 计算手指坐标
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # plugin
                blackboard_fn(landmark_list[8])  # finger No.8
                clicked_key = plugin.keyboard.check_on_keys(landmark_list[8])

                # 转换为相对坐标 & 归一化
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pre_processed_point_history_list = pre_process_point_history(debug_image, point_history)
                # 训练数据存储
                logging_csv(number, mode, pre_processed_landmark_list, pre_processed_point_history_list)

                # 手势分类
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                # if(300 < landmark_list[8][0] < 1000 and 40 < landmark_list[8][1] < 400):
                #    plugin.mouse.move_to(landmark_list[8])

                plugin.mouse.move_to(landmark_list[8])

                if hand_sign_id == 4:  # 4: click
                    if not button_pressed_down:
                        button, check_button, status = plugin.UI.check_on_buttons(landmark_list[8], debug_image)
                        if status is True:
                            status = False
                        else:
                            status = True

                        if check_button:
                            if button == 'blackboard':
                                plugin.blackboard.disable(status)
                            elif button == 'mouse':
                                plugin.mouse.disable(status)
                            else:
                                plugin.keyboard.disable(status)
                        button_pressed_down = True

                    if mouse_pressed_down is False:
                        plugin.mouse.mouse_press()
                        mouse_pressed_down = True

                    if clicked_key:
                        plugin.keyboard.press(clicked_key)

                    if blackboard_fn is plugin.blackboard.none:
                        blackboard_fn = blackboard_fn_backup
                else:
                    if mouse_pressed_down:
                        plugin.mouse.mouse_up()
                        mouse_pressed_down = False

                    if button_pressed_down:
                        button_pressed_down = False

                    blackboard_fn = plugin.blackboard.none

                    if len(plugin.blackboard.history) != 0 and plugin.blackboard.history[-1][0] is not None:
                        plugin.blackboard.pen([None, None])  # 断开

                    plugin.keyboard.release()

                # 手指手势分类
                finger_gesture_id = 0
                point_history_len = len(pre_processed_point_history_list)
                if point_history_len == (history_length * 2):
                    finger_gesture_id = point_history_classifier(pre_processed_point_history_list)

                # 计算最新检测中概率最大的手势 ID
                finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(finger_gesture_history).most_common()

                # 绘图
                # debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)

                cv.putText(debug_image, keypoint_classifier_labels[hand_sign_id], (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1,
                           (0, 0, 255), 2)
        else:
            # didn't have a result
            point_history.append([0, 0])
            # plugin.blackboard.pen([None, None])  # -1 represents all.

        debug_image = draw_info(debug_image, fps, mode, number)

        # plugin显示 #############################################################
        plugin.UI.buttons(debug_image)
        plugin.keyboard.print_rec(debug_image)  # keyboard plugin
        plugin.blackboard.draw_all_buttons(debug_image)
        plugin.blackboard.print_history(debug_image)
        plugin.blackboard.choose_color(landmark_list[8] if detected_hand else [0, 0])
        plugin.mouse.print_touchboard(debug_image)

        if pos:
            plugin.stablediffusion.render_image_overlay(debug_image, pos)

        # 显示画面 #############################################################
        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    if key == 104:  # h
        mode = 2
    return number, mode


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # 手指坐标
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z * 10

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # 转换为相对坐标
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # 转换为一维列表
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

    # 归一化
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def pre_process_point_history(image, point_history):
    image_width, image_height = image.shape[1], image.shape[0]

    temp_point_history = copy.deepcopy(point_history)

    # 转换为相对坐标
    base_x, base_y = 0, 0
    for index, point in enumerate(temp_point_history):
        if index == 0:
            base_x, base_y = point[0], point[1]

        temp_point_history[index][0] = (temp_point_history[index][0] - base_x) / image_width
        temp_point_history[index][1] = (temp_point_history[index][1] - base_y) / image_height

    # 转换为一维列表
    temp_point_history = list(itertools.chain.from_iterable(temp_point_history))

    return temp_point_history


def logging_csv(number, mode, landmark_list, point_history_list):
    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        csv_path = 'model/keypoint_classifier/keypoint.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
    if mode == 2 and (0 <= number <= 9):
        csv_path = 'model/point_history_classifier/point_history.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *point_history_list])
    return


def draw_landmarks(image, landmark_point):
    # 手指连线
    if len(landmark_point) > 0:
        # 大拇指
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), (255, 255, 255), 2)

        # 食指
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), (255, 255, 255), 2)

        # 中指
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), (255, 255, 255), 2)

        # 无名指
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), (255, 255, 255), 2)

        # 小指
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), (255, 255, 255), 2)

        # 手腕
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), (255, 255, 255), 2)

    # 手腕
    for index, landmark in enumerate(landmark_point):
        """
        使用标准的关键点规范。
        """
        if index == 0:  # 手腕1
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 1:  # 手腕2
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 2:  # 大拇指：指根
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 3:  # 大拇指：第1关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 4:  # 大拇指：指尖
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 5:  # 食指：指根
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 6:  # 食指：第2关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 7:  # 食指：第1关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 8:  # 食指：指尖
            if blackboard_fn is plugin.blackboard.erase:
                cv.circle(image, (landmark[0], landmark[1]), 15, (225, 255, 225), 2)
            else:
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255), -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 9:  # 中指：指跟
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 10:  # 中指：第2关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 11:  # 中指：第1关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 12:  # 中指：指尖
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 13:  # 无名指：指根
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 14:  # 无名指：第2关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 15:  # 无名指：第1关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 16:  # 无名指：指尖
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 17:  # 小指：指根
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 18:  # 小指：第2关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 19:  # 小指：第1关节
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 20:  # 小指：指尖
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255), -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

    return image


def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # 外接矩形
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 0, 0), 1)

    return image


def draw_info(image, fps, mode, number):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv.LINE_AA)
    if plugin.stablediffusion.generating_image:
        cv.putText(image, "Generating ... ", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 225), 2, cv.LINE_AA)

    mode_string = ['Logging Key Point', 'Logging Point History']
    if 1 <= mode <= 2:
        cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                   cv.LINE_AA)
        if 0 <= number <= 9:
            cv.putText(image, "NUM:" + str(number), (10, 110), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                       cv.LINE_AA)
    return image


if __name__ == '__main__':
    main()
