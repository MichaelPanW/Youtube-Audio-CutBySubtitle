
from pytube import YouTube
import os
from subprocess import run
import sys
import webvtt
from pydub import AudioSegment
#https://stackoverflow.com/questions/30770155/ffprobe-or-avprobe-not-found-please-install-one

class subtitleYoutube():
    """A class for an building and inferencing an lstm model"""

    def __init__(self, v, name=""):
        self.v = v
        self.sub_lang = "zh-TW"
        self.vttPath = ""
        self.wavPath = ""
        self.name = name
        self.audioType="wav"

    def downloadSubAndWav(self, filepath="Movies"):
        # os.system("youtube-dl --write-sub --sub-lang " + self.sub_lang + "  --extract-audio  --audio-format wav -o " +
        #          filepath + "/" + self.v + ".%(ext)s --write-sub  https://www.youtube.com/watch?v=" + self.v)
        #--skip-download
        #lang = run("youtube-dl --write-sub --sub-lang " + self.sub_lang + "  --extract-audio  --audio-format wav -o " +
        #      filepath + "/" + self.v + ".%\(ext\)s --write-sub  https://www.youtube.com/watch?v=" + self.v)
        self.shCode()
        self.vttPath = filepath + "/" + self.v + "." + self.sub_lang + ".vtt"
        self.wavPath = filepath + "/" + self.v + "."+self.audioType
    #下載影片與字幕的指令
    def shCode(self):
        run("youtube-dl --write-sub --sub-lang zh-TW  --extract-audio  --audio-format "+self.audioType+" -o  Movies/" + self.v + ".%(ext)s --write-sub  https://www.youtube.com/watch?v=" + self.v)
    #裁切audio
    def cutYoutube(self, src="box"):
        outputList = {"vttPath": self.vttPath,
                      "wavPath": self.wavPath,
                      "name": self.v,
                      "sub_lang": self.sub_lang,
                      "text": "",
                      "start": "",
                      "end": "",
                      "key": "",
                      "cutFile": ""}
        i = 0
        sound = AudioSegment.from_file(self.wavPath)
        for caption in webvtt.read(self.vttPath):
            outputList['text'] = (
                caption.text.replace("\n", ""))  # caption text
            outputList['start'] = (caption.start)  # caption text
            outputList['end'] = (caption.end)  # caption text
            outputList['cutFile'] = src + "/" + self.v + \
                "_" + str(i) + "."+self.audioType  # caption text

            first_half = sound[timemath(caption.start):timemath(caption.end)]
            first_half.export(src + "/" + self.v + "_" +
                              str(i) + ".wav", format="wav")
            i = i + 1
            self.saveCSV(outputList)

    def saveCSV(self,list):
        try:
            #print('log_' + self.name + '.csv')
            f = open('log_' + self.name + '.csv', 'a')
            # encoding='utf-8'
            outStr = ""
            for key in list.keys():
                outStr = outStr + (str(list[key]) + ",")
            f.write(outStr)

            f.write("\n")
            f.close()
        except :
            value = ""

    def cutSubtitle(self, src="audio"):
        outputList = {"vttPath": self.vttPath,
                      "wavPath": self.wavPath,
                      "name": self.v,
                      "sub_lang": self.sub_lang,
                      "text": "",
                      "start": "",
                      "end": "",
                      "key": "",
                      "cutFile": ""}
        i = 0
        try:
            sound = AudioSegment.from_file(self.wavPath)

            for caption in webvtt.read(self.vttPath):
                outputList['text'] = (
                    caption.text.replace("\n", ""))  # caption text
                outputList['start'] = (caption.start)  # caption text
                outputList['end'] = (caption.end)  # caption text
                outputList['cutFile'] = src + "/" + self.v + \
                    "_" + str(i) + ".wav"  # caption text
                outputList['key'] = "key"
                first_half = sound[
                    timemath(caption.start):timemath(caption.end)]
                first_half.export(src + "/" + self.v + "_" +
                                  str(i) + ".wav", format="wav")
                i = i + 1
                first_half.export((src + "/" + self.v + "_" +
                                  str(i) + ".wav"), format="wav")
                self.saveCSV(outputList)

        except :
            print("eror"+self.wavPath)
            value = ""


def timemath(spdata):
    hour = int(spdata[:2]) * 3600 * 1000
    sec = int(spdata[3:5]) * 60 * 1000
    minu = int(spdata[6:].replace('.', ''))
    value = hour + sec + minu
    return value

