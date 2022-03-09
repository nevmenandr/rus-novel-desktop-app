#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import re
import tkinter as tk


HEAD1 = '''<?xml version='1.0' encoding='utf-8'?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">
 <teiHeader>
  <fileDesc>
   <titleStmt>
    <title xml:id="Вставить_идентификатор">Вписать название романа. Электронная версия</title>
    <title type="sub">Вписать подзаголовок</title>
     <author>
       <persName>
         <forename>Имя автора</forename>
         <forename type="patronym">Отчество автора</forename>
         <surname>Фамилия автора</surname>
        </persName>
     </author>
     <respStmt>
       <resp>
         Подготовка текста
       </resp>
       <name>Вставить имя студента, который готовил или менял текст</name>
     </respStmt>
     <funder>
       Проект «Корпус русского романа» ФГН НИУ ВШЭ 
       </funder>
     <respStmt>
       <resp>
         Руководители проекта
       </resp>
       <name>
         А. В. Вдовин, А. А. Бонч-Осмоловская, Б. В. Орехов, К. А. Маслинский
       </name>
     </respStmt> 
     <respStmt>
       <resp>
         Участники проекта
       </resp>
       <name>
         И.И. Бендерский, Андрей Люстров, Анастасия Олещук, Дарья Челнокова, Злата Климас, Дарья Никифорова, Алина Турыгина
       </name>
     </respStmt>
     </titleStmt>
   <publicationStmt>
    <publisher>
     <orgName>
      Факультет Гуманитарных Наук НИУ ВШЭ
     </orgName>
    </publisher>
    <availability>
      <p>Текст представляет собой всеобщее достояние</p>
    </availability>
   </publicationStmt>
   <sourceDesc>
'''

HEAD_BOOK = '''      <bibl>
      <author>
       <name>Вставить имя автора романа</name>
      </author>
      <title type="main">Вставить название романа</title>
        <title type="sub">Вставить субтитл</title>
       <pubPlace>Вставить город публикации</pubPlace>
       <publisher>Вставить название издательства (Например: Государственное издательство "Художественная литература")</publisher>
       <date when="(вставить год публикации)" />
    </bibl>
'''

HEAD_JOURNAL = '''     <bibl>
       <author>Вставить имя автора романа</author>
       <title type="main" level="a">Вставить название романа</title>
       <title type="sub">Вставить субтитл</title>
       <title level="j">Вставить название журнала</title>
      <biblScope unit="volume">Вставить номер журнала</biblScope>
       <date when="(вставить год и месяц (YEAR))" />
     </bibl>
'''

HEAD3 = '''   </sourceDesc>
  </fileDesc>'''

encodingDesc = '''
   <encodingDesc>
     <classDecl>
     <taxonomy>
CAT_S
CAT_N
       </taxonomy>
       </classDecl>
  </encodingDesc>'''

SEXM = '''
        <category ana="M">
            <catDesc>пол автора произведения мужской</catDesc>
        </category>'''

SEXF = '''
        <category ana="F">
            <catDesc>пол автора произведения женский</catDesc>
        </category>'''

NARR1 = '''
       <category ana="narr1">
        <catDesc>написано от первого лица</catDesc>
       </category>'''

NARR3 = '''
       <category ana="narr3">
         <catDesc>написано от третьего лица</catDesc>
       </category>'''

profileDesc = '''
  <profileDesc>
   <creation>
    <date when="Вставить год создания">Вставить год создания</date>
    <rs type="country">
     Россия
    </rs>
   </creation>'''

textClass = '''
    <textClass>
    <catRef ana="Вставить идентификатор пола или пропустить"></catRef>
    <catRef ana="Вставить идентификатор наррации или пропустить"></catRef>
   </textClass>
'''

HEAD7 = '  </profileDesc>'

HEAD8 = '''
  <revisionDesc>
    <change when="YEAR-MM-DD">Оформление в XML-формате, РАЗМЕТЧИК</change>
  </revisionDesc> 
 </teiHeader>
 <text>
   <body>
     <p>Текст</p>
  </body>
 </text>
</TEI>
'''

def months_former(d):
    d = str(d)
    if len(d) < 2:
        d = '0{}'.format(d)
    return d

PUBL_TYPE = [
    "Отдельная книга",
    "Журнал"
] 

MONTHS = [months_former(x) for x in range(13)]

SEX = ['неизвестно', 'M', 'F']

NARRATION = ['неизвестно', 'narr3', 'narr1']

selection = PUBL_TYPE[0]
selection_month = MONTHS[0]
selection_sex = SEX[0]
selection_narr = NARRATION[0]

def check_main(name, fname, title, markup_name, biblio_name, biblio_title,
        biblio_year, input_filename):
    empty_fields = []
    if not name:
        empty_fields.append('Фамилия автора')
    elif not re.search('[А-Я]', name):
        empty_fields.append('Фамилия автора кириллицей с прописной буквы')
    if not fname:
        empty_fields.append('Имя автора')
    if not title:
        empty_fields.append('Название романа')
    if not markup_name:
        empty_fields.append('Ваше имя')
    if not biblio_name:
        empty_fields.append('Автор (в библиографическом описании)')
    if not biblio_name:
        empty_fields.append('Название романа (в библиографическом описании)')
    if not biblio_year:
        empty_fields.append('Год (в библиографическом описании)')
    elif not re.search('1[789][0-9]{2}', biblio_year):
        empty_fields.append('Год (в библиографическом описании) в формате YYYY, например, 1875')
    if not input_filename:
        empty_fields.append('Имя файла с текстом романа')
    return empty_fields


def check_book(biblio_place):
    empty_fields = []
    if not biblio_place:
        empty_fields.append('Место издания книги')
    return empty_fields


def check_journal(journal, number):
    empty_fields = []
    if not journal:
        empty_fields.append('Название журнала, в котором опубликован роман')
    if not number:
        empty_fields.append('Номер журнала')
    elif not re.search('([0-9]+)|([CXVI])', number):
        empty_fields.append('Номер журнала (цифра)')
    return empty_fields


def change_type(select):
    global selection
    selection = select


def change_month(select):
    global selection_month
    selection_month = select


def change_sex(select):
    global selection_sex
    selection_sex = select


def change_narration(select):
    global selection_narr
    selection_narr = select


def errors_display(title, message):
    window = tk.Tk()
    window.title(title)
    errors = tk.Label(window, text=message)
    errors.pack()
    window.mainloop()


def id_maker(name, fname, title, biblio_year):
    symbols = ("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
        (*list('abvgdee'), 'zh', *list('zijklmnoprstuf'), 'kh', 'z', 'ch', 'sh', 'sh', '',
        'y', '', 'e', 'yu','ya', *list('ABVGDEE'), 'ZH', 
        *list('ZIJKLMNOPRSTUF'), 'KH', 'Z', 'CH', 'SH', 'SH', *list('_Y_E'), 'YU', 'YA', ' '))
    
    coding_dict = {source: dest for source, dest in zip(*symbols)}
    translate = lambda x: ''.join([coding_dict[i] for i in x])
    
    name = translate(name.lower())
    fname = translate(fname.lower()[0])
    title = translate(title.lower())
    title = title.replace(' ', '_')
    id = '{}_{}_{}_{}'.format(name, fname, title, biblio_year)
    return id


def xml_former_book(biblio_name, biblio_title, biblio_sub, biblio_year,
        biblio_place):
    xml = HEAD_BOOK.replace('Вставить имя автора романа', biblio_name)
    xml = xml.replace('Вставить название романа', biblio_title)
    if biblio_sub:
        xml = xml.replace('Вставить субтитл', biblio_sub)
    else:
        xml = xml.replace('\n        <title type="sub">Вставить субтитл</title>', '')
    xml = xml.replace('Вставить город публикации', biblio_place)
    xml = xml.replace('(вставить год публикации)', biblio_year)
    return xml


def xml_former_journal(biblio_name, biblio_title, biblio_sub, biblio_year,
        journal, number):
    xml = HEAD_JOURNAL.replace('Вставить имя автора романа', biblio_name)
    xml = xml.replace('Вставить название романа', biblio_title)
    if biblio_sub:
        xml = xml.replace('Вставить субтитл', biblio_sub)
    else:
        xml = xml.replace('\n       <title type="sub">Вставить субтитл</title>', '')
    xml = xml.replace('Вставить название журнала', journal)
    xml = xml.replace('Вставить номер журнала', number)
    xml = xml.replace('(вставить год и месяц (YEAR))', biblio_year)
    return xml


def encoding_desc():
    if selection_sex == 'M':
        xml = encodingDesc.replace('\nCAT_S', SEXM)
    elif selection_sex == 'F':
        xml = encodingDesc.replace('\nCAT_S', SEXF)
    else:
        xml = encodingDesc.replace('\nCAT_S', '')

    if selection_narr == 'narr1':
        xml = xml.replace('\nCAT_N', NARR1)
    elif selection_narr == 'narr3':
        xml = xml.replace('\nCAT_N', NARR3)
    else:
        xml = xml.replace('\nCAT_N', '')
    return xml


def text_class():
    global selection_sex
    global selection_narr
    
    selection_sex = str(selection_sex)
    selection_narr = str(selection_narr)
    
    if selection_sex == 'неизвестно':
        xml = textClass.replace('\n    <catRef ana="Вставить идентификатор пола или пропустить"></catRef>', '')
    elif selection_sex == 'M':
        xml = textClass.replace('Вставить идентификатор пола или пропустить', selection_sex)
    elif selection_sex == 'F':
        xml = textClass.replace('Вставить идентификатор пола или пропустить', selection_sex)
    else:
        xml = textClass.replace('\n    <catRef ana="Вставить идентификатор пола или пропустить"></catRef>', '')
        
    if selection_narr == 'неизвестно':
        xml = xml.replace('\n    <catRef ana="Вставить идентификатор наррации или пропустить"></catRef>', '')
    elif selection_narr == 'narr1':
        xml = xml.replace('Вставить идентификатор наррации или пропустить', selection_narr)
    elif selection_narr == 'narr3':
        xml = xml.replace('Вставить идентификатор наррации или пропустить', selection_narr)
    else:
        xml = xml.replace('\n    <catRef ana="Вставить идентификатор наррации или пропустить"></catRef>', '')
    return xml


def text_process(input_filename):
    if not os.path.exists(input_filename):
        errors_display('Ошибка файла', '\n\nФайла с таким именем в этой директории нет\n\n')
    else:
        try:
            with open(input_filename, encoding='utf-8') as f:
                text = f.read()
        except:
            text = ''
        if not text:
            try:
                with open(input_filename, encoding='cp1251') as f:
                    text = f.read()
            except:
                text = ''
        if not text:
            errors_display('Ошибка файла', '\n\nФайл должен быть в формате txt и кодировке UTF-8\n\n')
        else:
            text = text.replace('&', '&amp;')
            return text
    

def xml_former(id, title, subtitle, name, fname, pname, markup_name, biblio_name,
            biblio_title, biblio_sub, biblio_year, biblio_place, journal,
            number, year_creation, input_filename, current_year, current_month,
            current_day):
    head1 = HEAD1.replace('Вставить_идентификатор', id)
    head1 = head1.replace('Вписать название романа', title)
    if subtitle:
        head1 = head1.replace('Вписать подзаголовок', subtitle)
    else:
        head1 = head1.replace('\n    <title type="sub">Вписать подзаголовок</title>', '')
    head1 = head1.replace('Фамилия автора', name)
    head1 = head1.replace('Имя автора', fname)
    if pname:
        head1 = head1.replace('Отчество автора', pname)
    else:
        head1 = head1.replace('\n            <forename type="patronym">Отчество автора</forename>', '')
    head1 = head1.replace('Вставить имя студента, который готовил или менял текст', markup_name)
    
    if selection == 'Журнал':
        head2 = xml_former_journal(biblio_name, biblio_title, biblio_sub, biblio_year, journal, number)
    else:
        head2 = xml_former_book(biblio_name, biblio_title, biblio_sub, biblio_year, biblio_place)
        
    if selection_sex != 'неизвестно' or selection_narr != 'неизвестно':
        head4 = encoding_desc()
    else:
        head4 = ''
    
    if year_creation:
        head5 = profileDesc.replace('Вставить год создания', year_creation)
    else:
        head5 = profileDesc.replace('\n    <date when="Вставить год создания">Вставить год создания</date>', '')
    
    if selection_sex != 'неизвестно' or selection_narr != 'неизвестно':
        head6 = text_class()
    else:
        head6 = ''
    
    text = text_process(input_filename)
    
    head8 = HEAD8.replace('РАЗМЕТЧИК', markup_name)
    head8 = head8.replace('YEAR', str(current_year))
    head8 = head8.replace('MM', months_former(current_month))
    head8 = head8.replace('DD', months_former(current_day))
    head8 = head8.replace('Текст', text)
    
    return '{}{}{}{}{}{}{}{}'.format(head1, head2, HEAD3, head4, head5, head6, HEAD7, head8)
    

def collect_data(name, fname, pname, title, subtitle, markup_name, biblio_name,
        biblio_title, biblio_sub, biblio_year, biblio_place, journal, number,
        year_creation, input_filename, current_year, current_month, current_day):
    
    empty_fields = check_main(name, fname, title, markup_name, biblio_name,
        biblio_title, biblio_year, input_filename)
    
    if selection == "Журнал":
        empty_fields.extend(check_journal(journal, number))
    else:
        empty_fields.extend(check_book(biblio_place))
    
    if empty_fields:
        errors_display('Ошибки разметки', '\n\nВы не заполнили следующие обязательные поля: \n\n' + ',\n'.join(empty_fields))
    else:
        id = id_maker(name, fname, title, biblio_year)
        xml = xml_former(id, title, subtitle, name, fname, pname, markup_name,
            biblio_name, biblio_title, biblio_sub, biblio_year, biblio_place,
            journal, number, year_creation, input_filename,
            current_year, current_month, current_day)
    
    with open('{}.xml'.format(id), "w", encoding='utf-8') as output_file:
        output_file.write(xml)
    
    errors_display('Результат', '\n\nРезультат сохранен \nв файл {}.xml\n\n'.format(id))


def main():
    
    global selection
    global selection_month
    global selection_sex
    global selection_narr
    
    root = tk.Tk()
    root.title('Разметка романа')
    canvas = tk.Canvas(root, width=1100, height=750, bg='#ADD8E6') # настройки холста
    canvas.create_text(150, 40, text='Введите ниже информацию о романе.\nПоля со звездочками обязательны.\nВ остальных случаях, если неизвестно,\nможно оставить пустым', fill='white') # где и какой текст
    
    label_name = tk.Label(root, text='*Фамилия автора')
    label_name.place(x=10, y=80)
    
    entry_name = tk.Entry(root) # поле ввода
    entry_name.place(x=150, y=80) # где
    
    label_fname = tk.Label(root, text='*Имя автора')
    label_fname.place(x=10, y=110)
    
    entry_fname = tk.Entry(root) 
    entry_fname.place(x=150, y=110) 
    
    label_pname = tk.Label(root, text='Отчество автора')
    label_pname.place(x=10, y=140)
    
    entry_pname = tk.Entry(root) 
    entry_pname.place(x=150, y=140) 
    
    label_title = tk.Label(root, text='*Название романа')
    label_title.place(x=10, y=170)
    
    entry_title = tk.Entry(root) 
    entry_title.place(x=150, y=170) 
    
    label_subtitle = tk.Label(root, text='Подзаголовок')
    label_subtitle.place(x=10, y=200)
    
    entry_subtitle = tk.Entry(root) 
    entry_subtitle.place(x=150, y=200) 
    
    label_markup = tk.Label(root, text='*Ваше имя')
    label_markup.place(x=10, y=230)
    
    entry_markup = tk.Entry(root) 
    entry_markup.place(x=150, y=230) 
    
    label_type = tk.Label(root, text = "*Тип публикации")
    label_type.place(x=10, y=260)
    
    selection = tk.StringVar(root)
    selection.set(PUBL_TYPE[0])
    
    opt = tk.OptionMenu(root, selection, *PUBL_TYPE, command=change_type)
    opt.place(x=150, y=260)
    
    canvas.create_text(130, 330, text='Вводите информацию ниже \nкак в печатном источнике.\nЭто библиографическое описание', fill='white') 
    
    label_name_biblio = tk.Label(root, text='*Автор')
    label_name_biblio.place(x=10, y=360)
    
    entry_name_biblio = tk.Entry(root)
    entry_name_biblio.place(x=150, y=360)
    
    label_title_biblio = tk.Label(root, text='*Название')
    label_title_biblio.place(x=10, y=390)
    
    entry_title_biblio = tk.Entry(root) 
    entry_title_biblio.place(x=150, y=390) 
    
    label_subtitle_biblio = tk.Label(root, text='Подзаголовок')
    label_subtitle_biblio.place(x=10, y=420)
    
    entry_subtitle_biblio = tk.Entry(root) 
    entry_subtitle_biblio.place(x=150, y=420) 
    
    label_year_biblio = tk.Label(root, text='*Год публикации')
    label_year_biblio.place(x=10, y=450)
    
    entry_year_biblio = tk.Entry(root) 
    entry_year_biblio.place(x=150, y=450) 
    
    canvas.create_text(90, 490, text='Для отдельной книги', fill='white') 
    
    label_place_biblio = tk.Label(root, text='Город')
    label_place_biblio.place(x=10, y=510)
    
    entry_place_biblio = tk.Entry(root) 
    entry_place_biblio.place(x=150, y=510) 
    
    
    canvas.create_text(55, 550, text='Для журнала', fill='white') 
    
    label_journal_biblio = tk.Label(root, text='Журнал')
    label_journal_biblio.place(x=10, y=570)
    
    entry_journal_biblio = tk.Entry(root) 
    entry_journal_biblio.place(x=150, y=570) 
    
    label_number_biblio = tk.Label(root, text='Номер')
    label_number_biblio.place(x=10, y=600)
    
    entry_number_biblio = tk.Entry(root) 
    entry_number_biblio.place(x=150, y=600) 
    
    
    label_year_creation = tk.Label(root, text='Год создания')
    label_year_creation.place(x=10, y=670)
    
    entry_year_creation = tk.Entry(root) 
    entry_year_creation.place(x=150, y=670) 
    
    label_text_box = tk.Label(root, text='Введите имя файла, из которого \
нужно взять текст романа. \nФайл должен быть в формате .txt и лежать \
в той же папке, что и эта программа.\nБудьте внимательны, файловые \
менеджеры часто скрывают расширение файла, \nно его всё равно нужно указать')
    label_text_box.place(x=400, y=10)
    
    entry_input = tk.Entry(root) 
    entry_input.place(x=500, y=110) 
    
    
    label_sex = tk.Label(root, text = "Пол автора")
    label_sex.place(x=400, y=320)
    
    selection_sex = tk.StringVar(root)
    selection_sex.set(SEX[0])
    
    opt_sex = tk.OptionMenu(root, selection_sex, *SEX, command=change_sex)
    opt_sex.place(x=650, y=320)
    
    
    label_narr = tk.Label(root, text = "Повествование (от 1 или 3 лица)")
    label_narr.place(x=400, y=370)
    
    selection_narr = tk.StringVar(root)
    selection_narr.set(NARRATION[0])
    
    opt_narr = tk.OptionMenu(root, selection_narr, *NARRATION, command=change_narration)
    opt_narr.place(x=650, y=370)
    
    
    canvas.pack() # заставляет работать canvas
    
    
    current_datetime = datetime.now()
    
    btn_calc = tk.Button(root, text='Нажмите сюда, когда все \nполя будут заполнены')
    btn_calc.bind('<Button-1>', lambda event: collect_data(entry_name.get().strip(),
        entry_fname.get().strip(), entry_pname.get().strip(),
        entry_title.get().strip(), entry_subtitle.get().strip(),
        entry_markup.get().strip(), entry_name_biblio.get().strip(),
        entry_title_biblio.get().strip(), entry_subtitle_biblio.get().strip(),
        entry_year_biblio.get().strip(), entry_place_biblio.get().strip(),
        entry_journal_biblio.get().strip(), entry_number_biblio.get().strip(),
        entry_year_creation.get().strip(), entry_input.get().strip(),
        current_datetime.year, current_datetime.month, current_datetime.day)) # получаем значение 
    btn_calc.place(x=800, y=550)
    
    root.mainloop() # открывает окно
    
    return 0


if __name__ == '__main__':
    main()
