# Class WBScreen for M5Stack UIFlow 1.0

![Cover](https://github.com/m5stack/WBScreen/blob/main/cover.jpg?raw=true)

## Introduction

Despite the existence of high-tech displays with very high resolution, rich color palettes, and high refresh rates, monochrome displays remain popular among both professionals and beginners. There are two obvious advantages to note - one technological and the other visual.

The technology of monochrome LCD involves changing the orientation of liquid crystals under the influence of an electric charge and reflecting the light flux from a reflective film on the back. Thus, these displays provide high readability in bright lighting conditions and do not require backlighting during daylight hours. Unfortunately, this advantage does not extend to the built-in display in the M5Stack, which is made using IPS technology.

However, attention should be paid to the second advantage, which is of a visual nature and can be implemented on any color display – aesthetic minimalism. This concept includes simplicity of creation, color palette unity, specificity (since each pixel has significance at low resolution), and the most interesting aspect – freedom of interpretation (the less details are known to a person, the more they can imagine).

This class is designed to create a virtual monochrome screen in the UIFlow development environment.

## Features

* Excellent compatibility with UIFlow
* Easy connection and ease of use
* Multiple palettes available, including "LCD backlight off," white, green (Nokia style), blue (Samsung style), and orange (Siemens style)
* Fast sprite rendering
* Four transparency modes: opaque, transparent inside the contour, transparent outside the contour, fully transparent
* Creating sprites from RAW bytes of WBMP images
* No flickering during frame updates

> Note: Complex transparency modes (0x01, 0x10) will be implemented later. You can help with this.

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

> Note: This feature will be added soon.

## Usage

The `WBScreen` class provides the following methods:

- `__init__(palette: int = 0, screenWidth: int = 320, screenHeight: int = 240, width: int = 84, height: int = 48, dotSize: int = 2, dotSpacing: int = 1)`: the class constructor initializes an instance of `WBScreen` with optional parameters;

- `Clear()`: it clears the virtual screen buffer by filling it with the background color from the selected palette;

- `Push()`: it sends the content of the virtual screen buffer to the physical display;

- `Pixel(x: int, y: int, value: int, width: int, destination: ptr8)`: it colors a pixel in the 565 buffer;

- `Dot(x: int, y: int, value: int, width: int, destination: ptr8`): it colors a pixel in the virtual screen buffer;

- `Sprite(width: int, height: int, content: ptr8)`: it creates a sprite from RAW WBMP image data;

- `Slice(source: ptr8, sourceIndex: int, sourceWidthX2: int, destination: ptr8, destinationIndex: int, transparencyMode: int)`: it copies a portion of the image from the source 565 buffer and pastes it into the target 565 buffer with a specified transparency mode;

- `Select(x: int, y: int, sprite, transparencyMode: int = 0x00)`: it places a sprite on the screen at a specified position with a specified transparency mode.

## Examples

Below is a simple example of adding a point to the virtual screen:

```python
# Creating an instance of a class
screen = WBScreen(palette = 1)

# Drawing a point in the virtual screen buffer
screen.Dot(10, 10, 0b0, screen.width, screen.window)

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
bubbleSprite = screen.Sprite(16, 16, bubble)

# Creating a sprite for fish
fishSprites = [screen.Sprite(16, 16, fish[0]), screen.Sprite(16, 16, fish[1])]

while True:
  for i in range(24, 48):
    # Copying the seaweed sprite to the virtual screen buffer
    screen.Select(15, 16, seaweedSprite, 0x00)
    
    # Copying the bubble sprite to the virtual screen buffer
    screen.Select(10 + random.randint(-1, 1), -i, bubbleSprite, 0x11)
    
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
