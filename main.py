import requests
import re
from datetime import datetime

burp0_url = "https://www.okooo.com:443/jingcai/"
burp0_cookies = {"_ga": "GA1.1.288433811.1771923461", "_ga_H8WNRJTRHH": "GS2.1.s1771923461$o1$g1$t1771923476$j45$l0$h1186845713", "LastUrl": "", "FirstURL": "www.baidu.com/link%3Furl%3D1WG497I1qicTD-9oX2PoWCEUjWXOIUeTNaMHLsG5o1O%26wd%3D%26eqid%3Df102e435000db09e0000000669c65607", "FirstOKURL": "https%3A//www.okooo.com/jingcai/", "First_Source": "www.baidu.com", "Hm_lvt_213d524a1d07274f17dfa17b79db318f": "1774605837", "HMACCOUNT": "8C86A5B9D6B01AE7", "pm": "", "LStatus": "N",
                 "LoginStr": "%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%22%22%2C%22loginSession%22%3A%22___GlobalSession%22%7D", "PHPSESSID": "4ca10ba48c301a9107b7b56682c5b85f773424a7", "Hm_lpvt_213d524a1d07274f17dfa17b79db318f": "1774607841", "acw_tc": "707c9f7317746078413102271e34b2bc0b41ac7ee54b6296bac6a73ac103a0", "_ga_B3LCXP8H9E": "GS2.1.s1774605836$o1$g1$t1774607841$j60$l0$h153130246"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"macOS\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                 "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://www.baidu.com/link?url=1WG497I1qicTD-9oX2PoWCEUjWXOIUeTNaMHLsG5o1O&wd=&eqid=f102e435000db09e0000000669c65607", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "X-Forwarded-For": "192.168.1.1", "If-Modified-Since": "Fri, 27 Mar 2026 10:35:29 GMT", "Priority": "u=0, i"}

# 获取响应内容，使用 gb2312 解码
response = requests.get(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies)
html = response.content.decode('gb2312', errors='ignore')

# 将 HTML 按行分割处理
lines = html.split('\n')


def get_weekday(date_str):
    """根据日期字符串获取星期几"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return weekdays[date_obj.weekday()]
    except:
        return ''


results = []
current_match = None
current_date = None

for line in lines:
    # 检查是否是新的比赛开始
    if 'class="touzhu_1"' in line and 'data-ordercn=' in line and 'id="match_' in line:
        current_match = {
            'sp_list': [],
            'rq_sp_list': [],
            'in_rq_section': False
        }

        # 提取基本信息
        order_match = re.search(r'data-ordercn="([^"]*)"', line)
        if order_match:
            order_cn = order_match.group(1)
            order_num = re.search(r'(\d+)', order_cn)
            current_match['order'] = order_num.group(1) if order_num else "000"

        rq_match = re.search(r'data-rq="([^"]*)"', line)
        current_match['rang_qiu'] = rq_match.group(1) if rq_match else "0"

        hname_match = re.search(r'data-hname="([^"]*)"', line)
        if hname_match:
            current_match['home_team'] = hname_match.group(1)

        aname_match = re.search(r'data-aname="([^"]*)"', line)
        if aname_match:
            current_match['away_team'] = aname_match.group(1)

    # 如果当前有正在处理的比赛
    if current_match is not None:
        # 提取联赛名称
        if 'class="saiming' in line and 'title=' in line:
            league_match = re.search(r'title="([^"]*)"[^>]*>([^<]*)</a>', line)
            if league_match:
                current_match['league'] = league_match.group(2).strip()

        # 提取比赛时间（包含日期）
        if 'class="shijian"' in line and 'title=' in line:
            # 尝试从 title 属性中提取完整日期时间
            datetime_match = re.search(r'title="比赛时间:([\d\-]+)\s+[\d:]+', line)
            if datetime_match:
                current_match['match_date'] = datetime_match.group(1)

            time_match = re.search(r'>(\d{2}:\d{2})</div>', line)
            if time_match:
                current_match['match_time'] = time_match.group(1)

        # 检查是否进入让球区域
        if 'rangqiuspf' in line:
            current_match['in_rq_section'] = True

        # 提取赔率
        sp_matches = re.findall(r'data-sp="([^"]*)"', line)

        if current_match.get('in_rq_section'):
            current_match['rq_sp_list'].extend(sp_matches)
        else:
            current_match['sp_list'].extend(sp_matches)

        # 检查是否到达比赛结束
        if '<div class="clear"></div>' in line:
            # 处理这场比赛
            if all(k in current_match for k in ['order', 'home_team', 'away_team']):
                # 过滤赔率 - 取前 3 个非零赔率
                sheng_ping_fu = [sp for sp in current_match.get(
                    'sp_list', []) if sp and sp != '0'][:3]
                rangqiu_sp = [sp for sp in current_match.get(
                    'rq_sp_list', []) if sp and sp != '0'][:3]

                # 只有当胜平负和让球胜平负都有赔率时才输出
                if len(sheng_ping_fu) >= 3 and len(rangqiu_sp) >= 3:
                    odds_str = f"{current_match['home_team']}{sheng_ping_fu[0]}:{sheng_ping_fu[1]}:{sheng_ping_fu[2]}{current_match['away_team']}"
                    rangqiu_str = f"{current_match['home_team']}{current_match['rang_qiu']}:{rangqiu_sp[0]}:{rangqiu_sp[1]}:{rangqiu_sp[2]}{current_match['away_team']}"

                    match_date = current_match.get('match_date', '')
                    match_time = current_match.get('match_time', '00:00')
                    league = current_match.get('league', '')

                    result = {
                        'date': match_date,
                        'time': match_time,
                        'order': current_match['order'],
                        'league': league,
                        'odds_str': odds_str,
                        'rangqiu_str': rangqiu_str
                    }
                    results.append(result)

            current_match = None

# 按日期分组
matches_by_date = {}
for result in results:
    date = result['date']
    if date not in matches_by_date:
        matches_by_date[date] = []
    matches_by_date[date].append(result)

# 按日期排序并输出
sorted_dates = sorted(matches_by_date.keys())

for date in sorted_dates:
    weekday = get_weekday(date)
    print(f"\n{date} {weekday}")

    matches = matches_by_date[date]
    for match in matches:
        # 解析赔率字符串
        odds_parts = match['odds_str'].split(
            '|')[0] if '|' in match['odds_str'] else match['odds_str']
        rangqiu_parts = match['rangqiu_str'].split(
            '|')[0] if '|' in match['rangqiu_str'] else match['rangqiu_str']

        # 提取主队、客队和赔率
        import re as re_module

        # 非让球格式：主队 + 胜平负赔率 + 客队
        odds_match = re_module.match(
            r'([^.]+)(\d+\.\d+):(\d+\.\d+):(\d+\.\d+)(.+)', odds_parts)
        if odds_match:
            home_team = odds_match.group(1)
            home_win = odds_match.group(2)
            draw = odds_match.group(3)
            away_win = odds_match.group(4)
            away_team = odds_match.group(5)
            odds_formatted = f"{home_team}VS {away_team}（赔率：胜{home_win} 平{draw} 负{away_win}）"
        else:
            odds_formatted = odds_parts

        # 让球格式：主队 + 让球数 + 胜平负赔率 + 客队
        rq_match = re_module.match(
            r'([^.]+)([+-]?\d+):(\d+\.\d+):(\d+\.\d+):(\d+\.\d+)(.+)', rangqiu_parts)
        if rq_match:
            rq_home = rq_match.group(1)
            rang_qiu = rq_match.group(2)
            rq_home_win = rq_match.group(3)
            rq_draw = rq_match.group(4)
            rq_away_win = rq_match.group(5)
            rq_away = rq_match.group(6)
            rq_formatted = f"{rq_home}{rang_qiu}VS {rq_away}（赔率：胜{rq_home_win} 平{rq_draw} 负{rq_away_win}）"
        else:
            rq_formatted = rangqiu_parts

        output = f"{match['order']}|{match['league']}|{match['time']}|{odds_formatted}|{rq_formatted}"
        print(output)

print(f"\n共找到 {len(results)} 场比赛数据")
print(f"涉及 {len(sorted_dates)} 个比赛日")
