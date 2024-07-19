import io
import pickle

buffer = io.BytesIO
print(buffer)
# print(buffer.seek(0))
t = open('test.txt', 'wb', encoding='utf-8')
print(t.read())