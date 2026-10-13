import requests 
from bs4 import BeautifulSoup
import urllib3
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



target_domain = input("Enter the target domain of the Origin header (example.com): ")
url_endpoint = input("Enter the testing endpoint (starts with https://example.com): ")
cookie = input("Enter your cookies ( press enter if no need to add cookies): ")

# payloads
TLDs = ["com","org","net","co","io","dev","ai","cloud","xyz","me","app","info"]
null = "null" 
at_start = f"https://{target_domain}.evil.com"
at_end = f"https://evil-{target_domain}"
combo = f"https://not{target_domain}"
at_sign = f"https://{target_domain}@https://evil.com"
payloads = [at_sign, at_start, at_end, combo, null]
subdomains = set()
live_subdomains = set()


try: 
	hackertarget = f"https://api.hackertarget.com/hostsearch/?q={target_domain}"

	response = requests.get(url=hackertarget,timeout=20)
	data = response.text
	for line in data.splitlines():
		if "," in line:
			sub = line.split(",")[0]
			subdomains.add(sub) 		
except Exception as e:
	print(e)

try:
	rapid_DNS = f"https://rapiddns.io/subdomain/{target_domain}?full=1"
	response = requests.get(url=rapid_DNS, timeout=20,verify=False)
	soup = BeautifulSoup(response.text, "html.parser")
	for td in soup.find_all("td"):
		text = td.text.strip()
		if text.endswith(target_domain):
			subdomains.add(text)
except Exception as e:
	print(e)

	
def checking(subdomain):
	try:
		url = f"https://{subdomain}"
		resp = requests.get(url=url, timeout=5, verify=False)
		if resp.status_code in (200, 302, 401, 403):
			return subdomain 
			
	except Exception as e:
		pass

with ThreadPoolExecutor(max_workers=10) as ex:
	results = ex.map(checking, subdomains) 

	for result in results:
		if result:
			live_subdomains.add(result)


for domain in live_subdomains:
	i = "https://" + domain
	payloads.append(i) 


for TLD in TLDs:
	parts = target_domain.split(".")
	parts[-1] = TLD
	TLD_target = "https://" + ".".join(parts)
	payloads.append(TLD_target)

# now the payloads is TLDs, prefix plays and subdomains

tasks = []
for payload in payloads:
	tasks.append((url_endpoint, payload, cookie))

#now we got hte endpoint for the test and the payload, we gotta pass it into the function


def cors_testing(task):
	try:
		red = "\033[91m"
		blue = "\033[96m"
		gray = "\033[90m"
		reset = "\033[0m"
		url_endpoint, payload, cookie = task
		headers = {"User-Agent": "Mozilla/5.0","Origin": payload,"Cookie": cookie}
		resp = requests.get(url=url_endpoint, headers=headers, timeout=3, verify=False)
		ACAO = resp.headers.get("access-control-allow-origin")
		ACAC = resp.headers.get("access-control-allow-credentials")
		if ACAO == payload and ACAC and ACAC.lower() == "true":
			return f"[+]{red}[{payload}]{reset} is reflected with credentials on {blue}[{url_endpoint}]{reset}"
		elif ACAO == "null" and ACAC and ACAC.lower == "true":
			return f"[+]{red}[null]{reset} is reflected with credentials on {blue}{url_endpoint}{reset}"
		else:
			return f"{gray}[{payload}] is not reflected{reset}"
	except Exception:
		pass

with ThreadPoolExecutor(max_workers=3) as ex:
	results = ex.map(cors_testing, tasks)
	for result in results:
			print(result)

