from flask import Flask
import boto3,io,os
import cv2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from flask import Flask, render_template
import base64,json

app = Flask(__name__)

@app.route("/emotions")
def home():
    return render_template('emotions_slide.html')


@app.route("/")
def index():
    # remove the existing file
    #os.remove("static/images/Test2.png")
    cap = cv2.VideoCapture(-1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
    myphoto = "Test.jpg"
    ret , photo = cap.read()
    cv2.imwrite( myphoto , photo)
    cap.release()

    # Initialize the Amazon Rekognition client
    rekognition = boto3.client('rekognition')

    # Specify the local image file
    image_path = '/home/isha/Documents/Isha/Seva-Mela/Test.jpg'

    # Read the image from the local file
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    # Call the DetectLabels API to analyze the image
    response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )

    # Process the response
    if 'FaceDetails' in response:
        for face_detail in response['FaceDetails']:
            # Emotions detected in the face
            emotions = face_detail['Emotions']
            first_emotion = emotions[0]
            first_emotion_type = first_emotion['Type']
            confidence = first_emotion['Confidence']
            confidence = round(confidence)
            confidence = str(confidence)
            score = first_emotion_type+": "+confidence+"%"
            #for emotion in emotions:
                #print(f"Emotion: {emotion['Type']}, Confidence: {emotion['Confidence']}")
            
    # Open an Image
    img = Image.open('Test.jpg')

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)

    # Custom font style and font size
    myFont = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 35)

    # Add Text to an image
    I1.text((245, 50), score, fill=(255, 255, 255),font=myFont)

    # Display edited image
    #img.show()

    # remove the existing file
    #os.remove("static/images/Test2.png")
    # Save the edited image 
    img.save("static/images/Test2.png")

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    image=base64.b64encode(img_byte_arr)
    #data['ProcessedImage'] = image.decode()

    return {"image": json.dumps(image.decode()) }

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

