import openai
from pymongo import MongoClient

# 這個優
openai.api_key = "API KEY"


def extract_keywords(text):
	response = openai.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
			{
				"role": "system",
				"content": "You will be provided with a block of text, and your task is to translate text to extract a list of keywords from it.for example: input: 今天期中考，但我覺得我還没有準備好，好焦慮 output: 期中考, 沒準備好, 焦慮",
			},
			{
				"role": "user",
				"content": f"Extract keywords from the following text:\n\n{text}\n\n",
			},
		],
		max_tokens=60,
		temperature=0.3,
	)
	message_dict = response.choices[0].to_dict()
	keywords = message_dict["message"]["content"].strip()
	return keywords


# # 示例文本
# documents = open("C:/Users/Acer/Desktop/1.txt", "r", encoding="utf-8").read()
# documents = documents.split('\n')
# # print(documents)
# # 提取关键字
# for i in documents:
#     keywords = extract_keywords(i)
#     with open("text_record.txt", "a", encoding="utf-8") as f:
#         f.write(keywords + "\n")
# # Keywords: 期中考, 准备, 焦虑, 下雨, 鸟屎, 衰, 派对, 朋友, 聊天, 尴尬, 孤独
# # 蛋糕, 快樂, 考試, 交作業, 焦慮, 時間不夠, 大雨, 衣服, 褲子, 鞋子, 濕掉, 倒楣

# 連接到 MongoDB Atlas
client = MongoClient(
	"mongodb+srv://jimmy147156:ubw2uG2QIkXYcgZf@cluster0.zbbv4pu.mongodb.net/"
)
db = client["test"]
collection = db["formdatas"]
AllDocument = collection.find()
text = []
for document in AllDocument:
	if document:
		mood_word = document.get("MoodWord", "")  # 假設文件中有一個 'MoodWord' 欄位
		text.append(mood_word)
  
with collection.watch() as stream:
	for change in stream:
		if change["operationType"] == "insert":
			document = change["fullDocument"]
			mood_word = document.get("MoodWord", "")
			text.append(mood_word)
			print(mood_word)
			text = ', '.join(text)
			print(text)
# keywords = extract_keywords(text)
# print(keywords)
