import btfpy
import mediapipe as mp
import cv2
#from pynput.keyboard import Controller

# 初始化 MediaPipe 和鍵盤模擬
drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands
#keyboard = Controller()  # 模擬鍵盤輸入

# 定義手勢變數字
def get_hand_number(landmarks, hand_label):
    # 每根手指的尖端和中節關節
    finger_tips = [8, 12, 16, 20]  # 食指、中指、無名指、小指
    finger_dips = [6, 10, 14, 18]
    fingers = []
    
    # 判斷大拇指
    thumb_tip = landmarks[4]  # 大拇指尖端
    index_mcp = landmarks[3]  
    if hand_label == "Left":  # left hand
        if thumb_tip.x > index_mcp.x:  # 大拇指在掌根外側
            fingers.append(1)
        else:
            fingers.append(0)
    elif hand_label == "Right":  # right hand
        if thumb_tip.x < index_mcp.x:  # 大拇指在掌根外側
            fingers.append(1)
        else:
            fingers.append(0)


    for tip, dip in zip(finger_tips, finger_dips):
        # 判斷是否伸展
        if landmarks[tip].y < landmarks[dip].y:  # Y 座標越小越高
            fingers.append(1)
        else :
            fingers.append(0)
    if fingers == [1,0,0,0,1]:
        return 6
    elif fingers == [1,1,0,0,0]:
        return 7
    elif fingers == [1,1,1,0,0]:
        return 8
    elif fingers == [1,1,1,1,0]:
        return 9
    
    return sum(fingers)

# 將數字變成對應的鍵盤內容
def number_to_letter(number):
    """
    將數字映射到英文字母。
    :param number: 數字（例如 11、12、13）
    :return: 對應的英文字母（例如 'a', 'b', 'c'）
    """
    mapping = {
        1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
        10: '0', 11: 'a', 12: 'b', 13: 'c', 14: 'd', 15: 'e', 16: 'f', 17: 'g', 18: 'h', 19: 'i',
        20: 'j', 21: 'k', 22: 'l', 23: 'm', 24: 'n',25: 'o', 26: 'p', 27: 'q', 28: 'r', 29: 's',
        30: 't', 31: 'u', 32: 'v', 33: 'w', 34: 'x', 35: 'y', 36: 'z', 37: ',', 38 : '.',39 : '?',
        41: '+', 42: '-', 43: '*', 44: '/', 45: '=', 46: 'up' , 47: 'down' , 48 : 'left' , 49 : 'right',
        51: 'backspace', 52: 'space', 53: 'enter', 54: 'tab', 55: 'capslock', 56: 'shift', 57: 'ctrl', 58: 'alt',
        61: '(',62: ')', 63: '[', 64: ']', 65: '{', 66: '}', 67: '<', 68: '>',
        70: 'esc', 71: 'f1' , 72: 'f2', 73: 'f3', 74: 'f4',75: 'f5' , 76: 'f6', 77: 'f7', 78: 'f8',79: 'f9' , 
        80: 'f10', 81: 'f11', 82: 'f12',83: ';', 84: ':', 85: 'single', 86: 'double', 87: 'reverse', 88: '|' ,89: '_',
        90: '~', 91: '!', 92: '@', 93: '#', 94: '$', 95:'%', 96: '^', 97:'&', 98: '`', 99: 'close'        
    }
    
    # 如果數字存在於映射表中，返回對應的字母
    return mapping.get(number, " ")  # 返回對應字符

# 對鍵盤輸入內容做預處理，方便後續程式運行
def letter_to_ascii(letter):
    # 特殊鍵映射表
    special_keys = {
        ',' : ',',
        '.' : '.',
        '?' : '?',
        '+' : '+',
        '-' : '-',
        '*' : '*',
        '/' : '/',
        '=' : '=',
        'up': 31,
        'down': 30,
        'left': 29,
        'right': 28,
        'backspace': 8,
        'enter': 10,
        'space': 'space',   # HID 編碼 for Space
        'tab': 9,
        'capslock' : 'capslock',
        'shift': 'shift',   # HID 編碼 for Left Shift
        'ctrl': 'ctrl',
        'alt' : 'alt',
        '(' : '(',
        ')' : ')',
        '[' : '[',
        ']' : ']',
        '{' : '{',
        '}' : '}',
        '<' : '<',
        '>' : '>',
        'esc': 27,
        'f1' : 14,
        'f2' : 15,
        'f3' : 16,
        'f4' : 17,
        'f5' : 18,
        'f6' : 19,
        'f7' : 20,
        'f8' : 21,
        'f9' : 22,
        'f10' : 23,
        'f11' : 24,
        'f12' : 25,
        ';' : ';',
        ':' : ':',
        'single' : 'single',
        'double' : 'double',
        'reverse' : 'reverse',
        '|' : '|',
        '_' : '_',
        '~' : '~',
        '!' : '!',
        '@' : '@',
        '#' : '#',
        '$' : '$',
        '%' : '%',
        '^' : '^',
        '&' : '&',
        '`' : '`',
        'close': 'close'    # Custom key for 'close'
    }
    
    # 判斷是否為數字
    if letter.isdigit():
        return int(letter) + 48  # ASCII 值對應數字鍵
    # 判斷是否為單個字母
    elif letter.isalpha() and len(letter) == 1:
        return ord(letter.lower())  # 返回小寫字母的 ASCII 值
    # 查找特殊鍵映射
    elif letter in special_keys:
        return special_keys[letter]
    # 無效輸入返回 0
    return 0


# 啟動攝影機
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 4)

#基本的藍芽連線設定
reportmap = [0x05,0x01,0x09,0x06,0xA1,0x01,0x85,0x01,0x05,0x07,0x19,0xE0,0x29,0xE7,0x15,0x00,\
             0x25,0x01,0x75,0x01,0x95,0x08,0x81,0x02,0x95,0x01,0x75,0x08,0x81,0x01,0x95,0x06,\
             0x75,0x08,0x15,0x00,0x25,0x65,0x05,0x07,0x19,0x00,0x29,0x65,0x81,0x00,0xC0]
 
report = [0,0,0,0,0,0,0,0]

name = "HID"
appear = [0xC1,0x03]  # 03C1 = keyboard icon appears on connecting device 
pnpinfo = [0x02,0x6B,0x1D,0x46,0x02,0x37,0x05]
protocolmode = [0x01]
hidinfo = [0x01,0x11,0x00,0x02]
battery = [100] 
reportindex = -1
node = 0

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
 

# 將前面預處理好的鍵盤內容傳輸出去
# 如果是兩種鍵盤才能輸入的(ex: _ 要 shift + -)則要額外修改modifier，modifier為額外要按的鍵(ex: shift)，hidcode則填你原本需要按的(ex : -，這邊 - 的hidcode為0x2D，每個鍵都不一樣需要額外查)
def send_key(key):
    global reportindex
    global node
    
    hidcode = 0
    modifier = 0
    # convert btferret code (key) to HID code
    if(key == ','):
        hidcode = 0x36
    elif(key == '.'):
        hidcode = 0x37
    elif(key == '?'):
        modifier = 0x02
        hidcode = 0x38
    elif(key == '+'):
        modifier = 0x02
        hidcode = 0x2E
    elif (key == '-'):
        hidcode = 0x2D
    elif (key == '*'):
        hidcode = 0x55
    elif (key == '/'):
        hidcode = 0x54
    elif (key == '='):
        hidcode = 0x2E
    elif(key == 'space'):
        hidcode = 0x2C
    elif(key == 'capslock'):
        hidcode = 0x39
    elif(key == 'shift'):
        modifier = 0x02  # 左 Shift HID 修飾符
        buf = [modifier, 0, 0, 0, 0, 0, 0, 0]  # 包含 Shift 的按鍵報告
        btfpy.Write_ctic(node, reportindex, buf, 0)
        buf = [0, 0, 0, 0, 0, 0, 0, 0]  # 釋放所有按鍵
        btfpy.Write_ctic(node, reportindex, buf, 0)
        return
    elif(key == 'ctrl'):
        modifier = 0x01
        buf = [modifier, 0, 0, 0, 0, 0, 0, 0]  # 包含 Ctrl 的按鍵報告
        btfpy.Write_ctic(node, reportindex, buf, 0)
        buf = [0, 0, 0, 0, 0, 0, 0, 0]  # 釋放所有按鍵
        btfpy.Write_ctic(node, reportindex, buf, 0)
        return
    elif(key == 'alt'):
        modifier = 0x04
        buf = [modifier, 0, 0, 0, 0, 0, 0, 0]  # 包含 Ctrl 的按鍵報告
        btfpy.Write_ctic(node, reportindex, buf, 0)
        buf = [0, 0, 0, 0, 0, 0, 0, 0]  # 釋放所有按鍵
        btfpy.Write_ctic(node, reportindex, buf, 0)
        return
    elif(key == '('):
        modifier = 0x02
        hidcode = 0x26
    elif(key == ')'):
        modifier = 0x02
        hidcode = 0x27
    elif(key == '['):
        hidcode = 0x2F
    elif(key == ']'):
        hidcode = 0x30
    elif(key == '{'):
        modifier = 0x02
        hidcode = 0x2F
    elif(key == '}'):
        modifier = 0x02
        hidcode = 0x30
    elif(key == '<'):
        modifier = 0x02
        hidcode = 0x36
    elif(key == '>'):
        modifier = 0x02
        hidcode = 0x37
    elif(key == ';'):
        hidcode =0x33
    elif(key == ':'):
        modifier = 0x02
        hidcode = 0x33
    elif(key == 'single'):
        hidcode = 0x34
    elif(key == 'double'):
        modifier = 0x02
        hidcode = 0x34
    elif(key == 'reverse'):
        hidcode = 0x31
    elif(key == '|'): 
        modifier = 0x02
        hidcode = 0x31
    elif(key == 'close'):
        cap.release()
        cv2.destroyAllWindows()
        exit(0)
    elif(key == '_'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x2D
    elif(key == '~'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x35
    elif(key == '!'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x1E
    elif(key == '@'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x1F
    elif(key == '#'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x20
    elif(key == '$'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x21
    elif(key == '%'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x22
    elif(key == '^'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x23
    elif(key == '&'):
        modifier = 0x02  # Shift 修飾符
        hidcode = 0x24
    elif(key == '`'):
        hidcode = 0x35
    else:
        hidcode = btfpy.Hid_key_code(key)
    
    if(hidcode == 0):
        return

    buf = [0,0,0,0,0,0,0,0] 
        
    # send key press to Report1
    buf[0] = modifier  # modifier
    buf[2] = hidcode & 0xFF         # key code
    btfpy.Write_ctic(node,reportindex,buf,0)
    # send no key pressed - all zero
    buf[0] = 0
    buf[2] = 0
    btfpy.Write_ctic(node,reportindex,buf,0) 
    return

############ 程式運行(藍芽連線部分) ###########
   
if(btfpy.Init_blue("keyboard.txt") == 0):
  exit(0)

if(btfpy.Localnode() != 1):
  print("ERROR - Edit keyboard.txt to set ADDRESS = " + btfpy.Device_address(btfpy.Localnode()))
  exit(0)
      
node = btfpy.Localnode()    

# look up Report1 index
uuid = [0x2A,0x4D]
reportindex = btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid)
if(reportindex < 0):
  print("Failed to find Report characteristic")
  exit(0)

  # Write data to local characteristics  node=local node
uuid = [0x2A,0x00]
btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),name,0) 

uuid = [0x2A,0x01]
btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),appear,0) 

uuid = [0x2A,0x4E]
btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),protocolmode,0)

uuid = [0x2A,0x4A]
btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),hidinfo,0)

uuid = [0x2A,0x4B]
btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),reportmap,0)

uuid = [0x2A,0x4D]
btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),report,0)

uuid = [0x2A,0x50]
btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),pnpinfo,0)
   
  #**** battery level *****
  # uuid = [0x2A,0x19]
  # btfpy.Write_ctic(node,btfpy.Find_ctic_index(node,btfpy.UUID_2,uuid),battery,1) 
  #************************     
                          
  # Set unchanging random address by hard-coding a fixed value.
  # If connection produces an "Attempting Classic connection"
  # error then choose a different address.
  # If set_le_random_address() is not called, the system will set a
  # new and different random address every time this code is run.  
 
  # Choose the following 6 numbers
  # 2 hi bits of first number must be 1
randadd = [0xD3,0x56,0xDB,0x15,0x32,0xA0]
btfpy.Set_le_random_address(randadd)
     
btfpy.Keys_to_callback(btfpy.KEY_ON,0)   # enable LE_KEYPRESS calls in lecallback2
                                         # 0 = GB keyboard  
btfpy.Set_le_wait(20000)  # Allow 20 seconds for connection to complete
                                         
btfpy.Le_pair(btfpy.Localnode(),btfpy.JUST_WORKS,0)  # Easiest option, but if client requires
                                                     # passkey security - remove this command  

btfpy.Le_server(lecallback2,0) #連線後執行主程式(手勢辨識)
  
btfpy.Close_all()