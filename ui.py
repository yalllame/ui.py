from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout


import json



note = {
    "Ласкаво просимо!" : {
        "текст" : "Це найкращий додаток для заміток у світі!",
        "теги" : ["добро", "інструкція"]
    }
}


with open("notes_data.json", "w", encoding="utf-8") as file:
   json.dump(note, file, ensure_ascii=False)



app = QApplication([])


'''Інтерфейс програми'''

notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)



list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')


button_note_create = QPushButton('Створити замітку') 
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')



layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)


col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)





def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "add note", "note name")
    if ok and note_name != "":
            list_notes.addItem(note_name)
            note[note_name] = {"text": "", "tags": []}
            field_text.clear()
            list_tags.clear()
            list_tags.addItem = note[note_name]["tags"]
            print("after add note", note)
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(note, file, ensure_ascii=False)


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        print("deleted note", key)
        del note[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        with open("notes_data.json", "w", encoding="utf-8") as file: # okr metod
            json.dump(note, file, ensure_ascii=False)
        list_notes.addItems(note)
        print("note after delete", note)
    else:
        print("note not taken")

def save_note ():
    if list_notes.selectedItems():
        text = field_text.toPlainText()
        key = list_notes.selectedItems()[0].text()
        note[key]["text"] = text
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(note, file, ensure_ascii=False)
    else:
        print("note not taken")




def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in note[key]["tags"]:
            note[key]["tags"].append(tag)
            list_tags.addItem(tag)
        field_tag.clear()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(note, file, ensure_ascii=False)
    else:
        print("Note not selected!")

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        note[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(note[key]["tags"])
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(note, file, ensure_ascii=False)
    else:
        print("Note not selected!")



def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        field_text.setText(note[key]["text"])
        list_tags.clear()
        list_tags.addItems(note[key]["tags"])



notes_win.show()

with open("notes_data.json", "r", encoding="UTF-8" )as file:
    note = json.load(file)
    print(f"notes onload {note}")
list_notes.addItems(note)


list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
app.exec_()