import requests,os

spaceName = input('请输入目录名:')

os.mkdir('../themes/lite/static/images/' + spaceName)

urlList = input('请输入图片地址，多个图片请使用","分隔~')

urlList = urlList.split(',')

print(urlList)

for index,url in enumerate(urlList):
  r = requests.get(url, stream=True)
  with open('../themes/lite/source/static/images/' + spaceName + '/' + str(index + 1) + '.png', 'wb') as fd:
      for chunk in r.iter_content():
          fd.write(chunk)
