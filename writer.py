# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

class Writer():
    
    textPos = (50,120)
    textColor = (255,0,0,255)
    textSize = 40
    
    def __init__(self, imageData, outputPath="./"):
        self.imageData = imageData
        self.writeImages()
    
    def writeImages(self):
        for data in self.imageData:
            self.writeTemperature(data["file"], data["temperature"])
    
    def writeTemperature(self, imagePath, temperature):
        image = Image.open(imagePath).convert("RGBA")
        text = Image.new("RGBA", image.size, (255,255,255,0))
        
        # get a font
        fnt = ImageFont.truetype('./tahoma.ttf', self.textSize)
        # get a drawing context
        d = ImageDraw.Draw(text)
        
        # draw text, half opacity
        d.text(self.textPos, u"%.2f °C" % temperature, font=fnt, fill=self.textColor)
        
        #/usr/share/wine/fonts/tahoma.ttf
        out = Image.alpha_composite(image, text)
        out.show()