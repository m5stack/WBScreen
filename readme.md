# Class WBScreen for M5Stack UIFlow 1.0

![Cover](https://github.com/m5stack/WBScreen/blob/main/cover.jpg?raw=true)

## Introduction

Despite the existence of high-tech displays with very high resolution, rich color palettes, and high refresh rates, monochrome displays remain popular among both professionals and beginners. There are two obvious advantages to note – one technological and the other visual.

The technology of monochrome LCD involves changing the orientation of liquid crystals under the influence of an electric charge and reflecting the light flux from a reflective film on the back. Thus, these displays provide high readability in bright lighting conditions and do not require backlighting during daylight hours. Unfortunately, this advantage does not extend to the built-in display in the M5Stack, which is made using IPS technology.

However, attention should be paid to the second advantage, which is of a visual nature and can be implemented on any color display – aesthetic minimalism. This concept includes simplicity of creation, color palette unity, specificity (since each pixel has significance at low resolution), and the most interesting aspect – freedom of interpretation (the less details are known to a person, the more they can imagine).

This class is designed to create a virtual monochrome screen in the UIFlow development environment.

## Features

* Excellent compatibility with UIFlow
* Easy connection and ease of use
* Multiple palettes are available, including "LCD backlight off," white, green (Nokia style), blue (Samsung style), orange (Siemens style), as well as OLED-style screen colors such as white, blue, and yellow
* Fast sprite rendering
* Three transparency modes: opaque, fully transparent and transparent region relative to a specified point
* Creating sprites from RAW bytes of WBMP images
* No flickering during frame updates

## Installation

### MicroPython

Copy the contents of the `WBScreen.py` file into the code editor (Python tab) in [UIFlow](https://flow.m5stack.com), as shown in the example below:

```python
from m5stack import *
from m5ui import *
from uiflow import *

class WBScreen:
	...
```
	
### Blockly

To connect the Blockly set, follow these steps:

1. Download the `WBScreen.m5b` file to your computer
2. Open [UIFlow](https://flow.m5stack.com)
3. In the `Custom` tab, select `Open *.m5b file`
4. Choose the downloaded file
5. Check the `Custom` tab again, the `WBScreen` section should now appear

## Usage

The `WBScreen` class provides the following methods:

- `__init__(palette: int = 0, screenWidth: int = 320, screenHeight: int = 240, width: int = 84, height: int = 48, dotSize: int = 2, dotSpacing: int = 1)`: The class constructor initializes an instance of `WBScreen` with optional parameters

- `Clear()`: It clears the virtual screen buffer by filling it with the background color from the selected palette

- `Push()`: It sends the content of the virtual screen buffer to the physical display

- `Pixel(x: int, y: int, value: int, width: int, destination: ptr8)`: It colors a pixel in the 565 buffer

- `Dot(x: int, y: int, value: int`): It colors a pixel in the virtual screen buffer

- `Sprite(width: int, height: int, content: ptr8, transparencyPoint: [int, int] = None)`: It creates a sprite from RAW WBMP image data. The argument `transparencyPoint` is an optional parameter used to determine the transparency mode. By default, if the value is `None`, it will be interpreted as no transparency. If the value is `[-1, -1]`, the sprite will be completely transparent. To enable the third transparency mode using the fill method, you can pass the coordinates of the origin point, for example, [0, 0]. This will make the space around the image transparent while keeping the inside opaque.

- `Slice(source: ptr8, sourceIndex: int, sourceWidthX2: int, destination: ptr8, destinationIndex: int, transparencyMode: int)`: It copies a portion of the image from the source 565 buffer and pastes it into the target 565 buffer with a specified transparency mode

- `Select(x: int, y: int, sprite)`: It places a sprite on the screen at a specified position

- `Transparency(x: int, y: int, width: int, height: int, destination: ptr8)`: It fills the 565 buffer with a background color that will be interpreted as transparent

## Examples

Below is a simple example of adding a point to the virtual screen:

```python
# Creating an instance of a class
screen = WBScreen(palette = 1)

# Drawing a point in the virtual screen buffer
screen.Dot(10, 10, 0b0)

# Outputting the contents of the virtual screen buffer to the physical screen
screen.Push()
```
Below is a complete example of an "Underwater World" where the output of three images is implemented: seaweed (static without transparency), bubble (moving with transparency), and fish (animated with transparency).

```python
import random

# class WBScreen:
#  ...

# Creating an instance of a class
screen = WBScreen(palette = 3)

# RAW data of three WBMP images:

# 1. Static image "seaweed"
seaweed = bytearray([0xFC, 0xFC, 0xFC, 0xFC, 0xDC, 0xCC, 0xEC, 0xEC, 0xEC, 0xE4, 0xE4, 0xCC, 0xDC, 0xDC, 0xCC, 0xEC, 0xCC, 0xDC, 0xD4, 0xC4, 0xCC, 0xEC, 0xAC, 0x84, 0xCC, 0xCC, 0x8C, 0x9C, 0xDC, 0xCC, 0xCC, 0xCC])

# 2. Moving image "bubble"
bubble = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x1F, 0xFB, 0xEF, 0xF7, 0xF7, 0xEF, 0xBB, 0xDF, 0x5D, 0xDB, 0xBD, 0xD7, 0xFD, 0xDF, 0xFD, 0xDF, 0xFD, 0xEF, 0xFB, 0xF7, 0xB7, 0xFB, 0xEF, 0xFC, 0x1F, 0xFF, 0xFF])

# 3. Moving animation "fish". It consists of two images
fish = [bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x3F, 0xFC, 0x7F, 0xF0, 0x3F, 0xEF, 0xDD, 0xDB, 0xEB, 0xDF, 0xF5, 0xE7, 0xEB, 0xF3, 0xDD, 0xF8, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]), bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0xFF, 0xFC, 0x1F, 0xF0, 0x3B, 0xEF, 0xDB, 0xDB, 0xEB, 0xDF, 0xF3, 0xE7, 0xEB, 0xF3, 0xDB, 0xF8, 0x3B, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])]

# Creating a sprite for seaweed
seaweedSprite = screen.Sprite(6, 32, seaweed)

# Creating a sprite for bubble
bubbleSprite = screen.Sprite(16, 16, bubble, [-1, -1])

# Creating a sprite for fish
fishSprites = [screen.Sprite(16, 16, fish[0], [0, 0]), screen.Sprite(16, 16, fish[1], [0, 0])]

while True:
  for i in range(24, 48):
    # Copying the seaweed sprite to the virtual screen buffer
    screen.Select(15, 16, seaweedSprite)
    
    # Copying the bubble sprite to the virtual screen buffer
    screen.Select(10 + random.randint(-1, 1), -i, bubbleSprite)
    
    if i % 2 == 0:
      # Copying the 0th fish sprite to the virtual screen buffer
      screen.Select(screen.width - i, 5, fishSprites[0])
    else:
      # Copying the 1st fish sprite to the virtual screen buffer
      screen.Select(screen.width - i, 5, fishSprites[1])
    
    # Outputting the contents of the virtual screen buffer to the physical screen
    screen.Push()
    
    # 50 milliseconds delay
    wait_ms(50)
```

## Contributing

If you want to contribute to the development of this project, please follow the recommendations:

1. **Fork** the repository and **Clone** it to your local machine
2. Create a new **Branch**
3. Make improvements to the code
4. Write clear and concise explanations in your **Commits**
5. Test your changes
6. Don't forget to **Push** your **Fork** to the repository
7. You can submit a **Pull Request** to the main repository, explaining the purpose and details of your contribution
8. Ensure that your **Pull Request** adheres to the project's coding conventions and formatting standards
