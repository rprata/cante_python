import requests, wget, os, re, urlparse

str_first_page = "http://cf.uol.com.br/cante/new/musicas.asp?O=Nacionais&A=1&B=*&L=1"
str_second_page_init = "http://cf.uol.com.br/cante/new/musicas.asp?D=1&P="
str_second_page_last = "&O=Nacionais&G=&A=1&B=*&L=1"
str_search = "http://p.download.uol.com.br/cante/kar/"
urls = []


#defs convertion

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

# in first page

r = requests.get(str_first_page)

if r.status_code == 200:

	pos = 0
	count = r.text.count(str_search)
	for i in range(0, count):
		initial_index =  r.text.index(str_search, pos)
		final_index = r.text.index(".", initial_index + len(str_search)) + 4
		#print r.text[initial_index : final_index]
		out = r.text[initial_index : final_index]
		urls.append(out)
		filename = wget.download(out)
		os.rename(filename, "musicas-nacionais/"+filename)

		pos = final_index

#print "primeira parte ok!"

#in next pages

for i in range(1, 89):
	r = requests.get(str_second_page_init + str(i) + str_second_page_last)

	if r.status_code == 200:

		pos = 0
		count = r.text.count(str_search)
		for i in range(0, count):
			initial_index =  r.text.index(str_search, pos)
			final_index = r.text.index(".", initial_index + len(str_search)) + 4
			#print r.text[initial_index : final_index]
			out = r.text[initial_index : final_index]
			urls.append(iriToUri(out))
			filename = wget.download(iriToUri(out))
			os.rename(filename, "musicas-nacionais/"+filename)
			pos = final_index
