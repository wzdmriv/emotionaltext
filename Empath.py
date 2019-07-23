import requests

url = 'https://api.webempath.net/v2/analyzeWav'


wavfilename = r"C:\Users\wzdmr\Desktop\Projects\sample.wav"
api_key = "xqLTBr_fo_nbI-V3SebCmBcs_1gB6OkzqlQckbGdBcY"
wav = open(wavfilename, 'rb').read()

headers  = {'Content-type': "multipart/form-data"}
data = {'apikey': api_key,
         'wav': open(wavfilename, 'rb')
        }

response = requests.post(url,data = data,headers = headers)

print(response.status_code)
print(response.content)