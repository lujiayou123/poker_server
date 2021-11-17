# a = "admin_2021111715513.txt".split(".")[0].split("_")[1].strip()
# b = "admin_2021120115513.txt".split(".")[0].split("_")[1].strip()
# print(a)
# print(b)
# print(b > a)

from util import getFileList
files = getFileList("./data/admin", ".txt")
print(files)