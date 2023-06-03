from flask import Flask, request
from demo import DeepFake
from utility import extract_audio, merge_audio2video , remove_tempfile

import os.path

from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME
import boto3


app = Flask(__name__)
@app.route('/boards/video',methods=['POST'])
async def upload_video():

    if request.method == 'POST':

        req_data = request.get_json()

        img_number = req_data['imgNumber'][0]
        store_file_name = req_data['name'][0]

        s3 = s3_connection()
        file_path = s3_download_temp_file(store_file_name,s3)

        print("store_file_name : ", store_file_name)

        source_img = './assets/'+img_number+'.png'
        result_video_path = './result/' + store_file_name
        deepfake.transfer_video(source_img, file_path, result_video_path)

        output_audio_path = extract_audio(file_path, store_file_name)
        merged_video_path = merge_audio2video(output_audio_path, result_video_path, store_file_name)

        s3.upload_file(merged_video_path,BUCKET_NAME, 'video/' + store_file_name)

        remove_tempfile([file_path, result_video_path, output_audio_path, merged_video_path])


        return '동영상 변환이 완료되었습니다.' + result_video_path, 200


def s3_connection():
    s3 = boto3.client("s3",region_name="ap-northeast-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
    return s3

def s3_download_temp_file(store_file_name,s3):
    s3.download_file('vingterview', 'temp/'+store_file_name, './temp/' + store_file_name)
    return './temp/' + store_file_name




if __name__ == '__main__':
    deepfake = DeepFake()
    app.run()

