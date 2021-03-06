
\version "2.18.2"
% automatically converted by musicxml2ly from ./Testing_Data/Ex1.xml

\header {
    encodingsoftware = "MuseScore 2.1.0"
    encodingdate = "2019-03-10"
    composer = algoRhythm
    title = Ex2    }

#(set-global-staff-size 20.0750126457)
\paper {
    paper-width = 21.59\cm
    paper-height = 27.94\cm
    top-margin = 1.0\cm
    bottom-margin = 2.0\cm
    left-margin = 1.0\cm
    right-margin = 1.0\cm
    }
\layout {
    \context { \Score
        autoBeaming = ##f
        }
    }
PartPOneVoiceOne =  {
    \clef "treble" \key c \major \numericTimeSignature\time 4/4 f'8 [ f'8 ]
    f'4 f'16 [f'16 f'8 ] f'8 [f'8] | % 2    
   f'4 f'4 f'16 [f'16 f'16 f'16] f'4| % 3
    f'8. f'16 f'8 [f'8] r8 f'8 f'4| % 4
    f'4 f'4 r8 r16 f'16\tempo 4=80  f'4 \bar "|."    }


% The score definition
\score {
    <<
        \new Staff <<
            \set Staff.instrumentName = "Piano"
            \set Staff.shortInstrumentName = "Pno."
            \context Staff << 
                \context Voice = "PartPOneVoiceOne" { \PartPOneVoiceOne }
                >>
            >>
        
        >>
    \layout {}
    % To create MIDI output, uncomment the following line:
    %  \midi {}
    }

