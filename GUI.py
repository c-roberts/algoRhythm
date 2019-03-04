from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import algoRhythm


def inputWAV():
    global audio_path, BPM, rhythm_leniency, pitch_leniency
    try:
        inputDataFile = askopenfilename()
        inDataFile = open(inputDataFile, 'r')

        if "wav" in inDataFile:
            audio_path = inDataFile
        else:
            progress['text'] = 'Data not recognized. Make sure file is .WAV format.'

        inDataFile.close()
    except IOError:
        progress['text'] = 'Data not loaded.'
    return

def inputXML():
    global sheet_music, BPM, rhythm_leniency, pitch_leniency
    try:
        inputDataFile = askopenfilename()
        inDataFile = open(inputDataFile, 'r')

        if "wav" in inDataFile:
            sheet_music = inDataFile
        else:
            progress['text'] = 'Data not recognized. Make sure file is .XML format.'

        inDataFile.close()
    except IOError:
        progress['text'] = 'Data not loaded.'
    return

def closeProgram():
    close = messagebox.askquestion(title='Close Application?', message='Are you sure you want to exit?')
    if close == 'yes':
        window.destroy()
    return

def submit():
    BPM = tempo.get()
    if (type(BPM) != int):
        progress['text'] = 'Please enter an integer value for tempo.'
    rhythm_score, rhythm_errors = algoRhythm.algoRhythm(audio_path, sheet_music, BPM, leniency)

def clear():

    return


def helpMe():
    helpWindow = Toplevel()
    helpWindow.title('Help')
    helpWindow.geometry('1000x800')
    scrollbar2 = Scrollbar(helpWindow)
    scrollbar2.pack(side=RIGHT, fill=Y)
    canvas = Canvas(helpWindow, width=1000, height=350)
    canvas.pack(side=TOP)
    '''
    img= PhotoImage(file='Example1.gif')
    canvas.image = img
    canvas.create_image(500, 250, image=img)
    '''
    text2 = Text(helpWindow, width=200, height=700, wrap=WORD, yscrollcommand=scrollbar2.set)
    text2.pack(side=BOTTOM)
    scrollbar2.config(command=text2.yview)
    ''' Add relevant help...
    text2.insert(INSERT, '\t\t\t\t\t\tFigure 1: Sample node input format\n\n')
    text2.insert(INSERT, 'This program will work for \"spcforc\" and \"nodout\" outputs from LS-DYNA. Additionally, '
                         'saved curves can be input.\n\n')
    text2.insert(INSERT, 'For spcforc:\n')
    text2.insert(INSERT, '1) Select the desired spcforc file; ensure it is named \"spcforc\"\n')
    text2.insert(INSERT, '2) Input the desired nodes in the format above (.txt)\n')
    text2.insert(INSERT, '3) The program will then output the min/max for each node. If a node is not found, it will'
                         ' output \"NA\" for the requested node\n')
    text2.insert(INSERT, '4) Click \"Save As...\". This will save the output as a .csv file which can then be easily'
                         ' opened and read in Excel\n\n')
    text2.insert(INSERT, 'For nodout:\n')
    text2.insert(INSERT, '1) Select the desired nodout file; ensure it is named \"nodout\"\n')
    text2.insert(INSERT, '2) The program will then output the min/max of x,y,z displacement, velocity, and acceleration'
                         ' for each node\n')
    text2.insert(INSERT, '3) Click \"Save As...\". This will save the output as a .csv file which can then be easily'
                         ' opened and read in Excel\n\n')
    text2.insert(INSERT, 'For saved prepost curves:\n')
    text2.insert(INSERT, '1) Click \"Import Prepost Curve\" and select the desired file;\n '
                         '*note* this program looks for the keyword \"Curveplot\" to ensure input is correct; '
                         'if this is absent from the start of the file, the program may not run\n')
    text2.insert(INSERT, '2) The program will then output the min/max of the pre-specified measurement and nodes'
                         'and the time of which they occur\n')
    text2.insert(INSERT, '3) Click \"Save As...\". This will save the output as a .csv file which can then be easily'
                         ' opened and read in Excel\n\n')
    text2.insert(INSERT, 'If an error is encountered:\n')
    text2.insert(INSERT, '1) Try running the program again\n')
    text2.insert(INSERT, '2) Ensure your input files are correctly formatted\n')
        '''
    text2.config(state=DISABLED)
    return

window = Tk()
window.title('algoRhythm')
window.geometry('1200x508')
frame1 = Frame(window)
frame1.pack()
scrollbar = Scrollbar(frame1)
#scrollbar.pack(side=RIGHT, fill=Y)
#text = Text(frame1, width=148, height=30, wrap=WORD, fg='black', yscrollcommand=scrollbar.set)
#text.config(state=DISABLED)
leniency = IntVar()
leniency_scale = Scale(frame1, var=leniency, label="Leniency", from_=1, to=10, orient=HORIZONTAL)
leniency_scale.pack()

tempo_lab = Label(frame1, text="Tempo (BPM)")
tempo_lab.pack()

tempo = StringVar()
tempo_ent = Entry(frame1, textvariable=tempo)
tempo_ent.pack()
#scrollbar.config(command=text.yview)
#text.pack()

progress = Label(window, text='Please load data files.')
progress.pack(side=TOP)

# generates menu for each event
menubar = Menu(window)
window.config(menu=menubar)

operationmenu1 = Menu(menubar, tearoff=0)
menubar.add_command(label='Import XML', command=inputXML)

operationmenu2 = Menu(menubar, tearoff=0)
menubar.add_command(label='Import WAV', command=inputWAV)

operationmenu3 = Menu(menubar, tearoff=0)
menubar.add_command(label='Submit', command=submit)

operationmenu5 = Menu(menubar, tearoff=0)
menubar.add_command(label='Reset', command=clear)

operationmenu6 = Menu(menubar, tearoff=0)
menubar.add_command(label='Help', command=helpMe)

operationmenu7 = Menu(menubar, tearoff=0)
menubar.add_command(label='Close', command=closeProgram)

window.mainloop()