# data-preprocessing_toogoodtogo_threatlines
We're the hackathon leftovers, but we are Too Good To Go ;-). A repo by Lukas Schubotz, Stef van Buuren, and Raymon van Dinter. We aim to improve current data preprocessing for FTM's WOB data to analyze Shell and Dutch Governmental contacts.


## Visualisation idea

Publications from the FTM "Dossier SHELL papers" <https://www.ftm.nl/dossier/shell-papers> suggest that timing of events is critical in the interactions between actors. It would therefore be useful if we could visualise the mail exchanges in time.

The idea is to visualise threads of mail exchanges between actors over time. When this is done for multiple threads, the display would give rapid insight into the structure and timing of exchanges between actors. For example, suppose we are able to construct a single thread from "RE:" and "FW:" mails in the data. A simple visualisation would be 

![](figures/simple.png)

See <https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.88.9825&rep=rep1&type=pdf> for variations on this display, for example by adding the interactions between the actors. 

![](figures/complex.png)

A generalisation to multiple simulataneous threads would stack multiple lines in a vertical way. Such a design calls for relatively simple thread displays that are synchronised in time. Therefore we will concentrate on using a simple **thread-line** that plots mail chronology against calender time. 

A somewhat grander idea would be to create a "film of events". This would place a cursor on the time axis, and allow the user to scroll through time. The new information per mail is displayed, for example by tiptools. 

