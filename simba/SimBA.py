import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=DeprecationWarning)
import os
import time
import subprocess
import itertools
#import deeplabcut
import csv
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename,askdirectory
from tkinter_functions import *
from create_project_ini import write_inifile
from tkinter import tix
import subprocess
import platform
import shutil
from tabulate import tabulate
from dlc_change_yamlfile import select_numfram2pick,updateiteration,update_init_weight,generatetempyaml,generatetempyaml_multi
from extract_features_wo_targets import extract_features_wotarget
from sklearn_DLC_RF_train_model import RF_trainmodel
from run_RF_model import rfmodel
from merge_frames import merge_frames_config
from prob_graph import *
from runmodel_1st import *
from path_plot import path_plot_config
from gantt import ganntplot_config
from data_plot import data_plot_config
from line_plot import line_plot_config
from merge_movie_ffmpeg import generatevideo_config_ffmpeg
from import_videos_csv_project_ini import *
from configparser import ConfigParser
from labelling_aggression import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from get_coordinates_tools_v2 import get_coordinates_nilsson
from process_data_log import analyze_process_data_log
from process_severity import analyze_process_severity
from process_movement import analyze_process_movement
import webbrowser
from process_videos_automation import *
from extract_seqframes import *
from classifierValidation import validate_classifier
from train_multiple_models_from_meta import *
from train_model_2 import *
from multiplecrop import *
import cv2
from validate_model_on_single_video import *
from ROI_freehand_draw_3 import roiFreehand
from ROI_analysis_2 import *
from ROI_plot import *
from ROI_draw_defined import *
from ROI_multiply import *
from ROI_reset import *
from ROI_add_to_features import *
from ROI_process_movement import *
from plot_heatmap import plotHeatMap
import warnings
from outlier_scripts.movement.correct_devs_mov_16bp import dev_move_16
from outlier_scripts.location.correct_devs_loc_16bp import dev_loc_16
from outlier_scripts.movement.correct_devs_mov_user_defined import dev_move_user_defined
from outlier_scripts.location.correct_devs_loc_user_defined import dev_loc_user_defined
from outlier_scripts.movement.correct_devs_mov_14bp import dev_move_14
from outlier_scripts.location.correct_devs_loc_14bp import dev_loc_14
from outlier_scripts.movement.correct_devs_mov_9bp import dev_move_9
# from outlier_scripts.movement.correct_devs_mov_8bp import dev_move_8
# from outlier_scripts.location.correct_devs_loc_8bp import dev_loc_8
# from outlier_scripts.movement.correct_devs_mov_7bp import dev_move_7
# from outlier_scripts.location.correct_devs_loc_7bp import dev_loc_7
# from outlier_scripts.movement.correct_devs_mov_4bp import dev_move_4
# from outlier_scripts.location.correct_devs_loc_4bp import dev_loc_4
from features_scripts.extract_features_16bp import extract_features_wotarget_16
from features_scripts.extract_features_14bp import extract_features_wotarget_14
from features_scripts.extract_features_14bp_from_16bp import extract_features_wotarget_14_from_16
from features_scripts.extract_features_9bp import extract_features_wotarget_9
from features_scripts.extract_features_8bp import extract_features_wotarget_8
from features_scripts.extract_features_7bp import extract_features_wotarget_7
from features_scripts.extract_features_4bp import extract_features_wotarget_4
from features_scripts.extract_features_user_defined import extract_features_wotarget_user_defined
from sklearn_plot_scripts.plot_sklearn_results_2 import plotsklearnresult
from drop_bp_cords import define_bp_drop_down
from drop_bp_cords import bodypartConfSchematic
from define_new_pose_config import define_new_pose_configuration
#from dpk_create_project_ini import write_dpkfile
#from dpk_script.create_annotation_set import createAnnotationSet
#from dpk_script.annotator import dpkAnnotator
#from dpk_script.train_model import trainDPKmodel
#from dpk_script.Predict_new_video import predictnewvideoDPK
#from dpk_script.Visualize_video import visualizeDPK
from reset_poseConfig import reset_DiagramSettings
from plot_threshold import plot_threshold
import threading

simBA_version = 1.1


class roitableRow(Frame):
    def __init__(self, parent =None ,dirname='',filename = '',widths = "" ,indexs='',projectini=''):
        self.projectini = projectini
        self.filename = os.path.join(dirname,filename)
        Frame.__init__(self,master=parent)
        var=StringVar()
        self.index = Entry(self,textvariable=var,width=4)
        var.set(indexs)
        self.index.grid(row=0,column=0)
        self.lblName = Label(self,text=filename,width =widths,anchor=W)
        self.lblName.grid(row=0,column=1,sticky=W)
        self.btnset = Button(self,text='Draw',command=self.draw)
        self.btnset.grid(row=0,column=2)
        self.btnreset = Button(self,text='Reset',command =self.reset)
        self.btnreset.grid(row=0,column=3)
        self.btnapplyall = Button(self, text='Apply to all', command=self.applyall)
        self.btnapplyall.grid(row=0, column=4)

    def draw(self):
        roiFreehand(self.projectini,self.filename)

    def reset(self):
        ROI_reset(self.projectini, self.filename)

    def applyall(self):
        multiplyFreeHand(self.projectini, self.filename)

class roitableMenu:
    def __init__(self,videofolder,inifile):
        self.filesFound = []
        self.row = []
        self.videofolder = videofolder

        ### FIND FILES #####
        for i in os.listdir(videofolder):
            if i.endswith(('.avi', '.mp4', '.mov', 'flv')):
                self.filesFound.append(i)

        ### longest string in list
        maxname = max(self.filesFound, key=len)

        ## popup window
        roimenu = Toplevel()
        roimenu.minsize(500, 400)
        roimenu.wm_title("ROI Table")

        scroll = Scrollable(roimenu)

        tableframe = LabelFrame(scroll,text='Video Name',labelanchor=NW)

        #### loop for tables######
        for i in range(len(self.filesFound)):
            self.row.append(roitableRow(tableframe, self.videofolder,str(self.filesFound[i]), str(len(maxname)),str(i+1)+'.',projectini=inifile))
            self.row[i].grid(row=i + 1, sticky=W)

        tableframe.grid(row=0)
        scroll.update()

class processvid_title(Frame):
    def __init__(self,parent=None,widths="",color=None,shortenbox =None,downsambox =None,graybox=None,framebox=None,clahebox=None,**kw):
        self.color = color if color is not None else 'black'
        Frame.__init__(self,master=parent,**kw)
        self.lblName = Label(self, text= 'Video Name',fg=str(self.color),width=int(widths)+5,font=("Helvetica",10,'bold'))
        self.lblName.grid(row=0,column=0,sticky=W)
        self.lblName3 = Label(self, text='Start Time',width = 13,font=("Helvetica",10,'bold'))
        self.lblName3.grid(row=0, column=1,columnspan=2)
        self.lblName4 = Label(self, text='End Time',width = 15,font=("Helvetica",10,'bold'))
        self.lblName4.grid(row=0, column=3)
        self.shorten = IntVar()
        self.lblName5 = Checkbutton(self,text='Select All',variable= self.shorten,command=shortenbox)
        self.lblName5.grid(row=0, column=4)
        self.lblName6 = Label(self, text='Width',width =13,font=("Helvetica",10,'bold'))
        self.lblName6.grid(row=0, column=5)
        self.lblName7 = Label(self, text='Height',width = 15,font=("Helvetica",10,'bold'))
        self.lblName7.grid(row=0, column=6)
        self.downsample = IntVar()
        self.lblName8 = Checkbutton(self,text='Select All',variable = self.downsample,command =downsambox)
        self.lblName8.grid(row=0,column=7,padx=8)
        self.grayscale = IntVar()
        self.lblName9 = Checkbutton(self,text='Select All',variable =self.grayscale,command = graybox)
        self.lblName9.grid(row=0,column=8,padx=7)
        self.frameno = IntVar()
        self.lblName10 = Checkbutton(self,text='Select All',variable = self.frameno,command = framebox)
        self.lblName10.grid(row=0,column=9,padx=6)
        self.clahe = IntVar()
        self.lblName11 = Checkbutton(self,text='Select All',variable =self.clahe,command =clahebox)
        self.lblName11.grid(row=0,column=10,padx=6)

class processvideotable(Frame):
    def __init__(self,parent=None,fileDescription="",widths = "" ,dirname ="",outputdir='',color=None,**kw):
        self.color = color if color is not None else 'black'
        self.croplist = []
        self.filename = os.path.join(dirname,fileDescription)
        self.outputdir = outputdir
        Frame.__init__(self,master=parent,**kw)
        self.lblName = Label(self, text=fileDescription,fg=str(self.color),width= widths,anchor=W)
        self.lblName.grid(row=0,column=0,sticky=W)
        self.btnFind = Button(self, text="Crop",command=self.cropvid)
        self.btnFind.grid(row=0,column=1)
        self.trimstart = Entry(self)
        self.trimstart.grid(row=0,column=2)
        self.trimend = Entry(self)
        self.trimend.grid(row=0, column=3)
        self.shortenvar = IntVar()
        self.downsamplevar = IntVar()
        self.grayscalevar = IntVar()
        self.superimposevar = IntVar()
        self.clahevar = IntVar()
        self.shortenvid = Checkbutton(self,text='Shorten',variable = self.shortenvar)
        self.shortenvid.grid(row=0,column=4)
        self.width = Entry(self)
        self.width.grid(row=0,column=5)
        self.height = Entry(self)
        self.height.grid(row=0,column=6)
        self.downsamplevid = Checkbutton(self,text='Downsample',variable = self.downsamplevar)
        self.downsamplevid.grid(row=0,column=7)
        self.grayscalevid = Checkbutton(self,text='Grayscale',variable= self.grayscalevar)
        self.grayscalevid.grid(row=0,column =8)
        self.superimposevid = Checkbutton(self,text='Add Frame #',variable =self.superimposevar)
        self.superimposevid.grid(row=0,column=9)
        self.clahevid = Checkbutton(self,text='CLAHE',variable = self.clahevar)
        self.clahevid.grid(row=0,column =10)

    def cropvid(self):
        self.croplist = []
        print(self.filename)
        command = cropvid_queue(self.filename,self.outputdir)
        self.croplist.append(command)
        self.btnFind.configure(bg='red')

    def get_crop_list(self):
        return self.croplist

    def getstarttime(self):
         return self.trimstart.get()
    def getendtime(self):
        return self.trimend.get()

    def shorten(self):
        return self.shortenvar.get()

    def downsample(self):
        return self.downsamplevar.get()
    def getwidth(self):
        return self.width.get()
    def getheight(self):
        return self.height.get()
    def grayscale(self):
        return self.grayscalevar.get()
    def addframe(self):
        return self.superimposevar.get()
    def get_clahe(self):
        return self.clahevar.get()

class processvid_menu:

    def __init__(self, videofolder, outputdir):
        self.filesFound = []
        self.row = []
        self.videofolder = videofolder
        self.outputdir = outputdir
        ########### FIND FILES ###########
        for i in os.listdir(videofolder):
            if i.endswith(('.avi','.mp4','.mov','flv')):
                self.filesFound.append(i)

        ### longest string in list
        maxname = max(self.filesFound,key=len)

        # Popup window
        vidprocessmenu = Toplevel()
        vidprocessmenu.minsize(1100, 400)
        vidprocessmenu.wm_title("Batch process video table")
        vidprocessmenu.lift()

        scroll =  Scrollable(vidprocessmenu)

        tableframe = LabelFrame(scroll)

        # table title
        self.title = processvid_title(tableframe, str(len(maxname)), shortenbox=self.selectall_shorten,
                                      downsambox=self.selectall_downsample, graybox=self.selectall_grayscale,
                                      framebox=self.selectall_addframe, clahebox=self.selectall_clahe)

        #### loop for tables######
        for i in range(len(self.filesFound)):
            self.row.append(processvideotable(tableframe,str(self.filesFound[i]), str(len(maxname)),self.videofolder,self.outputdir))
            self.row[i].grid(row=i+1, sticky=W)

        #organize table title
        self.title.grid(row=0, sticky=W)
        #button to trigger process video
        but = Button(scroll,text='Execute',command = lambda: threading.Thread(target=self.execute_processvideo).start(),font=('Times',12,'bold'),fg='navy')
        but.grid(row=2)
        #organize
        tableframe.grid(row=1)
        scroll.update()

    def selectall_clahe(self):
        for i in range(len(self.filesFound)):
            if self.title.clahe.get() == 1:
                self.row[i].clahevid.select()
            else:
                self.row[i].clahevid.deselect()

    def selectall_addframe(self):
        for i in range(len(self.filesFound)):
            if self.title.frameno.get() == 1:
                self.row[i].superimposevid.select()
            else:
                self.row[i].superimposevid.deselect()

    def selectall_grayscale(self):
        for i in range(len(self.filesFound)):
            if self.title.grayscale.get()==1:
                self.row[i].grayscalevid.select()
            else:
                self.row[i].grayscalevid.deselect()


    def selectall_downsample(self):
        for i in range(len(self.filesFound)):
            if self.title.downsample.get()==1:
                self.row[i].downsamplevid.select()
            else:
                self.row[i].downsamplevid.deselect()


    def selectall_shorten(self):
        for i in range(len(self.filesFound)):
            if self.title.shorten.get()==1:
                self.row[i].shortenvid.select()
            else:
                self.row[i].shortenvid.deselect()

    def get_thecroplist(self):
        self.croplistt = []

        for i in range(len(self.filesFound)):
           self.croplistt.append((self.row[i].get_crop_list()))
        print(self.croplistt)
        self.croplistt = list(itertools.chain(*self.croplistt))

        return self.croplistt

    def get_shortenlist(self):
        self.shortenlistt = []
        for i in range(len(self.filesFound)):
            if (self.row[i].shorten()) == 1:
                self.shortenlistt.append(shortenvideos1_queue(self.outputdir,self.filesFound[i],self.row[i].getstarttime(),self.row[i].getendtime()))

        return self.shortenlistt

    def get_downsamplelist(self):
        self.downsamplelistt = []
        for i in range(len(self.filesFound)):
            if (self.row[i].downsample()) == 1:
                self.downsamplelistt.append(downsamplevideo_queue(self.row[i].getwidth(),self.row[i].getheight(),self.filesFound[i],self.outputdir))

        return self.downsamplelistt

    def get_grayscalelist(self):
        self.grayscalelistt = []
        for i in range(len(self.filesFound)):
            if (self.row[i].grayscale()) == 1:
                self.grayscalelistt.append(greyscale_queue(self.outputdir,self.filesFound[i]))

        return self.grayscalelistt

    def get_superimposeframelist(self):
        self.superimposeframelistt = []
        for i in range(len(self.filesFound)):
            if (self.row[i].addframe()) == 1:
                self.superimposeframelistt.append(superimposeframe_queue(self.outputdir, self.filesFound[i]))

        return self.superimposeframelistt

    def execute_processvideo(self):
        # create a temp folder in the output dir
        tmp_folder = os.path.join(self.outputdir,'tmp')
        if os.path.exists(tmp_folder):
            shutil.rmtree(tmp_folder)
        os.mkdir(tmp_folder) #make temp folder

        # remove process txt file if process were killed half way
        try:
            os.remove(self.outputdir + '\\' + 'process_video_define.txt')
        except:
            print('Executing...')

        # compiling the list of commands
        try:
            crop = self.get_thecroplist()
            crop = [i for i in crop if i] ###remove any none in crop
        except:
            crop = []
        try:
            shorten = self.get_shortenlist()
        except:
            shorten = []
        try:
            downsample = self.get_downsamplelist()
        except:
            downsample = []
        try:
            grayscale = self.get_grayscalelist()
        except:
            grayscale = []
        try:
            superimpose = self.get_superimposeframelist()
        except:
            superimpose = []
        ## copy video and move it to output dir
        copyvideos = []
        for i in self.filesFound:
            command = 'copy \"' + str(self.videofolder) + '\\' + str(
                os.path.basename(i)) + '\" \"' + self.outputdir + '\"'
            copyvideos.append(command)

        #compiling all the commands into list
        all_list = copyvideos + crop + shorten + downsample + grayscale + superimpose
        print(len(all_list))
        #creating text file
        filepath = self.outputdir + '\\' + 'process_video_define.txt'

        if os.path.exists(filepath):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        ## writing into the txt file
        highscore = open(filepath, append_write)
        for i in all_list:
            highscore.write(i + '\n')
        highscore.close()
        ## running it using subprocess
        with open(filepath) as fp:
            for cnt, line in enumerate(fp):
                # add probably if ffmpeg then this if not then other subprocess
                subprocess.call(line, shell=True, stdout=subprocess.PIPE)
        ##clahe
        for i in range(len(self.filesFound)):
            if self.row[i].get_clahe() == 1:
                clahe_queue(self.outputdir +'\\'+ os.path.basename(self.filesFound[i]))
            else:
                print('Clahe not applied to',str(self.filesFound[i]))
        ##rename the txt file ran
        file = os.path.dirname(filepath) + '\\' + 'Processes_ran.txt'
        os.rename(filepath, file)
        dir = str(self.outputdir + '\\' + 'process_archive')
        try:
            os.makedirs(dir)
            print("Directory", dir, "created ")
        except FileExistsError:
            print("Directory", dir, "already exists")

        currentDT = datetime.now()
        currentDT = str(currentDT.month) + '_' + str(currentDT.day) + '_' + str(currentDT.year) + '_' + str(
            currentDT.hour) + 'hour' + '_' + str(currentDT.minute) + 'min' + '_' + str(currentDT.second) + 'sec'
        try:
            shutil.move(file, dir)
        except shutil.Error:
            os.rename(file, file[:-4] + str(currentDT) + '.txt')
            shutil.move(file[:-4] + str(currentDT) + '.txt', dir)

        print('Process video completed.')

class batch_processvideo: ##pre process video first menu (ask for input and output folder)

    def __init__(self):
        self.croplist = []
        self.shortenlist = []
        self.downsamplelist =[]
        self.grayscalelist = []
        self.superimposelist = []
        # Popup window
        batchprocess = Toplevel()
        batchprocess.minsize(400, 200)
        batchprocess.wm_title("Batch process video")

        #Video Selection Tab
        label_videoselection = LabelFrame(batchprocess,text='Folder selection',font='bold',padx=5,pady=5)
        self.folder1Select = FolderSelect(label_videoselection,'Video directory:',title='Select Folder with videos')

        #output video
        self.outputfolder = FolderSelect(label_videoselection,'Output directory:',title='Select a folder for your output videos')

        #create list of all videos in the videos folder
        button_cL = Button(label_videoselection,text='Confirm',command=self.confirmtable)

        #organize
        label_videoselection.grid(row=0,sticky=W)
        self.folder1Select.grid(row=0,sticky=W)
        self.outputfolder.grid(row=1,sticky=W)
        button_cL.grid(row=2,sticky=W)

    def confirmtable(self):

        if (self.outputfolder.folder_path!='No folder selected')and(self.folder1Select.folder_path!='No folder selected'):
            processvid_menu(self.folder1Select.folder_path, self.outputfolder.folder_path)
        elif (self.outputfolder.folder_path=='No folder selected'):
            print('Please select an output folder')
        elif (self.folder1Select.folder_path == 'No folder selected'):
            print('Please select a folder with videos')
        else:
            print('Please select folder with videos and the output directory')

class outlier_settings:
    def __init__(self,configini):
        self.configini = configini
        #get the no of animals
        config = ConfigParser()
        configFile = str(configini)
        config.read(configFile)
        animalno = config.getint('General settings','animal_no')
        # get list from csv
        bpcsv = (os.path.join(os.path.dirname(configini),'logs','measures','pose_configs','bp_names','project_bp_names.csv'))
        bplist = []
        with open(bpcsv) as f:
            for row in f:
                bplist.append(row)
        bplist = list(map(lambda x: x.replace('\n',''),bplist))

        if animalno != 1:
            animal1bp = [f for f in bplist if '1' in f]
            animal2bp = [f for f in bplist if '2' in f]
        else:
            animal1bp = bplist

        # Popup window
        outlier_set = Toplevel()
        outlier_set.minsize(400, 400)
        outlier_set.wm_title("Outlier Settings")

        # location correction for one animal
        label_location_correction = LabelFrame(outlier_set, text='Location correction',font=('Times',12,'bold'),pady=5,padx=5)
        label_choosem1bp1 = Label(label_location_correction, text='Choose Animal 1, body part 1:')
        label_choosem1bp2 = Label(label_location_correction, text='Choose Animal 1, body part 2:')
        self.var1 = StringVar()
        self.var1.set(animal1bp[0])  # set as default value
        self.var2 = StringVar()
        self.var2.set(animal1bp[1])  # set as default value
        dropdown_m1bp1 = OptionMenu(label_location_correction, self.var1, *animal1bp)
        dropdown_m1bp2 = OptionMenu(label_location_correction, self.var2, *animal1bp)
        self.location_criterion = Entry_Box(label_location_correction, 'Location criterion', '15')
        # movement
        label_movement_correction = LabelFrame(outlier_set, text='Movement correction', font=('Times', 12, 'bold'),
                                               pady=5, padx=5)
        mlabel_choosem1bp1 = Label(label_movement_correction, text='Choose Animal 1, body part 1:')
        mlabel_choosem1bp2 = Label(label_movement_correction, text='Choose Animal 1, body part 2:')
        self.mvar1 = StringVar()
        self.mvar1.set(animal1bp[0])  # set as default value
        self.mvar2 = StringVar()
        self.mvar2.set(animal1bp[1])  # set as default value
        mdropdown_m1bp1 = OptionMenu(label_movement_correction, self.mvar1, *animal1bp)
        mdropdown_m1bp2 = OptionMenu(label_movement_correction, self.mvar2, *animal1bp)
        self.movement_criterion = Entry_Box(label_movement_correction, 'Movement criterion', '15')

        # if two animals
        if animalno != 1:
            label_choosem2bp1 = Label(label_location_correction, text='Choose Animal 2, body part 1:')
            label_choosem2bp2 = Label(label_location_correction, text='Choose Animal 2, body part 2:')
            animal2bp = [f for f in bplist if '2' in f]
            self.var3 = StringVar()
            self.var3.set(animal2bp[0])  # set as default value
            self.var4 = StringVar()
            self.var4.set(animal2bp[1])  # set as default value
            dropdown_m2bp1 = OptionMenu(label_location_correction, self.var3, *animal2bp)
            dropdown_m2bp2 = OptionMenu(label_location_correction, self.var4, *animal2bp)
            #movement
            mlabel_choosem2bp1 = Label(label_movement_correction, text='Choose Animal 2, body part 1:')
            mlabel_choosem2bp2 = Label(label_movement_correction, text='Choose Animal 2, body part 2:')
            self.mvar3 = StringVar()
            self.mvar3.set(animal2bp[0])  # set as default value
            self.mvar4 = StringVar()
            self.mvar4.set(animal2bp[1])  # set as default value
            mdropdown_m2bp1 = OptionMenu(label_movement_correction, self.mvar3, *animal2bp)
            mdropdown_m2bp2 = OptionMenu(label_movement_correction, self.mvar4, *animal2bp)
            #organize for animal2
            label_choosem2bp1.grid(row=2, column=0, sticky=W)
            label_choosem2bp2.grid(row=3, column=0, sticky=W)
            dropdown_m2bp1.grid(row=2, column=1, sticky=W)
            dropdown_m2bp2.grid(row=3, column=1, sticky=W)
            mlabel_choosem2bp1.grid(row=2, column=0, sticky=W)
            mlabel_choosem2bp2.grid(row=3, column=0, sticky=W)
            mdropdown_m2bp1.grid(row=2, column=1, sticky=W)
            mdropdown_m2bp2.grid(row=3, column=1, sticky=W)
        #mean or median
        medianlist = ['mean','median']
        self.medianvar =StringVar()
        self.medianvar.set(medianlist[0])
        label_median = LabelFrame(outlier_set,text='Median or Mean',font=('Times',12,'bold'),pady=5,padx=5)
        mediandropdown = OptionMenu(label_median, self.medianvar, *medianlist)

        #button
        button_setvalues = Button(outlier_set,text='Confirm',command = self.set_outliersettings,font=('Arial',12,'bold'),fg='red')

        #organize
        label_location_correction.grid(row=1,sticky=W)
        label_choosem1bp1.grid(row=0,column=0,sticky=W)
        label_choosem1bp2.grid(row=1,column=0,sticky=W)
        self.location_criterion.grid(row=4,sticky=W)
        dropdown_m1bp1.grid(row=0, column=1, sticky=W)
        dropdown_m1bp2.grid(row=1, column=1, sticky=W)


        label_movement_correction.grid(row=0, sticky=W)
        mlabel_choosem1bp1.grid(row=0, column=0, sticky=W)
        mlabel_choosem1bp2.grid(row=1, column=0, sticky=W)
        self.movement_criterion.grid(row=4, sticky=W)

        mdropdown_m1bp1.grid(row=0, column=1, sticky=W)
        mdropdown_m1bp2.grid(row=1, column=1, sticky=W)

        label_median.grid(row=2,column=0,sticky=W)
        mediandropdown.grid(row=2,sticky=W)
        button_setvalues.grid(row=3,pady=10)

    def set_outliersettings(self):
        # export settings to config ini file
        configini = self.configini
        config = ConfigParser()
        config.read(configini)
        animalno = config.getint('General settings', 'animal_no')
        try:
            if animalno == 1:
                movement_bodyPart1_mouse1 = self.var1.get()
                movement_bodyPart2_mouse1 = self.var2.get()
                location_bodyPart1_mouse1 = self.mvar1.get()
                location_bodyPart2_mouse1 = self.mvar2.get()
                movementcriterion = self.movement_criterion.entry_get
                locationcriterion = self.location_criterion.entry_get
                mean_or_median = self.medianvar.get()
                config.set('Outlier settings', 'movement_criterion', str(movementcriterion))
                config.set('Outlier settings', 'location_criterion', str(locationcriterion))
                config.set('Outlier settings', 'movement_bodyPart1_mouse1', str(movement_bodyPart1_mouse1))
                config.set('Outlier settings', 'movement_bodyPart2_mouse1', str(movement_bodyPart2_mouse1))
                config.set('Outlier settings', 'location_bodyPart1_mouse1', str(location_bodyPart1_mouse1))
                config.set('Outlier settings', 'location_bodyPart2_mouse1', str(location_bodyPart2_mouse1))
                config.set('Outlier settings', 'mean_or_median', str(mean_or_median))

            if animalno == 2:
                movement_bodyPart1_mouse2 = self.var3.get()
                location_bodyPart1_mouse2 = self.mvar3.get()
                movement_bodyPart2_mouse2 = self.var4.get()
                location_bodyPart2_mouse2 = self.mvar4.get()
                movement_bodyPart1_mouse1 = self.var1.get()
                movement_bodyPart2_mouse1 = self.var2.get()
                location_bodyPart1_mouse1 = self.mvar1.get()
                location_bodyPart2_mouse1 = self.mvar2.get()
                mean_or_median = self.medianvar.get()
                movementcriterion = self.movement_criterion.entry_get
                locationcriterion = self.location_criterion.entry_get
                config.set('Outlier settings', 'movement_criterion', str(movementcriterion))
                config.set('Outlier settings', 'location_criterion', str(locationcriterion))
                config.set('Outlier settings', 'movement_bodyPart1_mouse2', str(movement_bodyPart1_mouse2))
                config.set('Outlier settings', 'movement_bodyPart2_mouse2', str(movement_bodyPart2_mouse2))
                config.set('Outlier settings', 'location_bodyPart1_mouse2', str(location_bodyPart1_mouse2))
                config.set('Outlier settings', 'location_bodyPart2_mouse2', str(location_bodyPart2_mouse2))
                config.set('Outlier settings', 'mean_or_median', str(mean_or_median))
                config.set('Outlier settings', 'movement_bodyPart1_mouse1', str(movement_bodyPart1_mouse1))
                config.set('Outlier settings', 'movement_bodyPart2_mouse1', str(movement_bodyPart2_mouse1))
                config.set('Outlier settings', 'location_bodyPart1_mouse1', str(location_bodyPart1_mouse1))
                config.set('Outlier settings', 'location_bodyPart2_mouse1', str(location_bodyPart2_mouse1))

            with open(configini, 'w') as configfile:
                config.write(configfile)

            print('Outlier settings updated in project_config.ini')
        except:
            print('Please make sure all fields are filled in correctly.')

class FolderSelect(Frame):
    def __init__(self,parent=None,folderDescription="",color=None,title=None,lblwidth =None,**kw):
        self.title=title
        self.color = color if color is not None else 'black'
        self.lblwidth = lblwidth if lblwidth is not None else 0
        self.parent = parent
        Frame.__init__(self,master=parent,**kw)
        self.folderPath = StringVar()
        self.lblName = Label(self, text=folderDescription,fg=str(self.color),width=str(self.lblwidth),anchor=W)
        self.lblName.grid(row=0,column=0,sticky=W)
        self.entPath = Label(self, textvariable=self.folderPath,relief=SUNKEN)
        self.entPath.grid(row=0,column=1)
        self.btnFind = Button(self, text="Browse Folder",command=self.setFolderPath)
        self.btnFind.grid(row=0,column=2)
        self.folderPath.set('No folder selected')
    def setFolderPath(self):
        folder_selected = askdirectory(title=str(self.title),parent=self.parent)
        if folder_selected:
            self.folderPath.set(folder_selected)
        else:
            self.folderPath.set('No folder selected')

    @property
    def folder_path(self):
        return self.folderPath.get()

class DropDownMenu(Frame):
    def __init__(self,parent=None,dropdownLabel='',choice_dict={},labelwidth='',**kw):
        Frame.__init__(self,master=parent,**kw)
        self.dropdownvar = StringVar()
        self.lblName = Label(self,text=dropdownLabel,width=labelwidth,anchor=W)
        self.lblName.grid(row=0,column=0)
        self.choices = choice_dict
        self.popupMenu = OptionMenu(self,self.dropdownvar,*self.choices)
        self.popupMenu.grid(row=0,column=1)
    def getChoices(self):
        return self.dropdownvar.get()
    def setChoices(self,choice):
        self.dropdownvar.set(choice)

class FileSelect(Frame):
    def __init__(self,parent=None,fileDescription="",color=None,title=None,lblwidth=None,**kw):
        self.title=title
        self.color = color if color is not None else 'black'
        self.lblwidth = lblwidth if lblwidth is not None else 0
        self.parent=parent
        Frame.__init__(self,master=parent,**kw)
        self.filePath = StringVar()
        self.lblName = Label(self, text=fileDescription,fg=str(self.color),width=str(self.lblwidth),anchor=W)
        self.lblName.grid(row=0,column=0,sticky=W)
        self.entPath = Label(self, textvariable=self.filePath,relief=SUNKEN)
        self.entPath.grid(row=0,column=1)
        self.btnFind = Button(self, text="Browse File",command=self.setFilePath)
        self.btnFind.grid(row=0,column=2)
        self.filePath.set('No file selected')
    def setFilePath(self):
        file_selected = askopenfilename(title=self.title,parent=self.parent)
        if file_selected:
            self.filePath.set(file_selected)
        else:
            self.filePath.set('No file selected')
    @property
    def file_path(self):
        return self.filePath.get()

class Entry_Box(Frame):
    def __init__(self,parent=None,fileDescription="",labelwidth='',status = None,**kw):
        self.status = status if status is not None else NORMAL
        Frame.__init__(self,master=parent,**kw)
        self.filePath = StringVar()
        self.lblName = Label(self, text=fileDescription,width=labelwidth,anchor=W)
        self.lblName.grid(row=0,column=0)
        self.entPath = Entry(self, textvariable=self.filePath,state=self.status)
        self.entPath.grid(row=0,column=1)

    @property
    def entry_get(self):
        self.entPath.get()
        return self.entPath.get()

    def entry_set(self, val):
        self.filePath.set(val)

    def set_state(self,setstatus):
        self.entPath.config(state=setstatus)

class newcolumn(Frame):
    def __init__(self,parent=None,lengthoflist=[],width='',**kw):
        Frame.__init__(self,master=parent,**kw)
        self.entPath = []
        self.entPathvars =[]
        for i in range(len(lengthoflist)):
            self.entPathvar = IntVar()
            self.entPathvars.append(self.entPathvar)
            self.entPath.append(Entry(self, textvariable=self.entPathvars[i],width=width))
            self.entPath[i].grid(row=i,pady=3)

    def entry_get(self,row):
        return self.entPath[row].get()

    def setvariable(self,row,vars):
        return self.entPathvars[row].set(vars)

class Button_getcoord(Frame):

    def __init__(self,parent=None,filename=[],knownmm=[],ppmlist = None,**kw): #set to list and use range i in list to call each elements in list

        Frame.__init__(self, master=parent, **kw)
        self.entPath = []
        self.ppm_list = []
        self.ppmvar = []
        labelgetcoord =Label(self,text='Get coord')
        labelgetcoord.grid(row=0,pady=6)

        labelppm =Label(self,text='Pixels/mm')
        labelppm.grid(row=0,column=1)

        for i in range(len(filename)-1):
            self.entPath.append(Button(self,text='Video'+str(i+1),command =lambda i=i :self.getcoord_forbutton(filename[i+1],knownmm[i+1],i)))
            self.entPath[i].grid(row=i+1)
            self.ppmvars=IntVar()
            self.ppmvar.append(self.ppmvars)
            self.ppm_list.append(Entry(self,textvariable=self.ppmvar[i]))
            self.ppm_list[i].grid(row=i+1,column=1)
        if ppmlist != None:
            for i in range(len(self.ppmvar)):
                self.ppmvar[i].set(ppmlist[i])
        print(ppmlist)
    def getcoord_forbutton(self,filename,knownmm,count):

        ppm = get_coordinates_nilsson(filename,knownmm)

        if ppm == float('inf'):
            print('Divide by zero error. Please make sure the values in [Distance_in_mm] are updated')
        else:
            self.ppmvar[count].set(ppm)

    def getppm(self,count):
        ppms = self.ppm_list[count].get()
        return ppms

def Exit():
    app.root.destroy()

class video_info_table:

    def __init__(self,configini):

        self.filesFound = [0]  #initiate files found
        video_info_csv = str(os.path.dirname(configini)+'\\logs\\video_info.csv')
        config = ConfigParser()
        self.configFile = str(configini)
        config.read(self.configFile)
        self.config_videofolders = str(config.get('General settings', 'project_path'))+'\\videos'
        config_distancemm = config.get('Frame settings', 'distance_mm')

        ########### FIND FILES ###########
        for i in os.listdir(self.config_videofolders):
            if i.endswith(('.avi','.mp4','.mov','flv')):
                self.filesFound.append(i)

        self.tkintertable = Toplevel()
        self.tkintertable.minsize(1000, 500)
        self.tkintertable.wm_title("Video Info")

        self.xscrollbar = Scrollable(self.tkintertable,width=32)
        self.myframe = LabelFrame(self.xscrollbar,text='Table')
        self.myframe.grid(row=6)

        self.new_col_list = ['index','Video','fps','Resolution_width','Resolution_height','Distance_in_mm']
        self.table_col=[]
        self.col_width= ['6','35','20','20','20','20']

        #### loop for tables######
        for i in range(len(self.new_col_list)):
            self.table_col.append(newcolumn(self.myframe,self.filesFound,self.col_width[i]))
            self.table_col[i].grid(row=0,column=i, sticky=W)


        ###set values for base####
        count = 0
        for i in self.filesFound:
            vid= cv2.VideoCapture(os.path.join(str(self.config_videofolders),str(i)))
            #print((os.path.join(str(self.config_videofolders),str(i))))
            self.table_col[0].setvariable(count,str(count)+'.')
            self.table_col[1].setvariable(count,i)
            self.table_col[2].setvariable(count, int(vid.get(cv2.CAP_PROP_FPS)))
            self.table_col[3].setvariable(count, int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)))
            self.table_col[4].setvariable(count, int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.table_col[5].setvariable(count,config_distancemm)
            count+=1

        #set title
        count=0
        for i in self.new_col_list:
            self.table_col[count].setvariable(0,i)
            count+=1

        ###set up get coord button on table####
        self.data_lists = []
        for i in range(len(self.table_col)):
            self.data_lists.append([])

        for i in self.filesFound:
            self.data_lists[1].append(str(self.config_videofolders +'\\'+ str(i)))
            self.data_lists[5].append(int(0))

        if os.path.exists(video_info_csv):
            df = pd.read_csv(video_info_csv)
            videoincsv = df['Video'].tolist()
            pixelsincsv = df['pixels/mm'].tolist()
            df_dict = dict(zip(videoincsv,pixelsincsv))
            videoslist = self.filesFound.copy()
            videoslist = videoslist[1:]

            for i in range(len(videoslist)):
                videoslist[i] = str(videoslist[i]).split('.')[0]

            videosdict = dict(zip(videoslist,range(len(videoslist))))

            for keys in videosdict.keys():
                if keys in df_dict:
                    videosdict[keys] = df_dict[keys]
                else:
                    videosdict[keys] = 0
            pixellist = list(videosdict.values())
            self.pixel_list = pixellist
            self.getdata()
            self.button = Button_getcoord(self.xscrollbar, self.data_lists[1], self.data_lists[5],pixellist)
            self.button.grid(row=6, column=1)

        else:
            self.pixel_list= None
            self.getdata()
            self.button = Button_getcoord(self.xscrollbar,self.data_lists[1],self.data_lists[5])
            self.button.grid(row=6,column=1)


        #instructions
        label_getdatadesc1 = Label(self.xscrollbar,text='1. Enter the known distance (mm) in the "Distance_in_mm" column. Consider using the "autopopulate" entry box if you have a lot of videos.')
        label_getdatadesc2 = Label(self.xscrollbar,text='2. Click on <Update distance_in_mm> button before clicking on the "Get coord" button(s) to calculate pixels/mm.')
        label_getdatadesc3 = Label(self.xscrollbar,text='3. Click <Save Data> when all the data are filled in. Use the <Add Columns> button to add infmation on each video, e.g., animal ID or experimental group.')
        label_getdatadesc1.grid(row=0,sticky=W)
        label_getdatadesc2.grid(row=1, sticky=W)
        label_getdatadesc3.grid(row=2, sticky=W)

        get_data_button = Button(self.xscrollbar, text='Update distance_in_mm', command=self.getdata)
        get_data_button.grid(row=3,sticky=W)

        add_column_button = Button(self.xscrollbar,text='<Add Column>',command=lambda:self.addBox(self.xscrollbar),fg='red')
        add_column_button.grid(row=4,sticky=W)

        generate_csv_button = Button(self.xscrollbar,text='Save Data',command=self.generate_video_info_csv,font='bold',fg='red')
        generate_csv_button.grid(row=5)

        self.xscrollbar.update()

    def addBox(self,scroll):
        self.new_col_list.append(0)
        self.next_column = len(self.new_col_list)
        #print(self.next_column)
        self.table_col.append(newcolumn(self.myframe,self.filesFound,'20'))
        self.table_col[(self.next_column)-1].grid(row=0,column=self.next_column)
        scroll.update()

    def getdata(self):
        self.data_lists =[]
        #get all data from tables
        for i in range(len(self.table_col)):
            self.data_lists.append([])
            for j in range(len(self.filesFound)):
                self.data_lists[i].append(self.table_col[i].entry_get(j))

        # add path to videos for get coord
        self.data_lists[1] = [str(self.config_videofolders)+'\\'+s for s in self.data_lists[1]]
        if self.pixel_list!= None:
            self.button = Button_getcoord(self.xscrollbar, self.data_lists[1], self.data_lists[5],self.pixel_list)
            self.button.grid(row=6, column=1)
        else:
            #update get coord with data
            self.button = Button_getcoord(self.xscrollbar,self.data_lists[1],self.data_lists[5])
            self.button.grid(row=6,column=1)

        print("Table updated.")

    def generate_video_info_csv(self):
        #get latest data from table
        self.data_lists = []
        # get all data from tables
        for i in range(len(self.table_col)):
            self.data_lists.append([])
            for j in range(len(self.filesFound)):
                self.data_lists[i].append(self.table_col[i].entry_get(j))
        #get the ppm from table
        self.ppm=['pixels/mm']
        for i in range(len(self.filesFound)-1):
            self.ppm.append((self.button.getppm(i)))
        self.data_lists.append(self.ppm)

        #remove .mp4 from first column
        self.data_lists[1] = [i.replace(i[-4:],'') for i in self.data_lists[1]]
        self.data_lists[1][0] ='Video'

        data=self.data_lists
        df=pd.DataFrame(data=data)
        df=df.transpose()
        df=df.rename(columns=df.iloc[0])
        df=df.drop(df.index[0])
        df=df.reset_index()
        df=df.drop(['index'],axis=1)
        df=df.drop(['level_0'],axis=1)
        logfolder=str(os.path.dirname(self.configFile))+'\\logs\\'
        csv_filename = 'video_info.csv'
        output=logfolder+csv_filename
        df.to_csv(str(output),index=False)
        print(os.path.dirname(output),'generated.')

class video_downsample:

    def __init__(self):
        # Popup window
        videosdownsample = Toplevel()
        videosdownsample.minsize(200, 200)
        videosdownsample.wm_title("Downsample Video Resolution")


        # Video Path
        self.videopath1selected = FileSelect(videosdownsample, "Video path",title='Select a video file')
        label_choiceq = Label(videosdownsample, text='Choose only one of the following method to downsample videos (Custom/Default)')

        #custom reso
        label_downsamplevidcustom = LabelFrame(videosdownsample,text='Custom resolution',font='bold',padx=5,pady=5)
        # width
        self.label_width = Entry_Box(label_downsamplevidcustom,'Width','10')
        # height
        self.label_height = Entry_Box(label_downsamplevidcustom,'Height','10')
        # confirm custom resolution
        self.button_downsamplevideo1 = Button(label_downsamplevidcustom, text='Downsample to custom resolution',command=self.downsample_customreso)
        #Default reso
        # Checkbox
        label_downsampleviddefault = LabelFrame(videosdownsample,text='Default resolution',font ='bold',padx=5,pady=5)
        self.var1 = IntVar()
        self.checkbox1 = Radiobutton(label_downsampleviddefault, text="1980 x 1080", variable=self.var1,value=1)
        self.checkbox2 = Radiobutton(label_downsampleviddefault, text="1280 x 720", variable=self.var1,value=2)
        self.checkbox3 = Radiobutton(label_downsampleviddefault, text="720 x 480", variable=self.var1, value=3)
        self.checkbox4 = Radiobutton(label_downsampleviddefault, text="640 x 480", variable=self.var1, value=4)
        self.checkbox5 = Radiobutton(label_downsampleviddefault, text="320 x 240", variable=self.var1, value=5)
        # Downsample video
        self.button_downsamplevideo2 = Button(label_downsampleviddefault, text='Downsample to default resolution',command=self.downsample_defaultreso)

        # Organize the window
        self.videopath1selected.grid(row=0,sticky=W)
        label_choiceq.grid(row=1, sticky=W,pady=10)

        label_downsamplevidcustom.grid(row=2,sticky=W,pady=10)
        self.label_width.grid(row=0, column=0,sticky=W)
        self.label_height.grid(row=1, column=0,sticky=W)
        self.button_downsamplevideo1.grid(row=3)

        label_downsampleviddefault.grid(row=3,sticky=W,pady=10)
        self.checkbox1.grid(row=0,stick=W)
        self.checkbox2.grid(row=1,sticky=W)
        self.checkbox3.grid(row=2, sticky=W)
        self.checkbox4.grid(row=3, sticky=W)
        self.checkbox5.grid(row=4, sticky=W)
        self.button_downsamplevideo2.grid(row=5)

    def downsample_customreso(self):
        self.width1 = self.label_width.entry_get
        self.height1 = self.label_height.entry_get

        ds = downsamplevideo(self.width1, self.height1, self.videopath1selected.file_path)

    def downsample_defaultreso(self):

        if self.var1.get()==1:
            self.width2 = str(1980)
            self.height2 = str(1080)
            print('The width selected is ' + str(self.width2) + ', the height is ' + str(self.height2))

        elif self.var1.get()==2:
            self.width2 = str(1280)
            self.height2 = str(720)
            print('The width selected is ' + str(self.width2) + ', the height is ' + str(self.height2))

        elif self.var1.get()==3:
            self.width2 = str(720)
            self.height2 = str(480)
            print('The width selected is ' + str(self.width2) + ', the height is ' + str(self.height2))

        elif self.var1.get()==4:
            self.width2 = str(640)
            self.height2 = str(480)
            print('The width selected is ' + str(self.width2) + ', the height is ' + str(self.height2))

        elif self.var1.get()==5:
            self.width2 = str(320)
            self.height2 = str(240)
            print('The width selected is ' + str(self.width2) + ', the height is ' + str(self.height2))

        ds = downsamplevideo(self.width2, self.height2, self.videopath1selected.file_path)

class Red_light_Convertion:

    def __init__(self):
        # Popup window
        redlightconversion = Toplevel()
        redlightconversion.minsize(200, 200)
        redlightconversion.wm_title("CLAHE")


        #CLAHE
        label_clahe = LabelFrame(redlightconversion,text='Contrast Limited Adaptive Histogram Equalization',font='bold',padx=5,pady=5)
        # Video Path
        self.videopath1selected = FileSelect(label_clahe, "Video path ",title='Select a video file')
        button_clahe = Button(label_clahe,text='Apply CLAHE',command=lambda:clahe(self.videopath1selected.file_path))

        #organize the window
        label_clahe.grid(row=0,sticky=W)
        self.videopath1selected.grid(row=0,sticky=W)
        button_clahe.grid(row=1,pady=5)

class crop_video:

    def __init__(self):
        # Popup window
        cropvideo = Toplevel()
        cropvideo.minsize(200, 200)
        cropvideo.wm_title("Crop Video")


        # Video Path
        label_cropvideo = LabelFrame(cropvideo,text='Crop Video',font='bold',padx=5,pady=5)
        self.videopath1selected = FileSelect(label_cropvideo,"Video path",title='Select a video file')
        # CropVideo
        button_cropvid = Button(label_cropvideo, text='Crop Video', command=lambda:cropvid(self.videopath1selected.file_path))

        #organize
        label_cropvideo.grid(row=0,sticky=W)
        self.videopath1selected.grid(row=0,sticky=W)
        button_cropvid.grid(row=1,sticky=W,pady=10)

class create_project_DLC:

    def __init__(self):

        # Popup window
        createproject = Toplevel()
        createproject.minsize(400, 250)
        createproject.wm_title("Create Project")


        self.label_dlc_createproject = LabelFrame(createproject,text='Create Project',font =("Helvetica",12,'bold'))
        #project name
        self.label_projectname = Entry_Box(self.label_dlc_createproject,'Project name','16')

        #Experimenter name
        self.label_experimentername = Entry_Box(self.label_dlc_createproject,'Experimenter name','16')

        #button 1
        button_videofol = Button(self.label_dlc_createproject,text='Import Single Video',command=self.changetovideo2,fg='blue')
        #button 2
        button_videofo2 = Button(self.label_dlc_createproject,text='Import Multiple Videos',command=self.changetovideo,fg='green4')

        # Video Path
        self.videopath1selected = FolderSelect(self.label_dlc_createproject, 'Video Folder          ',title='Select folder with videos',color='green4')
        self.videopath1selected.grid(row=4, sticky=W)

        #video folder
        self.folderpath1selected = FolderSelect(self.label_dlc_createproject,f'Project directory   ',title='Select main directory')

        #bodypart configuration file
        self.bodypartconfigfile = FileSelect(self.label_dlc_createproject, 'Bp config file ', title='Select a csv file')

        # # statusbar
        # self.projectcreated = IntVar()
        # Label(createproject, textvariable=self.projectcreated, bd=1, relief=SUNKEN).grid(row=7,sticky=W)
        # self.projectcreated.set('Status: Waiting for input...')

        #checkbox_apply golden aggresion config yaml settings
        self.var_changeyaml = IntVar()
        checkbox2 = Checkbutton(self.label_dlc_createproject,text='Apply Golden Lab 16-body part config',variable=self.var_changeyaml)

        #checkbox for copy videos true or false
        self.var_copyvid = IntVar()
        checkbox1 = Checkbutton(self.label_dlc_createproject,text='Copy videos (If unchecked, shortcuts are created)',variable=self.var_copyvid)

        #run create project
        button_createproject = Button(self.label_dlc_createproject,text='Create Project',fg='red',command=self.createprojectcommand)

        #organize
        self.label_dlc_createproject.grid(row=0)
        self.label_projectname.grid(row=0,column=0,sticky=W)
        self.label_experimentername.grid(row=1,column=0,sticky=W)
        button_videofol.grid(row=2,sticky=W,pady=5)
        button_videofo2.grid(row=3,sticky=W,pady=5)
        self.folderpath1selected.grid(row=5,sticky=W)
        self.bodypartconfigfile.grid(row=6, sticky=W)
        checkbox2.grid(row=7,column=0,sticky=W)
        checkbox1.grid(row=8,sticky=W)
        button_createproject.grid(row=9,column=3,pady=10,padx=5)

    def changetovideo(self):
        self.videopath1selected.grid_remove()
        self.videopath1selected = FolderSelect(self.label_dlc_createproject, 'Video Folder          ',title='Select folder with videos',color='green4')
        self.videopath1selected.grid(row=4, sticky=W)


    def changetovideo2(self):
        self.videopath1selected.grid_remove()
        self.videopath1selected = FileSelect(self.label_dlc_createproject, 'Video path             ',color='blue',title='Select a video file')
        self.videopath1selected.grid(row=4, sticky=W)

    def createprojectcommand(self):
        projectname = self.label_projectname.entry_get
        experimentalname = self.label_experimentername.entry_get
        if self.var_copyvid.get()==1:
            copyvid = True
        elif self.var_copyvid.get()==0:
            copyvid = False

        if 'FileSelect' in str(type(self.videopath1selected)):
            videolist = [self.videopath1selected.file_path]
        else:
            try:
                videolist = []

                for i in os.listdir(self.videopath1selected.folder_path):
                    if ('.avi' or '.mp4') in i:
                        i = self.videopath1selected.folder_path + '\\' + i
                        videolist.append(i)
            except:
                print('Please select a video folder to import videos')

        if 'FileSelect' in str(type(self.bodypartconfigfile)):
            bodyPartConfigFile = (self.bodypartconfigfile.file_path)


        if self.var_changeyaml.get()==1:
            if (projectname !='') and (experimentalname !='') and ('No'and'selected' not in videolist) and (self.folderpath1selected.folder_path!='No folder selected'):
                config_path = deeplabcut.create_new_project(str(projectname), str(experimentalname), videolist,working_directory=str(self.folderpath1selected.folder_path), copy_videos=copyvid)
                changedlc_config(config_path, 0)
            else:
                print('Please make sure all the information are filled in')
        else:
            if (projectname != '') and (experimentalname != '') and ('No' and 'selected' not in videolist) and (self.folderpath1selected.folder_path != 'No folder selected'):
                config_path = deeplabcut.create_new_project(str(projectname), str(experimentalname), videolist,working_directory=str(self.folderpath1selected.folder_path), copy_videos=copyvid)
            else:
                print('Please make sure all the information are filled in')
        if bodyPartConfigFile != 'No file selected':
            changedlc_config(config_path, bodyPartConfigFile)

class createDPK_project:
    def __init__(self):
        cdpkmenu = Toplevel()
        cdpkmenu.minsize(300,200)
        cdpkmenu.wm_title('Create DeepPoseKit project')

        cdpk_label = LabelFrame(cdpkmenu,pady=5,padx=5)
        self.inifile = FileSelect(cdpk_label,'SimBA project.ini file',lblwidth='18')
        self.projectName = Entry_Box(cdpk_label,'Project Name','18')

        #button
        generate_Button = Button(cdpk_label,text='Generate project',command=self.generateProject)

        #organize
        cdpk_label.grid(row=0,sticky=W)
        self.inifile.grid(row=0,sticky=W)
        self.projectName.grid(row=1,sticky=W)
        generate_Button.grid(row=2,sticky=W)

    def generateProject(self):
        projectdir = os.path.dirname(self.inifile.file_path)
        write_dpkfile(projectdir,self.projectName.entry_get)
        print('DeepPoseKit project generated.')


class deepPoseKitMenu:
    def __init__(self,inifile):
        self.configini = inifile
        # Popup window
        dpkMenu = Toplevel()
        dpkMenu.minsize(400, 400)
        dpkMenu.wm_title("DeepPoseKit")

        #parent tab
        tab_parent = ttk.Notebook(dpkMenu)
        #children tab
        tab0 = ttk.Frame(tab_parent)
        tab1 = ttk.Frame(tab_parent)
        tab2 = ttk.Frame(tab_parent)
        tab3 = ttk.Frame(tab_parent)
        tab4 = ttk.Frame(tab_parent)
        tab5 = ttk.Frame(tab_parent)

        tab_parent.add(tab0, text=f'{"[ Import Videos ]": ^20s}')
        tab_parent.add(tab1, text=f'{"[ Create annotation set ]": ^20s}')
        tab_parent.add(tab2, text=f'{"[ Annotater ]": ^20s}')
        tab_parent.add(tab3, text=f'{"[ Train model ]": ^20s}')
        tab_parent.add(tab4, text=f'{"[ Predict new video ]": ^20s}')
        tab_parent.add(tab5, text=f'{"[ Visualize video ]": ^20s}')

        tab_parent.grid(row=0)

        #import videos
        label_importvideo = LabelFrame(tab0, text='Import videos into DPK project', font=("Helvetica",12,'bold'), padx=15,pady=5,fg='black')
        # multi video
        label_multivideoimport = LabelFrame(label_importvideo, text='Import multiple videos', pady=5, padx=5)
        self.multivideofolderpath = FolderSelect(label_multivideoimport, 'Folder path',title='Select Folder with videos')
        self.video_type = Entry_Box(label_multivideoimport, 'File format (i.e., mp4/avi):', '20')
        button_multivideoimport = Button(label_multivideoimport, text='Import multiple videos',command=self.importvideo_multi, fg='black')
        # singlevideo
        label_singlevideoimport = LabelFrame(label_importvideo, text='Import single video', pady=5, padx=5)
        self.singlevideopath = FileSelect(label_singlevideoimport, "Video Path",title='Select a video file')
        button_importsinglevideo = Button(label_singlevideoimport, text='Import a video',command= self.importvideo_single,fg='black')

        #Create annotation
        createann_label = LabelFrame(tab1,pady=5,padx=5)
        annOutputName = Entry_Box(createann_label,'Annotation Output Name','21')
        readBatchSize = Entry_Box(createann_label,'Read Batch Size','21')
        kmeanbSize = Entry_Box(createann_label, 'k means batch size', '21')
        kmeanNcluster = Entry_Box(createann_label, 'k means n clusters', '21')
        kmeanmaxIter = Entry_Box(createann_label, 'k means max iterations', '21')
        kmeanNinit = Entry_Box(createann_label, 'k means n init', '21')
        crateaAnnButton = Button(createann_label,text='Create Annotation',command=lambda:self.dpkStep1(annOutputName.entry_get,readBatchSize.entry_get,kmeanbSize.entry_get,kmeanNcluster.entry_get,kmeanmaxIter.entry_get,kmeanNinit.entry_get))

        ## set
        readBatchSize.entry_set('100')
        kmeanbSize.entry_set('100')
        kmeanNcluster.entry_set('10')
        kmeanmaxIter.entry_set('1000')
        kmeanNinit.entry_set('10')

        #Annotator
        annfile_label = LabelFrame(tab2,pady=5,padx=5)
        annfile = FileSelect(annfile_label,'Annotation file',lblwidth='18')
        #button
        runann_button = Button(annfile_label,text='Run',command=lambda:dpkAnnotator(self.configini,annfile.file_path))

        def activate(box, *args):
            for entry in args:
                if box.get() == 0:
                    entry.set_state(DISABLED)
                elif box.get() == 1:
                    entry.set_state(NORMAL)

        #train model deeposekit
        trainmodel_label = LabelFrame(tab3,pady=5,padx=5)
        annpath = FileSelect(trainmodel_label,'Annotations path',lblwidth='18')
        savemodelPath = Entry_Box(trainmodel_label,'Output model name','18')
        epochs = Entry_Box(trainmodel_label,'epochs','18')
        dsFactor = Entry_Box(trainmodel_label,'Downsample factor','18')
        validationSplit = Entry_Box(trainmodel_label,'Validation split','18')
        sigma = Entry_Box(trainmodel_label,'Sigma','18')
        graphscale = Entry_Box(trainmodel_label,'Graph scale','18')
        TorFoptions = {'True','False'}
        augmenter = DropDownMenu(trainmodel_label,'Augmenter',TorFoptions,'18')
        validationbatchSize = Entry_Box(trainmodel_label,'Validation batch size','18')
        modelgrowthrate = Entry_Box(trainmodel_label,'Model growth rate','18')
        modelbatchsize = Entry_Box(trainmodel_label,'Model Batch Size','18')

        #logger
        loggervar = IntVar(value=1)
        loggervalidBatchSize = Entry_Box(trainmodel_label, 'Logger validation batch size', '18')
        loggercheckbox = Checkbutton(trainmodel_label, text='Logger', variable=loggervar,
                                     command=lambda: activate(loggervar, loggervalidBatchSize))

        # lr factor
        reducevar = IntVar(value=1)
        reducelrfactor = Entry_Box(trainmodel_label, 'Reduce LR factor', '18')
        reducelrcheckbox = Checkbutton(trainmodel_label, text='Reduce_Lr', variable=reducevar,
                                       command=lambda: activate(reducevar, reducelrfactor))

        checkpointscheckbox = DropDownMenu(trainmodel_label,'Model Checkpoints',TorFoptions,'18')
        earlyStopcheckbox = DropDownMenu(trainmodel_label,'Early stop',TorFoptions,'18')

        ## choose model
        modelsoption = {'DeepLabCut','LEAP','StackedDenseNet','StackedHourglass'}
        self.nnArchitecture = DropDownMenu(trainmodel_label,'NN_architecture',modelsoption,'18')
        modelsettingsbutton = Button(trainmodel_label,text='Model Settings',command=self.modelsettingschoice)

        #button
        trainmodelbutton = Button(trainmodel_label,text='Train model',command = lambda:self.traindpk(annpath.file_path,savemodelPath.entry_get,epochs.entry_get,dsFactor.entry_get,validationSplit.entry_get,sigma.entry_get,
                                                                                                     graphscale.entry_get,augmenter.getChoices(),validationbatchSize.entry_get,modelgrowthrate.entry_get,modelbatchsize.entry_get,
                                                                                                     loggervar.get(),loggervalidBatchSize.entry_get,reducevar.get(),reducelrfactor.entry_get,checkpointscheckbox.getChoices(),earlyStopcheckbox.getChoices(),self.nnArchitecture.getChoices()))

        #set
        epochs.entry_set('200')
        dsFactor.entry_set('2')
        validationSplit.entry_set('0.05')
        sigma.entry_set('5')
        graphscale.entry_set('1')
        augmenter.setChoices('True')
        validationbatchSize.entry_set('2')
        modelgrowthrate.entry_set('32')
        modelbatchsize.entry_set('2')
        loggervalidBatchSize.entry_set('2')
        reducelrfactor.entry_set('0.2')
        checkpointscheckbox.setChoices('True')
        earlyStopcheckbox.setChoices('True')
        self.nnArchitecture.setChoices('StackedDenseNet')

        #predict new video
        predictvid_label = LabelFrame(tab4,pady=5,padx=5)
        modelPath = FileSelect(predictvid_label,'Model path', lblwidth='12')
        vidfolderpredict = FolderSelect(predictvid_label,'Video Folder',lblwidth='12')
        #button
        predictbutton = Button(predictvid_label,text='Predict',command=lambda:self.runprediction(modelPath.file_path,vidfolderpredict.folder_path))

        #Visualize video
        visualize_label = LabelFrame(tab5,pady=5,padx=5)
        #button
        visualizeButton = Button(visualize_label,text='Run',command=lambda:visualizeDPK(self.configini))

        #organize
        #import videos
        label_importvideo.grid(row=0)
        # multi video
        label_multivideoimport.grid(row=0,sticky=W)
        self.multivideofolderpath.grid(row=0,sticky=W)
        self.video_type.grid(row=1,sticky=W)
        button_multivideoimport.grid(row=2,sticky=W)
        # singlevideo
        label_singlevideoimport.grid(row=1,sticky=W)
        self.singlevideopath.grid(row=0,sticky=W)
        button_importsinglevideo.grid(row=1,sticky=W)

        ##create annotation
        createann_label.grid(row=0,sticky=W,pady=1)
        annOutputName.grid(row=1, sticky=W, pady=1)
        readBatchSize.grid(row=2, sticky=W, pady=1)
        kmeanbSize.grid(row=3, sticky=W, pady=1)
        kmeanNcluster.grid(row=4, sticky=W, pady=1)
        kmeanmaxIter.grid(row=5, sticky=W, pady=1)
        kmeanNinit.grid(row=6, sticky=W, pady=1)
        crateaAnnButton.grid(row=7,pady=5)

        ##annotator
        annfile_label.grid(row=1,sticky=W,pady=1)
        annfile.grid(row=0,sticky=W,pady=1)
        runann_button.grid(row=2,pady=5)
        ##trainmodel
        trainmodel_label.grid(row=2,sticky=W,pady=1)
        annpath.grid(row=0,sticky=W,pady=1)
        savemodelPath.grid(row=1,sticky=W,pady=1)
        epochs.grid(row=2, sticky=W, pady=1)
        dsFactor.grid(row=3, sticky=W, pady=1)
        validationSplit.grid(row=4, sticky=W, pady=1)
        sigma.grid(row=5, sticky=W, pady=1)
        graphscale.grid(row=6, sticky=W, pady=1)
        augmenter.grid(row=7, sticky=W, pady=1)
        validationbatchSize.grid(row=8, sticky=W, pady=1)
        modelgrowthrate.grid(row=9, sticky=W, pady=1)
        modelbatchsize.grid(row=10, sticky=W, pady=1)
        loggercheckbox.grid(row=11, sticky=W, pady=1)
        loggervalidBatchSize.grid(row=12, sticky=W, pady=1)
        reducelrcheckbox.grid(row=13, sticky=W, pady=1)
        reducelrfactor.grid(row=14, sticky=W, pady=1)
        checkpointscheckbox.grid(row=15, sticky=W, pady=1)
        earlyStopcheckbox.grid(row=16, sticky=W, pady=1)
        self.nnArchitecture.grid(row=17, sticky=W, pady=1)
        modelsettingsbutton.grid(row=18, sticky=W, pady=5)
        trainmodelbutton.grid(row=19, pady=5)


        ##predictnewvideo
        predictvid_label.grid(row=3,sticky=W,pady=1)
        modelPath.grid(row=0,sticky=W,pady=1)
        vidfolderpredict.grid(row=1,sticky=W,pady=1)
        predictbutton.grid(row=4,pady=5)
        ##visualize
        visualize_label.grid(row=4,sticky=W,pady=1)
        visualizeButton.grid(row=2,pady=5)

    def importvideo_single(self):
        if (self.configini != 'No file selected') and (self.singlevideopath.file_path != 'No file selected'):
            copy_singlevideo_DPKini(self.configini, self.singlevideopath.file_path)
        else:
            print('Fail to import video, please select a video to import')

    def importvideo_multi(self):
        if (self.configini != 'No file selected') and (
                self.multivideofolderpath.folder_path != 'No folder selected') and (self.video_type.entry_get != ''):
            copy_multivideo_DPKini(self.configini, self.multivideofolderpath.folder_path, self.video_type.entry_get)
        else:
            print('Fail to import videos, please select folder with videos and enter the file format')

    def runprediction(self,modelpath,videofolder):
        configini = self.configini
        config = ConfigParser()
        config.read(configini)
        config.set('predict settings', 'modelPath',str(modelpath))
        # write
        with open(configini, 'w') as configfile:
            config.write(configfile)

        predictnewvideoDPK(configini,videofolder)

    def traindpk(self,annotationfilepath,outputmodelName,epochs,dsfactor,validationsplit,sigma,graphscale,augmenter,validationbatchsize,modelgrowthrate,modelbatchsize,logger,loggerentry,reduce,reducefactor,checkpoint,earlystop,architure):
        #get the config
        configini = self.configini
        config = ConfigParser()
        config.read(configini)
        ## main training settings
        config.set('train model settings', 'epochs', str(epochs))
        config.set('train model settings', 'downsampleFactor', str(dsfactor))
        config.set('train model settings', 'validation_split', str(validationsplit))
        config.set('train model settings', 'sigma', str(sigma))
        config.set('train model settings', 'graph_scale', str(graphscale))
        config.set('train model settings', 'augmenterCheck', str(augmenter))
        config.set('train model settings', 'validation_batch_size', str(validationbatchsize))
        config.set('train model settings', 'modelGrowthRate', str(modelgrowthrate))
        config.set('train model settings', 'model_batch_size', str(modelbatchsize))
        config.set('train model settings', 'loggerCheck', str(logger))
        config.set('train model settings', 'logger_validation_batch_size', str(loggerentry))
        config.set('train model settings', 'reducelrCheck', str(reduce))
        config.set('train model settings', 'reduce_lr_factor', str(reducefactor))
        config.set('train model settings', 'earlyStopCheck', str(earlystop))
        config.set('train model settings', 'modelcheckPointCheck', str(checkpoint))
        config.set('train model settings', 'NN_architecture', str(architure))

        #write
        with open(configini, 'w') as configfile:
            config.write(configfile)

        trainDPKmodel(configini,outputmodelName,annotationfilepath)


    def dpkStep1(self,annOutputName,readBatchSize,kmeansize,kmeancluster,kmeanmaxiter,kmeanNinit):
        print('Creating annotation set.')
        configini = self.configini

        config = ConfigParser()
        config.read(configini)

        config.set('create annotation settings', 'annotation_output_name', str(annOutputName))
        config.set('create annotation settings', 'read_batch_size', str(readBatchSize))
        config.set('create annotation settings', 'k_means_batch_size', str(kmeansize))
        config.set('create annotation settings', 'k_means_n_custers', str(kmeancluster))
        config.set('create annotation settings', 'k_means_max_iterations', str(kmeanmaxiter))
        config.set('create annotation settings', 'k_means_n_init', str(kmeanNinit))
        with open(configini, 'w') as configfile:
            config.write(configfile)

        createAnnotationSet(configini)
        print('Annotation set created')

    def modelsettingschoice(self):
        print(self.nnArchitecture.getChoices())
        if (self.nnArchitecture.getChoices() == 'StackedDenseNet') or (self.nnArchitecture.getChoices() == 'StackedHourglass'):
            self.stackMenu()

        elif (self.nnArchitecture.getChoices() == 'DeepLabCut'):
            self.deeplabcutMenu()

        elif(self.nnArchitecture.getChoices() =='LEAP'):
            self.leapmenu()

    def stackMenu(self):
        stacktoplevel = Toplevel()
        stacktoplevel.minsize(300, 200)
        stacktoplevel.wm_title("StackedDenseNet / StackHourglass")

        stacklabel = LabelFrame(stacktoplevel,pady=5,padx=5)
        n_stacks = Entry_Box(stacklabel,'N_stacks','15')
        n_transitions = Entry_Box(stacklabel,'N_transitions','15')
        growthrate = Entry_Box(stacklabel,'Growth rate','15')
        bottleneckFactor = Entry_Box(stacklabel,'Bottleneck factor','15')
        compressionfactor = Entry_Box(stacklabel,'Compression factor','15')
        TorFalseOptions = {'True','False'}
        pretrained = DropDownMenu(stacklabel,'Pretrained',TorFalseOptions,'15')
        subpixel = DropDownMenu(stacklabel, 'Subpixel', TorFalseOptions, '15')

        #set initial dropdown
        n_stacks.entry_set('1')
        n_transitions.entry_set('1')
        growthrate.entry_set('48')
        bottleneckFactor.entry_set('1')
        compressionfactor.entry_set('0.5')
        pretrained.setChoices('False')
        subpixel.setChoices('True')

        # button
        stackmenubutton = Button(stacklabel,text='Save settings',command= lambda:self.savestacksettings(n_stacks.entry_get, n_transitions.entry_get,growthrate.entry_get,bottleneckFactor.entry_get,compressionfactor.entry_get,pretrained.getChoices(),subpixel.getChoices()))

        #organize
        stacklabel.grid(row=0,sticky=W)
        n_stacks.grid(row=0,sticky=W,pady=1)
        n_transitions.grid(row=1,sticky=W,pady=1)
        growthrate.grid(row=2,sticky=W,pady=1)
        bottleneckFactor.grid(row=3,sticky=W,pady=1)
        compressionfactor.grid(row=4,sticky=W,pady=1)
        pretrained.grid(row=5,sticky=W,pady=1)
        subpixel.grid(row=6,sticky=W,pady=1)
        stackmenubutton.grid(row=7,pady=5)
    def savestacksettings(self,nstack,ntransitions,growthrate,bneckfactor,compressfactor,pretrain,subpixel):
        configini = self.configini
        config = ConfigParser()
        config.read(configini)

        config.set('StackedDenseNet/StackedHourglass settings', 'n_stacks', str(nstack))
        config.set('StackedDenseNet/StackedHourglass settings', 'n_transitions', str(ntransitions))
        config.set('StackedDenseNet/StackedHourglass settings', 'growth_rate', str(growthrate))
        config.set('StackedDenseNet/StackedHourglass settings', 'bottleneckfactor', str(bneckfactor))
        config.set('StackedDenseNet/StackedHourglass settings', 'compression_factor', str(compressfactor))
        config.set('StackedDenseNet/StackedHourglass settings', 'pretrained', str(pretrain))
        config.set('StackedDenseNet/StackedHourglass settings', 'subpixel', str(subpixel))

        with open(configini, 'w') as configfile:
            config.write(configfile)

        print('Settings saved.')

    def deeplabcutMenu(self):
        dlctoplevel = Toplevel()
        dlctoplevel.minsize(300, 200)
        dlctoplevel.wm_title("DeepLabCut")

        dlclabel = LabelFrame(dlctoplevel,pady=5,padx=5)
        weightsoptions = {'imagenet','none'}
        backboneoptions = {'resnet50','resnet101','resnet152','mobilenetv2','densenet121','densenet169','densenet201','xception'}
        torFalseoptions = {'True','False'}
        ##dropdowns
        weight = DropDownMenu(dlclabel,'Weights',weightsoptions,'10')
        backbone = DropDownMenu(dlclabel,'Backbone',backboneoptions,'10')
        alpha = Entry_Box(dlclabel,'Alpha','10')
        subpixel = DropDownMenu(dlclabel,'Subpixel',torFalseoptions,'10')

        ##sets
        #alpha.set(1)
        weight.setChoices('imagenet')
        backbone.setChoices('resnet50')
        subpixel.setChoices('True')

        #button
        dlcsettingsbutton = Button(dlclabel,text='Save Settings',command=lambda:self.savedlcsettings(weight.getChoices(),backbone.getChoices(),alpha.entry_get,subpixel.getChoices()))

        #organize
        dlclabel.grid(row=0,sticky=W)
        weight.grid(row=0,sticky=W,pady=1)
        backbone.grid(row=1, sticky=W, pady=1)
        alpha.grid(row=2, sticky=W, pady=1)
        subpixel.grid(row=3, sticky=W, pady=1)
        dlcsettingsbutton.grid(row=4,pady=5)
    def savedlcsettings(self,weight,backbone,alpha,subpixel):
        configini = self.configini
        config = ConfigParser()
        config.read(configini)

        config.set('DeepLabCut settings', 'weights', str(weight))
        config.set('DeepLabCut settings', 'backbone', str(backbone))
        config.set('DeepLabCut settings', 'alpha', str(alpha))
        config.set('DeepLabCut settings', 'subpixel', str(subpixel))

        with open(configini, 'w') as configfile:
            config.write(configfile)

        print('Settings saved.')

    def leapmenu(self):
        leaptoplevel = Toplevel()
        leaptoplevel.minsize(300, 200)
        leaptoplevel.wm_title("LEAP")

        leaplabel = LabelFrame(leaptoplevel,pady=5,padx=5)
        filters = Entry_Box(leaplabel,'Filters','10')
        torFalseoption = {'True','False'}
        upsamplinglayers = DropDownMenu(leaplabel,'Upsampling layers',torFalseoption,'15')
        batchnorm = DropDownMenu(leaplabel,'Batchnorm',torFalseoption,'15')
        poolingoption = {'max','average'}
        pooling = DropDownMenu(leaplabel,'Pooling',poolingoption,'15')
        interpolationoption = {'nearest','bilinear','bicubic'}
        interpolation = DropDownMenu(leaplabel,'Interpolation',interpolationoption,'15')
        initializeroption = {'glorot_uniform','lecun_normal'}
        initializer = DropDownMenu(leaplabel,'Initializer',initializeroption,'15')
        subpixel = DropDownMenu(leaplabel,'Subpixel',torFalseoption,'15')

        #sets
        filters.set('64')
        upsamplinglayers.setChoices('False')
        batchnorm.setChoices('False')
        pooling.setChoices('max')
        interpolation.setChoices('nearest')
        initializer.setChoices('glorot_uniform')
        subpixel.setChoices('True')
        #button
        leapbutton = Button(leaplabel,text='Save settings',command=lambda:self.saveleapsettings(filters.entry_get,upsamplinglayers.getChoices(),batchnorm.getChoices(),pooling.getChoices(),interpolation.getChoices(),initializer.getChoices(),subpixel.getChoices()))


        #organize
        leaplabel.grid(row=0,sticky=W)
        filters.grid(row=0,sticky=W)
        upsamplinglayers.grid(row=1,sticky=W)
        batchnorm.grid(row=2,sticky=W)
        pooling.grid(row=3,sticky=W)
        interpolation.grid(row=4,sticky=W)
        initializer.grid(row=5,sticky=W)
        subpixel.grid(row=6,sticky=W)
        leapbutton.grid(row=7,pady=5)
    def saveleapsettings(self,filters,upsampling,batchnorm,pooling,interpolation,initializer,subpixel):
        configini = self.configini
        config = ConfigParser()
        config.read(configini)

        config.set('LEAP settings', 'filters', str(filters))
        config.set('LEAP settings', 'upsampling_layers', str(upsampling))
        config.set('LEAP settings', 'batchnorm', str(batchnorm))
        config.set('LEAP settings', 'pooling', str(pooling))
        config.set('LEAP settings', 'interpolation', str(interpolation))
        config.set('LEAP settings', 'subpixel', str(subpixel))
        config.set('LEAP settings', 'initializer', str(initializer))

        with open(configini, 'w') as configfile:
            config.write(configfile)

        print('Settings saved.')

class Load_DLC_Model:

    def __init__(self):
        # Popup window
        loadmodel = Toplevel()
        loadmodel.minsize(200, 200)
        loadmodel.wm_title("Load DLC Model")


        tab_parent = ttk.Notebook(loadmodel)

        tab1 = ttk.Frame(tab_parent)
        tab2 = ttk.Frame(tab_parent)
        tab3 = ttk.Frame(tab_parent)
        tab4 = ttk.Frame(tab_parent)
        tab7 = ttk.Frame(tab_parent)
        tab8 = ttk.Frame(tab_parent)
        tab9 = ttk.Frame(tab_parent)
        tab10 = ttk.Frame(tab_parent)
        tab11 = ttk.Frame(tab_parent)
        tab12 = ttk.Frame(tab_parent)
        tab13 = ttk.Frame(tab_parent)
        tab14 = ttk.Frame(tab_parent)
        tab15 = ttk.Frame(tab_parent)

        tab_parent.add(tab1, text=f'{"[ Load model ]": ^20s}')
        tab_parent.add(tab2,text=f'{"[ Generate temp yaml ]": ^20s}')
        tab_parent.add(tab3, text=f'{"[ Add videos into project ]": ^20s}')
        tab_parent.add(tab4, text=f'{"[ Extract / label frames ]": ^20s}')
        tab_parent.add(tab7, text=f'{"[ Generate training set ]": ^20s}')
        tab_parent.add(tab10, text=f'{"[ Video analysis ]": ^20s}')
        tab_parent.add(tab13, text=f'{"[ Extract outliers ]": ^20s}')
        tab_parent.grid(row=0)

        #Load Model : configpath
        labelframe_loadmodel = LabelFrame(tab1, text='Load Model', font=("Helvetica",12,'bold'),padx=5,pady=5)
        self.label_set_configpath = FileSelect(labelframe_loadmodel, 'DLC config path (.yaml): ',title='Select a .yaml file')

        # generate yaml file
        label_generatetempyaml = LabelFrame(tab2,text='Generate Temp yaml (for extracting frames from subset of videos)', font=("Helvetica",12,'bold') ,padx=5,pady=5)
        label_tempyamlsingle = LabelFrame(label_generatetempyaml,text='Single video',padx=5,pady=5)
        self.label_genyamlsinglevideo = FileSelect(label_tempyamlsingle,'Select video:',title='Select a video file')
        button_generatetempyaml_single = Button(label_tempyamlsingle,text='Add single video',command=lambda:generatetempyaml(self.label_set_configpath.file_path,self.label_genyamlsinglevideo.file_path))
        label_tempyamlmulti =LabelFrame(label_generatetempyaml,text='Multiple videos',padx=5,pady=5)
        self.label_genyamlmultivideo = FolderSelect(label_tempyamlmulti,'Select video folder:',title='Select video folder')
        button_generatetempyaml_multi = Button(label_tempyamlmulti,text='Add multiple videos',command=self.generateyamlmulti)
        label_tempyml = Label(label_generatetempyaml,text='Note: After creating the temp yaml with the selected videos, load the temp.yaml file in "Load Model".',font=('Times',10,'italic'))
        label_tempyml2 = Label(label_generatetempyaml,text='       Then, you can proceed to extract frames.',font=('Times',10,'italic'))

        #singlevid multivid
        labelframe_singlemultivid = LabelFrame(tab3,text='Add Videos into project',font=("Helvetica",12,'bold'),padx=5,pady=5)
        labelframe_singlevid = LabelFrame(labelframe_singlemultivid,text='Single Video',padx=5,pady=5)
        labelframe_multivid = LabelFrame(labelframe_singlemultivid,text='Multiple Videos',padx=5,pady=5)
        self.label_set_singlevid = FileSelect(labelframe_singlevid, 'Select Single Video: ',title='Select a video file')
        self.label_video_folder = FolderSelect(labelframe_multivid, 'Select Folder with videos:',title='Select video folder')
        button_add_single_video = Button(labelframe_singlevid,text='Add single video',command = self.dlc_addsinglevideo,fg='red')
        button_add_multi_video = Button(labelframe_multivid,text='Add multiple videos',command = self.dlc_addmultivideo_command,fg='red')

        ###########extract frames########
        label_extractframes = LabelFrame(tab4, text='Extract Frames DLC', font=("Helvetica",12,'bold'),padx=15,pady=5)
        # mode
        self.label_numframes2pick = Entry_Box(label_extractframes,'numframes2pick:','26')
        label_mode = Label(label_extractframes, text='Mode', font="Verdana 10 underline")
        self.mode = IntVar()
        checkbox_auto = Radiobutton(label_extractframes, text="Automatic", variable=self.mode, value=1)
        checkbox_manual = Radiobutton(label_extractframes, text="Manual", variable=self.mode, value=2)
        # algorithm
        label_algo = Label(label_extractframes, text='Algorithm ', font="Verdana 10 underline")
        self.algo = IntVar()
        checkbox_uniform = Radiobutton(label_extractframes, text="Uniform", variable=self.algo, value=1)
        checkbox_kmean = Radiobutton(label_extractframes, text="KMeans", variable=self.algo, value=2)
        # cluster resize width
        self.label_clusterresize = Entry_Box(label_extractframes, 'Cluster Resize Width (Default = 30)', '26')
        # cluster step
        self.label_clusterstep = Entry_Box(label_extractframes, 'Cluster Step (Default = 1)', '26')
        # cluster color
        label_clustercolor = Label(label_extractframes, text='Cluster color', font="Verdana 10 underline")
        # checkbox cluster color
        self.var_clustercolor = IntVar()
        checkbox_clustercolor = Checkbutton(label_extractframes, text='True', variable=self.var_clustercolor)
        # use opencv
        label_useopencv = Label(label_extractframes, text='Use OpenCV', font="Verdana 10 underline")
        # checkbox use opencv or not
        self.var_useopencv = IntVar()
        checkbox_useopencv = Checkbutton(label_extractframes, text='True', variable=self.var_useopencv)
        # extractframecommand
        button_extractframe = Button(label_extractframes, text='Extract Frames', command=self.dlc_extractframes_command)

        ##########label Frames#####
        label_labelframes = LabelFrame(tab4, text='Label Frames', font=("Helvetica",12,'bold'),padx=15,pady=5)
        self.button_label_frames = Button(label_labelframes, text='Label Frames', command=self.dlc_label_frames_command)

        ##########Check Labels#####
        label_checklabels = LabelFrame(tab4, text='Check Labels', font=("Helvetica",12,'bold'),padx=15,pady=5)
        self.button_check_labels = Button(label_checklabels, text='Check Labelled Frames', command=self.dlc_check_labels_command)

        ####generate training sets#####
        label_generate_trainingsets = LabelFrame(tab7,text='Generate Training Set',font =("Helvetica",12,'bold'),padx=15,pady=5)
        self.button_generate_trainingsets = Button(label_generate_trainingsets, text='Generate training set',command=self.dlc_generate_trainingsets_command)

        #####train network####
        label_train_network = LabelFrame(tab7,text= 'Train Network',font =("Helvetica",12,'bold'),padx=15,pady=5)
        self.label_iteration = Entry_Box(label_train_network,'iteration','10')
        self.button_update_iteration = Button(label_train_network,text='Update iteration',command =lambda:updateiteration(self.label_set_configpath.file_path,self.label_iteration.entry_get))
        self.init_weight = FileSelect(label_train_network,'init_weight     ',title='Select training weight, eg: .DATA-00000-OF-00001 File')
        self.update_init_weight = Button(label_train_network,text='Update init_weight',command=lambda:update_init_weight(self.label_set_configpath.file_path,self.init_weight.file_path))
        self.button_train_network = Button(label_train_network, text='Train Network',command=self.dlc_train_network_command)

        #######evaluate network####
        label_eva_network = LabelFrame(tab7,text='Evaluate Network',font = ("Helvetica",12,'bold'),padx=15,pady=5)
        self.button_evaluate_network = Button(label_eva_network, text='Evaluate Network',command=self.dlc_evaluate_network_command)

        #####video analysis####
        label_video_analysis = LabelFrame(tab10,text='Video Analysis',font=("Helvetica",12,'bold'),padx=15,pady=5)
        #singlevideoanalysis
        label_singlevideoanalysis = LabelFrame(label_video_analysis,text='Single Video Analysis',pady=5,padx=5)
        self.videoanalysispath = FileSelect(label_singlevideoanalysis, "Video path",title='Select a video file')
        button_vidanalysis = Button(label_singlevideoanalysis, text='Single Video Analysis', command=self.dlc_video_analysis_command1)
        #multi video analysis
        label_multivideoanalysis = LabelFrame(label_video_analysis,text='Multiple Videos Analysis',pady=5,padx=5)
        self.videofolderpath = FolderSelect(label_multivideoanalysis,'Folder Path',title='Select video folder')
        self.video_type = Entry_Box(label_multivideoanalysis,'Video type(eg:mp4,avi):','18')
        button_multivideoanalysis = Button(label_multivideoanalysis,text='Multi Videos Analysis',command=self.dlc_video_analysis_command2)

        #### plot####
        label_plot = LabelFrame(tab10,text='Plot Video Graph',font=("Helvetica",12,'bold'),padx=15,pady=5)
        # videopath
        self.videoplotpath = FileSelect(label_plot, "Video path",title='Select a video file')
        # plot button
        button_plot = Button(label_plot, text='Plot Results', command=self.dlc_plot_videoresults_command)

        #####create video####
        label_createvideo = LabelFrame(tab10,text='Create Video',font=("Helvetica",12,'bold'),padx=15,pady=5)
        # videopath
        self.createvidpath = FileSelect(label_createvideo, "Video path",title='Select a video file')
        # save frames
        self.var_saveframes = IntVar()
        checkbox_saveframes = Checkbutton(label_createvideo, text='Save Frames', variable=self.var_saveframes)
        # create video button
        button_createvideo = Button(label_createvideo, text='Create Video', command=self.dlc_create_video_command)

        ######Extract Outliers####
        label_extractoutlier = LabelFrame(tab13,text='Extract Outliers',font=("Helvetica",12,'bold'),pady=5,padx=5)
        self.label_extractoutliersvideo = FileSelect(label_extractoutlier,'Videos to correct:',title='Select a video file')
        button_extractoutliers = Button(label_extractoutlier,text='Extract Outliers',command =lambda:deeplabcut.extract_outlier_frames(self.label_set_configpath.file_path, [str(self.label_extractoutliersvideo.file_path)],automatic=True) )

        ####label outliers###
        label_labeloutliers = LabelFrame(tab13,text='Label Outliers',font =("Helvetica",12,'bold'),pady=5,padx=5)
        button_refinelabels = Button(label_labeloutliers,text='Refine Outliers',command=lambda:deeplabcut.refine_labels(self.label_set_configpath.file_path))

        ####merge labeled outliers ###
        label_mergeoutliers = LabelFrame(tab13,text='Merge Labelled Outliers',font=("Helvetica",12,'bold'),pady=5,padx=5)
        button_mergelabeledoutlier = Button(label_mergeoutliers,text='Merge Labelled Outliers',command=lambda:deeplabcut.merge_datasets(self.label_set_configpath.file_path))

        #organize
        labelframe_loadmodel.grid(row=0,sticky=W,pady=5)
        self.label_set_configpath.grid(row=0,sticky=W)

        label_generatetempyaml.grid(row=1,sticky=W)
        label_tempyamlsingle.grid(row=0,sticky=W)
        self.label_genyamlsinglevideo.grid(row=0,sticky=W)
        button_generatetempyaml_single.grid(row=1,sticky=W)
        label_tempyamlmulti.grid(row=1,sticky=W)
        self.label_genyamlmultivideo.grid(row=0,sticky=W)
        button_generatetempyaml_multi.grid(row=1,sticky=W)
        label_tempyml.grid(row=2,sticky=W)
        label_tempyml2.grid(row=3, sticky=W)

        labelframe_singlemultivid.grid(row=2,sticky=W,pady=5)
        labelframe_singlevid.grid(row=0,sticky=W)
        self.label_set_singlevid.grid(row=0,sticky=W)
        button_add_single_video.grid(row=1,sticky=W)
        labelframe_multivid.grid(row=1,sticky=W)
        self.label_video_folder.grid(row=0,sticky=W)
        button_add_multi_video.grid(row=1,sticky=W)

        label_extractframes.grid(row=3,column=0, sticky=W,pady=5,padx=5)
        self.label_numframes2pick.grid(row=0,sticky=W)
        label_mode.grid(row=1, sticky=W)
        checkbox_auto.grid(row=2, sticky=W)
        checkbox_manual.grid(row=3, sticky=W)
        label_algo.grid(row=4, sticky=W)
        checkbox_uniform.grid(row=5, sticky=W)
        checkbox_kmean.grid(row=6, sticky=W)
        self.label_clusterresize.grid(row=7, sticky=W)
        self.label_clusterstep.grid(row=8, sticky=W)
        label_clustercolor.grid(row=9, sticky=W)
        checkbox_clustercolor.grid(row=10, sticky=W)
        label_useopencv.grid(row=11, sticky=W)
        checkbox_useopencv.grid(row=12, sticky=W)
        button_extractframe.grid(row=13,sticky=W)

        label_labelframes.grid(row=3,column=1,sticky=W+N,pady=5,padx=5)
        self.button_label_frames.grid(row=0,sticky=W)

        label_checklabels.grid(row=3,column=2,sticky=W+N,pady=5,padx=5)
        self.button_check_labels.grid(row=0,sticky=W)

        label_generate_trainingsets.grid(row=6,sticky=W,pady=5)
        self.button_generate_trainingsets.grid(row=0,sticky=W)

        label_train_network.grid(row=7,sticky=W,pady=5)
        self.label_iteration.grid(row=0,column=0,sticky=W)
        self.button_update_iteration.grid(row=0,column=1,sticky=W)
        self.init_weight.grid(row=1,column=0,sticky=W)
        self.update_init_weight.grid(row=1,column=1,sticky=W)
        self.button_train_network.grid(row=2,sticky=W)

        label_eva_network.grid(row=8,sticky=W,pady=5)
        self.button_evaluate_network.grid(row=0,sticky=W)
        #video analysis
        label_video_analysis.grid(row=9,sticky=W,pady=5)
        label_singlevideoanalysis.grid(row=0,sticky=W,pady=5)
        label_multivideoanalysis.grid(row=1,sticky=W,pady=5)
        self.videoanalysispath.grid(row=0,sticky=W)
        button_vidanalysis.grid(row=2,sticky=W)
        self.videofolderpath.grid(row=3,sticky=W,pady=5)
        self.video_type.grid(row=4,sticky=W)
        button_multivideoanalysis.grid(row=5,sticky=W)

        label_plot.grid(row=10,sticky=W,pady=5)
        self.videoplotpath.grid(row=0,sticky=W)
        button_plot.grid(row=1,sticky=W)

        label_createvideo.grid(row=11,sticky=W,pady=5)
        self.createvidpath.grid(row=0,sticky=W)
        checkbox_saveframes.grid(row=1,sticky=W)
        button_createvideo.grid(row=2,sticky=W)

        label_extractoutlier.grid(row=12,sticky=W,pady=5)
        self.label_extractoutliersvideo.grid(row=0,sticky=W)
        button_extractoutliers.grid(row=1,sticky=W)

        label_labeloutliers.grid(row=13,sticky=W,pady=5)
        button_refinelabels.grid(row=0,sticky=W)

        label_mergeoutliers.grid(row=14,sticky=W,pady=5)
        button_mergelabeledoutlier.grid(row=0,sticky=W)


    def dlc_addsinglevideo(self):
        try:
            deeplabcut.add_new_videos(self.label_set_configpath.file_path, [str(self.label_set_singlevid.file_path)],copy_videos=True)
        except FileNotFoundError:
            print('...')
            print('Fail to add video, please load .yaml file and select video file')

    def generateyamlmulti(self):
        try:

            config_path = self.label_set_configpath.file_path
            directory = self.label_genyamlmultivideo.folder_path
            filesFound = []

            ########### FIND FILES ###########
            for i in os.listdir(directory):
                if '.avi' or '.mp4' in i:
                    a = os.path.join(directory, i)
                    filesFound.append(a)
                    print(a)
            print(filesFound)

            generatetempyaml_multi(config_path,filesFound)
        except FileNotFoundError:
            print('Fail to add videos, please load .yaml file and select video folder')

    def dlc_addmultivideo_command(self):
        try:
            config_path = self.label_set_configpath.file_path
            directory = self.label_video_folder.folder_path
            filesFound = []

            ########### FIND FILES ###########
            for i in os.listdir(directory):
                if 'avi' or '.mp4' in i:
                    a = os.path.join(directory, i)
                    deeplabcut.add_new_videos(config_path, [str(a)], copy_videos=True)

            print("Videos added.")
        except FileNotFoundError:
            print('Fail to add videos, please load .yaml file and select video folder')

    def dlc_extractframes_command(self):

        config_path = self.label_set_configpath.file_path
        select_numfram2pick(config_path,self.label_numframes2pick.entry_get)

        if self.mode.get()==1:
            modes = str('automatic')
        elif self.mode.get()==2:
            modes = str('manual')

        if self.algo.get()==1:
            algorithm = str('uniform')
        elif self.algo.get()==2:
            algorithm = str('kmeans')

        if len(self.label_clusterresize.entry_get)==0:
            clusterresizewidth = int(30)
        else:
            clusterresizewidth = int(self.label_clusterresize.entry_get)

        if len(self.label_clusterstep.entry_get)==0:
            clusterstep = int(1)
        else:
            clusterstep = int(self.label_clusterstep.entry_get)

        if self.var_clustercolor.get()==1:
            clustercolor = True
        else:
            clustercolor = False

        if self.var_useopencv.get()==1:
            useopencv = True
        else:
            useopencv = False
        try:
            print(config_path,modes,algorithm,clusterstep,clusterresizewidth,clustercolor,useopencv)
            deeplabcut.extract_frames(config_path,mode=modes,algo=algorithm,crop=False,userfeedback=False,cluster_step=clusterstep,cluster_resizewidth=clusterresizewidth,cluster_color=clustercolor,opencv=useopencv)
        except:
            print('Fail to extract frames, please make sure all the information is filled in')

    def dlc_label_frames_command(self):
        config_path = self.label_set_configpath.file_path
        deeplabcut.label_frames(config_path)

    def dlc_check_labels_command(self):
        try:
            config_path = self.label_set_configpath.file_path
            deeplabcut.check_labels(config_path)
        except FileNotFoundError:
            print('Please load .yaml file to continue')

    def dlc_generate_trainingsets_command(self):
        try:
            config_path = self.label_set_configpath.file_path
            deeplabcut.create_training_dataset(config_path, num_shuffles=1)
        except FileNotFoundError:
            print('Please load .yaml file to continue')

    def dlc_train_network_command(self):
        try:
            config_path = self.label_set_configpath.file_path
            deeplabcut.train_network(config_path, shuffle=1, gputouse=0)
        except FileNotFoundError:
            print('Please load .yaml file to continue')

    def dlc_evaluate_network_command(self):
        try:
            config_path = self.label_set_configpath.file_path
            deeplabcut.evaluate_network(config_path, plotting=True)
        except FileNotFoundError:
            print('Please load .yaml file to continue')

    def dlc_video_analysis_command1(self):
        try:
            config_path = self.label_set_configpath.file_path

            vid_name = os.path.basename(self.videoanalysispath.file_path)
            vid_type = vid_name[-4:]

            deeplabcut.analyze_videos(config_path, [str(self.videoanalysispath.file_path)], shuffle=1,save_as_csv=True, videotype=vid_type)
        except FileNotFoundError:
            print('Please load .yaml file and select video path to continue')

    def dlc_video_analysis_command2(self):
        try:
            config_path = self.label_set_configpath.file_path

            folder_path = self.videofolderpath.folder_path
            vid_type = self.video_type.entry_get

            deeplabcut.analyze_videos(config_path, [str(folder_path)], shuffle=1,save_as_csv=True, videotype=vid_type)
        except FileNotFoundError:
            print('Please load .yaml file and select folder with videos to continue')


    def dlc_plot_videoresults_command(self):
        try:

            config_path = self.label_set_configpath.file_path
            deeplabcut.plot_trajectories(config_path, [str(self.videoplotpath.file_path)])
        except FileNotFoundError:
            print('Please load .yaml file and select a video file to plot graph')

    def dlc_create_video_command(self):
        try:
            config_path = self.label_set_configpath.file_path

            if self.var_saveframes==1:
                saveframes=True
            else:
                saveframes=False
            vid_name = os.path.basename(self.createvidpath.file_path)
            vid_type = vid_name[-4:]

            deeplabcut.create_labeled_video(config_path, [str(self.createvidpath.file_path)],save_frames=saveframes, videotype=vid_type)
        except FileNotFoundError:
            print('Please select .yaml file and select a video to continue.')

class shorten_video:

    def __init__(self):
        # Popup window
        shortenvid = Toplevel()
        shortenvid.minsize(200, 200)
        shortenvid.wm_title("Clip video")

        # videopath
        self.videopath1selected = FileSelect(shortenvid, "Video path",title='Select a video file')

        #timeframe for start and end cut
        label_cutvideomethod1 = LabelFrame(shortenvid,text='Method 1',font='bold',padx=5,pady=5)
        label_timeframe = Label(label_cutvideomethod1, text='Please enter the time frame in hh:mm:ss format')
        self.label_starttime = Entry_Box(label_cutvideomethod1,'Start at:','8')
        self.label_endtime = Entry_Box(label_cutvideomethod1, 'End at:',8)
        CreateToolTip(label_cutvideomethod1,
                      'Method 1 will retrieve the specified time input.(eg: input of Start at: 00:00:00, End at: 00:01:00, will create a new video from the chosen video from the very start till it reaches the first minute of the video)')

        #express time frame
        label_cutvideomethod2 = LabelFrame(shortenvid,text='Method 2',font='bold',padx=5,pady=5)
        label_method2 = Label(label_cutvideomethod2,text='Method 2 will retrieve from the end of the video (e.g.,: an input of 3 seconds will get rid of the first 3 seconds of the video).')
        # self.var_express = IntVar()
        # checkbox_express = Checkbutton(label_cutvideomethod2, text='Check this box to use Method 2', variable=self.var_express)
        self.label_time = Entry_Box(label_cutvideomethod2,'Seconds:','8')
        CreateToolTip(label_cutvideomethod2,'Method 2 will retrieve from the end of the video.(eg: an input of 3 seconds will get rid of the first 3 seconds of the video)')

        #button to cut video
        button_cutvideo1 = Button(label_cutvideomethod1, text='Cut Video', command=lambda:shortenvideos1(self.videopath1selected.file_path,self.label_starttime.entry_get,self.label_endtime.entry_get))
        button_cutvideo2 = Button(label_cutvideomethod2,text='Cut Video',command =lambda:shortenvideos2(self.videopath1selected.file_path,self.label_time.entry_get))
        #organize
        self.videopath1selected.grid(row=0,sticky=W)

        label_cutvideomethod1.grid(row=1,sticky=W,pady=5)
        label_timeframe.grid(row=0,sticky=W)
        self.label_starttime.grid(row=1,sticky=W)
        self.label_endtime.grid(row=2,sticky=W)
        button_cutvideo1.grid(row=3)


        label_cutvideomethod2.grid(row=2,sticky=W,pady=5)
        label_method2.grid(row=0,sticky=W)
        # checkbox_express.grid(row=1,sticky=W)
        self.label_time.grid(row=2,sticky=W)
        button_cutvideo2.grid(row=3)

class change_imageformat:

    def __init__(self):

        # Popup window
        chgimgformat = Toplevel()
        chgimgformat.minsize(200, 200)
        chgimgformat.wm_title("Change image format")

        #select directory
        self.folderpath1selected = FolderSelect(chgimgformat,"Image directory",title='Select folder with images')

        #change image format
        label_filetypein = LabelFrame(chgimgformat,text= 'Original image format',font=("Helvetica",12,'bold'),padx=15,pady=5)
        # Checkbox input
        self.varfiletypein = IntVar()
        checkbox_c1 = Radiobutton(label_filetypein, text=".png", variable=self.varfiletypein, value=1)
        checkbox_c2 = Radiobutton(label_filetypein, text=".jpeg", variable=self.varfiletypein, value=2)
        checkbox_c3 = Radiobutton(label_filetypein, text=".bmp", variable=self.varfiletypein, value=3)

        #ouput image format
        label_filetypeout = LabelFrame(chgimgformat,text='Output image format',font=("Helvetica",12,'bold'),padx=15,pady=5)
        #checkbox output
        self.varfiletypeout = IntVar()
        checkbox_co1 = Radiobutton(label_filetypeout, text=".png", variable=self.varfiletypeout, value=1)
        checkbox_co2 = Radiobutton(label_filetypeout, text=".jpeg", variable=self.varfiletypeout, value=2)
        checkbox_co3 = Radiobutton(label_filetypeout, text=".bmp", variable=self.varfiletypeout, value=3)

        #button
        button_changeimgformat = Button(chgimgformat, text='Convert image file format', command=self.changeimgformatcommand)

        #organized
        self.folderpath1selected.grid(row=0,column=0)
        label_filetypein.grid(row=1,column=0,pady=5)
        checkbox_c1.grid(row=2,column=0)
        checkbox_c2.grid(row=3,column=0)
        checkbox_c3.grid(row=4,column=0)
        label_filetypeout.grid(row=5,column=0,pady=5)
        checkbox_co1.grid(row=6,column=0)
        checkbox_co2.grid(row=7,column=0)
        checkbox_co3.grid(row=8, column=0)
        button_changeimgformat.grid(row=9,pady=5)

    def changeimgformatcommand(self):

        if self.varfiletypein.get()==1:
            filetypein = str('png')
        elif self.varfiletypein.get()==2:
            filetypein = str('jpeg')
        elif self.varfiletypein.get()==3:
            filetypein = str('bmp')

        if self.varfiletypeout.get()==1:
            filetypeout = str('png')
        elif self.varfiletypeout.get()==2:
            filetypeout = str('jpeg')
        elif self.varfiletypeout.get() == 3:
            filetypeout = str('bmp')

        cif=changeimageformat(self.folderpath1selected.folder_path, filetypein, filetypeout)

        print('Images converted to '+ str(cif) + ' format')

class convert_video:

    def __init__(self):
        # Popup window
        convertvid = Toplevel()
        convertvid.minsize(400, 400)
        convertvid.wm_title("Convert video format")

        #multi video
        label_multivideo = LabelFrame(convertvid, text='Convert multiple videos',font=("Helvetica",12,'bold'),padx=5,pady=5)
        vid_dir = FolderSelect(label_multivideo,'Video directory',title='Select folder with videos')
        ori_format = Entry_Box(label_multivideo,'Input format','12')
        final_format = Entry_Box(label_multivideo,'Output format','12')
        button_convertmultivid = Button(label_multivideo,text='Convert multiple videos',command = lambda: batch_convert_videoformat(vid_dir.folder_path,ori_format.entry_get,final_format.entry_get))

        #single video
        label_convert = LabelFrame(convertvid,text='Convert single video',font=("Helvetica",12,'bold'),padx=5,pady=5)
        self.videopath1selected = FileSelect(label_convert, "Video path",title='Select a video file')
        self.vvformat = IntVar()
        checkbox_v1 = Radiobutton(label_convert, text="Convert .avi to .mp4", variable=self.vvformat, value=1)
        checkbox_v2 = Radiobutton(label_convert, text="Convert mp4 into Powerpoint supported format", variable=self.vvformat, value=2)

        #button
        button_convertvid= Button(label_convert, text='Convert video format', command=self.convertavitomp)

        #organize
        label_multivideo.grid(row=0,sticky=W)
        vid_dir.grid(row=0,sticky=W)
        ori_format.grid(row=1,sticky=W)
        final_format.grid(row=2,sticky=W)
        button_convertmultivid.grid(row=3,pady=10)

        label_convert.grid(row=1,sticky=W)
        self.videopath1selected.grid(row=0,sticky=W)
        checkbox_v1.grid(row=1,column=0,sticky=W)
        checkbox_v2.grid(row=2,column=0,sticky=W)
        button_convertvid.grid(row=3,column=0,pady=10)

    def convertavitomp(self):

        if self.vvformat.get()== 1:
            cavi = convertavitomp4(self.videopath1selected.file_path)
            print('Video converted to ' + cavi)
        elif self.vvformat.get()== 2:
            cavi = convertpowerpoint(self.videopath1selected.file_path)
            print('Video converted to ' + cavi)

class extract_specificframes:

    def __init__(self):
        # Popup window
        extractsf = Toplevel()
        extractsf.minsize(200, 200)
        extractsf.wm_title("Extract defined Frames")

        # videopath
        self.videopath1selected = FileSelect(extractsf, "Video path",title='Select a video file')

        #entry boxes for frames to extract
        label_frametitle = LabelFrame(extractsf, text='Frames to be extracted',padx=5,pady=5)
        self.label_startframe1 = Entry_Box(label_frametitle,'Start Frame:','10')

        self.label_endframe1 = Entry_Box(label_frametitle, 'End Frame:','10')


        #button
        button_extractsf = Button(label_frametitle, text='Extract Frames', command=self.extractsfcommand)

        #organize
        self.videopath1selected.grid(row=0,column=0,sticky=W,pady=10)
        label_frametitle.grid(row=1,column=0,sticky=W)
        self.label_startframe1.grid(row=2,column=0,sticky=W)

        self.label_endframe1.grid(row=3,column=0,sticky=W)

        button_extractsf.grid(row=4,pady=5)

    def extractsfcommand(self):

        startframe1 = self.label_startframe1.entry_get
        endframe1 = self.label_endframe1.entry_get

        extractspecificframe(self.videopath1selected.file_path, startframe1, endframe1)
        print('Frames were extracted from '+ str(startframe1)+' to ' + endframe1)

def extract_allframes():

    # Popup window
    extractaf = Toplevel()
    extractaf.minsize(200, 200)
    extractaf.wm_title("Extract all frames")

    # videopath
    videopath = FileSelect(extractaf, "Video path",title='Select a video file')

    #button
    button_extractaf = Button(extractaf, text='Extract All Frames', command= lambda:extract_allframescommand(videopath.file_path))

    #organize
    videopath.grid(row=0,column=0)
    button_extractaf.grid(row=1,column=0)

class multicropmenu:
    def __init__(self):
        multimenu = Toplevel()
        multimenu.minsize(200, 200)
        multimenu.wm_title("Multi Crop")

        self.inputfolder = FolderSelect(multimenu,"Video Folder  ")
        self.outputfolder = FolderSelect(multimenu,"Output Folder")

        self.videotype = Entry_Box(multimenu,"Video type","10")
        self.croptimes = Entry_Box(multimenu,"# of crops","10")

        button_multicrop = Button(multimenu,text='Crop',command=lambda:multicrop(self.videotype.entry_get,self.inputfolder.folder_path,self.outputfolder.folder_path,self.croptimes.entry_get))

        #organize
        self.inputfolder.grid(row=0,sticky=W,pady=2)
        self.outputfolder.grid(row=1,sticky=W,pady=2)
        self.videotype.grid(row=2,sticky=W,pady=2)
        self.croptimes.grid(row=3,sticky=W,pady=2)
        button_multicrop.grid(row=4,pady=10)

class changefps:
    def __init__(self):
        fpsmenu = Toplevel()
        fpsmenu.minsize(200, 200)
        fpsmenu.wm_title("Change frame rate of video")

        # videopath
        videopath = FileSelect(fpsmenu, "Video path",title='Select a video file')

        #fps
        label_fps= Entry_Box(fpsmenu,'Output fps','10')

        #button
        button_fps = Button(fpsmenu,text='Convert',command=lambda:changefps_singlevideo(videopath.file_path,label_fps.entry_get))

        #organize
        videopath.grid(row=0,sticky=W)
        label_fps.grid(row=1,sticky=W)
        button_fps.grid(row=2)

class changefpsmulti:
    def __init__(self):
        multifpsmenu = Toplevel()
        multifpsmenu.minsize(400, 200)
        multifpsmenu.wm_title("Change frame rate of videos in a folder")

        # videopath
        videopath = FolderSelect(multifpsmenu, "Folder path", title='Select folder with videos')

        # fps
        label_fps = Entry_Box(multifpsmenu, 'Output fps', '10')

        # button
        button_fps = Button(multifpsmenu, text='Convert',
                            command=lambda: changefps_multivideo(videopath.folder_path, label_fps.entry_get))
        # organize
        videopath.grid(row=0, sticky=W)
        label_fps.grid(row=1, sticky=W)
        button_fps.grid(row=2)


class extract_seqframe:

    def __init__(self):
        extractseqtoplevel = Toplevel()
        extractseqtoplevel.minsize(200, 200)
        extractseqtoplevel.wm_title("Extract All Frames from Seq files")

        # videopath
        videopath = FileSelect(extractseqtoplevel, "Video Path",title='Select a video file')

        # button
        button_extractseqframe = Button(extractseqtoplevel, text='Extract All Frames', command=lambda: extract_seqframescommand(videopath.file_path))

        #organize
        videopath.grid(row=0)
        button_extractseqframe.grid(row=1)

class mergeframeffmpeg:

    def __init__(self):
        # Popup window
        mergeffmpeg = Toplevel()
        mergeffmpeg.minsize(250, 250)
        mergeffmpeg.wm_title("Merge images to video")

        # select directory
        self.folderpath1selected = FolderSelect(mergeffmpeg,"Working Directory",title='Select folder with frames')

        # settings
        label_settings = LabelFrame(mergeffmpeg,text='Settings',padx=5,pady=5)
        self.label_imgformat = Entry_Box(label_settings, 'Image format','10')
        label_to = Label(label_settings,text=' to ',width=0)
        self.label_vidformat = Entry_Box(label_settings,'Video format','10')
        self.label_bitrate = Entry_Box(label_settings,'Bitrate','10')
        self.label_fps = Entry_Box(label_settings,'fps','10')

        #button
        button_mergeimg = Button(label_settings, text='Merge Images', command=self.mergeframeffmpegcommand)

        #organize
        label_settings.grid(row=1,pady=10)
        self.folderpath1selected.grid(row=0,column=0,pady=10)
        self.label_imgformat.grid(row=1,column=0,sticky=W)

        label_to.grid(row=1,column=1)
        self.label_vidformat.grid(row=1,column=2,sticky=W)
        self.label_fps.grid(row=2,column=0,sticky=W,pady=5)
        self.label_bitrate.grid(row=3,column=0,sticky=W,pady=5)
        button_mergeimg.grid(row=4,column=1,sticky=E,pady=10)


    def mergeframeffmpegcommand(self):

        imgformat = self.label_imgformat.entry_get
        vidformat = self.label_vidformat.entry_get
        bitrate = self.label_bitrate.entry_get
        fps = self.label_fps.entry_get

        mergemovieffmpeg(self.folderpath1selected.folder_path,fps,vidformat,bitrate,imgformat)
        print('Video created.')

class creategif:

    def __init__(self):
        # Popup window
        create_gif = Toplevel()
        create_gif.minsize(250, 250)
        create_gif.wm_title("Generate Gif from video")


        #Create Gif
        label_creategif = LabelFrame(create_gif,text='Video to Gif',padx=5,pady=5,font='bold')
        # select video to convert to gif
        videoselected = FileSelect(label_creategif, 'Video path',title='Select a video file')
        label_starttime = Entry_Box(label_creategif,'Start time(s)','12')
        label_duration = Entry_Box(label_creategif,'Duration(s)','12')
        label_size = Entry_Box(label_creategif,'Width','12')
        size_description = Label(label_creategif,text='example width: 240,360,480,720,1080',font=("Times", 10, "italic"))
        #convert
        button_creategif = Button(label_creategif,text='Generate Gif',command=lambda :generategif(videoselected.file_path,label_starttime.entry_get,label_duration.entry_get,label_size.entry_get))

        #organize
        label_creategif.grid(row=0,sticky=W)
        videoselected.grid(row=0,sticky=W,pady=5)
        label_starttime.grid(row=1,sticky=W)
        label_duration.grid(row=2,sticky=W)
        label_size.grid(row=3,sticky=W)
        size_description.grid(row=4,sticky=W)
        button_creategif.grid(row=5,sticky=E,pady=10)

class new_window:

    def open_Folder(self):
        print("Current directory is %s" % os.getcwd())
        folder = askdirectory(title='Select Frame Folder')
        os.chdir(folder)
        print("Working directory is %s" % os.getcwd())
        # self.label = Label(new_window, text="Folder selected: %s" % os.getcwd()).grid(row=3, column=1)

    def __init__(self, script_name):
        window = Tk()

        folder = Frame(window)
        folder.grid(row = 0, column = 1, sticky = N)

        choose_folder = Label(folder, text="Choose Folder")
        choose_folder.grid(row = 0, column = 0, sticky = W)
        select_folder = Button(folder, text="Choose Folder...", command=self.open_Folder)
        select_folder.grid(row = 0, column = 0, sticky = W)
        run_script = Button(folder, text="Run", command=script_name.main)
        run_script.grid(columnspan = 2, sticky = S)

def createWindow(scriptname):
    new_window(scriptname)

class get_coordinates_from_video:

    def __init__(self):
        # Popup window
        getcoord = Toplevel()
        getcoord.minsize(200, 200)
        getcoord.wm_title('Get Coordinates in Video')

        # settings files selected
        self.videopath1selected = FileSelect(getcoord, "Video selected",title='Select a video file')

        # label for known mm
        self.label_knownmm = Entry_Box(getcoord,'Known length in real life(mm)','0')

        #button
        button_getcoord = Button(getcoord, text='Get Distance', command=self.getcoord)

        #organize
        self.videopath1selected.grid(row=0,column=0,pady=10,sticky=W)
        self.label_knownmm.grid(row=1,column=0,pady=10,sticky=W)
        button_getcoord.grid(row=2,column=0,pady=10)

    def getcoord(self):
        filename= self.videopath1selected.file_path
        knownmm_value = self.label_knownmm.entry_get
        if knownmm_value == '':
            print('Please enter the known millimeters to continue')

        elif filename != '' and filename != 'No file selected':

            getco = get_coordinates_nilsson(self.videopath1selected.file_path,knownmm_value)
            print('The distance between the two set points is ', str(getco))

        else:
            print('Please select a video')

class project_config:

    def __init__(self):
        self.all_entries = []
        self.allmodels = []
        # Popup window
        self.toplevel = Toplevel()
        self.toplevel.minsize(700, 700)
        self.toplevel.wm_title("Project Configuration")
        #scroll
        projectconfig = Scrollable(self.toplevel, width=25)

        #tab
        tab_parent = ttk.Notebook(projectconfig)
        tab1 = ttk.Frame(tab_parent)
        tab2 = ttk.Frame(tab_parent)
        tab3 = ttk.Frame(tab_parent)
        tab4 = ttk.Frame(tab_parent)
        #tab title
        tab_parent.add(tab1,text=f'{"[ Generate project config ]": ^20s}')
        tab_parent.add(tab2, text=f'{"[ Import videos into project folder ]": ^20s}')
        tab_parent.add(tab3, text=f'{"[ Import tracking data ]": ^20s}')
        tab_parent.add(tab4, text=f'{"[ Extract frames into project folder ]": ^20s}')
        #initiate tab
        tab_parent.grid(row=0)

        # General Settings
        self.label_generalsettings = LabelFrame(tab1, text='General Settings',fg='black',font =("Helvetica",12,'bold'),padx=5,pady=5)
        self.directory1Select = FolderSelect(self.label_generalsettings, "Project Path:", title='Select Main Directory')
        self.label_project_name = Entry_Box(self.label_generalsettings, 'Project Name:', '0')
        label_project_namedescrip = Label(self.label_generalsettings, text='(project name cannot contain spaces)')

        #SML Settings
        self.label_smlsettings = LabelFrame(self.label_generalsettings, text='SML Settings',padx=5,pady=5)
        self.label_notarget = Entry_Box(self.label_smlsettings,'Number of predictive classifiers (behaviors):','33')
        addboxButton = Button(self.label_smlsettings, text='<Add predictive classifier>', fg="navy", command=lambda:self.addBox(projectconfig))

        ##dropdown for # of mice
        dropdownbox = LabelFrame(self.label_generalsettings, text='Animal Settings')
        label_dropdownmice = Label(dropdownbox,text='# config')
        self.option_mice, optionsBasePhotosList = bodypartConfSchematic()
        self.var = StringVar()
        self.var.set(self.option_mice[6])
        micedropdown = OptionMenu(dropdownbox,self.var,*self.option_mice)

        self.var.trace("w", self.change_image)

        self.photos = []
        for i in range(len(optionsBasePhotosList)):
            self.photos.append(PhotoImage(file=os.path.join(os.getcwd(),(optionsBasePhotosList[i]))))


        self.label = Label(self.label_generalsettings, image=self.photos[6])
        self.label.grid(row=10,sticky=W)

        #reset button
        resetbutton = Button(self.label_generalsettings,text='Reset user-defined pose configs',command=self.resetSettings)

        #generate project ini
        button_generateprojectini = Button(self.label_generalsettings, text='Generate Project Config ', command=self.make_projectini, font=("Helvetica",10,'bold'),fg='navy')

        #####import videos
        label_importvideo = LabelFrame(tab2, text='Import Videos into project folder',fg='black', font=("Helvetica",12,'bold'), padx=15, pady=5)
        # multi video
        label_multivideoimport = LabelFrame(label_importvideo, text='Import multiple videos', pady=5, padx=5)
        self.multivideofolderpath = FolderSelect(label_multivideoimport, 'Folder path',title='Select Folder with videos')
        self.video_type = Entry_Box(label_multivideoimport, 'Format (i.e., mp4, avi):', '18')
        button_multivideoimport = Button(label_multivideoimport, text='Import multiple videos',command= self.import_multivid,fg='navy')
        # singlevideo
        label_singlevideoimport = LabelFrame(label_importvideo, text='Import single video', pady=5, padx=5)
        self.singlevideopath = FileSelect(label_singlevideoimport, "Video path",title='Select a video file')
        button_importsinglevideo = Button(label_singlevideoimport, text='Import a video',command= self.import_singlevid,fg='navy')


        #import all csv file into project folder
        label_import_csv = LabelFrame(tab3,text='Import DLC Tracking Data',fg='black',font=("Helvetica",12,'bold'),pady=5,padx=5)
        #multicsv
        label_multicsvimport = LabelFrame(label_import_csv, text='Import multiple csv files', pady=5, padx=5)
        self.folder_csv = FolderSelect(label_multicsvimport,'Folder Select:',title='Select Folder with .csv(s)')
        button_import_csv = Button(label_multicsvimport,text='Import csv to project folder',command = self.import_multicsv,fg='navy')
        #singlecsv
        label_singlecsvimport = LabelFrame(label_import_csv, text='Import single csv files', pady=5, padx=5)
        self.file_csv = FileSelect(label_singlecsvimport,'File Select',title='Select a .csv file')
        button_importsinglecsv = Button(label_singlecsvimport,text='Import single csv to project folder',command=self.import_singlecsv,fg='navy')


        #extract videos in projects
        label_extractframes = LabelFrame(tab4,text='Extract Frames into project folder',fg='black',font=("Helvetica",12,'bold'),pady=5,padx=5)
        label_note = Label(label_extractframes,text='Video frames are used for visualizations')
        label_caution = Label(label_extractframes,text='Caution: This extract all frames from all videos in project,')
        label_caution2 = Label(label_extractframes,text='and is computationally expensive if there is a lot of videos at high frame rates/resolution.')
        button_extractframes = Button(label_extractframes,text='Extract frames',command=self.extract_frames,fg='navy')

        #organize
        self.label_generalsettings.grid(row=0,sticky=W)
        self.directory1Select.grid(row=1,column=0,sticky=W)
        self.label_project_name.grid(row=2,column=0,sticky=W)
        label_project_namedescrip.grid(row=3,sticky=W)

        self.label_smlsettings.grid(row=4,column=0,sticky=W,pady=5,columnspan=2)
        self.label_notarget.grid(row=0,column=0,sticky=W,pady=5)
        addboxButton.grid(row=1,column=0,sticky=W,pady=6)

        dropdownbox.grid(row=5,column=0,sticky=W)
        resetbutton.grid(row=5,column=1,sticky=W)
        label_dropdownmice.grid(row=0,column=0,sticky=W)
        micedropdown.grid(row=0,column=1,sticky=W)

        button_generateprojectini.grid(row=20, pady=5, ipadx=5, ipady=5)

        label_importvideo.grid(row=4,sticky=W,pady=5)
        label_multivideoimport.grid(row=0, sticky=W)
        self.multivideofolderpath.grid(row=0, sticky=W)
        self.video_type.grid(row=1, sticky=W)
        button_multivideoimport.grid(row=2, sticky=W)
        label_singlevideoimport.grid(row=1,sticky=W)
        self.singlevideopath.grid(row=0,sticky=W)
        button_importsinglevideo.grid(row=1,sticky=W)


        label_import_csv.grid(row=5,sticky=W,pady=5)
        label_multicsvimport.grid(row=0,sticky=W)
        self.folder_csv.grid(row=0,sticky=W)
        button_import_csv.grid(row=1,sticky=W)
        label_singlecsvimport.grid(row=1,sticky=W)
        self.file_csv.grid(row=0,sticky=W)
        button_importsinglecsv.grid(row=1,sticky=W)


        label_extractframes.grid(row=6,sticky=W)
        label_note.grid(row=0,sticky=W)
        label_caution.grid(row=1,sticky=W)
        label_caution2.grid(row=2,sticky=W)
        button_extractframes.grid(row=3,sticky=W)

        projectconfig.update()

    def resetSettings(self):
        popup = Tk()
        popup.minsize(300, 100)
        popup.wm_title("Warning!")
        popupframe = LabelFrame(popup)
        label = Label(popupframe, text='Do you want to reset user-defined pose-configs?')
        label.grid(row=0,columnspan=2)
        B1 = Button(popupframe,text='Yes', command= lambda:reset_DiagramSettings(popup))
        B2 = Button(popupframe, text="No", command=popup.destroy)
        popupframe.grid(row=0,columnspan=2)
        B1.grid(row=1,column=0,sticky=W)
        B2.grid(row=1,column=1,sticky=W)

        popup.mainloop()


    def poseconfigSettings(self):
        # Popup window
        poseconfig = Toplevel()
        poseconfig.minsize(400, 400)
        poseconfig.wm_title("Pose Configuration")

        # define name for poseconfig settings
        self.configname = Entry_Box(poseconfig,'Pose config name','15')

        # no of animals
        self.noOfAnimals = Entry_Box(poseconfig,'# of Animals','15')

        # no of bodyparts
        self.noOfBp = Entry_Box(poseconfig,'# of Bodyparts','15')

        # path to image
        self.imgPath = FileSelect(poseconfig,'Image Path')

        # button for bodypart table
        tablebutton = Button(poseconfig,text='Confirm',command= lambda :self.bpTable(poseconfig))
        #button for saving poseconfig
        self.saveposeConfigbutton = Button(poseconfig,text='Save Pose Config',command=lambda:self.savePoseConfig(poseconfig))
        self.saveposeConfigbutton.config(state='disabled')

        #organize
        self.configname.grid(row=0,sticky=W)
        self.noOfAnimals.grid(row=1,sticky=W)
        self.noOfBp.grid(row=2,sticky=W)
        self.imgPath.grid(row=3,sticky=W,pady=2)
        tablebutton.grid(row=4,pady=5)
        self.saveposeConfigbutton.grid(row=6,pady=5)

    def savePoseConfig(self, master):
        configName = self.configname.entry_get
        noAnimals = self.noOfAnimals.entry_get
        noBps = self.noOfBp.entry_get
        Imagepath = self.imgPath.file_path
        BpNameList = []
        for i in self.bpnamelist:
            BpNameList.append(i.entry_get)
        define_new_pose_configuration(configName, noAnimals, noBps, Imagepath, BpNameList, noAnimals)
        master.destroy()
        self.toplevel.destroy()
        project_config()


    def bpTable(self,master):
        print(self.noOfBp.entry_get)
        noofbp = int(self.noOfBp.entry_get)
        self.bpnamelist = [0]*noofbp

        frame = LabelFrame(master,text='Bodyparts\' name')

        scroll = Scrollable(frame)

        frame.grid(row=5,sticky=W)
        for i in range(noofbp):
            self.bpnamelist[i] = Entry_Box(scroll,str(i+1),'2')
            self.bpnamelist[i].grid(row=i)

        self.saveposeConfigbutton.config(state='normal')

        scroll.update()

    def change_image(self,*args):
        if (self.var.get() != 'Create pose config...'):
            self.label.config(image=self.photos[self.option_mice.index(str(self.var.get()))])
        else:
            self.poseconfigSettings()

    def import_singlecsv(self):
        try:
            copy_singlecsv_ini(self.configinifile, self.file_csv.file_path)
        except:
            print('Please select csv file to proceed')

    def import_multicsv(self):
        try:
            copy_allcsv_ini(self.configinifile, self.folder_csv.folder_path)
        except:
            print('Please select folder with csv to proceed')

    def import_multivid(self):

        try:
            copy_multivideo_ini(self.configinifile, self.multivideofolderpath.folder_path, self.video_type.entry_get)
        except:
            print('Please select a folder containing the videos and enter the correct video format to proceed')

    def import_singlevid(self):
        try:
            copy_singlevideo_ini(self.configinifile, self.singlevideopath.file_path)
        except:
            print('Please select a video to proceed')

    def addBox(self,scroll):

        frame = Frame(self.label_smlsettings)
        frame.grid()

        # I use len(all_entries) to get nuber of next free column
        next_column = len(self.all_entries)

        # add label in first row
        lab = Label(frame, text=str('Classifier ') + str(next_column + 1))
        lab.grid(row=0, column=0,sticky=W)

        ent1 = Entry(frame)
        ent1.grid(row=0, column=1,sticky=W)
        self.all_entries.append(ent1)
        scroll.update()

    def setFilepath(self):
        file_selected = askopenfilename()
        self.modelPath.set(file_selected)

    def make_projectini(self):
        #get input from user
        #general settings input

        project_path = self.directory1Select.folder_path
        project_name = self.label_project_name.entry_get

        msconfig= str('yes')

        #sml settings
        no_targets = self.label_notarget.entry_get
        target_list = []
        for number, ent1 in enumerate(self.all_entries):
            target_list.append(ent1.get())

        ### animal settings
        listindex = self.option_mice.index(str(self.var.get()))

        if listindex == 0:
            bp = '4'
        elif listindex == 1:
            bp = '7'
        elif listindex == 2:
            bp = '8'
        elif listindex == 3:
            bp = '9'
        elif listindex == 4:
            bp = '8'
        elif listindex == 5:
            bp='14'
        elif listindex == 6:
            bp = '16'
        elif listindex == 7:
            bp = '987'
        else:
            bp = 'user_defined'

        noAnimalsPath = os.path.join(os.getcwd(), 'pose_configurations', 'no_animals', 'no_animals.csv')
        with open(noAnimalsPath, "r", encoding='utf8') as f:
            cr = csv.reader(f, delimiter=",")  # , is default
            rows = list(cr)  # create a list of rows for instance
        animalNo = str(rows[listindex])
        self.configinifile = write_inifile(msconfig,project_path,project_name,no_targets,target_list,bp, listindex, animalNo)
        #print(self.configinifile)
        print(os.path.basename(project_path))
        print('Project ' + '"' + str(project_name) + '"' + " created in folder " + '"' + str(os.path.basename(project_path)) + '"')
        # except:
        #     print('Please fill in the information correctly.')


    def extract_frames(self):
        try:
            videopath = str(os.path.dirname(self.configinifile) + '\\videos')

            extract_frames_ini(videopath)
        except:
            print('Please make sure videos are imported and located in /project_folder/videos')

class loadprojectMenu:
    def __init__(self,inputcommand):
        lpMenu = Toplevel()
        lpMenu.minsize(300, 200)
        lpMenu.wm_title("Load Project .ini file")

        # load project ini
        label_loadprojectini = LabelFrame(lpMenu, text='Load Project .ini', font=("Helvetica", 12, 'bold'), pady=5,
                                          padx=5, fg='black')
        self.projectconfigini = FileSelect(label_loadprojectini,'File Select:', title='Select config.ini file')

        #button
        launchloadprojectButton = Button(lpMenu,text='Load Project',command=lambda:self.launch(lpMenu,inputcommand))

        #organize
        label_loadprojectini.grid(row=0)
        self.projectconfigini.grid(row=0,sticky=W)
        launchloadprojectButton.grid(row=1,pady=10)

    def launch(self,master,command):
        if (self.projectconfigini.file_path.endswith('.ini')):
            master.destroy()
            print(self.projectconfigini.file_path)
            command(self.projectconfigini.file_path)
        else:
            print('Please select the project_config.ini file')

class loadprojectini:
    def __init__(self,configini):
        ##
        self.projectconfigini = configini
        simongui = Toplevel()
        simongui.minsize(1100, 450)
        simongui.wm_title("Load project")
        simongui.columnconfigure(0, weight=1)
        simongui.rowconfigure(0, weight=1)

        scroll = Scrollable(simongui)
        tab_parent = ttk.Notebook(scroll)

        tab2 = ttk.Frame(tab_parent)
        tab3 = ttk.Frame(tab_parent)
        tab4 = ttk.Frame(tab_parent)
        tab5 = ttk.Frame(tab_parent)
        tab6 = ttk.Frame(tab_parent)
        tab7 = ttk.Frame(tab_parent)
        tab8 = ttk.Frame(tab_parent)
        tab9 = ttk.Frame(tab_parent)
        tab10 = ttk.Frame(tab_parent)
        tab11 = ttk.Frame(tab_parent)

        tab_parent.add(tab2, text= f"{'[ Further imports (data/video/frames) ]':20s}")
        tab_parent.add(tab3, text=f"{'[ Video parameters ]':20s}")
        tab_parent.add(tab4, text=f"{'[ Outlier correction ]':20s}")
        tab_parent.add(tab6, text=f"{'[ ROI ]':10s}")
        tab_parent.add(tab5, text=f"{'[ Extract features ]':20s}")
        tab_parent.add(tab7, text=f"{'[ Label behavior] ':20s}")
        tab_parent.add(tab8, text=f"{'[ Train machine model ]':20s}")
        tab_parent.add(tab9, text=f"{'[ Run machine model ]':20s}")
        tab_parent.add(tab10, text=f"{'[ Visualizations ]':20s}")
        tab_parent.add(tab11, text=f"{'[ Classifier validation ]':20s}")

        tab_parent.grid(row=0)
        tab_parent.enable_traversal()

        #label import
        label_import = LabelFrame(tab2)

        #import all csv file into project folder
        label_import_csv = LabelFrame(label_import, text='Import further DLC tracking data', font=("Helvetica",12,'bold'), pady=5, padx=5,fg='black')
        # multicsv
        label_multicsvimport = LabelFrame(label_import_csv, text='Import multiple csv files', pady=5, padx=5)
        self.folder_csv = FolderSelect(label_multicsvimport, 'Folder selected:',title='Select Folder with .csv(s)')
        button_import_csv = Button(label_multicsvimport, text='Import csv to project folder',command= self.importdlctracking_multi,fg='navy')
        # singlecsv
        label_singlecsvimport = LabelFrame(label_import_csv, text='Import single csv files', pady=5, padx=5)
        self.file_csv = FileSelect(label_singlecsvimport, 'File selected',title='Select a .csv file')
        button_importsinglecsv = Button(label_singlecsvimport, text='Import single csv to project folder',command= self.importdlctracking_single,fg='navy')

        #import videos
        label_importvideo = LabelFrame(label_import, text='Import further videos into project folder', font=("Helvetica",12,'bold'), padx=15,pady=5,fg='black')
        # multi video
        label_multivideoimport = LabelFrame(label_importvideo, text='Import multiple videos', pady=5, padx=5)
        self.multivideofolderpath = FolderSelect(label_multivideoimport, 'Folder path',title='Select Folder with videos')
        self.video_type = Entry_Box(label_multivideoimport, 'File format (i.e., mp4/avi):', '20')
        button_multivideoimport = Button(label_multivideoimport, text='Import multiple videos',command=self.importvideo_multi, fg='black')
        # singlevideo
        label_singlevideoimport = LabelFrame(label_importvideo, text='Import single video', pady=5, padx=5)
        self.singlevideopath = FileSelect(label_singlevideoimport, "Video Path",title='Select a video file')
        button_importsinglevideo = Button(label_singlevideoimport, text='Import a video',command= self.importvideo_single,fg='black')

        #extract frames in project folder
        label_extractframes = LabelFrame(label_import, text='Extract further frames into project folder', font=("Helvetica",12,'bold'), pady=5,padx=5,fg='black')
        button_extractframes = Button(label_extractframes, text='Extract frames', command=self.extract_frames_loadini)

        #import frames
        label_importframefolder = LabelFrame(label_import, text='Import frame folders', font=("Helvetica",12,'bold'), pady=5,padx=5,fg='black')
        self.frame_folder = FolderSelect(label_importframefolder,'Main frame directory',title='Select the main directory with frame folders')
        button_importframefolder = Button(label_importframefolder,text='Import frames',command = self.importframefolder )

        #get coordinates
        label_setscale = LabelFrame(tab3,text='Video parameters (fps, resolution, ppx/mm, etc.)', font=("Helvetica",12,'bold'), pady=5,padx=5,fg='black')
        self.distanceinmm = Entry_Box(label_setscale, 'Known distance (mm)', '18')
        button_setdistanceinmm = Button(label_setscale, text='Autopopulate table',command=lambda: self.set_distancemm(self.distanceinmm.entry_get))
        button_setscale = Button(label_setscale,text='Set video parameters',command=self.setvideoparameter)

        #ROI
        ### define roi
        self.roi_define = LabelFrame(tab6, text='Define ROI')
        ## rectangle
        self.rec_entry = Entry_Box(self.roi_define, "# of rectangles", "12")
        ## circle
        self.cir_entry = Entry_Box(self.roi_define, "# of circles", "12")
        # polygons
        self.pol_entry = Entry_Box(self.roi_define, "# of polygons", "12")
        # button
        showname = Button(self.roi_define, text="Show Shape Definitions Table", command= lambda:self.table(self.roi_define,self.rec_entry.entry_get,self.cir_entry.entry_get,self.pol_entry.entry_get))

        # organize
        self.roi_define.grid(row=0, sticky=W)
        self.rec_entry.grid(row=1, sticky=W)
        self.cir_entry.grid(row=2, sticky=W)
        self.pol_entry.grid(row=3, sticky=W)
        showname.grid(row=4,pady=10)
        #load roi
        self.loadroi =  LabelFrame(tab6,text='Load ROI')
        self.getentrybutton = Button(self.loadroi, text="Load defined ROI table", command=self.loaddefinedroi)
        #organize
        self.loadroi.grid(row=0,column=1,sticky=N)
        self.getentrybutton.grid(row=0)

        ###analyze roi
        self.roi_draw = LabelFrame(tab6, text='Analyze ROI')
        # button
        analyzeROI = Button(self.roi_draw, text='Analyze ROI data',command= lambda:self.roi_settings('Analyze ROI Data','not append'))

        ##organize
        self.roi_draw.grid(row=0, column=2, sticky=N)
        analyzeROI.grid(row=0)

        ###plot roi
        self.roi_draw1 = LabelFrame(tab6, text='Visualize ROI')
        # button
        visualizeROI = Button(self.roi_draw1, text='Visualize ROI tracking', command=lambda: roiPlot(self.projectconfigini))
        ##organize
        self.roi_draw1.grid(row=0, column=3, sticky=N)
        visualizeROI.grid(row=0)

        #processmovementinroi (duplicate)
        processmovementdupLabel = LabelFrame(tab6,text='Analyze distances/velocity')
        button_process_movement1 = Button(processmovementdupLabel, text='Analyze distances/velocity',
                                         command=lambda: self.roi_settings('Analyze distances/velocity',
                                                                           'processmovement'))
        #organize
        processmovementdupLabel.grid(row=0,column=4,sticky=N)
        button_process_movement1.grid(row=0)


        #outlier correction
        label_outliercorrection = LabelFrame(tab4,text='Outlier correction',font=("Helvetica",12,'bold'),pady=5,padx=5,fg='black')
        label_link = Label(label_outliercorrection,text='[link to description]',cursor='hand2',font='Verdana 10 underline')
        button_settings_outlier = Button(label_outliercorrection,text='Settings',command = lambda: outlier_settings(self.projectconfigini))
        button_outliercorrection = Button(label_outliercorrection,text='Run outlier correction',command=self.correct_outlier)

        label_link.bind("<Button-1>",lambda e: self.callback('https://github.com/sgoldenlab/simba/blob/master/misc/Outlier_settings.pdf'))

        #extract features
        label_extractfeatures = LabelFrame(tab5,text='Extract Features',font=("Helvetica",12,'bold'),pady=5,padx=5,fg='black')
        button_extractfeatures = Button(label_extractfeatures,text='Extract Features',command = lambda: threading.Thread(target=self.extractfeatures).start())
        #roiappend
        appendDf = Button(label_extractfeatures, text='Append ROI data to features', command=self.appendroisettings)
        appendDf.grid(row=1,pady=10)

        #label Behavior
        label_labelaggression = LabelFrame(tab7,text='Label Behavior',font=("Helvetica",12,'bold'),pady=5,padx=5,fg='black')
        button_labelaggression = Button(label_labelaggression, text='Select folder with frames',command= lambda:choose_folder(self.projectconfigini))

        #train machine model
        label_trainmachinemodel = LabelFrame(tab8,text='Train Machine Models',font=("Helvetica",12,'bold'),padx=5,pady=5,fg='black')
        button_trainmachinesettings = Button(label_trainmachinemodel,text='Settings',command=self.trainmachinemodelsetting)
        button_trainmachinemodel = Button(label_trainmachinemodel,text='Train single model from global environment',fg='blue',command = lambda: threading.Thread(target=self.trainsinglemodel).start())
        button_train_multimodel = Button(label_trainmachinemodel, text='Train multiple models, one for each saved settings',fg='green',command = lambda: threading.Thread(target=self.trainmultimodel).start())

        ##Single classifier valid
        label_model_validation = LabelFrame(tab9, text='Validate Model on Single Video', pady=5, padx=5,
                                            font=("Helvetica", 12, 'bold'), fg='black')
        self.csvfile = FileSelect(label_model_validation, 'Select features file',
                                  title='Select .csv file in /project_folder/csv/features_extracted')
        self.modelfile = FileSelect(label_model_validation, 'Select model file  ', title='Select the model (.sav) file')
        button_runvalidmodel = Button(label_model_validation, text='Run Model',
                                      command=lambda: validate_model_one_vid_1stStep(self.projectconfigini,
                                                                                     self.csvfile.file_path,
                                                                                     self.modelfile.file_path))
        button_generateplot = Button(label_model_validation, text="Generate plot", command=self.updateThreshold)
        self.dis_threshold = Entry_Box(label_model_validation, 'Discrimination threshold', '28')
        self.min_behaviorbout = Entry_Box(label_model_validation, 'Minimum behavior bout length (ms)', '28')
        self.ganttvar = IntVar()
        self.generategantt = Checkbutton(label_model_validation,text='Generate Gantt plot',variable=self.ganttvar)
        button_validate_model = Button(label_model_validation, text='Validate', command=self.validatemodelsinglevid)

        #run machine model
        label_runmachinemodel = LabelFrame(tab9,text='Run Machine Model',font=("Helvetica",12,'bold'),padx=5,pady=5,fg='black')
        button_run_rfmodelsettings = Button(label_runmachinemodel,text='Model Settings',command=self.modelselection)
        # self.descrimination_threshold = Entry_Box(label_runmachinemodel,'Discrimination threshold','28')
        # self.shortest_bout = Entry_Box(label_runmachinemodel,'Minimum behavior bout length (ms)','28')
        button_runmachinemodel = Button(label_runmachinemodel,text='Run RF Model',command=self.runrfmodel)

        # machine results
        label_machineresults = LabelFrame(tab9,text='Analyze Machine Results',font=("Helvetica",12,'bold'),padx=5,pady=5,fg='black')
        button_process_datalog = Button(label_machineresults,text='Analyze machine predictions',command =self.analyzedatalog)
        button_process_movement = Button(label_machineresults,text='Analyze distances/velocity',command=lambda:self.roi_settings('Analyze distances/velocity','processmovement'))
        self.severityscale = Entry_Box(label_machineresults,'Severity scale 0 -',15)
        button_process_severity = Button(label_machineresults,text='Analyze attack severity',command=self.analyzseverity)

        #plot sklearn res
        label_plotsklearnr = LabelFrame(tab10,text='Sklearn visualization',font=("Helvetica",12,'bold'),pady=5,padx=5,fg='black')
        self.videovar = IntVar()
        self.genframevar = IntVar()
        videocheck = Checkbutton(label_plotsklearnr,text='Generate video',variable=self.videovar)
        framecheck = Checkbutton(label_plotsklearnr,text='Generate frame',variable=self.genframevar)
        button_plotsklearnr = Button(label_plotsklearnr,text='Visualize classification results',command =self.plotsklearn_result)

        #plotpathing
        label_plotall = LabelFrame(tab10,text='Visualizations',font=("Helvetica",12,'bold'),pady=5,padx=5,fg='black')
        #ganttplot
        label_ganttplot = LabelFrame(label_plotall,text='Gantt plot',pady=5,padx=5)
        button_ganttplot = Button(label_ganttplot,text='Generate gantt plot',command=self.plotgantt)
        #dataplot
        label_dataplot = LabelFrame(label_plotall,text='Data plot',pady=5,padx=5)
        button_dataplot = Button(label_dataplot,text='Generate data plot',command=self.plotdataplot)
        #path plot
        label_pathplot = LabelFrame(label_plotall,text='Path plot',pady=5,padx=5)
        self.Deque_points = Entry_Box(label_pathplot,'Max lines','15')
        self.severity_brackets = Entry_Box(label_pathplot,'Severity Scale: 0 - ','15')
        self.Bodyparts = Entry_Box(label_pathplot, 'Bodyparts', '15')
        self.plotsvvar = IntVar()
        checkboxplotseverity = Checkbutton(label_pathplot,text='plot_severity',variable=self.plotsvvar)
        button_pathplot = Button(label_pathplot,text='Generate Path plot',command=self.pathplotcommand)

        CreateToolTip(self.Deque_points,'Maximum number of path lines in deque list')
        CreateToolTip(self.Bodyparts, 'If golden aggression config: Nose, Left ear, Right ear, Centroid, Left lateral, Right lateral, Tail base, Tail end')
        CreateToolTip(self.severity_brackets,'Set number of brackets to severity measures')

        #distanceplot
        label_distanceplot = LabelFrame(label_plotall,text='Distance plot',pady=5,padx=5)
        self.poi1 = Entry_Box(label_distanceplot, 'Body part 1', '15')
        self.poi2 =Entry_Box(label_distanceplot, 'Body part 2', '15')
        button_distanceplot= Button(label_distanceplot,text='Generate Distance plot',command=self.distanceplotcommand)

        CreateToolTip(self.poi1,'The bodyparts from config yaml. eg: Ear_left_1,Ear_right_1,Nose_1,Center_1,Lateral_left_1,Lateral_right_1,Tail_base_1,Tail_end_1,Ear_left_2,Ear_right_2,Nose_2,Center_2,Lateral_left_2,Lateral_right_2,Tail_base_2,Tail_end_2')

        #Heatplot
        label_heatmap = LabelFrame(label_plotall, text='Heatmap', pady=5, padx=5)
        self.BinSize = Entry_Box(label_heatmap, 'Bin size (px)', '15')
        self.MaxScale = Entry_Box(label_heatmap, '# Scale increments', '15')
        self.Inc = Entry_Box(label_heatmap, 'Scale increment (s)', '15')

        hmchoices = {'viridis','plasma','inferno','magma','jet','gnuplot2'}
        self.hmMenu = DropDownMenu(label_heatmap,'Color Palette',hmchoices,'15')
        self.hmMenu.setChoices('jet')
        # get target
        config = ConfigParser()
        configFile = str(self.projectconfigini)
        config.read(configFile)
        notarget = config.getint('SML settings','no_targets')
        targetlist = {}
        for i in range(notarget):
            targetlist[(config.get('SML settings','target_name_'+str(i+1)))]=(config.get('SML settings','target_name_'+str(i+1)))
        self.targetMenu = DropDownMenu(label_heatmap,'Target',targetlist,'15')
        self.targetMenu.setChoices(targetlist[(config.get('SML settings','target_name_'+str(1)))])

        button_heatmap = Button(label_heatmap, text='Generate heatmap', command=self.heatmapcommand)

        #plot threshold
        label_plotThreshold = LabelFrame(label_plotall,text='Plot Threshold',pady=5,padx=5)
        self.behaviorMenu = DropDownMenu(label_plotThreshold,'Target',targetlist,'15')
        self.behaviorMenu.setChoices(targetlist[(config.get('SML settings','target_name_'+str(1)))])
        plotThresholdButton = Button(label_plotThreshold,text='Plot threshold',command=lambda:plot_threshold(self.projectconfigini,self.behaviorMenu.getChoices()))


        #Merge frames
        label_mergeframes = LabelFrame(tab10,text='Merge frames',pady=5,padx=5,font=("Helvetica",12,'bold'),fg='black')
        button_mergeframe = Button(label_mergeframes,text='Merge frames',command=self.mergeframesofplot)

        #create video
        label_createvideo = LabelFrame(tab10, text='Create Video', pady=5, padx=5,font=("Helvetica",12,'bold'),fg='black')
        self.bitrate = Entry_Box(label_createvideo,'Bitrate',8)
        self.fileformt = Entry_Box(label_createvideo,'File format',8)
        button_createvideo = Button(label_createvideo, text='Create Video',command=self.generate_video)

        ## classifier validation
        label_classifier_validation = LabelFrame(tab11, text='Classifier Validation', pady=5, padx=5,font=("Helvetica",12,'bold'),fg='black')
        self.seconds = Entry_Box(label_classifier_validation,'Seconds','8')
        self.cvTarget = DropDownMenu(label_classifier_validation,'Target',targetlist,'15')
        self.cvTarget.setChoices(targetlist[(config.get('SML settings', 'target_name_' + str(1)))])
        button_validate_classifier = Button(label_classifier_validation,text='Validate',command =self.classifiervalidation)


        #organize
        label_import.grid(row=0,column=0,sticky=W,pady=5)
        label_import_csv.grid(row=0, sticky=N+W, pady=5)
        label_multicsvimport.grid(row=0, sticky=W)
        self.folder_csv.grid(row=0, sticky=W)
        button_import_csv.grid(row=1, sticky=W)
        label_singlecsvimport.grid(row=1, sticky=W)
        self.file_csv.grid(row=0, sticky=W)
        button_importsinglecsv.grid(row=1, sticky=W)

        label_importvideo.grid(row=1,column=0, sticky=N+W, pady=5,padx=5)
        label_multivideoimport.grid(row=0, sticky=W)
        self.multivideofolderpath.grid(row=0, sticky=W)
        self.video_type.grid(row=1, sticky=W)
        button_multivideoimport.grid(row=2, sticky=W)
        label_singlevideoimport.grid(row=1, sticky=W)
        self.singlevideopath.grid(row=0, sticky=W)
        button_importsinglevideo.grid(row=1, sticky=W)

        label_extractframes.grid(row=0,column=1,sticky=N+W,pady=5,padx=5)
        button_extractframes.grid(row=0,sticky=W)

        label_importframefolder.grid(row=1,column=1,sticky=N+W,pady=5,padx=5)
        self.frame_folder.grid(row=0,sticky=W)
        button_importframefolder.grid(row=1,sticky=W)

        label_setscale.grid(row=2,sticky=W,pady=5,padx=5)
        self.distanceinmm.grid(row=0,column=0,sticky=W)
        button_setdistanceinmm.grid(row=0,column=1)
        button_setscale.grid(row=1,column=0,sticky=W)

        label_outliercorrection.grid(row=0,sticky=W)
        label_link.grid(row=0,sticky=W)
        button_settings_outlier.grid(row=1,sticky=W)
        button_outliercorrection.grid(row=3,sticky=W)

        label_extractfeatures.grid(row=4,sticky=W)
        button_extractfeatures.grid(row=0,sticky=W)

        label_labelaggression.grid(row=5,sticky=W)
        button_labelaggression.grid(row=0,sticky=W)

        label_trainmachinemodel.grid(row=6,sticky=W)
        button_trainmachinesettings.grid(row=0,column=0,sticky=W,padx=5)
        button_trainmachinemodel.grid(row=0,column=1,sticky=W,padx=5)
        button_train_multimodel.grid(row=0,column=2,sticky=W,padx=5)

        label_model_validation.grid(row=7, sticky=W, pady=5)
        self.csvfile.grid(row=0, sticky=W)
        self.modelfile.grid(row=1, sticky=W)
        button_runvalidmodel.grid(row=2, sticky=W)
        button_generateplot.grid(row=3, sticky=W)
        self.dis_threshold.grid(row=4, sticky=W)
        self.min_behaviorbout.grid(row=5, sticky=W)
        self.generategantt.grid(row=6,sticky=W)
        button_validate_model.grid(row=7, sticky=W)

        label_runmachinemodel.grid(row=8,sticky=W,pady=5)
        button_run_rfmodelsettings.grid(row=0,sticky=W)
        # self.descrimination_threshold.grid(row=1,sticky=W)
        # button_set_d_t.grid(row=1,column=1,sticky=W)
        # self.shortest_bout.grid(row=2,column=0,sticky=W)
        # button_set_shortbout.grid(row=2,column=1,sticky=W)
        button_runmachinemodel.grid(row=3,sticky=W,pady=5)

        label_machineresults.grid(row=9,sticky=W,pady=5)
        button_process_datalog.grid(row=1,column=0,sticky=W,padx=3)
        button_process_movement.grid(row=1,column=1,sticky=W,padx=3)
        self.severityscale.grid(row=0,column=2,sticky=W)
        button_process_severity.grid(row=1,column=2,sticky=W,padx=3)

        label_plotsklearnr.grid(row=10,column=0,sticky=W+N,padx=5)
        videocheck.grid(row=0,sticky=W)
        framecheck.grid(row=1,sticky=W)
        button_plotsklearnr.grid(row=2,sticky=W)

        label_plotall.grid(row=10,column=1,sticky=W+N,padx=5)
        #gantt
        label_ganttplot.grid(row=0,sticky=W)
        button_ganttplot.grid(row=0,sticky=W)
        #data
        label_dataplot.grid(row=1,sticky=W)
        button_dataplot.grid(row=0,sticky=W)
        #path
        label_pathplot.grid(row=2,sticky=W)
        self.Deque_points.grid(row=0,sticky=W)
        self.severity_brackets.grid(row=2,sticky=W)
        self.Bodyparts.grid(row=3,sticky=W)
        checkboxplotseverity.grid(row=4,sticky=W)
        button_pathplot.grid(row=5,sticky=W)
        #distance
        label_distanceplot.grid(row=3,sticky=W)
        self.poi1.grid(row=1,sticky=W)
        self.poi2.grid(row=2,sticky=W)
        button_distanceplot.grid(row=3,sticky=W)
        #heat
        label_heatmap.grid(row=4, sticky=W)
        self.BinSize.grid(row=0, sticky=W)
        self.Inc.grid(row=2, sticky=W)
        self.MaxScale.grid(row=1, sticky=W)
        self.hmMenu.grid(row=3,sticky=W)
        self.targetMenu.grid(row=4,sticky=W)
        button_heatmap.grid(row=5, sticky=W)
        #threshold
        label_plotThreshold.grid(row=5, sticky=W)
        self.behaviorMenu.grid(row=0, sticky=W)
        self.behaviorMenu.grid(row=1, sticky=W)
        plotThresholdButton.grid(row=2, sticky=W)

        label_mergeframes.grid(row=10,column=2,sticky=W+N,padx=5)
        button_mergeframe.grid(row=0,sticky=W)

        label_createvideo.grid(row=10,column=3,sticky=W+N,padx=5)
        self.bitrate.grid(row=0,sticky=W)
        self.fileformt.grid(row=1,sticky=W)
        button_createvideo.grid(row=2,sticky=W)

        label_classifier_validation.grid(row=14,sticky=W)
        self.seconds.grid(row=0,sticky=W)
        self.cvTarget.grid(row=1,sticky=W)
        button_validate_classifier.grid(row=2,sticky=W)

        #scrollbar update
        scroll.update()

    def loaddefinedroi(self):

        h5dir = os.path.dirname(self.projectconfigini) + '\\logs\\measures'
        h5list = os.listdir(h5dir)
        result = [i for i in h5list if '.h5' in i]
        if result == []:
            print('Please define ROI Shapes')
        else:
            videodir = os.path.join(os.path.dirname(self.projectconfigini), 'videos')

            roitableMenu(videodir, self.projectconfigini)


    def appendroisettings(self):
        apdroisettings = Toplevel()
        apdroisettings.minsize(400, 400)
        apdroisettings.wm_title("Append Roi Settings")

        # first choice frame
        firstMenu = LabelFrame(apdroisettings, text='Select number of animals')

        ## set up drop down for animals
        noOfAnimalVar = IntVar()
        animalOptions = {1, 2}
        noOfAnimalVar.set(1)

        animalMenu = OptionMenu(firstMenu, noOfAnimalVar, *animalOptions)
        animalLabel = Label(firstMenu, text="# of animals")
        setAnimalButton = Button(firstMenu, text="Confirm",
                                 command=lambda: self.run_roiAnalysisSettings(apdroisettings, noOfAnimalVar,'append'))

        # organize
        firstMenu.grid(row=0, sticky=W)
        animalLabel.grid(row=0, column=0, sticky=W)
        animalMenu.grid(row=0, column=1, sticky=W)
        setAnimalButton.grid(row=0, column=2, sticky=W)

    def roi_settings(self,title,selection):

        roisettings = Toplevel()
        roisettings.minsize(400, 400)
        roisettings.wm_title(title)

        #first choice frame
        firstMenu = LabelFrame(roisettings,text='Select number of animals')

        ## set up drop down for animals
        noOfAnimalVar = IntVar()
        animalOptions = {1,2}
        noOfAnimalVar.set(1)

        animalMenu = OptionMenu(firstMenu,noOfAnimalVar,*animalOptions)
        animalLabel = Label(firstMenu,text="# of animals")

        setAnimalButton = Button(firstMenu,text="Confirm",command=lambda:self.run_roiAnalysisSettings(roisettings,noOfAnimalVar,selection))


        #organize
        firstMenu.grid(row=0,sticky=W)
        animalLabel.grid(row=0,column=0,sticky=W)
        animalMenu.grid(row=0,column=1,sticky=W)
        setAnimalButton.grid(row=0,column=2,sticky=W)

    def run_roiAnalysisSettings(self,master,noofanimal,appendornot):
        try:
            self.secondMenu.destroy()
        except:
            pass

        self.secondMenu = LabelFrame(master,text="Choose bodyparts")
        runButton = Button(self.secondMenu,text='Run',command =lambda:self.run_analyze_roi(noofanimal.get(),animalbody1var.get(),animalbody2var.get(),appendornot))
        ## 1 animal
        animal1 = LabelFrame(self.secondMenu,text='Animal 1')
        animalbody1 = Label(animal1,text='Bodypart')
        animalbody1var = StringVar()
        configini = self.projectconfigini
        options, options2 = define_bp_drop_down(configini)
        animalbody1var.set(options[0])
        animalbodymenu1 = OptionMenu(animal1, animalbody1var, *options)

        ## 2 animals
        animal2 = LabelFrame(self.secondMenu, text='Animal 2')
        animalbody2 = Label(animal2, text='Bodypart')
        animalbody2var = StringVar()
        animalbody2var.set(options2[0])
        animalbodymenu2 = OptionMenu(animal2,animalbody2var,*options2)

        #organize
        self.secondMenu.grid(row=1, sticky=W)
        runButton.grid(row=3,padx=10,pady=10)
        if noofanimal.get()==1:
            animal1.grid(row=0,column=0,sticky=W)
            animalbody1.grid(row=0,column=0,sticky=W)
            animalbodymenu1.grid(row=0,column=1,sticky=W)
        elif noofanimal.get()==2:
            animal1.grid(row=0, column=0, sticky=W)
            animalbody1.grid(row=0, column=0, sticky=W)
            animalbodymenu1.grid(row=0, column=1, sticky=W)

            animal2.grid(row=0, column=1, sticky=W)
            animalbody2.grid(row=0, column=0, sticky=W)
            animalbodymenu2.grid(row=0, column=1, sticky=W)

    def run_analyze_roi(self,noofanimal,animal1bp,animal2bp,appendornot):
        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)

        if appendornot == 'processmovement':
            config.set('process movements', 'no_of_animals', str(noofanimal))
            config.set('process movements', 'animal_1_bp', str(animal1bp))
            config.set('process movements', 'animal_2_bp', str(animal2bp))
            with open(configini, 'w') as configfile:
                config.write(configfile)
        else:
            config.set('ROI settings', 'no_of_animals', str(noofanimal))
            config.set('ROI settings', 'animal_1_bp', str(animal1bp))
            config.set('ROI settings', 'animal_2_bp', str(animal2bp))
            with open(configini, 'w') as configfile:
                config.write(configfile)

        if appendornot == 'append':
            ROItoFeatures(configini)
        elif appendornot =='not append':
            roiAnalysis(configini,'outlier_corrected_movement_location')
        elif appendornot == 'processmovement':
            ROI_process_movement(configini)
        else:
            roiAnalysis(configini,'features_extracted')

    def updateThreshold(self):
        updateThreshold_graph(self.projectconfigini, self.csvfile.file_path, self.modelfile.file_path)

    def getEntry(self):
        # rectangle
        recName = []
        recWidth = []
        recHeight = []
        rec_shape = []
        try:
            for i in range(len(self.rect_list)):
                rec_shape.append("Rectangle")
                recName.append(self.rect_list[i].get())
                recWidth.append(int(self.rec_width_list[i].get()))
                recHeight.append(int(self.rec_height_list[i].get()))

            rec_df = pd.DataFrame(list(zip(rec_shape, recName, recWidth, recHeight)), columns=['Shape_type', 'Name', 'width', 'height'])

        except:
            rec_df = pd.DataFrame()

        # circle
        cirName = []
        cirRadius = []
        cir_shape = []
        try:
            for i in range(len(self.cir_entry_list)):
                cir_shape.append("Circle")
                cirName.append(self.cir_entry_list[i].get())
                cirRadius.append(int(self.cir_radius_list[i].get()))
            cir_df = pd.DataFrame(list(zip(cir_shape, cirName, cirRadius)), columns=['Shape_type', 'Name', 'Radius'])
        except:
            cir_df = pd.DataFrame()

        ## polygon
        polName = []
        polShape = []

        try:
            for i in range(len(self.pol_list)):
                polShape.append("Polygon")
                polName.append(self.pol_list[i].get())
            pol_df = pd.DataFrame(list(zip(polShape, polName)), columns=['Shape_type', 'Name'])
        except:
            pol_df = pd.DataFrame()

        if not os.path.exists(os.path.join(os.path.dirname(self.projectconfigini),"logs","measures")):
            os.makedirs(os.path.join(os.path.dirname(self.projectconfigini),"logs","measures"))

        ### to h5
        storePath = os.path.join(os.path.dirname(self.projectconfigini),"logs","measures",'ROI_index.h5')
        store = pd.HDFStore(storePath, mode='w')
        store['rectangles'] = rec_df
        store['circleDf'] = cir_df
        store['polygons'] = pol_df
        store.close()

        videodir = os.path.join(os.path.dirname(self.projectconfigini),'videos')

        roitableMenu(videodir,self.projectconfigini)

    def table(self,master,rectangle,circle,polygon):
        # refresh the frames
        try:
            self.rectbox.destroy()
            self.cirbox.destroy()
            self.polbox.destroy()
        except:
            pass

        try:
            ## make rectangle table
            self.rectbox = LabelFrame(master)
            self.rectbox.grid(row=6, sticky=W, pady=10)
            self.rect_list = list(range(int(rectangle)))
            self.rec_width_list = list(range(int(rectangle)))
            self.rec_height_list = list(range(int(rectangle)))
            rect_var = list(range(int(rectangle)))
            rec_name_list = list(range(int(rectangle)))

            #
            rectangleName = Label(self.rectbox, text="Rectangle Name")
            rectangleName.grid(row=0, column=1)

            rectangleWidth = Label(self.rectbox, text="Width")
            rectangleWidth.grid(row=0, column=2)

            rectangleHeight = Label(self.rectbox, text="Height")
            rectangleHeight.grid(row=0, column=3)

            for i in range(len(self.rect_list)):
                rec_name_list[i] = Label(self.rectbox, text="Rect_" + str(i + 1))
                rec_name_list[i].grid(row=int(i) + 1, padx=5, sticky=W)
                self.rect_list[i] = Entry(self.rectbox)
                self.rect_list[i].grid(row=int(i) + 1, column=1, padx=5)
                rect_var[i]=StringVar()
                self.rec_width_list[i] = Entry(self.rectbox,textvariable=rect_var[i])

                self.rec_width_list[i].grid(row=int(i) + 1, column=2, padx=5)
                self.rec_height_list[i] = Entry(self.rectbox,textvariable=rect_var[i])
                self.rec_height_list[i].grid(row=int(i) + 1, column=3, padx=5)

                rect_var[i].set('0')
        except:
            pass

        try:
            ## make circle table
            self.cirbox = LabelFrame(master)
            self.cirbox.grid(row=7, sticky=W)
            cir_list = list(range(int(circle)))
            self.cir_entry_list = list(range(int(circle)))
            self.cir_radius_list = list(range(int(circle)))
            cir_var = list(range(int(circle)))

            circleName = Label(self.cirbox, text="Circle Name")
            circleName.grid(row=0, column=1)

            radiusName = Label(self.cirbox, text='Radius')
            radiusName.grid(row=0, column=2)

            for i in range(len(cir_list)):
                cir_list[i] = Label(self.cirbox, text=("Cir_" + str(i + 1)))
                cir_list[i].grid(row=int(i) + 1, padx=5, sticky=W)
                self.cir_entry_list[i] = Entry(self.cirbox)
                self.cir_entry_list[i].grid(row=int(i) + 1, column=1, padx=5)
                cir_var[i] =  StringVar()
                self.cir_radius_list[i] = Entry(self.cirbox,textvariable=cir_var[i])
                self.cir_radius_list[i].grid(row=int(i) + 1, column=2, padx=5)
                cir_var[i].set('0')
        except:
            pass

        try:
            ## make polygon table/.;p
            self.polbox = LabelFrame(master)
            self.polbox.grid(row=8, sticky=W)
            self.pol_list = list(range(int(polygon)))
            pol_name = list(range(int(polygon)))
            polygonName = Label(self.polbox, text="Polygon Name")
            polygonName.grid(row=0, column=1)
            for i in range(len(pol_name)):
                pol_name[i] = Label(self.polbox, text="Pol_" + str(i + 1))
                pol_name[i].grid(row=int(i) + 1, column=0, sticky=W)
                self.pol_list[i] = Entry(self.polbox)
                self.pol_list[i].grid(row=int(i) + 1, column=1, padx=5)
        except:
            pass


        setbutton = Button(master,text='Set Shape Definitions',command=self.setvariables)
        setbutton.grid(row=10)

    def setvariables(self):
        measuresdir = os.path.join(os.path.dirname(self.projectconfigini),'logs','measures')
        try:
            os.remove(os.path.join(measuresdir,'ROI_definitions.h5'))
            os.remove(os.path.join(measuresdir, 'ROI_index.h5'))
        except:
            pass

        self.getEntry()

    def classifiervalidation(self):
        print('Generating video...')
        validate_classifier(self.projectconfigini, self.seconds.entry_get,self.cvTarget.getChoices())
        print('Videos generated')

    def mergeframesofplot(self):
        merge_frames_config(self.projectconfigini)

    def plotdataplot(self):
        data_plot_config(self.projectconfigini)

    def plotgantt(self):
        ganntplot_config(self.projectconfigini)

    def plotsklearn_result(self):
        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)
        plotsklearnresult(self.projectconfigini,self.videovar.get(),self.genframevar.get())

    def analyzseverity(self):
        analyze_process_severity(self.projectconfigini,self.severityscale.entry_get)

    def analyzedatalog(self):
        # Popup window
        datalogmenu = Toplevel()
        datalogmenu.minsize(400, 400)
        datalogmenu.wm_title("Analyze process log settings")

        dlmlabel = LabelFrame(datalogmenu)

        #use for loop to create intvar
        var=[]
        for i in range(7):
            var.append(IntVar())

        #use loop to create checkbox?
        checkbox = [0]*7
        titlebox =['events','sum duration (s)','mean duration (s)','median duration (s)','first occurance (s)','mean interval (s)','median interval (s)']
        for i in range(7):
            checkbox[i] = Checkbutton(dlmlabel,text=titlebox[i],variable=var[i])
            checkbox[i].grid(row=i,sticky=W)
        #organize
        dlmlabel.grid(row=0)
        button1 = Button(dlmlabel,text='Analyze',command=lambda:self.findDatalogList(titlebox,var))
        button1.grid(row=10)

    def findDatalogList(self,titleBox,Var):
        finallist = []
        for index,i in enumerate(Var):
            if i.get()==0:
                finallist.append(titleBox[index])

        #run analyze
        analyze_process_data_log(self.projectconfigini,finallist)


    def runrfmodel(self):
        rfmodel(self.projectconfigini)

    def modelselection(self):
        runmachinemodelsettings(self.projectconfigini)

    def validatemodelsinglevid(self):
        validate_model_one_vid(self.projectconfigini, self.csvfile.file_path, self.modelfile.file_path,
                                   self.dis_threshold.entry_get, self.min_behaviorbout.entry_get,self.ganttvar.get())

    def trainmultimodel(self):
        train_multimodel(self.projectconfigini)

    def trainsinglemodel(self):
        trainmodel2(self.projectconfigini)

    def trainmachinemodelsetting(self):
        trainmachinemodel_settings(self.projectconfigini)

    def extractfeatures(self):
        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)
        pose_estimation_body_parts = config.get('create ensemble settings', 'pose_estimation_body_parts')
        print('Pose-estimation body part setting for feature extraction: ' + str(pose_estimation_body_parts))

        if pose_estimation_body_parts == '16':
            extract_features_wotarget_16(self.projectconfigini)
        if (pose_estimation_body_parts == '14'):
            extract_features_wotarget_14(self.projectconfigini)
        if (pose_estimation_body_parts == '987'):
            extract_features_wotarget_14_from_16(self.projectconfigini)
        if pose_estimation_body_parts == '9':
            extract_features_wotarget_9(self.projectconfigini)
        if pose_estimation_body_parts == '8':
            extract_features_wotarget_8(self.projectconfigini)
        if pose_estimation_body_parts == '7':
            extract_features_wotarget_7(self.projectconfigini)
        if pose_estimation_body_parts == '4':
            extract_features_wotarget_4(self.projectconfigini)
        if pose_estimation_body_parts == 'user_defined':
            extract_features_wotarget_user_defined(self.projectconfigini)

    def setvideoparameter(self):
        video_info_table(self.projectconfigini)

    def importframefolder(self):
        if (self.projectconfigini!='No file selected') and (self.frame_folder.folder_path != 'No folder selected'):
            copy_frame_folders(self.frame_folder.folder_path, self.projectconfigini)
        else:
            print('Fail to import frame folder, please select a main directory containing all the frame folders')

    def importvideo_single(self):
        if (self.projectconfigini != 'No file selected') and (self.singlevideopath.file_path != 'No file selected'):
            copy_singlevideo_ini(self.projectconfigini, self.singlevideopath.file_path)
        else:
            print('Fail to import video, please select a video to import')

    def importvideo_multi(self):
        if (self.projectconfigini != 'No file selected') and (self.multivideofolderpath.folder_path != 'No folder selected') and (self.video_type.entry_get != ''):
            copy_multivideo_ini(self.projectconfigini, self.multivideofolderpath.folder_path,self.video_type.entry_get)
        else:
            print('Fail to import videos, please select folder with videos and enter the file format')

    def importdlctracking_single(self):
        if (self.projectconfigini != 'No file selected') and (self.file_csv.file_path != 'No file selected'):
            copy_singlecsv_ini(self.projectconfigini, self.file_csv.file_path)
        else:
            print('Fail to import csv file , please select a csv file to import and load config.ini file')

    def importdlctracking_multi(self):
        if (self.projectconfigini !='No file selected') and (self.folder_csv.folder_path!= 'No folder selected'):
            copy_allcsv_ini(self.projectconfigini, self.folder_csv.folder_path)
        else:
            print('Fail to import csv file, please select folder with the .csv files and load config.ini file')

    def set_distancemm(self, distancemm):

        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)

        config.set('Frame settings', 'distance_mm', distancemm)
        with open(configini, 'w') as configfile:
            config.write(configfile)

    def generate_video(self):

        print('Generating video...')
        configini = self.projectconfigini
        bitrate = self.bitrate.entry_get
        fileformat = '.'+ self.fileformt.entry_get

        config = ConfigParser()
        config.read(configini)

        config.set('Create movie settings', 'file_format', str(fileformat))
        config.set('Create movie settings', 'bitrate', str(bitrate))
        with open(configini, 'w') as configfile:
            config.write(configfile)

        generatevideo_config_ffmpeg(configini)
        print('Video generated.')


    def extract_frames_loadini(self):
        configini = self.projectconfigini
        videopath = str(os.path.dirname(configini) + '\\videos')

        extract_frames_ini(videopath)

    def correct_outlier(self):
        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)
        pose_estimation_body_parts = config.get('create ensemble settings', 'pose_estimation_body_parts')
        print('Pose-estimation body part setting for outlier correction: ' + str(pose_estimation_body_parts))
        if (pose_estimation_body_parts == '16') or (pose_estimation_body_parts == '987'):
            dev_move_16(configini)
            dev_loc_16(configini)
        if pose_estimation_body_parts == '14':
            dev_move_14(configini)
            dev_loc_14(configini)
        if (pose_estimation_body_parts == 'user_defined') or (pose_estimation_body_parts == '4') or (pose_estimation_body_parts == '7') or (pose_estimation_body_parts == '8') or (pose_estimation_body_parts == '9'):
            dev_move_user_defined(configini)
            dev_loc_user_defined(configini)
        print('Outlier correction complete.')

    def distanceplotcommand(self):
        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)

        config.set('Distance plot', 'POI_1', self.poi1.entry_get)
        config.set('Distance plot', 'POI_2', self.poi2.entry_get)
        with open(configini, 'w') as configfile:
            config.write(configfile)

        line_plot_config(configini)
        print('Distance plot complete.')

    def pathplotcommand(self):

        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)

        config.set('Path plot settings', 'deque_points', self.Deque_points.entry_get)
        config.set('Path plot settings', 'severity_brackets', self.severity_brackets.entry_get)
        config.set('Line plot settings', 'Bodyparts', self.Bodyparts.entry_get)

        if self.plotsvvar.get()==1:
            config.set('Path plot settings', 'plot_severity', 'yes')
        else:
            config.set('Path plot settings', 'plot_severity', 'no')

        with open(configini, 'w') as configfile:
            config.write(configfile)

        path_plot_config(configini)
        print('Path plot complete.')

    def heatmapcommand(self):
        configini = self.projectconfigini
        config = ConfigParser()
        config.read(configini)
        config.set('Heatmap settings', 'bin_size_pixels', self.BinSize.entry_get)
        config.set('Heatmap settings', 'Scale_max_seconds', self.MaxScale.entry_get)
        config.set('Heatmap settings', 'Scale_increments_seconds', self.Inc.entry_get)
        config.set('Heatmap settings', 'Palette', self.hmMenu.getChoices())
        config.set('Heatmap settings', 'Target', self.targetMenu.getChoices())
        with open(configini, 'w') as configfile:
            config.write(configfile)
        plotHeatMap(configini)

    def callback(self,url):
        webbrowser.open_new(url)

class trainmachinemodel_settings:
    def __init__(self,inifile):
        self.configini = str(inifile)
        # Popup window
        trainmmsettings = Toplevel()
        trainmmsettings.minsize(400, 400)
        trainmmsettings.wm_title("Machine model settings")

        trainmms = Scrollable(trainmmsettings)

        #load metadata
        load_data_frame = LabelFrame(trainmms, text='Load Metadata',font=('Helvetica',10,'bold'), pady=5, padx=5)
        self.load_choosedata = FileSelect(load_data_frame,'File Select',title='Select a meta (.csv) file')
        load_data = Button(load_data_frame, text = 'Load', command = self.load_RFvalues,fg='blue')

        #link to github
        label_git_hyperparameters = Label(trainmms,text='[Click here to learn about the Hyperparameters]',cursor='hand2',fg='blue')
        label_git_hyperparameters.bind('<Button-1>',lambda e: webbrowser.open_new('https://github.com/sgoldenlab/simba/blob/master/docs/tutorial.md#step-7-train-machine-model'))

        #setting drop downs
        label_mm = LabelFrame(trainmms, text='Machine model',font=('Helvetica',10,'bold'), pady=5, padx=5)
        label_choosemm = Label(label_mm, text='Choose machine model:')
        options =['RF','GBC','Xboost']

        self.var = StringVar()
        self.var.set(options[0]) #set as default value

        modeldropdown = OptionMenu(label_mm,self.var,*options)

        self.meta_dict = {}
        ## hyperparameter settings
        label_settings = LabelFrame(trainmms, text='Hyperparameters',font=('Helvetica',10,'bold'),pady=5,padx=5)
        self.settings = []
        self.label_nestimators = Entry_Box(label_settings,'RF N Estimators','25')
        self.label_maxfeatures = Entry_Box(label_settings,'RF Max features','25')
        self.label_criterion = Entry_Box(label_settings,'RF Criterion','25')
        self.label_testsize = Entry_Box(label_settings,'Train Test Size','25')
        self.label_minsampleleaf = Entry_Box(label_settings,'RF Min sample leaf','25')
        self.label_under_s_settings = Entry_Box(label_settings, 'Under sample setting', '25')
        self.label_under_s_correctionvalue = Entry_Box(label_settings,'Under sample ratio','25')
        self.label_over_s_settings = Entry_Box(label_settings, 'Over sample setting', '25')
        self.label_over_s_ratio = Entry_Box(label_settings,'Over sample ratio','25')

        self.settings = [self.label_nestimators, self.label_maxfeatures, self.label_criterion, self.label_testsize,
                    self.label_minsampleleaf, self.label_under_s_correctionvalue,self.label_under_s_settings,
                         self.label_over_s_ratio,self.label_over_s_settings]
        ## model evaluation settings for checkboxes
        self.label_settings_box = LabelFrame(trainmms,pady=5,padx=5,text='Model Evaluations Settings',font=('Helvetica',10,'bold'))
        self.box1 = IntVar()
        self.box2 = IntVar()
        self.box3 = IntVar()
        self.box4 = IntVar()
        self.box5 = IntVar()
        self.box6 = IntVar()
        self.box7 = IntVar()
        self.box8 = IntVar()
        self.box9 = IntVar()

        # model evaluations for entrybox
        self.LC_ksplit = Entry_Box(self.label_settings_box, 'LearningCurve shuffle K splits', '25',status=DISABLED)
        self.LC_datasplit = Entry_Box(self.label_settings_box, 'LearningCurve shuffle Data splits', '25',status=DISABLED)
        self.label_n_feature_importance_bars = Entry_Box(self.label_settings_box, 'N feature importance bars', '25',status=DISABLED)
        self.settings.extend([self.LC_ksplit, self.LC_datasplit, self.label_n_feature_importance_bars])

        def activate(box, *args):
            for entry in args:
                if box.get() == 0:
                    entry.set_state(DISABLED)
                elif box.get() == 1:
                    entry.set_state(NORMAL)

        checkbutton1 = Checkbutton(self.label_settings_box,text='Generate RF model meta data file',variable = self.box1)
        checkbutton2 = Checkbutton(self.label_settings_box, text='Generate Example Decision Tree (requires "graphviz")', variable=self.box2)
        checkbutton3 = Checkbutton(self.label_settings_box, text='Generate Fancy Example Decision Tree ("dtreeviz")', variable=self.box3)
        checkbutton4 = Checkbutton(self.label_settings_box, text='Generate Classification Report', variable=self.box4)
        checkbutton5 = Checkbutton(self.label_settings_box, text='Generate Features Importance Log', variable=self.box5)
        checkbutton6 = Checkbutton(self.label_settings_box, text='Generate Features Importance Bar Graph', variable=self.box6,
                                   command = lambda:activate(self.box6, self.label_n_feature_importance_bars))
        checkbutton7 = Checkbutton(self.label_settings_box, text='Compute Feature Permutation Importances (Note: CPU intensive)', variable=self.box7)
        checkbutton8 = Checkbutton(self.label_settings_box, text='Generate Sklearn Learning Curves (Note: CPU intensive)', variable=self.box8,
                                   command = lambda:activate(self.box8, self.LC_datasplit, self.LC_ksplit))
        checkbutton9 = Checkbutton(self.label_settings_box, text='Generate Precision Recall Curves', variable=self.box9)

        self.check_settings = [checkbutton1, checkbutton2, checkbutton3, checkbutton4, checkbutton5, checkbutton6,
                               checkbutton7, checkbutton8, checkbutton9]


        # setting drop downs for modelname
        configini = self.configini
        config = ConfigParser()
        config.read(configini)

        number_of_model = config['SML settings'].getint('No_targets')

        model_list = []
        count = 1
        for i in range(number_of_model):
            a = str('target_name_' + str(count))
            model_list.append(config['SML settings'].get(a))
            count += 1

        labelf_modelname = LabelFrame(trainmms,text='Model',font=('Helvetica',10,'bold'),pady=5,padx=5)
        label_modelname = Label(labelf_modelname,text='Model name')

        self.varmodel = StringVar()
        self.varmodel.set(model_list[0])  # set as default value

        model_name_dropdown = OptionMenu(labelf_modelname, self.varmodel, *model_list)

        # button
        button_settings_to_ini = Button(trainmms, text='Save settings into global environment', font=('Helvetica', 10, 'bold'),fg='blue', command=self.set_values)
        button_save_meta = Button(trainmms, text='Save settings for specific model', font=('Helvetica', 10, 'bold'),fg='green' ,command=self.save_new)
        button_remove_meta = Button(trainmms,text='Clear cache',font=('Helvetica', 10, 'bold'),fg='red',command = self.clearcache)

        # organize
        load_data_frame.grid(row=0, sticky=W, pady=5, padx=5)
        self.load_choosedata.grid(row=0, column=0, sticky=W)
        load_data.grid(row=1, column=0)

        label_mm.grid(row=1, sticky=W, pady=5)
        label_choosemm.grid(row=0, column=0, sticky=W)
        modeldropdown.grid(row=0, column=1, sticky=W)

        labelf_modelname.grid(row=2, sticky=W, pady=5)
        label_modelname.grid(row=0, column=0, sticky=W)
        model_name_dropdown.grid(row=0, column=1, sticky=W)

        label_git_hyperparameters.grid(row=3,sticky=W)

        label_settings.grid(row=4, sticky=W, pady=5)
        self.label_nestimators.grid(row=1, sticky=W)
        self.label_maxfeatures.grid(row=2, sticky=W)
        self.label_criterion.grid(row=3, sticky=W)
        self.label_testsize.grid(row=4, sticky=W)
        self.label_minsampleleaf.grid(row=7, sticky=W)
        self.label_under_s_settings.grid(row=8, sticky=W)
        self.label_under_s_correctionvalue.grid(row=9, sticky=W)
        self.label_over_s_settings.grid(row=10, sticky=W)
        self.label_over_s_ratio.grid(row=11,sticky=W)

        self.label_settings_box.grid(row=5,sticky=W)
        checkbutton1.grid(row=0,sticky=W)
        checkbutton2.grid(row=1,sticky=W)
        checkbutton3.grid(row=2,sticky=W)
        checkbutton4.grid(row=3,sticky=W)
        checkbutton5.grid(row=4,sticky=W)
        checkbutton6.grid(row=5,sticky=W)
        self.label_n_feature_importance_bars.grid(row=6, sticky=W)
        checkbutton7.grid(row=7,sticky=W)
        checkbutton8.grid(row=8, sticky=W)
        self.LC_ksplit.grid(row=9, sticky=W)
        self.LC_datasplit.grid(row=10, sticky=W)
        checkbutton9.grid(row=11, sticky=W)

        button_settings_to_ini.grid(row=6,pady=5)
        button_save_meta.grid(row=7)
        button_remove_meta.grid(row=8,pady=5)

        trainmms.update()

    def clearcache(self):
        configs_dir = os.path.join(os.path.dirname(self.configini),'configs')
        filelist = [f for f in os.listdir(configs_dir) if f.endswith('.csv')]
        for f in filelist:
            os.remove(os.path.join(configs_dir,f))
            print(f,'deleted')

    def load_RFvalues(self):

        metadata = pd.read_csv(str(self.load_choosedata.file_path), index_col=False)
        # metadata = metadata.drop(['Feature_list'], axis=1)
        for m in metadata.columns:
            self.meta_dict[m] = metadata[m][0]
        print('Meta data file loaded')

        for key in self.meta_dict:
            cur_list = key.lower().split(sep='_')
            # print(cur_list)
            for i in self.settings:
                string = i.lblName.cget('text').lower()
                if all(map(lambda w: w in string, cur_list)):
                    i.entry_set(self.meta_dict[key])
            for k in self.check_settings:
                string = k.cget('text').lower()
                if all(map(lambda w: w in string, cur_list)):
                    if self.meta_dict[key] == 'yes':
                        k.select()
                    elif self.meta_dict[key] == 'no':
                        k.deselect()

    def get_checkbox(self):
        ### check box settings
        if self.box1.get() == 1:
            self.rfmetadata = 'yes'
        else:
            self.rfmetadata = 'no'

        if self.box2.get() == 1:
            self.generate_example_d_tree = 'yes'
        else:
            self.generate_example_d_tree = 'no'

        if self.box3.get() == 1:
            self.generate_example_decision_tree_fancy = 'yes'
        else:
            self.generate_example_decision_tree_fancy  = 'no'

        if self.box4.get() == 1:
            self.generate_classification_report = 'yes'
        else:
            self.generate_classification_report = 'no'

        if self.box5.get() == 1:
            self.generate_features_imp_log = 'yes'
        else:
            self.generate_features_imp_log = 'no'

        if self.box6.get() == 1:
            self.generate_features_bar_graph = 'yes'
        else:
            self.generate_features_bar_graph = 'no'
        self.n_importance = self.label_n_feature_importance_bars.entry_get

        if self.box7.get() == 1:
            self.compute_permutation_imp = 'yes'
        else:
            self.compute_permutation_imp = 'no'

        if self.box8.get() == 1:
            self.generate_learning_c = 'yes'
        else:
            self.generate_learning_c = 'no'
        self.learningcurveksplit = self.LC_ksplit.entry_get
        self.learningcurvedatasplit = self.LC_datasplit.entry_get

        if self.box9.get() == 1:
            self.generate_precision_recall_c = 'yes'
        else:
            self.generate_precision_recall_c = 'no'

    def save_new(self):
        self.get_checkbox()
        meta_number = 0
        for f in os.listdir(os.path.dirname(self.configini)+'\\configs\\'):
            if f.__contains__('_meta') and f.__contains__(str(self.varmodel.get())):
                meta_number += 1

        # for s in self.settings:
        #     meta_df[s.lblName.cget('text')] = [s.entry_get]
        new_meta_dict = {'RF_n_estimators': self.label_nestimators.entry_get,
                         'RF_max_features': self.label_maxfeatures.entry_get, 'RF_criterion': self.label_criterion.entry_get,
                         'train_test_size': self.label_testsize.entry_get, 'RF_min_sample_leaf': self.label_minsampleleaf.entry_get,
                         'under_sample_ratio': self.label_under_s_correctionvalue.entry_get, 'under_sample_setting': self.label_under_s_settings.entry_get,
                         'over_sample_ratio': self.label_over_s_ratio.entry_get, 'over_sample_setting': self.label_over_s_settings.entry_get,
                         'generate_rf_model_meta_data_file': self.rfmetadata,
                         'generate_example_decision_tree': self.generate_example_d_tree,'generate_classification_report':self.generate_classification_report,
                         'generate_features_importance_log': self.generate_features_imp_log,'generate_features_importance_bar_graph':self.generate_features_bar_graph,
                         'n_feature_importance_bars': self.n_importance,'compute_feature_permutation_importance':self.compute_permutation_imp,
                         'generate_sklearn_learning_curves': self.generate_learning_c,
                         'generate_precision_recall_curves':self.generate_precision_recall_c, 'learning_curve_k_splits':self.learningcurveksplit,
                         'learning_curve_data_splits': self.learningcurvedatasplit}
        meta_df = pd.DataFrame(new_meta_dict, index=[0])
        meta_df.insert(0, 'Classifier_name', str(self.varmodel.get()))

        output_path = os.path.dirname(self.configini) + "\\configs\\" + \
                      str(self.varmodel.get())+ '_meta_' + str(meta_number) + '.csv'
        print(os.path.basename(str(output_path)),'saved')

        meta_df.to_csv(output_path, index=FALSE)

    def set_values(self):
        self.get_checkbox()
        #### settings
        model = self.var.get()
        n_estimators = self.label_nestimators.entry_get
        max_features = self.label_maxfeatures.entry_get
        criterion = self.label_criterion.entry_get
        test_size = self.label_testsize.entry_get
        min_sample_leaf = self.label_minsampleleaf.entry_get
        under_s_c_v = self.label_under_s_correctionvalue.entry_get
        under_s_settings = self.label_under_s_settings.entry_get
        over_s_ratio = self.label_over_s_ratio.entry_get
        over_s_settings = self.label_over_s_settings.entry_get
        classifier_settings = self.varmodel.get()

        #export settings to config ini file
        configini = self.configini
        config = ConfigParser()
        config.read(configini)

        config.set('create ensemble settings', 'model_to_run', str(model))
        config.set('create ensemble settings', 'RF_n_estimators', str(n_estimators))
        config.set('create ensemble settings', 'RF_max_features', str(max_features))
        config.set('create ensemble settings', 'RF_criterion', str(criterion))
        config.set('create ensemble settings', 'train_test_size', str(test_size))
        config.set('create ensemble settings', 'RF_min_sample_leaf', str(min_sample_leaf))
        config.set('create ensemble settings', 'under_sample_ratio', str(under_s_c_v))
        config.set('create ensemble settings', 'under_sample_setting', str(under_s_settings))
        config.set('create ensemble settings', 'over_sample_ratio', str(over_s_ratio))
        config.set('create ensemble settings', 'over_sample_setting', str(over_s_settings))
        config.set('create ensemble settings', 'classifier',str(classifier_settings))
        config.set('create ensemble settings', 'RF_meta_data', str(self.rfmetadata))
        config.set('create ensemble settings', 'generate_example_decision_tree', str(self.generate_example_d_tree))
        config.set('create ensemble settings', 'generate_classification_report', str(self.generate_classification_report))
        config.set('create ensemble settings', 'generate_features_importance_log', str(self.generate_features_imp_log))
        config.set('create ensemble settings', 'generate_features_importance_bar_graph', str(self.generate_features_bar_graph))
        config.set('create ensemble settings', 'N_feature_importance_bars', str(self.n_importance))
        config.set('create ensemble settings', 'compute_permutation_importance', str(self.compute_permutation_imp))
        config.set('create ensemble settings', 'generate_learning_curve', str(self.generate_learning_c))
        config.set('create ensemble settings', 'generate_precision_recall_curve', str(self.generate_precision_recall_c))
        config.set('create ensemble settings', 'LearningCurve_shuffle_k_splits',str(self.learningcurveksplit))
        config.set('create ensemble settings', 'LearningCurve_shuffle_data_splits',str(self.learningcurvedatasplit))
        config.set('create ensemble settings', 'generate_example_decision_tree_fancy',str(self.generate_example_decision_tree_fancy))


        with open(configini, 'w') as configfile:
            config.write(configfile)

        print('Settings exported to project_config.ini')

class runmachinemodelsettings:
    def __init__(self,inifile):
        self.row1 = []
        self.row2 = []
        self.row3 = []
        self.row4 = []
        self.targetname = []
        # Popup window
        runmms = Toplevel()
        runmms.minsize(200, 200)
        runmms.wm_title("Select model to run")

        ### read inifile and get the model
        config = ConfigParser()
        configini = str(inifile)
        config.read(configini)
        no_targets = config.get('SML settings','no_targets')

        ###get all target from ini
        for i in range(int(no_targets)):
            currentModelNames = 'target_name_' + str(i+1)
            currentModelNames = config.get('SML settings', currentModelNames)
            self.targetname.append(currentModelNames)

        ###loop for table
        table = LabelFrame(runmms)
        #set title
        tn = Label(table,text='Classifier',font=("Helvetica",10,'bold'))
        tn.grid(row=0,column=0,sticky=W,pady=5)

        selectmodel = Label(table,text='Model path (.sav)',font=("Helvetica",10,'bold'))
        selectmodel.grid(row=0,column=1)

        thresholdtitle = Label(table,text='Threshold',font=("Helvetica",10,'bold') )
        thresholdtitle.grid(row=0,column=2,sticky=W)

        minbouttitle = Label(table,text='Minimum Bout',font=("Helvetica",10,'bold'))
        minbouttitle.grid(row=0,column=3,sticky=W)

        # main loop for content of table
        for i in range(len(self.targetname)):
            self.row1.append(Label(table,text=str(self.targetname[i])))
            self.row1[i].grid(row=i+2,column=0,sticky=W)

            self.row2.append(FileSelect(table,title='Select model (.sav) file'))
            self.row2[i].grid(row=i+2,column=1,sticky=W)

            self.row3.append(Entry(table))
            self.row3[i].grid(row=i+2,column=2,sticky=W,padx=5)

            self.row4.append(Entry(table))
            self.row4[i].grid(row=i+2,column=3,sticky=W,padx=5)

        button_set = Button(runmms,text='Set model(s)',command =lambda:self.set_modelpath_to_ini(inifile),font=("Helvetica",10,'bold'),fg='red')

        table.grid(row=0,sticky=W,pady=5,padx=5)
        button_set.grid(row=1,pady=10)

    def set_modelpath_to_ini(self,inifile):
        config = ConfigParser()
        configini = str(inifile)
        config.read(configini)

        for i in range(len(self.targetname)):
            config.set('SML settings','model_path_'+(str(i+1)),str(self.row2[i].file_path))
            config.set('threshold_settings', 'threshold_' + (str(i + 1)), str(self.row3[i].get()))
            config.set('Minimum_bout_lengths', 'min_bout_' + (str(i + 1)), str(self.row4[i].get()))

        with open(configini, 'w') as configfile:
            config.write(configfile)

        print('Model paths saved in project_config.ini')


class Scrollable(Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbarX = Scrollbar(frame, width=width, orient='horizontal')
        scrollbarX.pack(side=BOTTOM, fill=X, expand=False)
        scrollbarY = Scrollbar(frame, width=width)
        scrollbarY.pack(side=RIGHT, fill=Y, expand=False)

        sizegrip= ttk.Sizegrip(frame)
        sizegrip.pack(in_=scrollbarX, side=BOTTOM, anchor="se")

        self.canvas = Canvas(frame, yscrollcommand=scrollbarY.set,xscrollcommand=scrollbarX.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbarX.config(command=self.canvas.xview)
        scrollbarY.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=NW)

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        try:
            scrollSpeed = event.delta
            if platform.system() == 'Darwin':
                scrollSpeed = event.delta
            elif platform.system() == 'Windows':
                scrollSpeed = int(event.delta/120)
            self.canvas.yview_scroll(-1*(scrollSpeed), "units")
        except:
            pass
    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width

        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))




def get_frame(self):
    '''
      Return the "frame" useful to place inner controls.
    '''
    return self.canvas

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class aboutgui:

    def __init__(self):
        about = Toplevel()
        about.minsize(657, 398)
        about.wm_title("About")

        canvas = Canvas(about,width=657,height=398,bg='black')
        canvas.pack()

        img = PhotoImage(file='TheGoldenLab_aboutme.png')
        canvas.create_image(0,0,image=img,anchor='nw')
        canvas.image = img

class App(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('SimBA')
        self.root.minsize(750,750)
        self.root.geometry("750x750")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        img = PhotoImage(file='golden.png')
        background = Label(self.root, image=img, bd=0)
        background.pack(fill='both', expand=True)
        background.image = img

        ### drop down menu###f
        menu = Menu(self.root)
        self.root.config(menu=menu)

        #first menu
        fileMenu = Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='Create a new project',command=project_config)
        fileMenu.add_command(label='Load project', command=lambda:loadprojectMenu(loadprojectini))
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=Exit)

        # Process video
        pvMenu = Menu(menu)
        menu.add_cascade(label='Process Videos', menu=pvMenu)
        pvMenu.add_command(label='Batch pre-process videos', command=batch_processvideo)

        #third menu
        thirdMenu = Menu(menu)
        menu.add_cascade(label='Tracking',menu=thirdMenu)
        #dlc
        dlcmenu = Menu(thirdMenu)
        dlcmenu.add_command(label='Create DLC Model',command=create_project_DLC)
        dlcmenu.add_command(label='Load DLC Model',command=Load_DLC_Model)
        #deepPoseKit
        dpkmenu = Menu(thirdMenu)
        dpkmenu.add_command(label='Create DeepPoseKit project', command=createDPK_project)
        dpkmenu.add_command(label='Load DeepPoseKit project', command=lambda:loadprojectMenu(deepPoseKitMenu))
        #labelling tool
        labellingtoolmenu = Menu(thirdMenu)
        labellingtoolmenu.add_command(label='labelImg', command=lambda: subprocess.call(["labelImg"]))
        labellingtoolmenu.add_command(label='labelme', command=lambda: subprocess.call(["labelme"]))
        #third menu organize
        thirdMenu.add_cascade(label='DeepLabCut', menu=dlcmenu)
        thirdMenu.add_cascade(label='DeepPoseKit', menu=dpkmenu)
        thirdMenu.add_command(label='LEAP', command=lambda: print('coming soon'))
        thirdMenu.add_cascade(label='Labelling tools', menu=labellingtoolmenu)

        #fifth menu
        fifthMenu = Menu(menu)
        #changefpsmenu
        fpsMenu = Menu(fifthMenu)
        fpsMenu.add_command(label='Change fps for single video', command=changefps)
        fpsMenu.add_command(label='Change fps for multiple videos',command=changefpsmulti)
        menu.add_cascade(label='Tools',menu=fifthMenu)
        fifthMenu.add_command(label='Clip videos',command=shorten_video)
        fifthMenu.add_command(label='Crop videos',command=crop_video)
        fifthMenu.add_command(label='Multi-crop',command=multicropmenu)
        fifthMenu.add_command(label='Downsample videos',command=video_downsample)
        fifthMenu.add_command(label='Get mm/ppx',command = get_coordinates_from_video)
        fifthMenu.add_cascade(label='Change fps',menu =fpsMenu)
        #changefpsmenu organize

        changeformatMenu = Menu(fifthMenu)
        changeformatMenu.add_command(label='Change image file formats',command=change_imageformat)
        changeformatMenu.add_command(label='Change video file formats',command=convert_video)
        changeformatMenu.add_command(label='Change .seq to .mp4', command=lambda:convertseqVideo(askdirectory(title='Please select video folder to convert')))
        fifthMenu.add_cascade(label='Change formats',menu=changeformatMenu)

        fifthMenu.add_command(label='CLAHE enhance video',command=Red_light_Convertion)
        fifthMenu.add_command(label='Superimpose frame numbers on video',command=lambda:superimposeframe(askopenfilename()))
        fifthMenu.add_command(label='Convert to grayscale',command=lambda:greyscale(askopenfilename()))
        fifthMenu.add_command(label='Merge frames to video',command=mergeframeffmpeg)
        fifthMenu.add_command(label='Generate gifs', command=creategif)

        extractframesMenu = Menu(fifthMenu)
        extractframesMenu.add_command(label='Extract defined frames',command=extract_specificframes)
        extractframesMenu.add_command(label='Extract frames',command=extract_allframes)
        extractframesMenu.add_command(label='Extract frames from seq files', command=extract_seqframe)
        fifthMenu.add_cascade(label='Extract frames',menu=extractframesMenu)

        #sixth menu
        sixthMenu = Menu(menu)
        menu.add_cascade(label='Help',menu=sixthMenu)
        #labelling tool
        links = Menu(sixthMenu)
        links.add_command(label='Download weights',command = lambda:webbrowser.open_new(str(r'https://osf.io/5t4y9/')))
        links.add_command(label='Ex. feature list',command=lambda: webbrowser.open_new(str(r'https://github.com/sgoldenlab/simba/blob/master/misc/Feature_description.csv')))
        links.add_command(label='SimBA github', command=lambda: webbrowser.open_new(str(r'https://github.com/sgoldenlab/simba')))
        links.add_command(label='Gitter Chatroom', command=lambda: webbrowser.open_new(str(r'https://gitter.im/SimBA-Resource/community')))
        links.add_command(label='Install FFmpeg',command =lambda: webbrowser.open_new(str(r'https://m.wikihow.com/Install-FFmpeg-on-Windows')))
        links.add_command(label='Install graphviz', command=lambda: webbrowser.open_new(str(r'https://bobswift.atlassian.net/wiki/spaces/GVIZ/pages/20971549/How+to+install+Graphviz+software')))
        sixthMenu.add_cascade(label="Links",menu=links)
        sixthMenu.add_command(label='About', command= aboutgui)

        #Status bar at the bottom
        self.frame = Frame(background, bd=2, relief=SUNKEN, width=300, height=300)
        self.frame.pack(expand=True)
        self.txt = Text(self.frame, bg='white')
        self.txt.config(state=DISABLED)
        self.txt.pack(expand=True, fill='both')
        sys.stdout = StdRedirector(self.txt)


# writes text out in GUI
class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.update()
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)

class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.Splash()
        self.Window()

    def Splash(self):
        self.image = Image.open(r".\TheGoldenLab.png")
        self.imgSplash = ImageTk.PhotoImage(self.image)

    def Window(self):
        width, height = self.image.size
        halfwidth = (self.parent.winfo_screenwidth()-width)//2
        halfheight = (self.parent.winfo_screenheight()-height)//2
        self.parent.geometry("%ix%i+%i+%i" %(width, height, halfwidth,halfheight))
        Label(self.parent, image=self.imgSplash).pack()


if __name__ == '__main__':
    root = Tk()
    root.overrideredirect(True)
    app = SplashScreen(root)
    root.after(1000, root.destroy)
    root.mainloop()


app = App()
print('Welcome fellow scientists :)' + '\n' + 'SimBA version ' + str(simBA_version))
print('\n')
print(tabulate([['Region of Interest support (ROI Module)'], ['DeepPoseKit support (DPK Module)'], ['Flexible Annotation Module'], ['Interactive thresholding'], ['Heatmap visualizations'], ['Extended validation tools'], ['Multi-crop'],['...many bug fixes']], headers=['March 2020 Updates/Fixes'], tablefmt='fancy_grid'))



maincwd=os.getcwd()
app.root.mainloop()
