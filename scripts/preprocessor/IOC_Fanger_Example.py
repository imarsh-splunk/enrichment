import ioc_fanger

fanged_ip = 'hxxps://subnet[.]example[.]com/phishing.php'

# fanged = ioc_fanger.defang(fanged_ip)
# print(fanged)

defanged = ioc_fanger.fang(fanged_ip)
print(defanged)
