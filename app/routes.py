from flask import Flask, request, render_template
import aiohttp, asyncio, uvicorn, os, json
from fastai import *
from fastai.vision import *
from app import app
import app.module.dropbox_api as dropbox_api

dropbox_access_token = app.config['DROPBOX_ACCESS_TOKEN']
export_file_url = app.config['EXPORT_FILE_URL']
export_filename = app.config['EXPORT_FILENAME']

path = Path(__file__).parent # root

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_filename)
    try:
        learn = load_learner(path, export_filename)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

# Set up async so the page renders while learner is downloaded.
loop = asyncio.new_event_loop()    
asyncio.set_event_loop(loop)
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # saves uploaded file to static/uploads
    f = request.files["file"]
    f.save(os.path.join(path, 'static/uploads', f.filename))
    return {"filename" : f.filename }

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # feed the saved image to the learner and return the prediction
    f_name = json.loads(request.data)['f_name']
    img = open_image(os.path.join(path, f_name))
    pred = str(learn.predict(img)[0])
    pred = pred[0].upper() + pred[1:-1]
    return {'pred': str(pred)}

@app.route('/upload_to_dropbox', methods=['POST'])
def upload_to_dropbox():
    # upload the misclassified image to dropbox
    f_name = json.loads(request.data)['f_name']
    transferData = dropbox_api.TransferData(dropbox_access_token)
    dropbox_filepath = '/misclassification/'
    transferData.upload_file(os.path.join(path, f_name), dropbox_filepath + dropbox_api.timestamp_filename(f_name))
    return {}

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")