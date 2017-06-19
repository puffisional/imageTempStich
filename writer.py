# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from os.path import splitext, split, join, exists
from os import makedirs
import numpy as np

class Writer():
    
    textPos = (50,120)
    textColor = (255,0,0,255)
    textSize = 40
    fps = 1
    
    def __init__(self, imageData, outputPath="./", createVideo="1"):
        self.imageData = imageData
        self.outpuPath = outputPath
        self.createVideo = createVideo
        
        if not exists(self.outpuPath):
            makedirs(self.outpuPath)
        
        self.writeImages()
    
    def writeImages(self):
        videoFile = None
        for data in self.imageData:
            img = self.writeTemperature(data["file"], data["temperature"])
            if self.createVideo == True:
                if videoFile is None: 
                    from imageTempStich.videoWriter import FFMPEG_VideoWriter
                    videoFile = FFMPEG_VideoWriter(join(self.outpuPath, "videoOutput.mp4"), img.size, fps=self.fps, pixelFormat="rgba")
                    
                videoFile.write_frame(np.asanyarray(img))
    
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
#         out.show()
        fileExtension = splitext(split(imagePath)[-1])
        out.save(join(self.outpuPath, "".join((fileExtension[0], "_stich", fileExtension[1]))))
        
        return out