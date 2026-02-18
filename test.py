from urllib.parse import urlparse
from scraper import check_website

url = "https://www.amazon.com/Logitech-Wireless-Lightspeed-Headset-Headphone/dp/B081PP4CB6/ref=pd_ci_mcx_mh_mcx_views_0_title?pd_rd_w=YAR8h&content-id=amzn1.sym.781fe6e1-9487-4a74-b81e-5a879e5ec273%3Aamzn1.symc.c3d5766d-b606-46b8-ab07-1d9d1da0638a&pf_rd_p=781fe6e1-9487-4a74-b81e-5a879e5ec273&pf_rd_r=HEE4G6H4RG8PBMAFRKFW&pd_rd_wg=f6PqP&pd_rd_r=5939ee49-f3ac-48ea-90bf-6561410983da&pd_rd_i=B081PP4CB6&th=1"

check_website(url)