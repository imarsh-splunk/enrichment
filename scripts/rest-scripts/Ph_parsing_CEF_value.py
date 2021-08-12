import re

cef = "<159>Dec 14 22:59:29 10.205.71.254 LEEF:1.0|Forcepoint|Security|8.5.0|transaction:permitted|sev=1	" \
      "cat=203	usrName=-	loginID=-	src=10.10.244.2	srcPort=0	srcBytes=0	dstBytes=0	" \
      "dst=152.195.32.112	dstPort=80	proxyStatus-code=-	serverStatus-code=-	duration=0	method=-	" \
      "disposition=1026	contentType=-	reason=-	policy=-	role=0	RefererURL=-	filename=-	" \
      "userAgent=-	url=http://152.195.32.112/pubapi/3.0/10126.1/3890297/0/0/ADTECH;cfp\=1;rndc\=1544857169;v\=2;" \
      "cmd\=bid;cors\=yes;alias\=ml300x50;misc\=1544857170036 HTTP/1.1\r\n" \
      "Host: adserver-us.adtech.advertising.com\r\n" \
      "Content-Type: text/plain\r\nOrigin: http://quemas.mamaslatinas.com\r\nAccept: */*\r\n" \
      "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) " \
      "Mobile/16B92 [FBAN/FBIOS;FBAV/199.0.0.69.98;FBBV/132813153;FBDV/iPhone10,5;FBMD/iPhone;FBSN/iOS;FBSV/12.1;" \
      "FBSS/3;FBCR/T-Mobile;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/134878664]\r\n" \
      "Referer: http://quemas.mamaslatinas.com/entertainment/154449/conoce-por-dentro-la-lujosa-mansion-"

url = re.search(r'url=(.*?);', cef).group(1)
host = re.search(r'Host: (.*)\r\n', cef).group(1)
origin = re.search(r'Origin: (.*?)\r\n', cef).group(1)
user_agent = re.search(r'User-Agent: (.*?)\r\n', cef).group(1)
print(user_agent)

cef = "<22>Dec 14 13:20:02 Mail_Logs_QRadar: Info: MID 38566026 Custom Log Entry: Mail Policy: $THROTTLED " \
      "Content Filter: Executive_Quarantine_Phishing \xe2\x80\x93 To: steve.streit@greendot.com " \
      "From: ZygenX_plus_trial <8shxd-steve.streit.w0cb56jZ7rz3fBt3LbRR@JOBNPVjYT5pLI.ikexpress.com> \xe2\x80\x93 " \
      "Subject: [SPAM]Intensify Orgasms with ZygenX \xe2\x80\x93 Rep Score: -2.8 \xe2\x80\x93 " \
      "Remote Host: host32-245-211-80.static.arubacloud.pl - Remote IP: 80.211.245.32 \xe2\x80\x93 " \
      "Filename:  - Xmailer:  - SpamResult: POSITIVE - HAT Group: SUSPECTLIST"

recipient = re.search(r'To: (.*?) ', cef).group(1)
from_email = re.search(r'From: (.*?) Subject:', cef).group(1)
sender = re.search(r'<(.*?)>', from_email).group(1)
remote_host = re.search(r'Remote Host: (.*?) ', cef).group(1)
remote_ip = re.search(r'Remote IP: (.*?) ', cef).group(1)
print(remote_ip)
