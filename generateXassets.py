#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = "Mohamed Habbat (mohamedhabbat@icloud.com)"

import os
import sys
import json
import shutil
import argparse
from time import sleep

iphone = 'iphone'	
scale = ['1x', '2x', '3x']
ext = ['.jpeg', '.jpg', '.png']
log = ''
imageset = '.imageset'
DicOfMissingImages = {}
global verbose

# Get list of images from directory
def getListOfImages(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(directory+'/'+f)
             if f.endswith(tuple(ext))]
    if(verbose):
    	print 'files length  {} \n'.format(len(files))
    sorted(files)
    return files


def add2xToImage(lst,directory):
	for i in range(0, len(lst) , 1):
		tmp=lst[i]
		imagename = tmp[0:len(tmp) - 4]
		extention = tmp[len(tmp) - 4:len(tmp)]
		if(verbose):
			print 'Image name %s' % (imagename,extention)
		tmp[0:len(tmp) - 4]
		os.rename(directory+'/'+tmp,directory+'/'+imagename+'@2x'+extention)
	

# Create tuple of available image assets from list of image name
def group(lst):
	finalList = []
	global log
	global DicOfMissingImages
	listOf1xImg = []
	listOf2xImg = []
	listOf3xImg = []
	for i in range(0, len(lst) , 1):
	
		tmp=lst[i]
	
		val=''
		val2x = ''
		val3x = ''
		valLen = len(tmp)
		tl = [None,None,None]

		if tmp and scale[2] in tmp:
			val3x = tmp
			val2x = tmp.replace('@3x','@2x')
			val = tmp.replace('@3x','')
		elif tmp and scale[1] in tmp:
			val2x = tmp
			val3x = tmp.replace('@2x','@3x')
			val = tmp.replace('@2x','')
		elif tmp:
			val = tmp
			val2x = val[0:valLen - 4]+'@2x' + val[valLen - 4:valLen]
			val3x = val[0:valLen - 4]+'@3x' + val[valLen - 4:valLen]
		
		if valExistOnTlist(val,finalList) or valExistOnTlist(val2x,finalList) or valExistOnTlist(val3x,finalList):
			continue
				
		if val in lst:
			tl[0] = val
		else:
			log = log + 'Image %s does not exist\n' % val
			listOf1xImg.append(val)
			
		if val2x in lst:
			tl[1] = val2x
		else:
			log = log + 'Image %s does not exist\n' % val2x
			listOf2xImg.append(val)
			
		if val3x in lst:
			tl[2] = val3x
		else:
			log = log + 'Image %s does not exist\n' % val3x
			listOf3xImg.append(val)
		
		DicOfMissingImages= {'1x' : listOf1xImg, '2x': listOf2xImg, '3x':listOf3xImg}
		finalList.append(tuple(tl))
	return finalList


def printListOfTuple(listOfTuple):
    for x in listOfTuple:
        print x[0], x[1]
        
def valExistOnTlist(val, finalList):
	for j, (a, b,c) in enumerate(finalList):
		if (val and val == a) or (val and val == b) or (val and  val == c):
			return True
	return False

# createXassests: Create images directories, move images to directory and generate Contents.json file
def createXassests(listOfTuple, defaultDir='.'):

    print 'createXassests function\n'
    print 'listOFtuple length  {}\n'.format(len(listOfTuple))
    
    for (i, a) in enumerate(listOfTuple):
        #print 'tuple a {} b {} c {} \n'.format(a[0], a[1], a[2])
        
    	data = {}
    	dic1 = {}
    	dic2 = {}
    	dic3 = {'idiom': iphone, 'scale': '2x', 'subtype': 'retina4'}
    	dic4 = {'idiom': iphone, 'scale': scale[2]}
    	
    	extension = ''
    	imagename = ''
    	
        if a[0]:
        	dic1 = {'idiom': iphone, 'scale': scale[0], 'filename': a[0]}
        	folderName = (a[0])[0:len(a[0]) - 4]
    	else:
        	dic1 = {'idiom': iphone, 'scale': scale[0]}       
        if a[1]:
        	dic2 = {'idiom': iphone, 'scale': scale[1], 'filename': a[1]}
        	folderName = (a[1])[0:len(a[1]) - 4]
        	folderName = folderName.replace('@2x','')
        else:
        	dic2 = {'idiom': iphone, 'scale': scale[1]}
        
        if a[2]:
        	dic4 = {'idiom': iphone, 'scale': scale[2], 'filename': a[2]}
        	folderName = (a[2])[0:len(a[2]) - 4]
        	folderName = folderName.replace('@3x','')
        else:
        	dic4 = {'idiom': iphone, 'scale': scale[2]}

        data = {'images': [dic1, dic2, dic3, dic4],'info': {'version': 1, 'author': 'xcode'}}
        
        if folderName:
        	folderName = folderName + imageset
        	setupImageDirectory(defaultDir + '/' + folderName)
    	else:
    		continue
    	
    	
    	with open(defaultDir + '/' + folderName + '/' + 'Contents.json', 'wb') as outfile:
    		try:
    			json.dump(data, outfile, indent=4)
    		except TypeError:
    			print 'Unable to serialize the object'
    	if a[0]:
    		try:
    			shutil.copy(defaultDir + '/' + a[0], defaultDir + '/' + folderName)
    		except IOError, e:
    			print 'Unable to copy file. %s' % e
    	if a[1]:
    		try:
    			shutil.copy(defaultDir + '/' + a[1], defaultDir + '/' + folderName)
    		except IOError, e:
    			print 'Unable to copy file. %s' % e
    	if a[2]:
    		try:
    			shutil.copy(defaultDir + '/' + a[2], defaultDir + '/' + folderName)
    		except IOError, e:
    			print 'Unable to copy file. %s' % e


def setupImageDirectory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)


if __name__ == '__main__':
	
	#############################################
	#############################################
	# Usage: 									#
	#	python generateXassects.py directory -v # 
	#	python generateXassects.py directory  	#
	#############################################
	#############################################
	verbose = False
	parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(__file__, description="This script organise assets as per iOS xassets structure\n Folder name contain Images (1x - 2x  -3x) and Contents.json")
	parser.add_argument("--directory", "-d", help="The directory name", type=str, default='.')
	parser.add_argument("--rename", "-r", help="Add @2x to images", action="store_true")
	parser.add_argument("--missing", "-m", help="Save missing images as json file", action="store_true")
	parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
	
	args = parser.parse_args()
	if(args.verbose):
		verbose = args.verbose
	if(args.directory):
		if os.path.exists(args.directory):
			print 'Directory %s\n' % args.directory 
	else:
		print 'Directory does not exist'
		sys.exit()
		
	if(args.rename):
		add2xToImage(getListOfImages(args.directory), args.directory)
	else:
		createXassests(list(group(getListOfImages(args.directory))),args.directory)

		
	if(args.missing):
		with open(defaultDir + '/'  + 'missingimages.json', 'wb') as outfile:
			try:
				json.dump(DicOfMissingImages, outfile, indent=4)
			except TypeError:
				print 'Unable to serialize the object'
	if(args.verbose and DicOfMissingImages and not args.rename):
		print "There are %s missing 1x images " % len(DicOfMissingImages['1x'])
		print "There are %s missing 2x images " % len(DicOfMissingImages['2x'])
		print "There are %s missing 3x images " % len(DicOfMissingImages['3x'])