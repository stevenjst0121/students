## Summary

The tool helps to read into a downloaded registration spread sheet from JSJ, and convert the profile picture file names according to the register's Name or ID.

## How To Run

- Make sure `python3` is installed from https://www.python.org/downloads/
- Install `pandas` and `openpyxl` by running
```bash
python3 -m pip install pandas
python3 -m pip install openpyxl
```
- Run the `profile_pic_name_converter.py` file
```bash
cd students
python3 tasks/profile_pic_name_converter.py
```

## Data Input

The application expects the `data` folder to look like the following:
```txt
data
|- jsj_data.xlsx
|- pictures
    |- *.jpg
    |- *.jpeg
    |- ...
```

## Requirements

1、以身份证为关键字删除重复项
 保留有照片且序号最大的项

2、创建两个文件夹
文件夹1：
源文件夹：照片
源文件名：“2寸蓝底照片”列中的文字列
目标文件夹：照片-身份证
目标文件名：身份证号.jpg

文件夹2：
源文件夹：照片
源文件名：“2寸蓝底照片”列中的文字列
目标文件夹：照片-身份证
目标文件名：姓名身份证号.jpg
