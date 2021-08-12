import urllib
import urlparse




urldefense = 'https://urldefense.proofpoint.com/v2/url?u='

raw_url = "https://urldefense.proofpoint.com/v2/url?u=http-3A__therehabstore.com_&d=DwQFAg&c=kUmgHTyNdJXU_" \
          "CAV6hobjYYef1jqCQRoPJiZpgsNcHg&r=6lBuZ0cwqMxWNU-5VOArDw&m=EeuFbalTfTpNPhQF0_iKPrz7Nb_3_p-1l9hw3zzC7xY&s=" \
          "iq6vJ7ak4NIAFLANtOrlSKjhBOtoNJ396Roj5RLX2Ek&e="

if urldefense in raw_url:
    split_url = raw_url.split(urldefense)[1]
    print(split_url)

    encoded = split_url.replace("*", "%")
    decoded = urllib.unquote(encoded)
    # print(decoded)

    # parsed_uri = urllib.parse.unquote(decoded)
    # result = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri).replace('__', '')
    # print(result)
