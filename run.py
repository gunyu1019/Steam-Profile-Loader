import os
import requests
import io
import lxml

from bs4 import BeautifulSoup
from IPython.display import Image
from PIL import Image as PILImage

url = "스팀 ID 대입"
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')

image_list = []

header = soup.find('div',{'class':'profile_header_bg'})
for i in header.find('div',{'class':'playerAvatarAutoSizeInner'}).find_all('img') :
    img_data = requests.get(i['src']).content
    #사진 저장
    im = PILImage.open(io.BytesIO(img_data))
    #io를 통하여 사진값을 불러옴.
    image_list.append(im)
    #image_list에 im값을 저장함.
total_size = image_list[0].size
#젤 큰 사진의 사이즈를 기준으로 선정함. 액자가 존재할 경우 경우 액자의 사이즈, 없을 경우 일반 사이즈가 대입됨.

canvas = PILImage.new('RGBA', total_size, (0,0,0,100)) #캔버스를 생성함.
canvas.paste(image_list[0], (0, 0)) #액자가 존재하면 액자값이 들어가고, 프로필 사진을 넣어줌.
if len(image_list) == 2: #액자가 존재할경우 0번값에는 액자값이 들어감. 따라서 프로필 사진을 따로 넣어주어야 함.
    profile_width, profile_height = image_list[1].size
    profile_size = (int(total_size[0]/2-profile_width/2),int(total_size[0]/2-profile_height/2))
    #액자크기가 이미 프로필사진보다 크다는 특징이 있음. 따라서 (액자 사이즈/2 - 프로필 사이즈/2)를 통해 사진 위치를 선정함.
    canvas.paste(image_list[1], profile_size) #프로필 사진 대입
canvas.save('steam profile.png')
 

