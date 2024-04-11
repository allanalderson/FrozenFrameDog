Setup:
vMix should have the the main input as Input 1. This input will be checked for frozen frames.
vMix should have the secondary input as Input 2. This input will be selected if a frozen frame is detected.
vMix should have Input 1 sent as an NDI output.
vMix should have a shortcut that responds to keystroke 2 with QuickPlay to Input 2.
NDI Tools webcam vMix Input 1 should be selected as NDI webcam 1. 

If vMix input 2 is a SINGLE GRAPHIC, configure its trigger: OnTransitionIn, CutDirect, Input 1, Delay(5000mS)
If vMix input 2 is a SINGLE VIDEO, configure its trigger: OnCompletion, CutDirect, Input 1.
If vMix input 2 is a PHOTOS FOLDER, configure its trigger: OnTransitionIn, QuickPlay, Input 2 AND OnCompletion, CutDirect, Input 1.
If vMix input 2 is a LIST OF VIDEOS, configure its trigger: OnTransitionIn, SelectIndex, Input 2, Delay 0, Value 1 AND OnCompletion, CutDirect, Input 1.

vMix General settings should be Automatically mix audio