import btfpy
import mediapipe as mp
import cv2
from gesture_recognition import get_hand_number,number_to_letter,letter_to_ascii,send_key

# 初始化 MediaPipe 和鍵盤模擬
drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands

# 接受藍芽後持續運行的主程式，
def lecallback2(clientnode,op,cticn):
    
    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 調整影像大小
            frame1 = cv2.resize(frame, (640, 480))
            rgb_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

            # 手部偵測
            results = hands.process(rgb_frame)

            # 繪製框架
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    drawingModule.draw_landmarks(frame1, hand_landmarks, handsModule.HAND_CONNECTIONS)


            if results.multi_hand_landmarks and len(results.multi_handedness)==2:
                # 確認每隻手都有完整的 21 個 Landmark
                hands_complete = all(len(hand_landmarks.landmark) == 21 for hand_landmarks in results.multi_hand_landmarks)
                if hands_complete:
                    # 儲存左右手的數字
                    left_hand_number = 0
                    right_hand_number = 0

                    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        # 繪製手部骨架
                        drawingModule.draw_landmarks(frame1, hand_landmarks, handsModule.HAND_CONNECTIONS)

                        # 獲取手部標記的資訊
                        landmarks = hand_landmarks.landmark

                        # 判斷是哪隻手
                        hand_label = results.multi_handedness[idx].classification[0].label  # 左手或右手
                        wrist = landmarks[0]
                        palm_center = landmarks[9]
                        #print(palm_center.y)
                        #print(wrist.y)
                        print('-------------------------------------')
                        # more right , x bigger
                        # more lower , y bigger

                        # 判斷手掌方向（掌心朝向攝影機）
                        if palm_center.z < wrist.z:  # 手心朝向鏡頭
                            hand_number = get_hand_number(landmarks, hand_label)
                            
                            # left and right oppositely
                            if hand_label == "Left":
                                right_hand_number = hand_number
                            elif hand_label == "Right":
                                left_hand_number = hand_number

                    # 計算最終數字並映射到字母
                    total_number = left_hand_number * 10 + right_hand_number
                    print(number_to_letter(total_number))
                    send_key(letter_to_ascii(number_to_letter(total_number)))

            # 顯示影像
            cv2.imshow("Frame", frame1)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    if(op == btfpy.LE_DISCONNECT):
        return(btfpy.SERVER_EXIT)
    return(btfpy.SERVER_CONTINUE)