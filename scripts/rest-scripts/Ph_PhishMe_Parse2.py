import re

bodytxt = """-----BEGIN REPORTER AGENT-----
Reporter agent: Cofense Reporter for Mobile|3.0.0|Mac OS X 10.14.5|Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36
Reporting User: tim.briggs@crowdstrike.com

-----END REPORTER AGENT-----

-----BEGIN EMAIL HEADERS-----
Received: from Casmbox03.crowdstrike.sys (10.100.11.66) by casmbox05.crowdstrike.sys (10.100.11.72) with Microsoft SMTP Server (TLS) id 15.0.1473.3 via Mailbox Transport; Tue, 21 May 2019 11:07:25 -0700
Received: from Casmbox04.crowdstrike.sys (10.100.11.70) by Casmbox03.crowdstrike.sys (10.100.11.66) with Microsoft SMTP Server (TLS) id 15.0.1473.3; Tue, 21 May 2019 11:07:24 -0700
Received: from ee01.crowdstrike.sys (10.100.0.12) by Casmbox04.crowdstrike.sys (10.100.11.70) with Microsoft SMTP Server (TLS) id 15.0.1473.3 via Frontend Transport; Tue, 21 May 2019 11:07:24 -0700
Received: from mx0b-00206401.pphosted.com (148.163.148.21) by ee01.crowdstrike.sys (10.100.0.12) with Microsoft SMTP Server (TLS) id 15.0.1473.3; Tue, 21 May 2019 11:07:22 -0700
Received: from pps.filterd (m0092946.ppops.net [127.0.0.1])	by mx0a-00206401.pphosted.com (8.16.0.27/8.16.0.27) with SMTP id x4LI3pB0020540;	Tue, 21 May 2019 11:06:13 -0700
Received: from mail-yw1-xc2f.google.com (mail-yw1-xc2f.google.com [IPv6:2607:f8b0:4864:20::c2f])	by mx0a-00206401.pphosted.com with ESMTP id 2sjgg8xp39-1	(version=TLSv1.2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128 verify=NOT)	for <tim.briggs@crowdstrike.com>; Tue, 21 May 2019 11:06:13 -0700
Received: by mail-yw1-xc2f.google.com with SMTP id 186so7652778ywo.4        for <tim.briggs@crowdstrike.com>; Tue, 21 May 2019 11:06:12 -0700 (PDT)
Received: from DESKTOP6T8N3O4 ([2601:cc:c101:28f2:190d:6c86:2480:ee29])        by smtp.gmail.com with ESMTPSA id b132sm6226062ywb.87.2019.05.21.11.06.10        for <tim.briggs@crowdstrike.com>        (version=TLS1_2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);        Tue, 21 May 2019 11:06:10 -0700 (PDT)
Authentication-Results: ppops.net;	spf=pass smtp.mailfrom=tim.briggs37@gmail.com;	dkim=pass header.d=gmail.com header.s=20161025;	dmarc=pass header.from=gmail.com
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20161025;        h=from:to:subject:date:message-id:mime-version:content-language         :thread-index;        bh=ssKKrlGcRZNQoVdhlthF55ZcDulDGE8Ab3uGcWPTDoc=;        b=VYMNM9cUYwOh4c6IpB0lbG1+r6fs701toE1GI49vNpLu8Oa3lPOD7MSWZSddki2tXA         DSaj4bEq1xlkGWCyv7yzZxzOU5kF49Ka2jTphGdYH6W+VTXcIKoAeSlQiMgX+lmqW/Pn         ggU4ADzf4ASnDGrCn6X0yEZzzyWpC5itwoygDh0+SlSZ7Mt6JO1INcgOLcf0YFzvObQc         6FsDQKJZThOL/VTYQ0FcIgJooh9A2rHJjhDKYGA3ZoD1X73Mq3tZi3lUd+p3QItwc/kq         ECpiec68yMFi6InjlYbuyL3K9Um/ZS/sAqmUlb/kE8vZVZomb9KTbNZEVS5reaKnNujv         kMkQ==
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20161025;        h=x-gm-message-state:from:to:subject:date:message-id:mime-version         :content-language:thread-index;        bh=ssKKrlGcRZNQoVdhlthF55ZcDulDGE8Ab3uGcWPTDoc=;        b=T9ERHPRBZM6HHL7UXsQrKrmH8Assr2j0XwWyGHQ08D+hDveS9xWlKJhjxG5ubrtyFF         BfiflVhmK90e2xss057pzPlc5xXHqDcZ6Ooy+SEYlF2yZZFyw2H931yYi9sXI42vsZ3A         Ox5xIDWIWTxd586rElyq9zMCuFhE3j2mbFGgCWL7zliDuDHg4fkk6e/qnrcjDAMD+DXD         cuSoTXu8m2YWSCh1N7uPOxHHOmW9/uU/rHrTscLT5jpfq8cMURcGTScA0Adcf0XocYn9         ahyFurLXL+ocJT7cMG+jbLCDM/1nrbSktAglqjBKt5pck7ragcIuXVV1MEiWwhBvrtyP         bUHg==
X-Gm-Message-State: APjAAAVkVMLcQW+37XL6004iOlQD8SSc2eH/1pFF+1ttn+NCfo68zgma	1kJDd7JNu/uqIp3Q6eZWTM5WLSPV
X-Google-Smtp-Source: APXvYqzcmlysSqTtXeAChiN66RaJsM4sfCm/TB98W5Tyf/cC1uyfJ8R5pz92G96forPWbpOJkmEBRQ==
X-Received: by 2002:a81:b717:: with SMTP id v23mr39365318ywh.120.1558461971285;        Tue, 21 May 2019 11:06:11 -0700 (PDT)
Date: Tue, 21 May 2019 14:06:08 -0400
Message-ID: <011501d50fff$ddc85af0$995910d0$@gmail.com>
Content-Type: multipart/mixed
X-Mailer: Microsoft Outlook 16.0
Content-Language: en-us
Thread-Index: AdUP/9BjONGDn039QEGR9EpcBMRLRA==
X-CLX-Shades: MLX
X-CLX-Response: 1TFkXGxoaGxEKWUQXaBtwQhNTRH9EfWQRClhYF2UYZV0cGGBPX01eEQp4Thd jU2NrexNYfhpfXhEKeUMXZmYfemZiY15ackIRCllNF2dmchEKWUkXEQpZXhdsbHkRCklGF0lYRV 1OWV5YQ0FPdUJFWV5PThEKQ04XTEBkGmsfW3JYHm9TeG9taVNeGEF9dR5LbW5LX295UlwRClhcF x8EGgQbHRkHSR0eTk5ME0gFGxoEGxoaBB4SBBwQGx4aHxoRCl5ZF39tT2FdEQpNXBcbHxwRCkxG F29va2tra2sRCkNaFxgfHwQYHx8EGB8fBBgfHxEKQlwXGxEKXk4XGxEKQksXY1Nja3sTWH4aX14 RCkJJF2NTY2t7E1h+Gl9eEQpCRRdpGkkfYl1haX5LWBEKQk4XY1Nja3sTWH4aX14RCkJMF2UYZV 0cGGBPX01eEQpCbBdhSWVTYgFnWFlMGxEKQkAXZWVGYhxLRm9ZXHoRCkJYF2JuYF9paGUFGmJZE QpwaBdlRHMee0hTc1N+chAaEQpwaBdkYmASS2R4aGFATBAaEQpwfxdgaF9IfG1NUEJobhAbGR8R CnB9F2BoX0h8bU1QQmhuEBsZHxEKcH0XYGhfSHxtTVBCaG4QGxkfEQpwbBdvW2tBRHpTc34SHBA cHxEKbX4XGhEKWE0XSxEg
MIME-Version: 1.0
Subject: [External] Report me
x-external: true
X-Proofpoint-Virus-Version: vendor=fsecure engine=2.50.10434:,, definitions=2019-05-21_04:,, signatures=0
X-Proofpoint-Spam-Details: rule=inbound_notspam policy=inbound score=0 priorityscore=1501 malwarescore=0 suspectscore=0 phishscore=0 bulkscore=0 spamscore=0 clxscore=1001 lowpriorityscore=0 mlxscore=0 impostorscore=0 mlxlogscore=445 adultscore=0 classifier=spam adjust=0 reason=mlx scancount=1 engine=8.0.1-1810050000 definitions=main-1905210111
Return-Path: tim.briggs37@gmail.com
X-MS-Exchange-Organization-Network-Message-Id: 0b645e28-bc57-4b64-76b7-08d6de172d9d
X-MS-Exchange-Organization-AuthSource: ee01.crowdstrike.sys
X-MS-Exchange-Organization-AuthAs: Anonymous
-----END EMAIL HEADERS-----

-----BEGIN REPORT COUNT-----
PhishMe emails reported: 0
Suspicious emails reported: 3
-----END REPORT COUNT-----

Reported from folder: Inbox

-----BEGIN URLS-----
Link text: cnn.com
URL: https://urldefense[.]proofpoint[.]com/v2/url?u=http-3A__cnn[.]com&amp;d=DwQFAg&amp;c=08AGY6txKsvMOP6lYkHQpPMRA1U6kqhAwGa8-0QCg3M&amp;r=lV8VDDHWZws6hp_AvE05eTVdMbS9_AONNYZYVOb8sTA&amp;m=fLtT-XZvMh3-sXLCRWYSf-l_LDrzp7Q1Jk45n61XILw&amp;s=_zwBr9MxNb9tDcHGzWTtQLL5xMNa05eZHair2wv9s04&amp;e=
URL Domain: urldefense[.]proofpoint[.]com

Link text: https://cnn.com
 [cnn.com]
URL: https://urldefense[.]proofpoint[.]com/v2/url?u=https-3A__cnn[.]com&amp;d=DwMFAg&amp;c=08AGY6txKsvMOP6lYkHQpPMRA1U6kqhAwGa8-0QCg3M&amp;r=lV8VDDHWZws6hp_AvE05eTVdMbS9_AONNYZYVOb8sTA&amp;m=fLtT-XZvMh3-sXLCRWYSf-l_LDrzp7Q1Jk45n61XILw&amp;s=5TeQDN9fcVWfKhnUuKMJwk0RtQatB81z-WgiOV3NZ1E&amp;e=
URL Domain: urldefense[.]proofpoint[.]com

Link text: https://urldefense.proofpoint.com/v2/url?u=http-3A__cnn.com&d=DwQFAg&c=08AGY6txKsvMOP6lYkHQpPMRA1U6kqhAwGa8-0QCg3M&r=lV8VDDHWZws6hp_AvE05eTVdMbS9_AONNYZYVOb8sTA&m=fLtT-XZvMh3-sXLCRWYSf-l_LDrzp7Q1Jk45n61XILw&s=_zwBr9MxNb9tDcHGzWTtQLL5xMNa05eZHair2wv9s04&e=
URL: https://urldefense[.]proofpoint[.]com/v2/url?u=http-3A__cnn[.]com&d=DwQFAg&c=08AGY6txKsvMOP6lYkHQpPMRA1U6kqhAwGa8-0QCg3M&r=lV8VDDHWZws6hp_AvE05eTVdMbS9_AONNYZYVOb8sTA&m=fLtT-XZvMh3-sXLCRWYSf-l_LDrzp7Q1Jk45n61XILw&s=_zwBr9MxNb9tDcHGzWTtQLL5xMNa05eZHair2wv9s04&e=
URL Domain: urldefense[.]proofpoint[.]com

Link text: https://cnn.com
URL: https://cnn[.]com
URL Domain: cnn[.]com

Link text: https://urldefense.proofpoint.com/v2/url?u=https-3A__cnn.com&d=DwMFAg&c=08AGY6txKsvMOP6lYkHQpPMRA1U6kqhAwGa8-0QCg3M&r=lV8VDDHWZws6hp_AvE05eTVdMbS9_AONNYZYVOb8sTA&m=fLtT-XZvMh3-sXLCRWYSf-l_LDrzp7Q1Jk45n61XILw&s=5TeQDN9fcVWfKhnUuKMJwk0RtQatB81z-WgiOV3NZ1E&e=
URL: https://urldefense[.]proofpoint[.]com/v2/url?u=https-3A__cnn[.]com&d=DwMFAg&c=08AGY6txKsvMOP6lYkHQpPMRA1U6kqhAwGa8-0QCg3M&r=lV8VDDHWZws6hp_AvE05eTVdMbS9_AONNYZYVOb8sTA&m=fLtT-XZvMh3-sXLCRWYSf-l_LDrzp7Q1Jk45n61XILw&s=5TeQDN9fcVWfKhnUuKMJwk0RtQatB81z-WgiOV3NZ1E&e=
URL Domain: urldefense[.]proofpoint[.]com
-----END URLS-----

-----BEGIN ATTACHMENTS-----
File Name: BadBad.txt
File Size: 274
MD5 File Checksum: 2983366002c981d761ec02cec7522f5c
SHA1 File Checksum: abc62716e4574e83815bdbfc6c4634a5d26a047d
SHA256 File Checksum: 05777190217ea563abb45c258aa8f982f0800b0c502e06f264827c4c1d285757
-----END ATTACHMENTS-----"""
# print(bodytxt)

msgid = re.search(r'Message-ID: (.*?)\n', bodytxt).group(1)
# print(msgid)
xmailer = re.search(r'X-Mailer: (.*?)\n', bodytxt).group(1)
# print(xmailer)
rpath = re.search(r'Return-Path: (.*?)\n', bodytxt).group(1)
# print(rpath)
reporter = re.search(r'Reporting User: (.*?)\n', bodytxt).group(1)
# print(reporter)
subject = re.search(r'Subject: (.*?)\n', bodytxt).group(1)
# print(subject)

if "[External] " in subject:
    psubject = subject.split('[External] ')[1]
    # print(psubject)

authas = re.search(r'X-MS-Exchange-Organization-AuthAs: (.*?)\n', bodytxt).group(1)
# print(authas)

# ------------------------------------------------------------------------------------------------

# Define list of matched "Link text: X URL: X Domain: X" results
match_list = re.findall(r'Link text: (.*?)\nURL: (.*?)\nURL Domain: (.*?)\n', bodytxt, re.DOTALL)

all_urls = []
all_domains = []

for match in match_list:
    if not match[1].startswith("http"):
        continue

    all_urls.append(match[1].replace("[.]", "."))
    all_domains.append(match[2].replace("[.]", "."))

unique_urls = list(set(all_urls))
unique_domains = list(set(all_domains))

# print(unique_urls)
# print(unique_domains)

# Create blank dictionaries to append found URLs/Domains to
raw = {}
cef = {}

# Strip out any 'urldefense.proofpoint.com' URL prefixes
for url in unique_urls:
    # print(url)
    if 'urldefense.proofpoint.com' in url:
        # print('url before: {}'.format(url))
        url_parsed = re.findall(r'u=(.*)', url)[0]
        url_decoded = url_parsed.replace('-3A__', '://').split('&')[0]

        # Add only unique and filtered URLs into the single-key CEF dictionary
        cef['requestURL'] = url_decoded
        print(cef)

# Clear CEF dictionary
del cef['requestURL']

for domain in unique_domains:
    if 'urldefense.proofpoint.com' not in domain:
        # Add only unique and filtered Domains into the single-key CEF dictionary
        cef['destinationDnsDomain'] = domain
        print(cef)
