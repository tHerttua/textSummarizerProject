import os
from tkinter import *
from tkinter import scrolledtext
import dailyParser.dailyMailparser as dp
import summarizers.summarizer as summ
from rougeEvaluator.RougeEvaluation import RougeEvaluation
from namedEntitySummarizer.NamedEntitySumm import NERSummarizer

#Initialize the TKinter windows 
window = Tk()
window.title("Text Summarizer")
window.geometry('600x700')
frame = Frame(window)
rowIndex = 1

#Initialize the classes needed
parser = dp.DailyMailParser()
rouge = RougeEvaluation()
ner = NERSummarizer()

def summarize(sel):
    """
    Runs the whole thing: First finds the article content and facets,
    then summarizes the article using the selected summarizer,
    last performs the rouge scoring and shows the output
    """
    data = getArticle(entry.get())
    facets = parser.findFacets()
    result = runSummarize(sel, data.replace("\xa0"," "), len(facets))
    summary = ""
    for line in result:
        summary += (" " + line)
    summaryText.delete("1.0", "end")
    summaryText.insert(END, result)
    evaluateText(summary, facets)
    

def runSummarize(sel, data, refSentences):
    """
    Create summary using a summarizer selected by the user
    """
    if sel == 1:
        summary = summ.textRank(data, refSentences)
    elif sel == 2:
        summary = summ.LSA_O(data, refSentences)
    elif sel == 3:
        summary = summ.LSA_S(data, refSentences)
    elif sel == 4:
        summary = summ.relevance(data, refSentences)
    elif sel == 5:
        summary = ner.Named_Entity_Summary(data, refSentences)
    return summary

def getArticle(URL):
    """
    Opens the article and find the content.
    If this fails, the program cannot do further operations
    """
    parser.openURL(URL)
    article = parser.findContent()
    return article

def evaluateText(summary, facets):
    """
    Calculates the rouge scoring and creates the label with content
    """
    refText = ""
    for facet in facets:
        refText += (" "+facet.replace("\xa0"," "))
    evalScore = rouge.rouge_evaluations(str(summary), str(refText))
    rougeLabel = Label(frame, text="Rouge Results")
    rougeResults = ("Rouge-2 recall: "+ str(round(float(evalScore[0]), 2))+"\n"
                   +"Rouge-2 precision: "+ str(round(float(evalScore[1]), 2))+"\n"
                   +"Rouge-3 recall: "+ str(round(float(evalScore[2]), 2))+"\n"
                   +"Rouge-3 precision: "+ str(round(float(evalScore[3]), 2))+"\n")
    rougeLabel['text'] = rougeResults
    rougeLabel.grid(row=rowIndex+5, column=0)


#GUI initialization
#Create the radio button
MODES = [
    ("Text Rank",1),
    ("LSA Ozsoy",2),
    ("LSA Steinberg",3),
    ("Relevance", 4),
    ("Named Entity Summarizer",5)
    ]
selection = IntVar(frame)
selection.set(1)
for text, mode, in MODES:
    Radiobutton(frame, text=text, value=mode, variable=selection).grid(row=rowIndex, column=0)
    rowIndex += 1

#Create helper text
Label(frame, text="Select a summarizer").grid(row=0, column=0)

#Create field that takes user input
#NOTE doesn't include sanitization
entry = Entry(frame, width=50)
entry.grid(row=rowIndex+1, column=0)
entry.insert(0, "Write your Daily Mail article URL here")

#Create the button to fire off everything
launchButton = Button(frame, text="Submit", command=lambda: summarize(selection.get()))
launchButton.grid(row=rowIndex+2, column=0)

#Create the field that will contain summary
summaryLabel = Label(frame, text="Summary")
summaryLabel.grid(row=rowIndex+6, column=0)
summaryText = scrolledtext.ScrolledText(frame, width=70, height=30)
summaryText.grid(column=0)

#Start the GUI
frame.pack()
window.mainloop()