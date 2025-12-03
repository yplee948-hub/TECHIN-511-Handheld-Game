import time
import random

import board
import busio
import digitalio
import neopixel

import adafruit_ssd1306
import adafruit_adxl34x


# =========================
#  I2C + 디스플레이 + 센서 설정
# =========================

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
time.sleep(0.2)

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

accel = adafruit_adxl34x.ADXL345(i2c)
accel.range = adafruit_adxl34x.Range.RANGE_4_G


# =========================
#  Rotary Encoder + 버튼
# =========================

rot_a = digitalio.DigitalInOut(board.D1)
rot_a.direction = digitalio.Direction.INPUT
rot_a.pull = digitalio.Pull.UP

rot_b = digitalio.DigitalInOut(board.D2)
rot_b.direction = digitalio.Direction.INPUT
rot_b.pull = digitalio.Pull.UP

rot_btn = digitalio.DigitalInOut(board.D3)
rot_btn.direction = digitalio.Direction.INPUT
rot_btn.pull = digitalio.Pull.UP


# =========================
#  NeoPixel (D6)
# =========================

pixels = neopixel.NeoPixel(board.D6, 1, brightness=0.3, auto_write=True)


def set_pixel_color(color):
    pixels[0] = color  # color = (R, G, B)


# =========================
#  OLED 헬퍼 함수
# =========================

def clear_oled():
    oled.fill(0)
    oled.show()


def show_lines(lines):
    oled.fill(0)
    y = 0
    for i, line in enumerate(lines):
        if i >= 4:
            break
        oled.text(line, 0, y, 1)
        y += 16
    oled.show()


# =========================
#  버튼 입력 함수
# =========================

def wait_for_button_press():
    while not rot_btn.value:
        pass

    last = rot_btn.value
    while True:
        now = rot_btn.value
        if last and (not now):
            time.sleep(0.15)
            return
        last = now
        time.sleep(0.01)


# =========================
#  ADXL 제스처 인식
# =========================

def read_filtered_accel(samples=5):
    sum_x = sum_y = sum_z = 0.0
    for _ in range(samples):
        x, y, z = accel.acceleration
        sum_x += x
        sum_y += y
        sum_z += z
        time.sleep(0.01)
    return sum_x / samples, sum_y / samples, sum_z / samples


def detect_gesture(timeout_sec):
    start = time.monotonic()
    base_x, base_y, base_z = read_filtered_accel()

    while (time.monotonic() - start) < timeout_sec:
        x, y, z = read_filtered_accel(3)
        dx = x - base_x
        dy = y - base_y

        threshold = 2.0
        gesture = None

        if abs(dx) > abs(dy) and abs(dx) > threshold:
            gesture = "LEFT" if dx > 0 else "RIGHT"
        elif abs(dy) > threshold:
            gesture = "UP" if dy > 0 else "DOWN"

        if gesture:
            return gesture

    return None


# =========================
#  게임 설정
# =========================

DIFFICULTIES = ["EASY", "MED", "HARD"]
TIME_LIMITS = {"EASY": 4.0, "MED": 2.5, "HARD": 1.5}
SCORE_PER_LEVEL = {"EASY": 10, "MED": 15, "HARD": 20}
MAX_HEARTS = 3

ACTIONS = ["FEED", "PLAY", "CLEAN", "SLEEP"]
ACTION_TO_GESTURE = {"FEED": "LEFT", "PLAY": "RIGHT", "CLEAN": "UP", "SLEEP": "DOWN"}


def pet_face(mood):
    if mood == "happy": return "(^_^)"
    if mood == "sad": return "(T_T)"
    if mood == "tired": return "(-_-)"
    return "(o_o)"


# =========================
#  펫 스프라이트
# =========================

EGG_SPRITE = [
    "0000011111000000","0001111111110000","0011111111111000","0111111111111100",
    "0111111111111100","1111111111111110","1111111111111110","1111111111111110",
    "1111111111111110","1111111111111110","1111111111111110","0111111111111100",
    "0111111111111100","0011111111111000","0001111111110000","0000011111000000"
]

BABY_SPRITE = [
    "00000000000000000000000000000000000000000",
"00000000000000001111111110000000000000000",
"00000000000000111100000111100000000000000",
"00000000000011100000000000111000000000000",
"00000000000110000000000000001100000000000",
"00000000001100000000000000000110000000000",
"00000000011000000000000000000011000000000",
"00000000110000000000000000000001100000000",
"00000001100000000000000000000000110000000",
"00000001000000000000000000000000010000000",
"00000011000000000000000000000000011000000",
"00000010000000000000000000000000001000000",
"00000110000000000000000000000000001100000",
"00000100000000000000000000000000000100000",
"00000100000000000000000000000000000100000",
"00001100000001110000000001110000000110000",
"00001100000001110000000001110000000110000",
"00001000000001110000000001110000000010000",
"00001000000000000000000000000000000010000",
"00001000000000000000000000000000000010000",
"00001000000000000000000000000000000010000",
"00001000000000000000000000000000000010000",
"00001000000000000000000000000000000010000",
"00001000000000000000000000000000000010000",
"00001100000000001111111110000000000110000",
"00001100000001111111111111110000000110000",
"00000100000011110000000001111000000100000",
"00000100000110000000000000001100000100000",
"00000110000100000000000000000100001100000",
"00000010000000000000000000000000001000000",
"00000011000000000000000000000000011000000",
"00000001000000000000000000000000010000000",
"00000001100000000000000000000000110000000",
"00000000110000000000000000000001100000000",
"00000000011000000000000000000011000000000",
"00000000001100000000000000000110000000000",
"00000000000110000000000000001100000000000",
"00000000000011100000000000111000000000000",
"00000000000000111100000111100000000000000",
"00000000000000001111111110000000000000000",
"00000000000000000000000000000000000000000"
]

TEEN_SPRITE = [
"000011111000000001111111100000000",
"001111111111000011111111110000000",
"001111111111100011111111110000000",
"001111111111100011111111100000000",
"001111111111100011111111100000000",
"000011111111111111111111100000000",
"000001111111111111111111110000000",
"000001111111111111111111111000000",
"000011000111011111111111001100000",
"000010000111000000000111000111110",
"111110111000110011001001110110011",
"100110010000111111111000010011111",
"111110000000000000000000000010000",
"000010000000000000000000000010000",
"000011100000000000000000000110000",
"000011111110001111111111111100000",
"000010001111111111111100110000000",
"000011111000000000001111110000000"
]

ADULT_SPRITE = [
    "0000000000000000000000000000000000001111",
    "0000000111111110000000011111111000000000",
    "0000011111111111100000111111111110000000",
    "0000111111111111100000111111111110000000",
    "0000111111111111100001111111111111000000",
    "0000111111111111100001111111111111000000",
    "0000111111111111111111111111111111000000",
    "0000111111111111111111111111111111000000",
    "0011111111111111111111111111111111110000",
    "0111000011111111111111111111111111111000",
    "1100111111111110000001111111111000011100",
    "1100110111110111000011111111011100001100",
    "1000111111110011000011111111001100000100",
    "1100111111111110000011111111111100000100",
    "1100111111111000000000111111111110001100",
    "0111111111000011101110000001111110111000",
    "0011111110000001111110000000101111110000",
    "0000011111111111111111111111111100000000",
    "0000000000110111111111111011000000000000",
    "0000000001101100000000000111100000000000",
    "0000000001111100000000000111100000000000",
    "0000000000001101000000000100000000000000",
    "0000000000001111111111111100000000000000",
    "0000000000001110000000111100000000000000",
]


def draw_sprite(sprite, x, y, scale_x=1, scale_y=2):
    """
    가로는 scale_x, 세로는 scale_y로 늘리기
    (지금은 scale_x=1, scale_y=2로 세로만 키움)
    """
    for row, line in enumerate(sprite):
        for col, ch in enumerate(line):
            if ch == "1":
                px = x + col * scale_x
                py = y + row * scale_y
                for dy in range(scale_y):
                    for dx in range(scale_x):
                        oled.pixel(px + dx, py + dy, 1)


def get_stage(score):
    if score < 40: return "EGG"
    if score < 100: return "BABY"
    if score < 180: return "TEEN"
    return "ADULT"


def draw_pet_by_score(score):
    stage = get_stage(score)
    if stage == "EGG":
        sprite = EGG_SPRITE
    elif stage == "BABY":
        sprite = BABY_SPRITE
    elif stage == "TEEN":
        sprite = TEEN_SPRITE
    else:
        sprite = ADULT_SPRITE

    # 오른쪽에 세로만 2배로 길게 표시
    # TEEN은 가로가 길어서 x=84 정도로 살짝 안쪽에 배치
    draw_sprite(sprite, 84, 4, scale_x=1, scale_y=2)


# =========================
#  Splash Screen
# =========================

def splash_screen():
    clear_oled()
    set_pixel_color((0, 0, 50))

    for y in range(64, 0, -8):
        oled.fill(0)
        oled.text("TamaPet", 24, y, 1)
        oled.show()
        time.sleep(0.05)

    for i in range(4):
        oled.fill(0)
        oled.text("TamaPet", 28, 0, 1)
        face = "(^_^)" if i % 2 == 0 else "(-_-)"
        oled.text(face, 32, 24, 1)
        oled.text("Loading", 32, 48, 1)
        oled.show()
        time.sleep(0.3)

    clear_oled()


# =========================
#  화면들
# =========================

def start_screen():
    clear_oled()
    oled.text("TamaPet", 32, 8, 1)
    oled.text("Press Btn", 24, 28, 1)
    oled.text("to start", 28, 44, 1)
    oled.show()
    set_pixel_color((0, 0, 50))
    wait_for_button_press()


def select_difficulty():
    idx = 0
    last_a = rot_a.value
    last_btn = rot_btn.value

    while True:
        diff = DIFFICULTIES[idx]

        oled.fill(0)
        oled.text("Diff", 0, 0, 1)
        oled.text("> "+diff, 0, 16, 1)
        oled.text("Turn=chg", 0, 32, 1)
        oled.text("Press=OK", 0, 48, 1)
        oled.show()

        while True:
            a = rot_a.value
            b = rot_b.value

            if a != last_a:
                if not a:
                    idx = min(len(DIFFICULTIES)-1, idx+1) if b else max(0, idx-1)
                last_a = a
                break

            now_btn = rot_btn.value
            if last_btn and (not now_btn):
                time.sleep(0.15)
                oled.fill(0)
                oled.text("Diff OK", 0, 0, 1)
                oled.text(diff, 0, 16, 1)
                oled.text("Get ready", 0, 32, 1)
                oled.show()
                time.sleep(1.5)
                return diff

            last_btn = now_btn
            time.sleep(0.002)


# =========================
#  라운드
# =========================

def play_round(level, difficulty, score, hearts):
    """
    왼쪽: 텍스트 (대략 60%)
    오른쪽: 펫 (40%)
    """
    action = random.choice(ACTIONS)
    needed = ACTION_TO_GESTURE[action]
    limit = TIME_LIMITS[difficulty]

    oled.fill(0)

    # LEFT 텍스트 영역
    oled.text(f"H{hearts} S{score}", 0, 0, 1)
    oled.text(f"L{level} {difficulty[0]}", 0, 10, 1)
    oled.text(action, 0, 20, 1)
    oled.text("T:{:.1f}s".format(limit), 0, 30, 1)
    oled.text("Tilt →", 0, 45, 1)

    # RIGHT 펫
    draw_pet_by_score(score)

    oled.show()
    set_pixel_color((0, 0, 50))

    gesture = detect_gesture(limit)

    if gesture == needed:
        gained = SCORE_PER_LEVEL[difficulty]
        new_score = score + gained

        oled.fill(0)
        oled.text("GOOD!", 0, 0, 1)
        oled.text(f"+{gained}p", 0, 12, 1)
        oled.text("Score:", 0, 24, 1)
        oled.text(str(new_score), 0, 34, 1)
        draw_pet_by_score(new_score)
        oled.show()
        time.sleep(0.8)
        return True, new_score, hearts
    else:
        hearts -= 1
        reason = gesture if gesture else "SLOW"

        oled.fill(0)
        oled.text("MISS!", 0, 0, 1)
        oled.text(reason, 0, 12, 1)
        oled.text(f"H{hearts} S{score}", 0, 24, 1)
        oled.text("TRY", 0, 34, 1)
        draw_pet_by_score(score)
        oled.show()
        time.sleep(1.2)

        return False, score, hearts


# =========================
#  게임 루프
# =========================

def game_loop(difficulty):
    score = 0
    hearts = MAX_HEARTS

    for level in range(1, 11):
        ok, score, hearts = play_round(level, difficulty, score, hearts)
        if hearts <= 0:
            return False, score, hearts
        if ok:
            continue
    return True, score, hearts


# =========================
#  엔딩 화면
# =========================

def game_over_screen(score, hearts):
    oled.fill(0)
    oled.text("GAME OVER", 0, 0, 1)
    oled.text("(T_T)", 0, 16, 1)
    oled.text("Score", 0, 32, 1)
    oled.text(str(score), 0, 48, 1)
    draw_pet_by_score(score)
    oled.show()
    wait_for_button_press()


def game_win_screen(score, hearts):
    oled.fill(0)
    oled.text("YOU WIN!", 0, 0, 1)
    oled.text("(^_^)", 0, 16, 1)
    oled.text("Score", 0, 32, 1)
    oled.text(str(score), 0, 48, 1)
    draw_pet_by_score(score)
    oled.show()
    wait_for_button_press()


# =========================
#  메인 루프
# =========================

def main():
    splash_screen()

    while True:
        start_screen()
        diff = select_difficulty()
        result, score, hearts = game_loop(diff)

        if result:
            game_win_screen(score, hearts)
        else:
            game_over_screen(score, hearts)


main()

