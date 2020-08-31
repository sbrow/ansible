
; Define games here
GroupAdd, Games, Minecraft

; Code here
#IfWinActive ahk_group Games
LAlt & w::
KeyDown := !KeyDown
If KeyDown
	SendInput {w down}
Else
	SendInput {w up}
Return

LAlt & RButton::
KeyDown := !KeyDown
If KeyDown
	Click, right down
Else
	Click, right up
Return

LAlt & LButton::
KeyDown := !KeyDown
If KeyDown
	Click, left down
Else
	Click, left up
Return

LAlt & LShift::
Pressed := !Pressed
if Pressed
	SendInput {LShift down}
else
	SendInput {LShift up}
return
#IfWinActive

