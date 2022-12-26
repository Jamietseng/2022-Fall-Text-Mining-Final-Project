import requests
from bs4 import BeautifulSoup as bs4
import re
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#example: https://mojim.com/twh100012.htm
def getArtistAllTracks(href):
    resp = requests.get(href)
    soup = bs4(resp.text, 'html.parser')
    track_html = soup.select('.hc3 > a')
    track_href = [i.get('href') for i in track_html]
    track_name = [i.get_text() for i in track_html]
    res = {'trackNames':track_name, 'trackHrefs': track_href}
    print("Finish Retrieving Hrefs.")
    return res

# example: https://mojim.com/twy100012x78x1.htm
def exportOneTrackLyrics(href):
    try:
        # 1. get html
        domain = 'https://mojim.com'
        res = requests.get(domain+href)
        # 2. parse into tree
        soup2 = bs4(res.text, 'html.parser')
        # 3. get track name, get lyrics
        trackName = soup2.select('#fsZx2')[0].get_text().strip()
        print(f"Start Processing {trackName}...")
        # 4. text cleaning:
            # 4-a: 去除最下面的感謝tag: <ol>
        lyrics = soup2.select('#fsZx3')[0]
        for i in lyrics("ol"): 
            i.extract()
            #4-b: 去除雜訊
        result = list()
        for line in lyrics.stripped_strings:
            if "更多更詳盡歌詞" in line or "魔鏡歌詞網" in line or "Mojim.com" in line:
                continue
            if "："in line: 
                continue
            if line.find('[') != -1 or line.find(']') != -1 : 
                continue
            if "無歌詞" in line:
                continue
            if "---" in line:
                continue
            if len(re.findall('[　１２３４５６７８９０＊●＃＠＄％＾＆！＿『』｜，。？a-zA-Z0-9～【】＿\"\!\&\.\?\(\)\~\-\…\,]', line)) != 0:
                line = re.sub('[　１２３４５６７８９０＊●＃＠＄％＾＆！＿『』｜，。？a-zA-Z0-9～【】＿\"\!\&\.\?\(\)\~\-\…\,]', "", line)
            result.append(line)
            #4-c: 製作無空格版本
        nos2 = ["".join(i.split()) for i in result]
        nos2 = "".join(nos2)
        # 5. 製作json, 輸出
        r = {'trackName': trackName, 'lyric_line': result, 'lyric_full': nos2}
        print("Export Over.")
        return r
    except:
        print("no data.")
        return None
    

# produce lyrics of artist tracks
def exportArtistAllTracks(href, fileName):
    alltracks = getArtistAllTracks(href)['trackHrefs']
    data = pd.DataFrame(columns=['trackName', 'lyric_line', 'lyric_full'])
    for i in range(len(alltracks)):
        result = exportOneTrackLyrics(alltracks[i])
        if result != None and len(result['lyric_line']) > 0:
            data = data.append({'trackName': result['trackName'], 'lyric_line': result['lyric_line'], 'lyric_full': result['lyric_full']}, ignore_index=True)
    data.to_csv(f"{fileName}.csv", encoding='utf-8-sig', index=False)
    print("Finish Processing.")
    return


# artists = ['https://mojim.com/twh100951.htm', 'https://mojim.com/twh104266.htm', 'https://mojim.com/twh100163.htm']
# name = ["JayChou", "PiggyLo", "Jolin"]
artists = ['https://mojim.com/twh100163.htm']
name = ["Jolin2"]
for i in range(1):
    print(f"Now: {name[i]}")
    exportArtistAllTracks(artists[i], name[i])