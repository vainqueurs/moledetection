import os,sys,re
import numpy as np
import pandas as pd
import pickle
import shutil
import clarifai
import matplotlib
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import regex as re
import matplotlib.pyplot as plt
import urllib
import urllib2
import requests

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage


%matplotlib inline
class DeepMole(object):

def __init__(self):
    self.PATH= "C:/data/CXO/ISIC-images"
    self.names=['Benign','Malignant']
    self.app = ClarifaiApp(api_key=key)
    self.model = self.app.models.get("general-v1.3")
    #self.errors =self.PATH+'/errorfile.csv'



def returntags(self,filename='',url='',returned=10):
    if len(filename)>0:
        a= self.model.predict_by_filename(filename)
        im = plt.imread(filename)
    else:
        urllib.urlretrieve(url,"clar2.jpg")
        a= self.model.predict_by_filename("clar2.jpg")
        im = plt.imread('clar2.jpg')
    for index in range(returned):
        print a['outputs'][0]['data']['concepts'][index]['name'], a['outputs'][0]['data']['concepts'][index]['value']
    plt.imshow(im)


def writeimages(self,counts=20):
    #  make a copy of the calendar folder with decoded data 
    # move to dask or map_async : seems slow
    data =set()
    self.counts = counts
    ids= dict()
    images=[]
    for name in self.names: 
        count =0
        os.chdir(str(self.PATH+'/' + name))
        filelist =  os.listdir(str(self.PATH+'/' + name+'/'))

        for fil  in filelist :
            if count < self.counts :
                try:
                    #print name, fil
                    filename=str(self.PATH+'/' + name+'/'+fil)

                    if str(fil).find('.txt')<0:
                        img = ClImage(filename=filename, concepts=[name])
                        images.append(img)
                        print filename
                        count +=1
                except Exception, e: 
                    print e
            else :
                break#print str(fil)
    print len(images)
    return images


def passimages(self,number,name):
    self.app.inputs.bulk_create_images(self.writeimages(number))
    self.model = self.app.models.create(model_id=name, concepts=(['Benign'],['Malignant']))
    self.model.train()
    #app.close()
    print 'done'
