import pandas as pd
import pygsheets
import glob
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

# Google Sheets 授權
key = "/Users/chenyaoxuan/Desktop/myproject/marketProject/astute-harmony-425407-p9-826d675d86f9.json"
gc = pygsheets.authorize(service_file=key)
url = "https://docs.google.com/spreadsheets/d/1DsltZgJorvsgEVJnRAJ6NSR17PpNFYwN8RmJmGjiYWw/edit#gid=381406896"
sheet = gc.open_by_url(url)
wks = sheet[0]

# 讀取數據的文件夾路徑
folder_path = '/Users/chenyaoxuan/Desktop/myproject/marketProject/marketExcel/'
market_files = glob.glob(folder_path + '*.xlsx') + glob.glob(folder_path + '*.xls')

user_data = {
    "d51gtsdkij": {"003": "鐘維嘉"},
    "575r0skk49": {"004(黃士嘉)": "黃士嘉"},
    "chi6na8": {"004(許嘉傑)": "許嘉傑"},
    "fctjhc9fvo": {"006": "胡勝斐"},
    "pingfan_0320": {"013": "廖子萍"},
    "2ihsyc3mrq": {"015": "賴宗成"},
    "qdtfdj4asx": {"022": "蕭喬文"},
    "tookls01": {"027": "王緯德"},
    "csherswa": {"034": "趙偉廷"},
    "0l19pqrp8s": {"042": "劉漢成"},
    "gyk9k3og52": {"043": "陳冠華"},
    "ruili888": {"044": "蕭兆揚"},
    "f0ylv571rl": {"045": "李崇恺"},
    "scxt7aw8ic": {"053": "沈安培"},
    "_2_r71g7fi": {"061": "李識智"},
    "km52cd0j8a": {"063": "洪楷琳"},
    "cr9qpc0org": {"064": "阮羿勲"},
    "irerghmt0p": {"076": "沈政彥"},
    "29bije5j5k": {"079": "張庭語"},
    "li5wdw27p1": {"082": "吳祥瑋"},
    "nnpythqs51": {"083": "潘楷元"},
    "fo8l6z5o3p": {"085": "王俊凱"},
    "qgo3uvja8e": {"104": "饒傑華"},
    "6wpf6cem28": {"110": "李耕宇"},
    "mvb3e87s63": {"117": "洪健欽"},
    "kgxeetqg20": {"120": "蔡榮璜"},
    "magical_store": {"121": "林顯明"},
    "z7tfd2a_7f": {"129": "張文騰"},
    "5v5mkughjk": {"156": "賴慧淑"},
    "kf_1ky5z1m": {"161": "陳冠霖"},
    "j401zjn1zq": {"162": "蔡阜澄"},
    "0lleyve_zl": {"163": "劉彥詢"},
    "j3hp3kxofz": {"167": "邱瓊葦"},
    "jxz4dpuvi6": {"169": "李政恩"},
    "kf8g90s8vt": {"170": "黃鈺寶"},
    "mufz9f1hkj": {"171": "黃喻鎂"},
    "lfb21qr8x1": {"184": "邱淮蔓"},
    "rhkwlcjotf": {"189": "盧錦名"},
    "nz7e0khlio": {"193": "陳清白"},
    "klo4ayncfj": {"197": "徐昀伶"},
    "35f425rlqd": {"198": "張嘉玲"},
    "mr_3i5jljz": {"205": "曾韋綸"},
    "heimaostjk666": {"212": "董志忠"},
    "bnczq9jjne": {"230": "陳建良"},
    "mie5793": {"231": "曾崝豪"},
    "vsnkyse708": {"235": "劉祥慶"},
    "cmychal": {"237": "姜禹彤"},
    "kp1usft_6x": {"240": "張文彰"},
    "u_gepzjb3x": {"254": "柯英丞"},
    "6udpyyp72u": {"256": "林紓戎"},
    "4ildmehv0p": {"258": "林斯珮"}
}

# 初始化數據字典
market_data = {}

# 讀取每個 Excel 文件並處理數據
for file in market_files:
    df = pd.read_excel(file)
    data_list = df.values.tolist()

    market_acc = data_list[4][1]
    market_details = data_list[17:]
    result = []

    # 處理每一筆市場細節
    for detail in market_details:
        if detail[1] == '已提款金額' and detail[4] == '支出' and detail[6] != '失敗':
            date = detail[0][:10].replace('-', '/')  # 轉換日期格式
            amount = abs(detail[5])  # 確保金額為正數
            result.append([date, amount])

    # 將結果排序並存儲於字典
    market_data[market_acc] = sorted(result, key=lambda x: x[0])

# 清空工作表
wks.clear()

# 调整工作表大小
wks.resize(rows=None, cols=len(market_data)*5)

# 創建格式化模板
gray_background = pygsheets.Cell('A1')
gray_background.color = (0.8, 0.8, 0.8)
gray_background.set_text_format('fontSize', 12)
gray_background.set_text_format('bold', True)
gray_background.set_text_format('fontFamily', 'Arial')
gray_background.horizontal_alignment = pygsheets.HorizontalAlignment.CENTER
gray_background.vertical_alignment = pygsheets.VerticalAlignment.MIDDLE

red_text = pygsheets.Cell('A1')
red_text.set_text_format('foregroundColor', {'red': 1, 'green': 0, 'blue': 0})
red_text.set_text_format('fontSize', 12)
red_text.set_text_format('bold', True)
red_text.set_text_format('fontFamily', 'Arial')
red_text.horizontal_alignment = pygsheets.HorizontalAlignment.CENTER
red_text.vertical_alignment = pygsheets.VerticalAlignment.MIDDLE

blue_text = pygsheets.Cell('A1')
blue_text.set_text_format('foregroundColor', {'red': 0, 'green': 0, 'blue': 1})
blue_text.set_text_format('fontSize', 12)
blue_text.set_text_format('bold', True)
blue_text.set_text_format('fontFamily', 'Arial')
blue_text.horizontal_alignment = pygsheets.HorizontalAlignment.CENTER
blue_text.vertical_alignment = pygsheets.VerticalAlignment.MIDDLE

normal_template = pygsheets.Cell('A1')
normal_template.set_text_format('fontSize', 12)
normal_template.set_text_format('bold', True)
normal_template.set_text_format('fontFamily', 'Arial')
normal_template.horizontal_alignment = pygsheets.HorizontalAlignment.CENTER
normal_template.vertical_alignment = pygsheets.VerticalAlignment.MIDDLE

# 計算需要格式化的列數
cols_to_format = len(market_data) * 5

# 批量應用格式
for col in range(1, cols_to_format + 1):
    col_mod = (col - 1) % 5

    start_addr = pygsheets.format_addr((1, col))
    end_addr = pygsheets.format_addr((2, col))
    head_format = pygsheets.datarange.DataRange(start=start_addr, end=end_addr, worksheet=wks)
    head_format.apply_format(normal_template)

    start_addr = pygsheets.format_addr((3, col))
    end_addr = pygsheets.format_addr((4, col))
    head02_format = pygsheets.datarange.DataRange(start=start_addr, end=end_addr, worksheet=wks)

    start_addr = pygsheets.format_addr((3, col))
    end_addr = pygsheets.format_addr((1000, col))
    body_format = pygsheets.datarange.DataRange(start=start_addr, end=end_addr, worksheet=wks)

    start_addr = pygsheets.format_addr((1, col))
    end_addr = pygsheets.format_addr((1000, col))

    if col_mod == 0 or col_mod == 2:   # A, C, F, H...
        body_format.apply_format(gray_background)
    elif col_mod == 1:  # B, G...
        body_format.apply_format(red_text)
    elif col_mod == 3:  # D, I...
        body_format.apply_format(blue_text)
    elif col_mod == 4:  # E, J...
        body_format.apply_format(normal_template)
    # 為每一列添加四周邊框
    head_format.update_borders(top=True, bottom=True, left=True, right=True, style='SOLID')
    head02_format.update_borders(top=True, bottom=True, left=True, right=True, style='SOLID')
    body_format.update_borders(top=True, bottom=True, left=True, right=True, style='SOLID')


# 設定初始位置
start_col = 1

# 寫入數據
for account, details in market_data.items():
    print(user_data[account].values())
    if account in user_data:
        # 寫入用戶編號和名稱
        user_info = user_data[account]
        wks.update_value((1, start_col), list(user_info.keys())[0])
        wks.update_value((2, start_col), list(user_info.values())[0])
        
        # 寫入標題和公式
        wks.update_value((3, start_col), '總計')
        sum_formula = f"=SUM({chr(64 + start_col + 1)}5:{chr(64 + start_col + 1)}1000)"
        wks.update_value((3, start_col + 1), sum_formula)
        wks.update_value((4, start_col), '日期')
        wks.update_value((4, start_col + 1), '轉出')
        
        row = 5
        # 寫入日期和金額
        for date, amount in details:
            wks.update_value((row, start_col), date)
            wks.update_value((row, start_col + 1), amount)
            row += 1
        
        # 加入額外的標題和公式
        wks.update_value((3, start_col + 2), '總計')
        sum_formula_in = f"=SUM({chr(64 + start_col + 3)}5:{chr(64 + start_col + 3)}1000)"
        wks.update_value((3, start_col + 3), sum_formula_in)
        wks.update_value((4, start_col + 2), '日期')
        wks.update_value((4, start_col + 3), '轉入')
        wks.update_value((3, start_col + 4), '備註')  

        # 合併儲存格
        wks.merge_cells(start=f'{chr(64 + start_col)}1', end=f'{chr(64 + start_col + 4)}1', merge_type='MERGE_ALL')
        wks.merge_cells(start=f'{chr(64 + start_col)}2', end=f'{chr(64 + start_col + 4)}2', merge_type='MERGE_ALL')  
        wks.merge_cells(start=f'{chr(64 + start_col + 4)}3', end=f'{chr(64 + start_col + 4)}4', merge_type='MERGE_ALL')
        
        # 移動到右邊五列
        start_col += 5
        
# 凍結前四列
wks.frozen_rows=4

print("數據寫入完成！")