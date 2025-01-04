import btfpy
import mediapipe as mp
import cv2

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