from utils.excel_manager import ExcelReader


def test_read_excel():
    reader = ExcelReader("小哈皮家庭教育指导师_高级_学员信息表2_20211218131455.xlsx")
    df = reader.read()
    print(df.columns)
    print(df.data)
