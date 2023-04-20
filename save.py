import os

class Save:
    def __init__(self):
        self.__path = os.path.dirname(__file__)
        self.__data = os.path.join(self.__path, "resoure", "save.txt")
        try:
            self.__high_score_txt = int(self.__Data_Reading())
        except: # 파일이 없으면 FileNotFoundError, 읽은 내용이 숫자가 아니면 ValueError
            with open(self.__data, "w", encoding='utf8') as f:
                f.write(str(0))

            self.__high_score_txt = int(self.__Data_Reading())

    def save(self, num : int):
        self.__high_score_txt = num

        self.__Data_Write(self.__high_score_txt)

    def road(self):
        return self.__high_score_txt

    def __Data_Reading(self):
        with open(self.__data, "r", encoding='utf8') as f:
            data = f.read()
        return data

    def __Data_Write(self, txt):
        with open(self.__data, "w", encoding='utf8') as f:
            f.write(str(txt))

if __name__ == "__main__":
    os.startfile("C:/code/가디언테일즈/T-tatGee Runner/main.py")