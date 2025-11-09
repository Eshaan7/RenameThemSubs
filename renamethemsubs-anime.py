#!/usr/bin/env python3

import os
import re

def menu():
	print("\t"+"*"*8+"MENU"+"*"*8)
	print("\n\t"+"-"*20)
	print("\tFor subs and video files,")
	print("\t1. In same directory")
	print("\t2. In different directory")
	print("\t3. In current directory: {0}".format(os.getcwd()))
	print("\t"+"-"*20)
	choice = int(input("\n\tEnter choice(1-3): "))
	return choice

def diff_path():
	vid_path = str(input("Full path to video directory(example: /home/...): "))
	sub_path = str(input("Full path to subtitles directory(example: /home/...): "))
	sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
	vidFiles = []
	subFiles = []
	for name in os.listdir(vid_path):
		if (name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')):
			vidFiles.append(name)
	for name in os.listdir(sub_path):
		if (name.endswith(sub_format)):
			subFiles.append(name)
	rename_files(sub_path, vidFiles, subFiles, sub_format)
	return 

def same_path():
	dir_path = str(input("Full path to video directory(example: /home/...): "))
	sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
	dirFiles = os.listdir(dir_path)
	vidFiles = []
	subFiles = []
	for name in dirFiles:
		if (name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')):
			vidFiles.append(name)
		elif (name.endswith(sub_format)):
			subFiles.append(name)
	rename_files(dir_path, vidFiles, subFiles, sub_format)
	return

def for_current_dir():
	dir_path = os.getcwd()
	dirFiles = os.listdir(dir_path)
	vidFiles = []
	subFiles = []
	sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
	for name in dirFiles:
		if (name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')):
			vidFiles.append(name)
		elif (name.endswith(sub_format)):
			subFiles.append(name)
	rename_files(dir_path, vidFiles, subFiles, sub_format)
	return

def extract_episode_number(filename):
	pattern1 = r'\[(\d{2})\]'
	match = re.search(pattern1, filename)
	if match:
		return int(match.group(1))
	
	pattern2 = r'(?<!\d)(\d{2})(?!\d)'
	match = re.search(pattern2, filename)
	if match:
		return int(match.group(1))
	
	return None

def rename_files(path, vidFiles, subFiles, sub_format):
	vid_episodes = []
	sub_episodes = []
	
	for vfile in vidFiles:
		ep_num = extract_episode_number(vfile)
		if ep_num is None:
			print(f"ERROR: Could not extract episode number from video file: {vfile}")
			return
		vid_episodes.append((ep_num, vfile))
	
	for sfile in subFiles:
		ep_num = extract_episode_number(sfile)
		if ep_num is None:
			print(f"ERROR: Could not extract episode number from subtitle file: {sfile}")
			return
		sub_episodes.append((ep_num, sfile))
	
	vid_episodes.sort(key=lambda x: x[0])
	sub_episodes.sort(key=lambda x: x[0])
	
	os.chdir(path)
	try:
		assert(len(sub_episodes)==len(vid_episodes))
		for i, (vid_ep, vname) in enumerate(vid_episodes):
			sub_ep, sname = sub_episodes[i]
			print("{0} (ep {1}) renamed to {2} (ep {3})".format(sname, sub_ep, os.path.splitext(vname)[0], vid_ep))
			os.rename(sname, os.path.splitext(vname)[0]+sub_format)
	except AssertionError:
		print(f"ERROR: Number of subtitle files ({len(sub_episodes)}) does not match number of video files ({len(vid_episodes)})")
	return



def main():
	choice = menu()
	if choice==1:
		same_path()
	elif choice==2:
		diff_path()
	elif choice==3:
		for_current_dir()
		
main()

