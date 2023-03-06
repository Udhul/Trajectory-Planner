#__________________________________________________________________________________________________________
#------ Requirements -------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
import PySimpleGUI as sg
import json
import serial



#---Header
FONT_TOP_BLOCK = 'verdana 16'
COLOR_TOP_BG = 'blue'
PAD_BLOCK_TOP       = (0,0)

#---Footer
PAD_BLOCK_BOTTOM    = (0,0)
COLOR_BOTTOM_BG = 'dark blue'

#---Start window
SIZE_BLOCK_START = (512,256)
NAME_WINDOW_START = 'CNC Trajectory Planner: Connect to Controller'

#__________________________________________________________________________________________________________
#------ Startup Window ------------------------------------------------------------------------------------>
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def window_start():
    #---Top Block
    block_top = [
        [
            sg.Column([
                [sg.Text('CNC Trajectory Planner', font=FONT_TOP_BLOCK, text_color='black', border_width=5, background_color=COLOR_TOP_BG)]
            ], element_justification='c', background_color=COLOR_TOP_BG, pad=(PAD_BLOCK_TOP), expand_x=True)
        ],
    ]

    #---Bottom Block
    block_bottom = [
        [
            sg.Column([
                #---Navigation buttons
                [
                    sg.Button('Connect', size=20),
                    sg.Sizer(50,1),
                    sg.Button('Exit', size=20),
                ],
            ], element_justification='c', background_color=COLOR_BOTTOM_BG, pad=PAD_BLOCK_BOTTOM, expand_x=True)
        ],
    ]


    block_body = [
        [
        sg.Input('115200', key='start/baudrate', tooltip=' Type Baud Rate'),
        sg.Input('0', key='start/port', tooltip=' Type Port Number')
        ],

        # Separator
        [
            sg.HorizontalSeparator()
        ],

        # 
        [
        ],
    ]


    #---Define layout
    layout = [
        [block_top],
        [sg.Column(block_body, size=SIZE_BLOCK_START, background_color='grey', pad=(0,0))],
        [block_bottom]
    ]

    window = sg.Window(NAME_WINDOW_START, layout, modal=True, element_padding=(0,0), keep_on_top=True, no_titlebar=True)

    #---Reset event flags
    proceed = False
    
    #---Defines
    # ser = serial.Serial()

    #---Window Main Loop
    while True:
        #---Open connect window
        event, values = window.read()

        #---Window close check
        if event == "Exit" or event == "Cancel" or event == sg.WIN_CLOSED:
            break

        #---Connect click event
        if event == "Connect":
            # ser.baudrate = values['start/baudrate']
            # ser.port = values['start/port']
            # ser.open()

            proceed = True
            break

    window.close()
    if proceed: window_main()



#__________________________________________________________________________________________________________
#------ Main Window --------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def window_main():
    ...



#__________________________________________________________________________________________________________
#------ Main loop ----------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
def main():
    window_start()



#__________________________________________________________________________________________________________
#------ Run main loop ------------------------------------------------------------------------------------->
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
if __name__ == '__main__':
    main()