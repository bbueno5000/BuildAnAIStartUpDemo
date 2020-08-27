"""
DOCSTRING
"""
import app
import flask
import keras
import numpy
import os
import random

@app.app.route('/')

#disease_list = [
#    'Atelectasis',
#    'Consolidation',
#    'Infiltration',
#    'Pneumothorax',
#    'Edema',
#    'Emphysema',
#    'Fibrosis',
#    'Effusion',
#    'Pneumonia',
#    'Pleural_Thickening',
#    'Cardiomegaly',
#    'Nodule',
#    'Mass',
#    'Hernia']

@app.app.route('/contact')
def contact():
    return flask.render_template('contact.html', title='Contact')

@app.app.route('/index')
def index():
    return flask.render_template('index.html', title='Home')

@app.app.route('/map')
def map():
    return flask.render_template('map.html', title='Map')

@app.app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(
        random.uniform(48.8434100, 48.8634100),
        random.uniform(2.3388000, 2.3588000)) for _ in range(random.randint(2, 9))]
    return flask.jsonify({'points': points})

@app.app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if flask.request.method == 'POST':
      f = flask.request.files['file']
      path = os.path.join(app.app.config['UPLOAD_FOLDER'], f.filename)
      model = keras.applications.resnet50.ResNet50(weights='imagenet')
      img = keras.preprocessing.image.load_img(path, target_size=(224, 224))
      x = keras.preprocessing.image.img_to_array(img)
      x = numpy.expand_dims(x, axis=0)
      x = keras.applications.resnet50.preprocess_input(x)
      preds = model.predict(x)
      preds_decoded = keras.applications.resnet50.decode_predictions(preds, top=3)[0] 
      print(keras.applications.resnet50.decode_predictions(preds, top=3)[0])
      f.save(path)
      return flask.render_template(
          'uploaded.html', title='Success',
          predictions=preds_decoded, user_image=f.filename)

@app.app.route('/upload')
def upload_file2():
   return flask.render_template('index.html')
