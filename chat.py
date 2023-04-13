import eel
import eel.browsers
import os
import shutil
import subprocess
import json
import vocal_splitter
import multiprocessing as mp
import threading
import re

fullScreen = False

eel.init("web")
download_path = 'C:/Users/V Yang/pikaraoke-songs/'

# Exposing the random_python function to javascript

@eel.expose
def startNewDownload(song_url):
	threading.Thread(target = download_video, args=(song_url, ), daemon=True).start()

@eel.expose
def download_video(song_url = '', include_subtitles = False, high_quality = True):
		dl_path = "%(title)s---%(id)s.%(ext)s"
		opt_quality = ['-f', 'bestvideo[ext!=webm][height<=1080]+bestaudio[ext!=webm]/best[ext!=webm]'] if high_quality else ['-f', 'mp4']
        
		opt_sub = ['--sub-langs', 'all', '--embed-subs'] if include_subtitles else []
		
		cmd = [get_default_youtube_dl_path('windows')] + opt_quality + \
            ["-o", download_path+'tmp/'+dl_path] + opt_sub + [song_url]

		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

		progress_regex = re.compile(r'\s+(\d+\.\d)%')

		for line in process.stdout:
        # Check if the line contains the download progress
			match = progress_regex.search(line)
			if match:
				percentage = float(match.group(1))
				eel.getDownloadProgress(get_downloaded_file_basename(song_url), percentage)


		_, stderr = process.communicate()
		rc = process.wait()

		if rc != 0:
			error_message = stderr.strip()
			if "is not a valid URL" in error_message: 
				eel.errorMessage(error_message)
			else:
				cmd = [get_default_youtube_dl_path('windows'), "-o", download_path + 'tmp/' + dl_path] + opt_sub + [song_url]
				rc = subprocess.call(cmd)  # retry once. Seems like this can be flaky
		if rc == 0:
			bn = get_downloaded_file_basename(song_url)
			if bn:
				shutil.move(download_path+'tmp/'+bn, download_path+bn)

		return rc
    
def get_yt_dlp_json(url):
        out_json = subprocess.check_output(
            [get_default_youtube_dl_path('windows'), '-j', url], creationflags=subprocess.CREATE_NO_WINDOW)
        return json.loads(out_json)

def get_downloaded_file_basename(url):
        try:
            youtube_id = url.split("watch?v=")[1].split('&')[0]
        except:
            try:
                info_json = get_yt_dlp_json(url)
                youtube_id = info_json['id']
            except:
                return None

        try:
            return [i for i in os.listdir(download_path+'tmp/') if youtube_id in i][0]
        except:
            pass

        filename = f"{info_json['title']}---{info_json['id']}.{info_json['ext']}"
        return filename if os.path.isfile(download_path+'tmp/'+filename) else None

def get_default_youtube_dl_path(platform):
	# use Python's cross-platform way
	shutil_path = shutil.which('yt-dlp')
	if shutil_path:
		return shutil_path

	if platform == "windows":
		choco_ytdl_path = r"C:\ProgramData\chocolatey\bin\yt-dlp.exe"
		scoop_ytdl_path = os.path.expanduser(r"~\scoop\shims\yt-dlp.exe")
		if os.path.isfile(choco_ytdl_path):
			return choco_ytdl_path
		if os.path.isfile(scoop_ytdl_path):
			return scoop_ytdl_path
		return r"C:\Program Files\yt-dlp\yt-dlp.exe"
	default_ytdl_unix_path = "/usr/local/bin/yt-dlp"
	if platform == "osx":
		if os.path.isfile(default_ytdl_unix_path):
			return default_ytdl_unix_path
		else:
			# just a guess based on the default python 3 install in OSX monterey
			return "/Library/Frameworks/Python.framework/Versions/3.10/bin/yt-dlp"
	else:
		return default_ytdl_unix_path
	
@eel.expose
def get_devocalised_song():
	# print(f'{download_path}/completed/{bn1}')
	song_list = []
	devocalised_path = download_path + 'completed'
	for bn in [i for i in os.listdir(devocalised_path) if not i.startswith('.') and os.path.isfile(devocalised_path+'/'+i)]:
		song_list.append(bn)

	eel.getCompletedSong(song_list)

@eel.expose
def get_downloaded_song():
	# print(f'{download_path}/completed/{bn1}')
	song_list = []
	downlaoded_path = download_path
	for bn in [i for i in os.listdir(downlaoded_path) if not i.startswith('.') and os.path.isfile(downlaoded_path+'/'+i)]:
		song_list.append(bn)

	eel.getDownloadedSong(song_list)

@eel.expose
def get_downloading_song():
	# print(f'{download_path}/completed/{bn1}')
	song_list = []
	downlaoding_path = download_path + 'tmp'
	for bn in [i for i in os.listdir(downlaoding_path) if not i.startswith('.') and os.path.isfile(downlaoding_path+'/'+i)]:
		if os.path.splitext(downlaoding_path+'/'+bn)[1].lower() == '.mp4':
			song_list.append(bn)

	eel.getDownloadingSong(song_list)

def remove_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# Usage example


# download_video('https://www.youtube.com/watch?v=ODiudky168I')
if __name__ == '__main__':
	
	# threading.Thread(target = download_video, args=('https://www.youtube.com/watch?v=ODiudky168I', ), daemon=True).start()
	# threading.Thread(target = download_video, args=('https://www.youtube.com/watch?v=sVTy_wmn5SU', ), daemon=True).start()
	eel.start("index.html", block=False, mode='electron', port=4000)

	# remove_all_files_in_folder(download_path + 'tmp')
	vocal_process = mp.Process(target=vocal_splitter.main, args=(['-p', '-d', download_path],))
	vocal_process.start()

	o = 0
	while True:
		eel.sleep(1)
		o += 10
					

	