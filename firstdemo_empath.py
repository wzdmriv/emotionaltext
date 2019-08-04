import pyaudio
import wave
import os
import librosa
import requests
import json
import pydub
from pydub import AudioSegment

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\wzdmr\Emotionaltext\speech-recogniti-1562941973317-b302ca3682c5.json'
audiotext = ""

RECORD_SECONDS = 4 #録音する時間の長さ（秒）
WAVE_OUTPUT_FILENAME = "sample.wav" #音声を保存するファイル名
WAVE_OUTPUT_FILENAME1 = "sample1.wav" #音声を保存するファイル名
iDeviceIndex = 0 #録音デバイスのインデックス番号

#基本情報の設定
FORMAT = pyaudio.paInt16 #音声のフォーマット
CHANNELS = 1             #モノラル
RATE = 44100             #サンプルレート
RATE1 = 11025             #サンプルレート
CHUNK = 2**11            #データ点数
audio = pyaudio.PyAudio() #pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
        frames_per_buffer=CHUNK)
stream1 = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE1, input=True,
        input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
        frames_per_buffer=CHUNK)

#--------------録音開始---------------

print ("recording...")
frames = []
frames1 = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    if i%4 == 0:
        data1 = stream1.read(CHUNK)
        frames1.append(data1)

print ("finished recording")

#--------------録音終了---------------

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
waveFile = wave.open(WAVE_OUTPUT_FILENAME1, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE1)
waveFile.writeframes(b''.join(frames1))
waveFile.close()

#音量上げる
voice = AudioSegment.from_wav(r'C:\Users\wzdmr\Emotionaltext\sample.wav')
voice = voice +20
voice.export(r'C:\Users\wzdmr\Emotionaltext\sample.wav', "wav")
voice = AudioSegment.from_wav(r'C:\Users\wzdmr\Emotionaltext\sample1.wav')
voice = voice +20
voice.export(r'C:\Users\wzdmr\Emotionaltext\sample1.wav', "wav")

#----------文字起こし----------
def transcribe_file(speech_file):
    global audiotext
    import io
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

#importするファイルの設定
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='ja-JP')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        audiotext = format(result.alternatives[0].transcript)
        print(audiotext)

transcribe_file(r"C:\Users\wzdmr\Emotionaltext\sample.wav")


#----------Empath感情分析----------
url = 'https://api.webempath.net/v2/analyzeWav'
files = {
    'apikey': (None, 'xqLTBr_fo_nbI-V3SebCmBcs_1gB6OkzqlQckbGdBcY'),
    'wav': (None, open(r'C:\Users\wzdmr\Emotionaltext\sample1.wav', 'rb')),
}
response = requests.post(url, files=files)
print(response.content)
json_dict = json.loads(response.content)


#----------描画----------
from PIL import Image, ImageDraw, ImageFont
im = Image.new("RGB", (1024,512), (220, 220, 220))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('C:\Windows\Fonts\meiryo.ttc', 80)
max_k = max(json_dict, key=json_dict.get)

if max_k == "calm":
    fill = (0,0,255)
elif max_k == "anger":
    fill = (255,0,0)
elif max_k == "joy":
    fill = (0,255,0)
elif max_k == "sorrow":
    fill = (128,128,0)
elif max_k == "energy":
    fill = (255,255,0)
else:
    fill = (0,0,0)

draw.multiline_text((0, 0), audiotext, fill=fill, font=font)
im.show()