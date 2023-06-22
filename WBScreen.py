class WBScreen:
  palettes = [
    # [byte1, byte0] for 'black', 'white', 'backlight'
    [[0x00, 0x00], [0x18, 0xe3], [0x21, 0x03]], # "LCD backlight OFF"
    [[0x00, 0x00], [0x6b, 0xac], [0x73, 0xed]], # white
    [[0x00, 0x00], [0x5c, 0xa6], [0x64, 0xe6]], # green
    [[0x00, 0x00], [0x22, 0x56], [0x22, 0x77]], # blue
    [[0x00, 0x00], [0xab, 0x44], [0xB3, 0x84]], # orange
    [[0xff, 0xff], [0x00, 0x00], [0x00, 0x00]], # white OLED style
    [[0x7f, 0xdf], [0x00, 0x00], [0x00, 0x00]], # blue OLED style
    [[0xff, 0xa0], [0x00, 0x00], [0x00, 0x00]]  # yellow OLED style
  ]

  dSiSp: int
  dSiSpWindowWidthX2: int
  dSiSpX2: int
  dotSize: int
  dotSpacing: int
  height: int
  hSpacing: int
  palette: int
  screenHeight: int
  screenWidth: int
  vSpacing: int
  width: int
  window: ptr8 = None
  windowBlank: ptr8 = None
  windowLength: int
  windowLengthX2: int
  windowWidth: int
  windowWidthX2: int
  windowX0 = [int, int]
  windowX01: ptr8 = None
  windowX1 = [int, int]
  windowY0 = [int, int]
  windowY01: ptr8 = None
  windowY1 = [int, int]

  def __init__(self, palette: int = 0, screenWidth: int = 320, screenHeight: int = 240, width: int = 84, height: int = 48, dotSize: int = 2, dotSpacing: int = 1):
    self.palette = palette

    self.screenWidth = screenWidth
    self.screenHeight = screenHeight

    self.width = width
    self.height = height

    self.dotSize = dotSize
    self.dotSpacing = dotSpacing
    self.dSiSp = self.dotSize + self.dotSpacing

    self.hSpacing = int((self.screenWidth - (self.width * self.dotSize + self.width)) / 2)
    self.vSpacing = int((self.screenHeight - (self.height * self.dotSize + self.height)) / 2)

    x0 = self.hSpacing
    self.windowX0[0] = x0 & 0xFF
    self.windowX0[1] = (x0 >> 8) & 0xFF

    x1 = self.hSpacing + self.dSiSp * self.width - 1
    self.windowX1[0] = x1 & 0xFF
    self.windowX1[1] = (x1 >> 8) & 0xFF

    y0 = self.vSpacing
    self.windowY0[0] = y0 & 0xFF
    self.windowY0[1] = (y0 >> 8) & 0xFF

    y1 = self.vSpacing + self.dSiSp * self.height - 1
    self.windowY1[0] = y1 & 0xFF
    self.windowY1[1] = (y1 >> 8) & 0xFF

    self.windowX01 = bytearray([self.windowX0[1], self.windowX0[0], self.windowX1[1], self.windowX1[0]])
    self.windowY01 = bytearray([self.windowY0[1], self.windowY0[0], self.windowY1[1], self.windowY1[0]])

    self.windowWidth = x1 - x0 + 1
    self.windowLength = self.windowWidth * (y1 - y0 + 1)

    self.window = bytearray(self.windowLength * 2)

    self.dSiSpX2 = self.dSiSp * 2
    self.windowWidthX2 = self.windowWidth * 2
    self.windowLengthX2 = self.windowLength * 2
    self.dSiSpWindowWidthX2 = self.dSiSp * self.windowWidthX2

    self.Clear()

    lcd.fill(self.RGBfrom565((self.palettes[self.palette][2][0] << 8) | self.palettes[self.palette][2][1]))

  def RGBfrom565(self, rgb565):
    r = (rgb565 >> 11) & 0x1F
    g = (rgb565 >> 5) & 0x3F
    b = rgb565 & 0x1F

    r = (r << 3) | (r >> 2)
    g = (g << 2) | (g >> 4)
    b = (b << 3) | (b >> 2)

    return (r << 16) | (g << 8) | b

  @micropython.native
  def Clear(self):
    if self.windowBlank == None:
      self.windowBlank = bytearray(self.palettes[self.palette][2] * self.windowLength)

      for i in range(self.height):
        for j in range(self.width):
          self.Dot(j, i, 0b1, self.width, self.windowBlank)

    self.window[:] = self.windowBlank[:]

  @micropython.viper
  def Push(self):
    lcd.tft_writecmddata(0x2A, memoryview(self.windowX01))
    lcd.tft_writecmddata(0x2B, memoryview(self.windowY01))
    lcd.tft_writecmddata(0x2C, memoryview(self.window))

    # So slow part ×_×'
    windowLengthX2: int = int(self.windowLength) * 2
    window: ptr8 = self.window
    windowBlank: ptr8 = self.windowBlank

    for i in range(windowLengthX2):
      window[i] = windowBlank[i]

  def Pixel(self, x: int, y: int, value: int, width: int, destination: ptr8):
    index = (width * y + x) * 2

    destination[index] = self.palettes[self.palette][value][0]
    destination[index + 1] = self.palettes[self.palette][value][1]

  def GetPixel(self, x: int, y: int, width: int, destination: ptr8):
    index = (width * y + x) * 2

    return [destination[index], destination[index + 1]]

  def Dot(self, x: int, y: int, value: int):
    self.Dot(x, y, value, self.width, self.window)

  def Dot(self, x: int, y: int, value: int, width: int, destination: ptr8):
    width *= self.dSiSp

    nx: int = self.dSiSp * x
    ny: int = self.dSiSp * y

    for i in range(self.dotSize):
      for j in range(self.dotSize):
        self.Pixel(nx + j, ny + i, value, width, destination)

  def GetDot(self, x: int, y: int, width: int, destination: ptr8):
    width *= self.dSiSp

    nx: int = self.dSiSp * x
    ny: int = self.dSiSp * y

    return self.GetPixel(nx, ny, width, destination)

  def Sprite(self, width: int, height: int, content: ptr8, transparencyPoint: [int, int] = None):
    spriteWidth: int = self.dSiSp * width
    spriteHeight: int = self.dSiSp * height
    spriteContent: ptr8 = bytearray(self.palettes[self.palette][2] * (spriteWidth * spriteHeight * 2))

    usefulBits: int = 8 if width > 8 else width

    for by in range((8 if width < 8 else width) * height // 8):
      for bi in range(usefulBits):
        index = by * usefulBits + bi
        x = index % width
        y = index // width
        value = (content[by] >> (7 - bi)) & 0b1

        self.Dot(x, y, value, width, spriteContent)

    transparencyMode: int

    if transparencyPoint == None:
      transparencyMode = 0x00

    elif transparencyPoint == [-1, -1]:
      transparencyMode = 0x11

    else:
      transparencyMode = 0x01
      self.Transparency(transparencyPoint[0], transparencyPoint[1], width, height, spriteContent)

    spriteWidth -= 1
    spriteHeight -= 1

    return spriteWidth + 1, spriteHeight + 1, spriteContent, transparencyMode

  @micropython.native
  def Slice(self, source: ptr8, sourceIndex: int, sourceWidthX2: int, destination: ptr8, destinationIndex: int, transparencyMode: int):
    sourceSlice = memoryview(source)[sourceIndex:sourceIndex + sourceWidthX2]
    destinationSlice = memoryview(destination)[destinationIndex:destinationIndex + sourceWidthX2]

    if transparencyMode == 0x00:
      destinationSlice[:] = sourceSlice

    elif transparencyMode == 0x11:
      for byteCouple in range(sourceWidthX2 // 2):
        byte1st = byteCouple * 2
        byte2nd = byte1st + 1

        if sourceSlice[byte1st] == self.palettes[self.palette][0][0] and sourceSlice[byte2nd] == self.palettes[self.palette][0][1]:
          destinationSlice[byte1st] = self.palettes[self.palette][0][0]
          destinationSlice[byte2nd] = self.palettes[self.palette][0][1]

    else:
      for byteCouple in range(sourceWidthX2 // 2):
        byte1st = byteCouple * 2
        byte2nd = byte1st + 1

        if sourceSlice[byte1st] != self.palettes[self.palette][2][0] and sourceSlice[byte2nd] != self.palettes[self.palette][2][1]:
          destinationSlice[byte1st] = sourceSlice[byte1st]
          destinationSlice[byte2nd] = sourceSlice[byte2nd]

  @micropython.native
  def Select(self, x: int, y: int, sprite):
    width: int = sprite[0]
    height: int = sprite[1]
    content565: ptr8 = sprite[2]
    transparencyMode: int = sprite[3]

    sourceWidthX2: int = width * 2

    for i in range(height):
      sourceIndex = i * sourceWidthX2
      destinationIndex = i * self.windowWidthX2

      destinationIndex += x * self.dSiSpX2
      destinationIndex += y * self.dSiSpWindowWidthX2

      self.Slice(content565, sourceIndex, sourceWidthX2, self.window, destinationIndex, transparencyMode)

  def Transparency(self, x: int, y: int, width: int, height: int, destination: ptr8):
    startColor = self.GetDot(x, y, width, destination)

    if startColor == self.palettes[self.palette][2]:
      return

    stack = [(x, y)]

    while stack:
      currentX, currentY = stack.pop()

      currentColor = self.GetDot(currentX, currentY, width, destination)

      if currentColor == self.palettes[self.palette][2]:
        continue

      self.Dot(currentX, currentY, 2, width, destination)

      neighborsDots = [
        (currentX, currentY - 1),
        (currentX, currentY + 1),
        (currentX - 1, currentY),
        (currentX + 1, currentY)
      ]

      for neighborX, neighborY in neighborsDots:
        if neighborX >= 0 and neighborX < width and neighborY >= 0 and neighborY < height:
          neighborColor = self.GetDot(neighborX, neighborY, width, destination)

          if neighborColor == startColor:
            stack.append((neighborX, neighborY))
