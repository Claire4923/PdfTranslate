### 功能
在OcrTranslateDemo.py中提供翻译pdf路径，项目将自动拆解为图片存入images。每个image向有道接口发起图片翻译，并写回。最后打包回pdf文件。

##### BTW
如果一开始就已经是图片，请自行改代码跳过第一步骤。

### 运行环境
1. python 3.6版本及以上。

### 使用
1. 接口参数、应用ID及应用密钥需自行填充，可以访问 [有道](https://ai.youdao.com)。
2. 运行python OcrTranslateDemo.py

### 说明
本项目基于有道智云paas接口的python语言调用示例。