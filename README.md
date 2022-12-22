591 租屋網爬蟲-台中地區
==================

## 說明
自 591租屋網 下載台中地區所有租屋物件的數據


## 使用方式
### 安裝
1. 先 clone 一份 repo 至本地端
```sh
git clone https://github.com/looies/crawler591.git
```

2. 執行 pip install

```bash
pip install -r requirements.txt
```

3. log 存檔 與 下載檔案 存放位置請去修改 property\a.property

4. 執行 .\py\crawler591.py 
```bash
python .\py\crawler591.py 
```

5. 檔案會下載到 output 資料夾底下, 每個租屋物件會存成一個 .json 檔