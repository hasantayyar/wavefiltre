# -*- coding: utf-8 -*-
#!/usr/bin/python
# Copyright (C) 2010  Hasan Tayyar BEŞİK
# tayyar.besik@gmail.com


import re
import urllib2


from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi.document import Range



def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


def OnBlipSubmitted(properties, context):
	"""Invoked when a Blip is submitted to the wave."""
	blip = context.GetBlipById(properties['blipId'])
	contents = blip.GetDocument().GetText()
	dic1 = {'manyak':'m***k','okuz':'o***z','aptal':'a***l','mongol':'****','yalaka':'******','salak':'******'}	

	response = urllib2.urlopen('http://tayyarrobotfiltre.appspot.com/argo.txt')
	#dic = eval('{%s}' % open("/argo.txt","r").read())
	dic = eval('{%s}' % response.read().encode('utf-8'))

	newcontents = replace_all(contents,dic)
	if newcontents != contents:
		blip.GetDocument().SetText(newcontents)
	#blip.GetDocument().SetText(dic)
	#blip.GetDocument().SetText(response.read())
	
def OnDocumentChanged(properties, context):
        """Invoked when the document is edited."""
        pass

def OnRobotAdded(properties, context):
        """Invoked when the robot has been added."""
        root_wavelet = context.GetRootWavelet()
        root_wavelet.CreateBlip().GetDocument().SetText("Merhaba; Ben bir robotum. Konuşmalardaki kötü ifadeleri kaldırırım.  ;)")

if __name__ == '__main__':
        myRobot = robot.Robot('Tayyar Robot Filtreleme',
                        image_url='http://tayyarrobotfiltre.appspot.com/assets/icon.png',
                        version='2',
                        profile_url='http://tayyarrobotfiltre.appspot.com/assets/profile.html')
        myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
        myRobot.RegisterHandler(events.DOCUMENT_CHANGED, OnDocumentChanged)
        myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
        myRobot.Run()