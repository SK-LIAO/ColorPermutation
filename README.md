# ColorPermutation
A algorithm for dyeing pollution 

在紡織產業裡，將一塊布染出準確的顏色極為重要。
染缸染完一塊胚布時，通常需要將染缸做清洗動作以避免染料殘留，
導致下一缸染色時，胚布遭到污染而使顏色失去準確性。
不同的染料胚布都有其特殊的物理性質，
本程式利用胚布及染料建立出染色的基礎光譜數據，
並根據 Kubelka Munk Theory建立出染劑混色後光譜推估公式。
並將光譜轉換到CIE(國際照明協會)創立的 CIEL*a*b*色彩空間座標。
此空間以客觀科學的方法定義顏色為空間座標，分為
L軸-明度 a*軸-紅綠 b*軸-黃藍，以人類對顏色感知的均勻性而建立。
因此可使用空間上的距離來表現兩色的差異。
本程式利用 CIEDE2000標準<0.6來定義兩顏色為相等。
降前一缸殘留量混入下一缸染劑所計算出來的光譜、
與前一缸完全不殘留所計算出來的光譜做色差的計算，
若色差小於0.6即可不洗缸，可以來減少成本與增加產能。
並且可對不種配方做有效排序，減少人員手動排序作業的負擔。

Data為基礎數據範例,使用程式時需先將基礎數據匯入。
不同業者需自己建立自己的基礎數據。
執行檔為app.py
