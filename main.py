import streamlit as st
import requests
from PIL import Image
from PIL import ImageDraw
import io


st.title('顔認識アプリ')

uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
  img = Image.open(uploaded_file)
  subscription_key ='0d144fee129a4997a0c155d4de3ab421'
  assert subscription_key
  face_api_url = 'https://20211228aking.cognitiveservices.azure.com/face/v1.0/detect'
  with io.BytesIO() as output:
      img.save(output, format="JPEG")
      binary_img = output.getvalue()
  headers = {
      'Content-Type': 'application/octet-stream',
      'Ocp-Apim-Subscription-Key': subscription_key
  }
  params = {
      'returnFaceAttributes': 'smile,headPose,gender,age,facialHair,glasses,emotion,blur,exposure,noise,makeup,accessories,occlusion,hair',
      'returnFaceId': 'true'
  }
  res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
  results = res.json()
  for result in results:
      rect = result['faceRectangle']
      draw = ImageDraw.Draw(img)
      draw.rectangle([(rect['left'], rect['top']), (rect['left'] + rect['width'], rect['top'] + rect['height'])],fill=None, outline='green', width=5)
  st.image(img, caption='Uploaded Image.', use_column_width=True)