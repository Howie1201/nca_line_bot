# 點餐bot

## 專案介紹

為了減少團訂午餐花費的時間，同時減少人為的疏失，一時興起開發的專案。

使用語言主要是python，是個以line bot api和flask為核心，heroku為server打造的line bot專案。

很多東西都是首次嘗試，還有很多可以改進的地方，目前正在一邊學習一邊持續更新。

## 如何使用

1. 註冊Line developer和heroku，並將環境設置好

2. 將主程式line_bot.py中的line_bot_api, handler, app_name等變數改成自己的

3. 將主程式line_bot.py中的admins, groups, restaurants等變數修改成自己要用的，admins代表管理員，groups代表需要使用機器人的群組，user_id, group_id等資訊可在heroku後台查看

4. 額外加入自己想要的feature，deploy到heroku

5. 大功告成，有問題的話可以找專案的原作者(jackyh1999)，會盡量排解

## 目前接受指令

聽取使用說明:

`說明/`

獲取餐廳列表:

`餐廳/`

決定今天吃的餐廳:

`吃/[餐廳名稱]`

點餐:

`點/[餐點編號1]/[餐點編號2]/...`

取消點餐:

`取消/[餐點編號1]/[餐點編號2]/...`

餐點有額外需求:

`備註/[備註內容]`

統計數量、金額、生成明細表

`統計/`

關閉點餐:

`截止/`

清除訂餐資料:

`clear/`

## 使用範例

![](https://i.imgur.com/e0TbX29.jpg)

![](https://i.imgur.com/lMqG3IZ.jpg)

## 


## 注意事項

1. 所有指令一定包含"/" (半形斜線) 

2. 部分指令需要管理員權限才能使用

3. 先統計再截止



