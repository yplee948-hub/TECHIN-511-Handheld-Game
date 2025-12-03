# TECHIN-511-Handheld-Game
# TamaPet Handheld Game  
A 90’s-style ESP32-based electronic pet game  
Built for TECHIN 511 – Fabrication & Prototyping  
By: Youngpyung Lee (Cohort 9)

---

## 🎮 Project Overview
**TamaPet** is a 90’s-era electronic pet inspired handheld game built with an  
**ESP32 (Xiao ESP32-C3)**, **OLED display**, **ADXL345 accelerometer**, **rotary encoder**,  
**push button**, and **NeoPixel LED**.

The game combines **gesture-based inputs** (tilting using the accelerometer)  
with classic Tamagotchi-style **pet evolution**, scoring, HP management,  
and level progression up to 10 stages.

Players complete actions within a time limit using tilt gestures.  
Correct actions increase score and evolve the pet.  
Mistakes reduce HP; losing all HP triggers Game Over.

---

## 🎯 Game Features

### ✔ 1. Three Difficulty Levels
- **EASY** – 4.0 seconds  
- **MEDIUM** – 2.5 seconds  
- **HARD** – 1.5 seconds  
Selected using the **rotary encoder** (turn to select, press to confirm).

---

### ✔ 2. Four Player Actions  
Each action requires matching a directional gesture:

| Action | Gesture Required |
|--------|------------------|
| FEED   | LEFT             |
| PLAY   | RIGHT            |
| CLEAN  | UP               |
| SLEEP  | DOWN             |

Gestures are detected using **ADXL345** with filtered acceleration values.

---

### ✔ 3. Pet Evolution System  
Your TamaPet evolves depending on your score:

| Stage | Score Range |
|-------|-------------|
| EGG   | 0–39        |
| BABY  | 40–99       |
| TEEN  | 100–179     |
| ADULT | 180+        |

Sprites are drawn using **custom 16×16 pixel art** scaled for OLED.

---

### ✔ 4. HUD Layout (Final UI)
The OLED is divided into:
- **Left 60% (0–79px)** → HUD text  
- **Right 40% (80–127px)** → Pet sprite  

This prevents overlapping text + sprite for maximum clarity.

---

### ✔ 5. Game Progression
- 10 total levels  
- Increasing difficulty  
- Score grows based on difficulty  
- HP system (3 hearts)  
- Win screen / Game Over screen  
- Start screen + animated splash screen  

---

## 🧩 Hardware Used

### Microcontroller
- Seeed Studio **Xiao ESP32-C3**

### Components
- **128×64 OLED** (I2C, addr 0x3C)
- **ADXL345 Accelerometer** (I2C, addr 0x53)
- **Rotary Encoder** (A/B pins + push button)
- **1× NeoPixel LED**
- **LiPo battery**
- **On/Off slide switch**

### Wiring Overview
(If you include wiring.png or system diagram images, upload them inside `/docs`)

---

## 📁 File Structure
/code.py → Main game code
/README.md → Documentation
/docs/ → System diagram, wiring diagram (optional)
/images/ → Pet sprite images (optional)
---

## 🚀 How to Run  
1. Flash **CircuitPython** onto the Xiao ESP32-C3  
2. Install required libraries onto `CIRCUITPY/lib`:  
   - `adafruit_ssd1306`  
   - `adafruit_bus_device`  
   - `adafruit_framebuf`  
   - `adafruit_adxl34x`  
   - `neopixel`  
3. Connect hardware as wired  
4. Upload `code.py` to the root of the device  
5. Reset → game launches automatically

---

### Gesture Detection
- Uses **baseline-calibrated delta values**  
- Filters noise via averaging  
- Robust LEFT/RIGHT flip handling (your board orientation issue fixed)

### Scaled Sprite Rendering
- Custom function draws 16×16 sprites  
- Scaled down via `scale=2` to avoid UI collision  
- Dynamically reflects growth stage

### UI/UX Design for Low-Resolution OLED
- Clear separation between text and sprite  
- Shortened labels to prevent wrapping  
- Consistent text anchor positions

---

## 🏁 Completion Status
- ✔ Complete code  
- ✔ Working gesture detection  
- ✔ Pet evolution working  
- ✔ UI layout finalized  
- ✔ Hardware fully functioning  
- ✔ Ready for submission

---

## 📎 Repository Link
(Insert your GitHub link after uploading code.py)

**https://github.com/yplee948-hub/TECHIN-511-Handheld-Game**

---

## 🙌 Credits
Designed & built by **Youngpyung Lee**  
University of Washington – Global Innovation Exchange  
TECHIN 511 (Fabrication & Prototyping)

