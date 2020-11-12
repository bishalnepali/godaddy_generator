# This is needed to send POST and GET requests
import requests
from random_file_generator import RandomNameGenerator
# This is needed to limit the frequeny 
# by which we are going to hit the API 
# endpoints. Only certain number of 
# requests can be made in a mintue
import time
from api_key_authentication import API_KEY,SECRET_KEY
# This is needed to convert API 
# responses into JSON objects
import json

# Godaddy developer key and secret
api_key = API_KEY
secret_key = SECRET_KEY

# API key and secret are sent in the header
headers = {"Authorization" : "sso-key {}:{}".format(api_key, secret_key)}

# Domain availability and appraisal end points
url = "https://api.godaddy.com/v1/domains/available"
appraisal = "https://api.godaddy.com/v1/appraisal/{}"

# If a domain name is available 
# decide whether to appraise or not
do_appraise = True

# Number of domains to check in each call. 
# For example, we can not check more than 500 
# domain names in one call so we need to split 
# the list of domain names into chunks
chunk_size = 500

# Filter domain names by length
max_length = 30

# Filter domain names by price range
min_price = 0
max_price = 5000

# If appraisal is enabled, only include 
# domain names with min appraisal price
min_appr_price = 0

# When a domain is appraised, Godaddy API 
# returns similar domains sold. This is a 
# nice feature to take a look at sold domains. 
# To filter similar sold domains we can do that 
# by setting the min sale price and the min 
# year the domain was sold
min_sale_price = 0
min_sale_year = 2000

# Domain name structure: 
# prefix + keyword + suffix + extension
# You can manually insert few values into
# these lists and start the search or read
# from files as demonstrated below
prefixes = []
keywords = []
suffixes = []
extensions = []

# This list holds all generated domains
# It is the list we are going to check
all_domains = []
# This list holds similar domains sold
# This is retrieved from Godaddy appraisal API
similar_domains = []
# This holds available domains found that match
# the search criteria
found_domains = {}

# Open prefix, keyword, suffix and extension from files
# with open("prefix.txt") as f:
#    prefixes = f.read().splitlines()
# with open("keyword.txt") as f:
#    keywords = f.read().splitlines()
# with open("suffix.txt") as f:
#    suffixes = f.read().splitlines()
# with open("extension.txt") as f:
#    extensions = f.read().splitlines()
extensions = ['com','net']
# Generate domains
# for prefix in prefixes:
#    for keyword in keywords:
#       for suffix in suffixes:
prefix,keyword = RandomNameGenerator().generate_random()
for extension in extensions:
   domain = "{}{}.{}".format(prefix, keyword, extension)
   # Filter by length
   if len(domain) <= max_length:
      all_domains.append(domain)         

# This function splits all domains into chunks
# of a given size
def chunks(array, size):
   for i in range(0, len(array), size):
      yield array[i:i + size]
# Split the original array into subarrays
domain_chunks = list(chunks(all_domains, chunk_size))

# For each domain chunk (ex. 500 domains)
for domains in domain_chunks:
   # Get availability information by calling availability API
   availability_res = requests.post(url, json=domains, headers=headers)
   #import pdb;pdb.set_trace()
   # Get only available domains with price range
   for domain in json.loads(availability_res.text)["domains"]:
      if domain["available"]:
         price = float(domain["price"])/1000000
         if price >= min_price and price <= max_price:
            print("{:30} : {:10}".format(domain["domain"], price))
            found_domains[domain["domain"]]=price
   print("-----------------------------------------------")
   # API call frequency should be ~ 30 calls per minute 
   time.sleep(2)

# For each domain found get appraisal value and similar sold domains
# Filter domains by appraisal price
# Filter similar sold domains by sale price and year
if not do_appraise:
   exit()
for domain, price in found_domains.items():
   # Call appraisl API
   appraisal_res = requests.get(appraisal.format(domain), headers=headers).json()
   try:
      # Get appraisal and similar sold domains
      govalue = appraisal_res["govalue"]
      comparable_sales = appraisal_res["comparable_sales"]
   except:
      print(appraisal_res)
      continue
   # Filter by min appraisal price
   if govalue >= min_appr_price:
      print("{:30} : {:10} : {}".format(domain, price, govalue))
   for sale in comparable_sales:
      # Filter similar sold domains by price and year
      if sale["price"] >= min_sale_price and sale["year"] >= min_sale_year:
         similar_domain = "{:30} : {:10} : {:10}".format(
            sale["domain"], sale["price"], sale["year"])
         # Do not include duplicates
         if similar_domain not in similar_domains:
            similar_domains.append(similar_domain)
   # Do not abuse the API
   time.sleep(2)

# Print similar sold domains
print("--------------------------------------------------------")
for domain in similar_domains:
   print(domain)
print("--------------------------------------------------------")