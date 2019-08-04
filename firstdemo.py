import pyaudio
import wave
import os
import librosa

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\wzdmr\Emotionaltext\speech-recogniti-1562941973317-b302ca3682c5.json'
audiotext = ""
score = ""
hogetext = "実装辛い"

RECORD_SECONDS = 4 #録音する時間の長さ（秒）
WAVE_OUTPUT_FILENAME = "sample.wav" #音声を保存するファイル名
iDeviceIndex = 0 #録音デバイスのインデックス番号

#基本情報の設定
FORMAT = pyaudio.paInt16 #音声のフォーマット
CHANNELS = 1             #モノラル
RATE = 44100             #サンプルレート
CHUNK = 2**11            #データ点数
audio = pyaudio.PyAudio() #pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
        frames_per_buffer=CHUNK)

#--------------録音開始---------------

print ("recording...")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

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


def sample_analyze_sentiment(content):
    global score
    #----------感情分析----------
    from google.cloud import language_v1
    from google.cloud.language_v1 import enums
    import six
    client = language_v1.LanguageServiceClient()

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    score = format(sentiment.score)
    print('Score: %s' % score)
    print('Magnitude: {}'.format(sentiment.magnitude))

transcribe_file(r"C:\Users\wzdmr\Emotionaltext\sample.wav")
sample_analyze_sentiment(audiotext)


from PIL import Image, ImageDraw, ImageFont
im = Image.new("RGB", (1024,512), (220, 220, 220))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('C:\Windows\Fonts\meiryo.ttc', 80)
draw.multiline_text((0, 0), audiotext, fill=(int((float(score)+1)*127), 0, int((1-float(score))*127)), font=font)
im.show()