import requests

# Menggunakan header jika perlu mengirimkan informasi tambahan dalam permintaan
data_header = {
    'authority':'id.wikipedia.org',
    'method':'GET',
    'path':'/wiki/Daftar_kota_di_Indonesia_menurut_provinsi',
    'scheme':'https',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie':'WMF-Last-Access-Global=05-Jul-2025; GeoIP=ID:JI:Surabaya:-7.24:112.76:v4; WMF-Uniq=mxuUVFPmqlhya39ArZeNxAILAAUEAFvdIQr0wffMcw7VEEnL9aUEf6mmYGp9JuN2; WMF-Last-Access=05-Jul-2025; idwikimwuser-sessionId=91d2fc86203fcb68d3c0; NetworkProbeLimit=0.001',
    'Priority':'u=0,i',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}

# Menggunakan proxy jika ingin menyembunyikan identitas atau akses konten dibatasi
# data_proxy = {
#     'http':'http://47.91.120.190:1025',
#     'https':'https://57.129.81.201:8080'
# }

url = 'https://id.wikipedia.org/wiki/Daftar_kota_di_Indonesia_menurut_provinsi'
response = requests.get(url, headers=data_header)
print(response)