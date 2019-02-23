# algoRhythm
## A System for Evaluating Accuracy of Rhythm in Recorded Audio

Rhythm an objective element of music and is essential to any great musical performance. It is a skill that a developing musician will focus on as they improve their skills. Private lessons—while immensely beneficial to student musicians—can be quite expensive. Tools such as this can increase equity for music instruction, offering additional evaluational tools to students outside of often pricey private instruction.

The user will provide the system with a .wav file of their performance, BPM, a .png reference sheet music, and a leniency value. The system will convert the sheet music into audio using the given BPM and then compare the two signals. The system will output an accuracy grade and timestamps of mistakes in the user’s performance. When creating an accuracy evaluation, an leniency will be used. If the onset is within the leniency range, the onset will be considered correct. The final evaluation will be a fraction of correct notes and total notes.

### Bibliography
Chin, Francis, and Stephen Wu. “An Efficient Algorithm for Rhythm-Finding.” Computer Music Journal, vol. 16, no. 2, 1992, pp. 35–44. JSTOR, www.jstor.org/stable/3680714. 

Ellis, Daniel (2007). “Beat Tracking by Dynamic Programming.” J. New Music Research, Special Issue on Beat and Tempo Extraction, vol. 36 no. 1, March 2007, pp. 51-60. DOI: 10.1080/09298210701653344, www.ee.columbia.edu/~dpwe/pubs/Ellis07-beattrack.pdf 

Scheirer, Eric D. “Tempo and Beat Analysis of Acoustic Musical Signals.” The Journal of the Acoustical Society of America, vol. 103, no. 1, 1998, pp. 588–601., doi:10.1121/1.421129, https://asa.scitation.org/doi/pdf/10.1121/1.421129?class=pdf.

A. Gkiokas, V. Katsouros, G. Carayannis and T. Stajylakis, "Music tempo estimation and beat tracking by applying source separation and metrical relations," 2012 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Kyoto, 2012, pp. 421-424.
doi: 10.1109/ICASSP.2012.6287906, https://ieeexplore.ieee.org/abstract/document/6287906.
