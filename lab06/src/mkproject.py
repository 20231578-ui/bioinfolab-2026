import sys
import os

if len(sys.argv) < 2:
    print("사용법: python3 mkproject.py <프로젝트이름>")
    sys.exit(1)

name = sys.argv[1]

if os.path.isdir(name):
    print("ERROR", name, "Folder exist.")
    sys.exit(1)

os.makedirs(name)
os.makedirs(name + "/data")
os.makedirs(name + "/doc")
os.makedirs(name + "/src")

print("프로젝트 생성 완료:", name)