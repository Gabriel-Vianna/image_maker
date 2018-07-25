from flask import Flask, render_template, request, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES
from .converter import convert_bw
from PIL import Image
import os
import glob


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        #Salva a foto selecionada no site na pasta de uploads
        uploaded_image = photos.save(request.files['photo'])
        #Abre a foto salva na pasta de uploads
        novo_arquivo = Image.open('uploads/{}'.format(uploaded_image))
        #Utiliza o algoritmo criado no arquivo converter.py para converter a imagem em preto e branco
        novo_arquivo = convert_bw(novo_arquivo)
        #Salva a imagem em preto e branco com o sufixo "bw" na frente do nome com que ela foi upada
        novo_arquivo.save('{}{}{}'.format('uploads/',"bw_" , uploaded_image))
        #Salva uma variável com o mesmo nome da imagem que foi criada em preto e branco e passa essa variavel para o link do download da imagem
        bw_image = '{}{}'.format("bw_" , uploaded_image)
        return render_template('download.html', bw_image = bw_image)
    return render_template('upload.html')


@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)
