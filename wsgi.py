from flask import Flask, send_file, request, send_from_directory, make_response
import pymysql
import json
import datetime
from util import guarantee_path_exists
from util import getFileList
import os

# app = Flask(__name__)
app = Flask('production')

def getTimeFromHandInfo(handInfo_string):
    datetime = handInfo_string.split("-")[1][1:].strip()
    yyyymmdd = datetime.split(" ")[0]
    hhmmss = datetime.split(" ")[1]
    left = yyyymmdd.split("/")
    right = hhmmss.split(":")
    time = ""
    for i in range(3):
        time = time + left[i]
    for i in range(3):
        time = time + right[i]
    return time

def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='poker',
        charset='utf8'
    )

def query_mysql_data(data_id):
    conn = get_conn()
    sql = "select * from room where id={}".format(data_id)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()
    result = cursor.fetchall()
    print(result)
    return result

def merge_txt(nickName):
    folder_path = "./data/{}/".format(nickName)
    output_folder_path = "./merged/{}/".format(nickName)
    guarantee_path_exists(output_folder_path)
    file_name = "merged.txt"
    output_file_path = output_folder_path + file_name
    result = open(output_file_path, 'w', encoding='utf-8')
    files = getFileList(folder_path, ".txt")
    file_num = len(files)
    for i in range(file_num):
        file = open(folder_path + files[i], 'r', encoding='utf-8')
        lines = file.readlines()
        result.writelines(lines)
        result.write("\n")

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

@app.route('/query_data/<data_id>', methods=['get'])
def query_data(data_id):
    result = query_mysql_data(data_id)
    result_json = json.dumps(result, cls=DateEncoder)
    print(result_json)
    return result_json

@app.route('/generate_hand', methods=["GET","POST"])
def generate_hand():
    data_bytes = request.data
    # print(data_bytes)
    data_string = str(data_bytes, encoding="utf-8")
    # print(data_string)
    data_json = json.loads(data_string)
    # print(data_json)
    handInfo = data_json['handInfo']
    # print(type(handInfo))
    # print(handInfo)
    nickName = data_json['nickName']
    # print(type(nickName))
    # print(nickName)
    rows_num = len(handInfo)
    handInfo_string = handInfo[0]
    file_name = getTimeFromHandInfo(handInfo_string)
    folder_path = "./data/{}/".format(nickName)
    guarantee_path_exists(folder_path)
    file_path = folder_path + "{}_{}.txt".format(nickName, file_name)
    print("saving hand to {}".format(file_path))
    file = open(file_path, 'w', encoding='utf-8')
    for i in range(rows_num):
        line = handInfo[i]
        if line == "" or line == None:
            pass
        else:
            file.write(line)
    return 'Generate {} Success!!!'.format(file_path)

@app.route('/download_hands/<nickName>', methods=["GET"])
def download_hands(nickName):
    # 将nickName对应的所有txt合并
    merge_txt(nickName)
    data_dir = os.path.join(app.root_path, "merged")
    data_dir = os.path.join(data_dir, nickName)
    fname = f"merged.txt"
    return send_from_directory(data_dir, fname, as_attachment=True)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
