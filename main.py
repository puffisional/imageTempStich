#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import argparse

from imageTempStich import writer
from imageTempStich import reader

if __name__ == "__main__":
    cmdInput = argparse.ArgumentParser()
    cmdInput.add_argument("--logFile", required=True, help="Logfile with temperatures")
    cmdInput.add_argument("--inputDir", default="./", help="Input directory with images")
    cmdInput.add_argument("--outputDir", default="./", help="Output directory")
    args = cmdInput.parse_args()
    
    r = reader.Reader(args.logFile, args.inputDir)
    w = writer.Writer(r.imageData, args.outputDir)
