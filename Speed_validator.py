'''
Speed Validator
This module is used to validate the crew's speed during their RSP validations.  
Drag and drop routes onto the route list window to use this.  

Created on Oct 9, 2013

@author: Elliott Locke
'''
from Tkinter import Tk
from tkFileDialog import askdirectory
import tkMessageBox
import easygui as eg
import os, sys, glob
import numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
# These imports below needed to be added in order to get a usable py app.  
from reportlab.pdfbase import _fontdata_enc_winansi
from reportlab.pdfbase import _fontdata_enc_macroman
from reportlab.pdfbase import _fontdata_enc_standard
from reportlab.pdfbase import _fontdata_enc_symbol
from reportlab.pdfbase import _fontdata_enc_zapfdingbats
from reportlab.pdfbase import _fontdata_enc_pdfdoc
from reportlab.pdfbase import _fontdata_enc_macexpert
from reportlab.pdfbase import _fontdata_widths_courier
from reportlab.pdfbase import _fontdata_widths_courierbold
from reportlab.pdfbase import _fontdata_widths_courieroblique
from reportlab.pdfbase import _fontdata_widths_courierboldoblique
from reportlab.pdfbase import _fontdata_widths_helvetica
from reportlab.pdfbase import _fontdata_widths_helveticabold
from reportlab.pdfbase import _fontdata_widths_helveticaoblique
from reportlab.pdfbase import _fontdata_widths_helveticaboldoblique
from reportlab.pdfbase import _fontdata_widths_timesroman
from reportlab.pdfbase import _fontdata_widths_timesbold
from reportlab.pdfbase import _fontdata_widths_timesitalic
from reportlab.pdfbase import _fontdata_widths_timesbolditalic
from reportlab.pdfbase import _fontdata_widths_symbol
from reportlab.pdfbase import _fontdata_widths_zapfdingbats

def speedValidator():
    #Go through the filepath text - which is created from the drag and drop GUI.  
    
    filepath = "/usr/local/Library/Digilog_Utilites.txt"
    filetext = open(filepath, 'r')

    routesdir = []
    for path in filetext:
        routesdir.append(path.strip())

    rspfilepaths = []    
    for route in routesdir:
        os.chdir(route)
        for files in glob.glob("*.rsp"):
            rspfilepaths.append(route + files)
    
    fileDir = eg.diropenbox(msg = "Where would you like your Speed Reports?", title = "Choose the directory for your Reports.")
    
#     rspfilepaths = []
# #     RouteDirs = get_immediate_subdirectories(fileDir)
#     
#     for dirs in RouteDirs:
#         fulldir = os.path.join(fileDir,dirs)
#         os.chdir(fulldir)
 
    
    #Make a bunch of lists of the items that I will need from each route.  
    MaximumList = []
    MinimumList = []
    AverageList = []
    listoftenthavgspeedlist = []
    listoflistsofspeedlist = []
    stdevList = []
    listofspeedlists = [] 
    cnt = 1
    for thisrsp in rspfilepaths:
        speedList, interval = getrspinfo(thisrsp)

        #Averages:
        total = 0
        speedlistfloat = []
        for num in speedList:
            speedlistfloat.append(float(num))
            total = float(num) + total
            listofspeedlists.append(float(num))  
        listoflistsofspeedlist.append(listofspeedlists)
        lengthList = float(len(speedList))
        average =  float(total)/float(lengthList)
        AverageList.append(average)

        #min and max:
        maximumspeed = max(speedlistfloat)
        minimumspeed = min(speedlistfloat)
        MaximumList.append(float(maximumspeed))
        MinimumList.append(float(minimumspeed))
        
        #stdev:
        stdSpeedList = []
        for num in speedList:
            stdSpeedList.append(float(num))
        stdev = numpy.std(stdSpeedList)
        stdevList.append(stdev)
        
        #get the tenth of a route list
        listoftenthavgspeedlist.append(getlistaverageforten(speedList, lengthList)) #This will be a list of the averages of a tenth of the route.  
        
        #Distance list
        xdistanceAxis_notrounded = []
        for i in range(0,int(lengthList)):
            xdistanceAxis_notrounded.append(i*interval)
            xmax = i*interval
        xdistanceAxis = []
        for number in xdistanceAxis_notrounded:
            xdistanceAxis.append(round(number, 4))
            
        #Graph:
        plt.plot(xdistanceAxis, speedList, label = 'route '+ str(cnt))  #Don't want the entire route's name in the legend.  
        plt.ylabel("Speed (mph)")
        plt.xlabel("Distance (miles )")
        ymax = float(maximumspeed)+int(5)
        ymin = float(minimumspeed)-int(10)
        plt.axis([0, xmax, ymin, ymax])
        legend(loc=4, ncol=2, mode="expand", borderaxespad=0, prop={'size':10} )
        plt.title(os.path.basename(fileDir) + " Speed Validation")
        
        #Count for the graph legend
        cnt = cnt + 1
        
    graphPath = fileDir + '/' + os.path.basename(fileDir) + "_Graph.pdf"
    plt.savefig(graphPath) 
    
    #total routes std dev.
    totalstdev = numpy.mean(stdevList)
    if totalstdev >= 0.5:
        passfail = "Fail"
    else:
        passfail = "Pass"
    
    #total maximum/minimum
    totalMax = max(MaximumList)
    totalMin = min(MinimumList)
    
    #Total average of all the routes.
    totalspeed = 0
    for numb in AverageList:
        totalspeed = numb + totalspeed
    totalcount = len(AverageList)
    totalaverage = float(totalspeed)/totalcount
    totalaverage = round(totalaverage,1)
    
    #the rounded values for the averagelist.  This is not used really.  
    roundAvgList = []
    for avgnum in AverageList:
        roundAvgList.append(round(avgnum,1))
    
    #WAYYYY TOOO many variables put into this function.  Probably not the best programming technique.  
    textFilePath = createthetextfile(fileDir, listoftenthavgspeedlist, MaximumList, MinimumList, rspfilepaths, stdevList, roundAvgList, totalstdev, totalMax, totalMin, totalaverage, passfail)  
    #________________________________________________________________________________________________________________________________
    MainPDFPath = fileDir + "/" + os.path.basename(fileDir) + "_Validation.pdf"

    #Read the data from the text file
    MainValidation = open(textFilePath, 'r')
    Data = []
    for line in MainValidation:
        Data.append(line)
    MainValidation.close()
    
    elements = []
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(MainPDFPath)
     
    # Create two 'Paragraph' Flowables and add them to our 'elements'
    count = 1
    for line in Data:
        if count == 1: #This is the title line.
            elements.append(Paragraph('<font size = 18>' + line + '</font',  styles['Heading1']))
            elements.append(Paragraph('\n',  styles['Heading1']))
        elif count == 7: #This is the line at the end of the validation summary.  
            elements.append(Paragraph('<br/>',  styles['Heading1']))
            elements.append(Paragraph('<br/>',  styles['Heading1']))
            elements.append(Paragraph('<font size = 14>' + line + '</font',  styles['Normal']))
            elements.append(Paragraph('<br/>',  styles['Heading1']))
            elements.append(Paragraph('<br/>',  styles['Heading1']))
            elements.append(Paragraph('<br/>',  styles['Heading1']))
        else:
            elements.append(Paragraph('<font size = 10>' + line + '</font',  styles['Normal']))
        count = count + 1
    # Write the document to disk
    doc.build(elements)
    #________________________________________________________________________________________________________________________________
    #remove that text file and then display an ending message.
    os.remove(textFilePath)  
    window = Tk()
    window.wm_withdraw()
    tkMessageBox.showinfo(title="This is the End", message = "Work Complete.")
    

#Put the min, max, and averages in a text file.  and stdev
def createthetextfile(fileDir, listoftenthavgspeedlist, MaximumList, MinimumList, rspfilepaths, stdevList, roundAvgList, totalstdev, totalMax, totalMin, totalaverage, passfail):
        
    textFilePath = fileDir + "/SpeedValidation.txt"
    validationfile = open(textFilePath, 'w')
    validationfile.write("Speed Validation for: " + os.path.basename(fileDir) + '\n\n')
    
    validationfile.write("Average speed = " + str(totalaverage) + '\n')
    validationfile.write("Maximum speed = " + str(totalMax) + '\n')
    validationfile.write("Minimum speed = " + str(totalMin) + '\n')
    roundstdev = str(round(totalstdev,4))
    validationfile.write("Average Standard Deviation = " + roundstdev + '\n')
    
    validationfile.write("Grade: " + passfail + '\n')
    
    for x in range(0,len(rspfilepaths)):
        thisRoute = os.path.basename(rspfilepaths[x])
        validationfile.write(str(thisRoute) + '\n')
        thisroutespeed = listoftenthavgspeedlist[x]
        validationfile.write("Average list: ")
        for speed in thisroutespeed:
            validationfile.write(str(speed) + " ")
        validationfile.write("\n")
        thisaverage = str(roundAvgList[x])
        thisstddev = str(round(stdevList[x],4))
        thisRouteMax = str(MaximumList[x])
        thisRouteMin = str(MinimumList[x])
        validationfile.write("Average speed: " + thisaverage + " Standard Deviation: " + thisstddev + " Max: " + thisRouteMax + " Min: " + thisRouteMin + '\n<br/>')
    
    return textFilePath    
    
#Take the speed list and average it over a tenth of the route.  And then puts that in a list.
def getlistaverageforten(speedList, lengthList): 
    averageSpeedTen = []
    oneTenth = int(round(lengthList/10,0))
    for i in range(0,10):
        thisspeedList = speedList[int(i*oneTenth):int((i+1)*oneTenth)]
        thistotal = 0
        for num in thisspeedList:
            thistotal = float(num) + thistotal
        thisaverage = thistotal/oneTenth
        averageSpeedTen.append(thisaverage)
    roundavgspeed = []
    for avgnum in averageSpeedTen:
        roundavgspeed.append(round(avgnum,1))
    return roundavgspeed

#Get the speed information from the rsp path.
def getrspinfo(rspPath):
    rspfile = open(rspPath,'r')
    speedRows = []
    speed = []
    for line in rspfile:
        if line.startswith("5403"):
            speedRows.append(line)
    for row in speedRows:
        columns = row.split(',')
        speed.append(columns[3].strip())
    for thisrow in speedRows:
        columns = thisrow.split(',')
        dis2 = columns[2].strip()
        dis1 = columns[1].strip()
        interval = float(dis2)-float(dis1)
        break
    return speed, interval
    
def get_immediate_subdirectories(dirs):
    return [name for name in os.listdir(dirs) if os.path.isdir(os.path.join(dirs, name))]

if __name__ == '__main__':
    speedValidator()