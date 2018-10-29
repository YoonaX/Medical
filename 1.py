# -*- coding: UTF-8 -*-
import MySQLdb
import jieba.analyse
import os
import json


def get_json(path_list, path_list_, jsons_all_path, f):
    path_list.sort()
    for path in path_list:
        files_path = os.listdir(path)
        i = 0
        for index in files_path:
            index_ = path + "\\" + index
            if os.path.isfile(index_):
                if i < 2:
                    jsons_all_path.append(index_)
                    f.write(index_ + '\n')
                    # notepad.open(index_)
                    # notepad.runMenuCommand("Encoding", "Convert to UTF-8")
                    # notepad.save()
                    # notepad.close()
                    i += 1
            else:
                    path_list_.append(index_)


def extract():
    f = open("file.txt", "w")
    path_list = ["F:\\Ask_Information"]
    path_list_ = []
    jsons_all_path = []

    for i in range(4):
        get_json(path_list, path_list_, jsons_all_path, f)
        path_list.clear()
        path_list = path_list_
        path_list_ = []
        print("-" * 50)
        print("\n")
        print("-" * 50)

    f.close()


def select_add_jieba(cursor, attribute, table):
    sql = "Select %s FROM %s  WHERE (%s != '' && %s != 'NULL')" % (attribute, table, attribute, attribute)
    cursor.execute(sql)
    results = cursor.fetchall()
    for index in results:
        # print(index[0])
        jieba.add_word(index[0], 1)


def count(cursor, attribute, table, value):
    sql1 = "Select count(*) FROM %s  WHERE (%s != '' and %s != 'NULL' and " % (table, attribute, attribute)
    # if(len(value) >= 4):
    #     R = ""
    #     for str in value:
    #         R += str
    #         R += "%"
    #     sql2 = attribute + " like '%" + R + "');"
    # else:
    sql2 = attribute + " = '" + value + "');"
    sql = sql1 + sql2
    cursor.execute(sql)
    results = cursor.fetchall()
    if results[0][0] > 0:
        # print(sql)
        # print(results[0][0])
        return 1

    return 0


def add_jiabe_lexicon():
    db = MySQLdb.connect("localhost", "root", "123456", "medical", charset='utf8')
    cursor = db.cursor()

    select_add_jieba(cursor, "cpNameCn", "atc_omaha")
    select_add_jieba(cursor, "cpNameCn", "atc_yaozh")
    select_add_jieba(cursor, "FrequencyExplain", "atc_yaozh")
    select_add_jieba(cursor,"desease", "icd_10_1")
    select_add_jieba(cursor,"desease", "icd_10_2")
    select_add_jieba(cursor,"desease", "icd_10_3")
    select_add_jieba(cursor,"desease", "icd_10_4")
    select_add_jieba(cursor,"desease", "icd_10_5")
    select_add_jieba(cursor,"operation", "icd_9_1")
    select_add_jieba(cursor,"operation", "icd_9_1")
    select_add_jieba(cursor,"label_zh", "mesh")


if __name__ == '__main__':
    add_jiabe_lexicon()
    db = MySQLdb.connect("localhost", "root", "123456", "medical", charset='utf8')
    cursor = db.cursor()
    i = 0
    Count = 0
    with open("file.txt", "r") as f_read:
        while True:
            lines = f_read.readline()[:-1]
            if not lines:
                break
            # print(lines)
            with open(lines,  encoding='UTF-8') as load_f:
                i += 1
                load_dict = json.load(load_f)
                seg_list1 = jieba.cut(load_dict["description"], cut_all=False)
                seg_list1 = " / ".join(seg_list1)
                print("Description: " + load_dict["description"])
                print("Cut_Description: " + seg_list1)

                words = jieba.posseg.cut(load_dict["description"])
                Count_Medical_Desc1 = 0
                Word_Medical_Desc1 = ""

                Count_Desease_Desc1 = 0
                Word_Desease_Desc1 = ""

                Count_Medical_Reply1 = 0
                Word_Medical_Reply1 = ""

                Count_Desease_Reply1 = 0
                Word_Desease_Reply1 = ""

                Count_Medical_Desc = 0
                Word_Medical_Desc = ""

                Count_Desease_Desc = 0
                Word_Desease_Desc = ""

                Count_Medical_Reply = 0
                Word_Medical_Reply = ""

                Count_Desease_Reply = 0
                Word_Desease_Reply = ""

                for word, flag in words:
                    if flag == 'n':
                        c_m_1 = count(cursor, "cpNameCn", "atc_omaha", word)
                        c_m_2 = count(cursor, "cpNameCn", "atc_yaozh", word)
                        c_m_max = max(c_m_1, c_m_2)
                        if (c_m_max > 0 and (word not in Word_Medical_Desc1)):
                            Word_Medical_Desc1 += (word + " ")
                            Count_Medical_Desc1 += c_m_max

                        c_d_1 = count(cursor, "desease", "icd_10_1", word)
                        c_d_2 = count(cursor, "desease", "icd_10_2", word)
                        c_d_3 = count(cursor, "desease", "icd_10_3", word)
                        c_d_4 = count(cursor, "desease", "icd_10_4", word)
                        c_d_5 = count(cursor, "desease", "icd_10_5", word)
                        c_d_max = max(c_d_1, c_d_2, c_d_3, c_d_4, c_d_5)

                        if (c_d_max > 0 and (word not in Word_Desease_Desc1) ):
                            Word_Desease_Desc1 += (word + " ")
                            Count_Desease_Desc1 += c_d_max

                print("Count_Medical_Des: " + str(Count_Medical_Desc1))
                print("Word_Medical_Desc: " + Word_Medical_Desc1)
                print("Count_Desease_Des: " + str(Count_Desease_Desc1))
                print("Word_Desease_Desc: " + Word_Desease_Desc1)
                print("")

                Reply_Information = []
                for item in load_dict["ask_reply"]:
                    for reply in item["doctor_reply"]:

                        Count_Medical_Reply = 0
                        Word_Medical_Reply = ""

                        Count_Desease_Reply = 0
                        Word_Desease_Reply = ""

                        seg_list = jieba.cut(reply[:-22], cut_all=False)
                        seg_list = " / ".join(seg_list)
                        print("Doctor_reply: " + reply[:-22])
                        print("Cut_Doctor_reply: " + seg_list)

                        words1 = jieba.posseg.cut(reply[:-22])
                        for word, flag in words1:
                            if flag == 'n':
                                c_m_1 = count(cursor, "cpNameCn", "atc_omaha", word)
                                c_m_2 = count(cursor, "cpNameCn", "atc_yaozh", word)
                                c_m_max = max(c_m_1, c_m_2)

                                if ( (c_m_max > 0) and (word not in Word_Medical_Reply) ):
                                    Word_Medical_Reply += (word + " ")
                                    Count_Medical_Reply += c_m_max

                                c_d_1 = count(cursor, "desease", "icd_10_1", word)
                                c_d_2 = count(cursor, "desease", "icd_10_2", word)
                                c_d_3 = count(cursor, "desease", "icd_10_3", word)
                                c_d_4 = count(cursor, "desease", "icd_10_4", word)
                                c_d_5 = count(cursor, "desease", "icd_10_5", word)
                                c_d_max = max(c_d_1, c_d_2, c_d_3, c_d_4, c_d_5)

                                if ( c_d_max > 0 and (word not in Word_Desease_Reply)):
                                    Word_Desease_Reply += (word + " ")
                                    Count_Desease_Reply += c_d_max

                        print("Count_Medical_Reply: " + str(Count_Medical_Reply))
                        print("Word_Medical_Reply: " + Word_Medical_Reply)
                        print("Count_Desease_Reply: " + str(Count_Desease_Reply))
                        print("Word_Desease_Reply:" + Word_Desease_Reply)
                        print(" ")

                        if (Count_Medical_Reply > 0 or Count_Desease_Reply > 0):
                            Reply = {
                                "Doctor_Reply": reply[:-22],
                                "Cut_Doctor_Reply": seg_list,
                                "Count_Medical_Reply": str(Count_Medical_Reply),
                                "Word_Medical_Reply": Word_Medical_Reply,
                                "Count_Desease_Reply": str(Count_Desease_Reply),
                                "Word_Desease_Reply": Word_Desease_Reply,
                            }
                            Reply_Information.append(Reply)

                Cut_Information = {
                    "json_file_name": lines,
                    "Description": load_dict["description"],
                    "Cut_Description": seg_list1,
                    "Count_Medical_Des": str(Count_Medical_Desc1),
                    "Word_Medical_Desc": Word_Medical_Desc1,
                    "Count_Desease_Des": str(Count_Desease_Desc1),
                    "Word_Desease_Desc": Word_Desease_Desc1,
                    "Reply_Information": Reply_Information
                }
                if ( (Count_Medical_Desc1 > 0) or (Count_Desease_Desc1 > 0) or (len(Reply_Information) > 0) ):
                    Count += 1
                    file = open("G:\\json1\\" + str(Count) + ".json", "w", encoding="utf-8")
                    # write data to json
                    json.dump(Cut_Information, file, ensure_ascii=False, indent=4)
                    file.close()
                load_f.close()
    print(i)
    f_read.close()
