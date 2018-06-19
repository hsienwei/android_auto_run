import cv2
import numpy as np
import os
import time
import datetime

DEBUG_TOUCH = True

def screen_capture(file_name):
    os.system('adb shell screencap -p /sdcard/Download/'+ file_name +'.png') 
    os.system('adb pull /sdcard/Download/'+ file_name +'.png') 
    os.system('adb shell rm /sdcard/Download/'+ file_name +'.png')

def find_template_exist(target_pic_name, template_pic_Name, threshold):
    print('find ' + template_pic_Name +' in ' + target_pic_name)
    img = cv2.imread(target_pic_name) 
    img2 = cv2.imread(template_pic_Name) 
    w = img2.shape[1]
    h = img2.shape[0]   
    result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
    
    loc = np.where( result >= threshold)
        
    test_data = list(zip(*loc[::-1]))
    print(test_data)
    is_match = len(test_data) > 0
    point = []
    if is_match:
        point.append((test_data[0][0] + w/2, test_data[0][1] + h/2 ))

    return is_match, point

def touch_screen(pos):
    cmd = 'adb shell input tap ' + str(pos[0]) + ' ' + str(pos[1])
    print('cmd:'+ cmd)
    os.system(cmd)
    
    if DEBUG_TOUCH:
        template = cv2.imread('temp.png')
        cv2.rectangle(template,(int(pos[0]), int(pos[1])), (int(pos[0]) + 5, int(pos[1] + 5)), 255, 2)

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        cv2.imwrite(st +'.jpg', template, [cv2.IMWRITE_JPEG_QUALITY, 80])
    time.sleep(3)



#ref : http://cuteparrot.pixnet.net/blog/post/190898697-%5Bandroid%5D%E5%9C%A8-adb-shell%E4%B8%8B%E5%88%A9%E7%94%A8-screencap-%E6%8A%93%E5%9C%96%E6%8C%87%E4%BB%A4%E6%8A%93%E5%9C%96

#screen_capture('temp')

# ref : http://zwindr.blogspot.com/2017/02/python-opencv-matchtemplate.html


#result = []
#is_match = find_template_exist("s1.png", "s1_s.png", 0.9,  result)
def check_is_auto_battle():
    is_match, result = find_template_exist("temp.png", "part_endauto.png", 0.9)
    if is_match:
        print('is auto battle state, wait...')
        time.sleep(15)
        return 1
    print('battle end')    
    return 3    

def idle():
    print('just idle')
    return 2   

def test_idle():
    print('test')
    return 4    

def check_battle_end_state():

    is_match, result = find_template_exist("temp.png", "part_sure.png", 0.9)
    if is_match:
        touch_screen(result[0])
    screen_capture('temp')
    is_match, result = find_template_exist("temp.png", "part_gopack.png", 0.9)
    if is_match:
        touch_screen(result[0])
        return 5  
    return 2    

def check_is_in_pack():
    while True:
        is_match, result = find_template_exist("temp.png", "part_packtitle.png", 0.9)

        if is_match:
            time.sleep(10) # 有時會有成就提示造成判斷錯誤
            is_match2, result2 = find_template_exist("temp.png", "part_broke.png", 0.9)
            if is_match2:
                touch_screen(result2[0])
                return 6
            else: 
                print(result2)
                print('not find item broke btn')
                return 2
        else:
            time.sleep(10)    
            screen_capture('temp')

def check_patch_broke():
    is_match, result = find_template_exist("temp.png", "part_patch_broke.png", 0.9)
    if is_match:
        touch_screen(result[0])
        return 7
    else:
        print('not find part_patch_broke') 
        return 2        

def check_patch_broke_ok():
    is_match, result = find_template_exist("temp.png", "part_broke2.png", 0.9)
    if is_match:
        touch_screen(result[0])
        return 8
    else:
        print('not find part_patch_broke') 
        return 2       

def check_patch_broke_ok_check():
    is_match, result = find_template_exist("temp.png", "part_ok.png", 0.9)
    if is_match:
        touch_screen(result[0])
        return 9
    else:
        print('not find part_patch_broke') 
        return 2                    

def broke_item_pass():
    while True:
        is_match, result = find_template_exist("temp.png", "part_broke_done.png", 0.9)
        if is_match:
            touch_screen(result[0])
            screen_capture('temp')
        else:
            break
    return 10        

def back_battle_info():
    while True:
        is_match, result = find_template_exist("temp.png", "part_packtitle.png", 0.9)
        if is_match:
            touch_screen(result[0])
            break
    return 11

def enter_battle():
    is_match, result = find_template_exist("temp.png", "part_icon_ready_fight.png", 0.9)
    if is_match:
        touch_screen(result[0])
    screen_capture('temp')
    while True:
        is_match, result = find_template_exist("temp.png", "part_ready_fight.png", 0.9)
        if is_match:
            touch_screen(result[0])
            break
    return 12

def enter_battle_repeat():
    while True:
        is_match, result = find_template_exist("temp.png", "part_auto_repeat.png", 0.9)
        if is_match:
            touch_screen(result[0])
            break
    screen_capture('temp')
    while True:
        is_match, result = find_template_exist("temp.png", "part_sure.png", 0.9)        
        if is_match:
            touch_screen(result[0])
            break

    return 1 

state_func = { 1: check_is_auto_battle,
               2: idle ,
               3: check_battle_end_state ,
               4: test_idle ,
               5: check_is_in_pack ,
               6: check_patch_broke ,
               7: check_patch_broke_ok,
               8: check_patch_broke_ok_check,
               9: broke_item_pass,
               10: back_battle_info,
               11 :enter_battle,
               12:enter_battle_repeat
                }



if __name__ == "__main__":
    state = 1
    while True:
        screen_capture('temp')
        state = state_func[state]() 
        
    print('end')
    


#ref : http://bigdata.51cto.com/art/201709/552579.htm  阈值檢測

# ref: https://zhuanlan.zhihu.com/p/30936804   特徵檢測
# matchtemplate一定會有結果  感覺不是很好

#ref: https://blog.csdn.net/huiguixian/article/details/11925389

#input tap <x> <y>
#input swipe <x1> <y1> <x2> <y2>