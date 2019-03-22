from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import algoRhythm



def inputWAV():
    global audio_path
    try:
        inputDataFile = askopenfilename()

        if "wav" in inputDataFile:
            audio_path = inputDataFile
            progress['text'] = 'User performance loaded.'

        else:
            progress['text'] = 'Data not recognized. Make sure file is .WAV format.'

    except IOError:
        progress['text'] = 'WAV not loaded.'
    return

def inputXML():
    global sheet_music
    try:
        inputDataFile = askopenfilename()
        if "xml" in inputDataFile:
            sheet_music = inputDataFile
            progress['text'] = 'Sheet music loaded.'

        if "xml" in inDataFile:
            sheet_music = inDataFile
        else:
            progress['text'] = 'Data not recognized. Make sure file is .XML format.'
    except IOError:
        progress['text'] = 'XML not loaded.'
    return

def closeProgram():
    close = messagebox.askquestion(title='Close Application?', message='Are you sure you want to exit?')
    if close == 'yes':
        window.destroy()
    return

def submit():
    BPM = tempo.get()
    print("\n\n----RUNNING----")
    print("Sheet music path: ", sheet_music)
    print("Audio path: ", audio_path)
    try:
        if (type(int(BPM)) != int):
            progress['text'] = 'Please enter an integer value for tempo.'
            return
    except ValueError:
        progress['text'] = 'Please enter an integer value for tempo.'
        return
    print("BPM: ", BPM)
    print("Leniency: ", leniency.get())
    print("\n\n")


    rhythm_score, rhythm_errors = algoRhythm.algoRhythm(audio_path, sheet_music, BPM, leniency.get())

    # display score
    # change color based on score?
    mistakes = len(rhythm_errors)
    #print(mistakes)

    score_['text'] = str(rhythm_score) + '%'
    if rhythm_score >= 80:
        score_['fg'] = 'green'
    elif rhythm_score >= 60:
        score_['fg'] = 'orange'
    else:
        score_['fg'] = 'red'
    mistakes_['text']=(str(mistakes) + " missed rhythms")
    progress['text'] = 'Downloading report...'

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
window.geometry('1000x400')
window.resizable(False, False)


submit_butt = Button(window, text="Submit", fg="white", bg="orange",
                            activebackground="pink", command=submit,
                            height=1, width=20, font=('Sans','14','bold'))
submit_butt.pack(side=BOTTOM, anchor=S, fill='both')

# Progress text input #############
progress = Label(window, text='Please load data files.', font=('Sans','14'))
progress.pack(side=BOTTOM)


#### INPUT FRAME ####
in_frame = Frame(window, width=150, height=350)
in_frame.pack(side=LEFT, anchor=W, fill='x')
#scrollbar = Scrollbar(in_frame)

# Load XML/WAV buttons #############
butt_frame=Frame(in_frame)
padding1=Frame(in_frame)
#padding1.grid(row=0, column=0, columnspan= 2, padx=20, pady=30)

in_sheet = Button(butt_frame, text="Input Sheet Music", fg="white", bg="blue",
                              activebackground="light blue", command=inputXML,
                              height=1, width=17, font=('Sans','14','bold'))
in_sheet.grid(row=0, column=0, padx=20)

in_wav = Button(butt_frame, text="Input Performance", fg="white", bg="green",
                            activebackground="light green", command=inputWAV,
                            height=1, width=17, font=('Sans','14','bold'))
in_wav.grid(row=0, column=1)
butt_frame.grid(row=1, column=0, columnspan= 4, padx=20, pady=0)

padding2=Frame(in_frame)
#padding2.grid(row=2, column=0, columnspan= 2, padx=15, pady=30)

# Leniency Input #############
leniency_lab = Label(in_frame, text="Leniency: ", font=('Sans','13'))
leniency_lab.grid(row=4, column=0, padx=35, pady=10, sticky=SE)

leniency = IntVar()
leniency_scale = Scale(in_frame, var=leniency, from_=1, to=5, orient=HORIZONTAL, width=15, length=170)
leniency_scale.grid(row=4, column=1, pady=10, sticky=SW)

# BPM Input #############
tempo_lab = Label(in_frame, text="Tempo (BPM): ", font=('Sans','13'))
tempo_lab.grid(row=6, column=0, padx=35, pady=10, sticky=SE)

tempo = StringVar()
tempo_ent = Entry(in_frame, textvariable=tempo, width=16, font=('Sans','14'))
tempo_ent.grid(row=6, column=1, pady=10, sticky=SW)





#### RESULTS FRAME ####
out_frame = Frame(window, width=150, height=350)
out_frame.pack(side=RIGHT, anchor=E, padx=150, fill='x')

#score = StringVar()
score="100"
mistakes="0"

score_lab = Label(out_frame, text="Your score...", font=('Sans','14', 'bold'))
score_ = Label(out_frame, text=(score + "%"), font=('Sans','50', 'bold'), fg="green" )
mistakes_ = Label(out_frame, text=(mistakes + " missed rhythms"), font=('Sans','14'))

score_lab.pack()
score_.pack(pady=15)
mistakes_.pack()




# generates menu
menubar = Menu(window)
window.config(menu=menubar)

operationmenu1 = Menu(menubar, tearoff=0)
menubar.add_command(label='Reset', command=clear)
'''
operationmenu2 = Menu(menubar, tearoff=0)
menubar.add_command(label='Help', command=helpMe)
'''
operationmenu3 = Menu(menubar, tearoff=0)
menubar.add_command(label='Close', command=closeProgram)

window.mainloop()
