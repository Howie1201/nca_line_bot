'''
        # create and send order datail image
        img = Image.new('RGB', (600, 800), color=(255, 255, 255))
        font = ImageFont.truetype('data/arial.ttf', size = 24)
        iDraw = ImageDraw.Draw(img)
        iDraw.text((40, 40), 'Hello', fill=(0, 0, 0), font = font)
        
        img.save('data/detail.png')
        line_bot_api.reply_message(event.reply_token, ImageSendMessage('data/detail.png', 'data/detail.png'))
'''