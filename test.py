# -*- coding: utf-8 -*-
import json
import csv
#from PIL import Image, ImageDraw, ImageFont
import io
import os
import re

message = 'a/ bbc/ \n de'
message = message.replace(' ','').replace('\n','').split('/',1)
print (message)