from UI_seting_black import Ui_Seting_Black
from UI_seting_white import Ui_Seting_White
from black_theme import Ui_MainWindow_Black
from white_theme import Ui_MainWindow_White
from UI_add_command_black import Ui_Add_Command_Black
from UI_add_command_white import Ui_Add_Command_White


set_value = [tuple(i.strip('\n').split('\t')) for i in open('setings.txt').readlines()]

THEME = None
SET_THEME = None
ADD_THEME = None
VOICE = None

if set_value[0][1] == 'black':
    THEME = Ui_MainWindow_Black
elif set_value[0][1] == 'white':
    THEME = Ui_MainWindow_White

if set_value[1][1] == 'man':
    VOICE = 'Artemiy'
elif set_value[1][1] == 'woman' or set_value[1][1] == 'wowoman':
    VOICE = 'Tatiana'

if THEME == Ui_MainWindow_Black:
    SET_THEME = Ui_Seting_Black
elif THEME == Ui_MainWindow_White:
    SET_THEME = Ui_Seting_White
if THEME == Ui_MainWindow_Black:
    ADD_THEME = Ui_Add_Command_Black
elif THEME == Ui_MainWindow_White:
    ADD_THEME = Ui_Add_Command_White
print(set_value)


def recognize():
    import speech_recognition as sr

    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print('sda')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    q = r.recognize_google(audio, language='ru-RU')
    return q