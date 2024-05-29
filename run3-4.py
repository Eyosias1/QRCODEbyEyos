from PIL import Image, ImageDraw
from reedsolo import RSCodec

def draw_meta_data(lenght_of, current_x, current_y, color_list, row):
    for e in range(lenght_of):
        xtuple = (current_x +2*e, row)
        Ytuple = (current_y +2*e, row+1)
        draw.rectangle([xtuple, Ytuple], fill=color_list[e], width=1)
    xtuple = (xtuple[0]+2, xtuple[1])
    Ytuple = (Ytuple[0]+2, Ytuple[1])
    return xtuple, Ytuple




def hccb_encode(binary_data):
    color_mapping = {
        "00": (0, 0, 0), #noir
        "01": (128, 128, 128), # grey
        "10": (191, 0, 255), #Electric purple
        "11": (255, 165, 0), #orange
    }

    segments = [binary_data[i:i+2] for i in range(0, len(binary_data), 2)]
    colors = [color_mapping[segment] for segment in segments]

    return colors


data = input("Enter a string: ")

#ask user if with or without redundancy
redundancy_sol = input("Do you want redundancy \nPlease enter True or False: ")
redundancy_sol = redundancy_sol.lower()


level_of_sol = 0


binary_data = ""
for c in data:
    ascii_code = ord(c)
    ascii_binary = format(ascii_code, '08b')
    binary_data += ascii_binary



if redundancy_sol == 'true':
    # Ask user for an integer input
    solomon_level = int(input("Choose level between 1, 2 or 3: "))
    # Apply Reed-Solomon error correction
    if solomon_level == 1:
        rs = RSCodec(10) # 10 error correction symbols
        level_of_sol = 10
    elif solomon_level == 2:
        rs = RSCodec(100)
        level_of_sol = 100
    else:
        rs =  RSCodec(250)
        level_of_sol = 250
    encoded_data = rs.encode(bytearray(binary_data, 'utf-8'))
    encoded_data = encoded_data[::-1]
    binary_encoded_data = ''.join(format(byte, '08b') for byte in encoded_data)
    colors = hccb_encode(binary_encoded_data)
else:
    colors = hccb_encode(binary_data)

squares_per_row = 4
square_size = 1
space_size = 1

width = 70
height = 70
image_size = max(width, height) + 2 * space_size
colored_img = Image.new("RGBA", (image_size, image_size), (255, 255, 255, 255))
draw = ImageDraw.Draw(colored_img)

color_index = 0
border_width = 1

for y in range(1, height - 1, square_size + space_size):
    for x in range(1, width - 1, square_size + space_size):
        if color_index < len(colors):
            color = colors[color_index]
            color_index += 1
        else:
            color = (255, 255, 255)

        draw.rectangle([(1 + x, 1 + y), (1 + x + square_size, 1 + y + square_size)], fill=color, width=border_width)

draw.rectangle([(0,0), (1,1)], fill=(255, 0, 0), width=1)

# Bottom left
bottom_left = [(0, width + square_size), (square_size, height)]
draw.rectangle(bottom_left, fill=(255, 0, 0), width=1)

# Top right
top_right = [(width, 0), (width + square_size, 1)]
draw.rectangle(top_right, fill=(255, 0, 0), width=1)




############################
#    @meta data section@   #
############################
# 1. add meta data version 1
draw.rectangle([(2,0), (3,1)], fill=(128, 128, 128), width=1)
# add space between meta data
draw.rectangle([(4,0), (5,1)], fill=(255, 255, 255), width=1)
len_data = len(data)
binary_len_data = format(len_data, '08b')
len_data_color = hccb_encode(binary_len_data)
# 2. data length
x, y = draw_meta_data(len(len_data_color),6, 7, len_data_color, 0)
# add space between meta data
x, y = draw_meta_data(1,x[0], y[0], [(255,255,255)], 0)
# 3. The size of the image WAcode
len_data = width
binary_len_data = format(len_data, '08b')
len_data_color = hccb_encode(binary_len_data)
x, y = draw_meta_data(len(len_data_color),x[0], y[0], len_data_color, 0)
# add space between meta data
x, y = draw_meta_data(1,x[0], y[0], [(255,255,255)], 0)
# 4. add solomon reed redundancy level
binary_level = format(level_of_sol, '08b')
level_color = hccb_encode(binary_level)
x, y = draw_meta_data(len(level_color),x[0], y[0], level_color, 0)
# add space between meta data
x, y = draw_meta_data(1,x[0], y[0], [(255,255,255)], 0)
# 5. add meta data of encoding scheme (encoding format)
x, y = draw_meta_data(1,x[0], y[0], [(128, 128, 128)], 0)

############################
#    @meta data redundancy@   #
############################
# add meta data version 1
draw.rectangle([(2,width), (3, height + square_size)], fill=(128, 128, 128), width=1)
# add space between meta data
draw.rectangle([(4,width ), (5, height + square_size)], fill=(255, 255, 255), width=1)
len_data = len(data)
binary_len_data = format(len_data, '08b')
len_data_color = hccb_encode(binary_len_data)
# data length
x, y = draw_meta_data(len(len_data_color),6, 7, len_data_color, width)
# add space between meta data
x, y = draw_meta_data(1,x[0], y[0], [(255,255,255)], width)
# The size of the WAcode
len_data = width
binary_len_data = format(len_data, '08b')
len_data_color = hccb_encode(binary_len_data)
x, y = draw_meta_data(len(len_data_color),x[0], y[0], len_data_color, width)
# add space between meta data
x, y = draw_meta_data(1,x[0], y[0], [(255,255,255)], width)
# add solomon read redundancy level
binary_level = format(level_of_sol, '08b')
level_color = hccb_encode(binary_level)
# data length
x, y = draw_meta_data(len(level_color),x[0], y[0], level_color, width)
# add space between meta data
x, y = draw_meta_data(1,x[0], y[0], [(255,255,255)], width)
# add meta data of encoding scheme (encoding format)
x, y = draw_meta_data(1,x[0], y[0], [(128, 128, 128)], width)
colored_img.save("colored_grid.png")

img1 = Image.open("colored_grid.png")
img2 = Image.open("img.png")
width, height = img2.size

img1.paste(img2, (25, 30 , 25+width, 30+height))

img1.save("output.png")
