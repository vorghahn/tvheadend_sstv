#!/usr/bin/env python
# -*- coding: utf-8 -*-

#generate m3u8 file for TVHeadend
#Save this into /usr/bin ensure HTS user has read/write and the file is executable

from os import path
import urllib.request
import json

__appname__ = 'TVH_SSTV_M3u8_automator'
__author__ = 'A few dudes'
__version__ = '1.0'
__license__ = 'MIT'


class programinfo:
	epg = ""
	description = ""
	channel = 0
	channelname = ""


def main():
	m3u8 = "/home/hts/.xmltv/SmoothStreamsTV.m3u8" #i wouldn't change this
	script = "pipe:///path/to/file/sstv-play.sh" #change this
	print('Generating playlist')

	jsonGuide1 = getJSON("https://sstv.fog.pt/epg/channels.json")
	generatePlaylists(jsonGuide1, script, m3u8)

def getJSON(sURL):
	try:
		sJSON = urllib.request.urlopen(sURL).read().decode("utf-8")
		retVal = json.loads(sJSON)
	except:
		return json.loads("{}")

	return retVal

def writePlaylistFile(fileName, body):
	'''write playlist to a local file'''

	# open file to write, or create file if DNE, write <body> to file and save

	with open(fileName, 'w+', encoding='utf-8') as f:
		f.write(body)
		f.close()

	# check for existence/closure of file
	if f.closed:
		print('Playlist built successfully, located at: ' + path.abspath(fileName))
	else:
		raise FileNotFoundError


def generatePlaylists(jsonGuide1, script, m3u8location):
	urlTemplate = script + ' {0}'
	m3u8TrackTemplate = '#EXTINF:-1 tvg-name="{0}" tvg-id="{1}" tvh-chnum="{2}" tvg-logo="http://guide.smoothstreams.tv/assets/images/channels/{2}.png",{0}\n{3}\n'
	m3u8 = '#EXTM3U\n'

	trackCounter = 0
	foundChannels = 0
	guide = getProgram(jsonGuide1)
	maxChannel = 0
	for item in guide:
		if int(item) > maxChannel:
			maxChannel = int(item)



	for channel in range(1, len(guide)+1):
		program = guide[channel]
		url = urlTemplate.format(format(channel, "02"))
		print('\r' + str(channel) + "/" + str(maxChannel),)
		if program.channelname == "":
			program.channelname = str(channel)
		else:
			program.channelname = str(channel) + " " + program.channelname
		m3u8 += m3u8TrackTemplate.format(program.channelname, program.epg, program.channel, url)
		foundChannels += 1
		trackCounter = trackCounter + 1
	print()

	if (foundChannels == 0):
		print("No channels found")
	else:
		print(str(foundChannels) + " channels found")
		writePlaylistFile(m3u8location, m3u8)


def getProgram(jsonGuide1):
	guide = {}

	for item in jsonGuide1:
		retVal = programinfo()
		# print(jsonGuide1)
		oChannel = jsonGuide1[item]
		retVal.channel = oChannel["channum"]
		channel = int(oChannel["channum"])
		retVal.channelname = oChannel["channame"].replace(format(channel, "02") + " - ", "").strip()
		if retVal.channelname == 'Empty':
			retVal.channelname = ""
		retVal.epg = oChannel["xmltvid"]
		guide[channel] = {}
		guide[channel] = retVal

	return guide

if __name__ == '__main__':
	main()
