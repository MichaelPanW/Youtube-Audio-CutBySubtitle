
import sys
from subtitleYoutube import subtitleYoutube

#video_id = sys.argv[1]
# stYoutube=subtitleYoutube(video_id)
# stYoutube.downloadSubAndWav()
# stYoutube.cutYoutube()
from subprocess import run
#playlist=run("youtube-dl -f mp4 PL02zpjjwMEjrqiaue3yhtlVqP_3b4gOiP")
from pytube import Playlist
import progressbar

#傳入播放清單網址,保存的標籤
def list(url,mName=""):
    pl = Playlist(url)
    index = 0
    p = progressbar.ProgressBar()
    p.start()
    f = open('list_' + mName + '.csv', 'w')
    f.close()
    for i in pl.parse_links():
        index = index + 1
        # print(i.replace("/watch?v=",""))
        stYoutube = subtitleYoutube(i.replace("/watch?v=", ""),mName)
        stYoutube.downloadSubAndWav()
        stYoutube.cutSubtitle()
        p.update(int(index / len(pl.parse_links()) * 100))
    p.finish()

if __name__ == '__main__':
    list("https://www.youtube.com/watch?v=d2m7StPgmeU&list=PL02zpjjwMEjq6BTXjukFc3e4ylsYzXkif","xiaohe")
