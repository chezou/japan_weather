"""Fetch Japanese weather data

Usage:
	fetch_weather.py [--from-year=FY] [--to-year=TY]
	fetch_weather.py -h | --help

Options:
	-h --help			Show this screen
	--from-year=<FY>	Start year to fetch [default: 2016]
	--to-year=<TY>		End year to fetch [deefault: 2016]
"""


from datetime import datetime
import pandas

_base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no={0}&block_no={1}&year={2}&month={3}&day=1&view="
_columns = ["日", "現地平均気圧", "海面平均気圧", "合計降水量", \
"1時間最大降水量", "10分間最大降水量", "平均気温", "最高気温", "最低気温", \
"平均湿度", "最小湿度", "平均風速", "最大風速", "最大風速風向", "最大瞬間風速", "最大瞬間風速風向", \
"日照時間", "降雪", "最深積雪", "天気概況昼", "天気概況夜", "都道府県", "都市", "年", "月"]

def fetch_weather(prefecture, year=2016, month=1):
	now = datetime.now()
	if year > now.year or (year == now.year and month > now.month):
		return

	url = _base_url.format(prefecture['prec_no'], prefecture['block_no'], year, month)
	_df = pandas.read_html(url)
	if len(_df) > 1:
		_df = _df[0][4:]
		_df['都道府県'] = prefecture['prec_ch']
		_df['都市'] = prefecture['block_ch']
		_df['年'] = year
		_df['月'] = month
		_df.columns = _columns
		return _df

if __name__ == '__main__':
	import json, time, itertools
	from docopt import docopt
	import os

	output_dir = "./output"
	now = datetime.now()

	args = docopt(__doc__)
	from_year = int(args["--from-year"]) if args["--from-year"] else 2016
	to_year = int(args["--to-year"]) if args["--to-year"] else 2016
	with open('prefecture.json') as f:
		prefectures = json.load(f)

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	for prefecture in prefectures:
		print(prefecture)
		df = pandas.DataFrame([])
		for year, month in itertools.product(range(from_year, to_year+1), range(1, 13)):
			if year > now.year or (year == now.year and month > now.month):
				break

			print(year, month)
			_df = fetch_weather(prefecture, year=year, month=month)
			if type(_df) == pandas.core.frame.DataFrame:
				df = df.append(_df, ignore_index=True)
			time.sleep(1)

		fname = output_dir+"/monthly_weather_{0}_{1}_{2}-{3}.csv".format(prefecture['prec_ch'], prefecture['block_ch'], from_year, to_year)
		df.to_csv(fname, index=False)
