from pyrst.handlers import JsonHandler
from pyrst.client import BirstClient

c = BirstClient(configfile = "/Users/CVoncsefalvay/Developer/pyrst/pyrst/config.yaml")
c.login()


p = c.retrieve(query = "SELECT [item_dim.item_sub_segment] 'F3',[store_dim.store_state] 'F5',[Sum: sales_volume] 'F1' FROM [ALL]", space = "1f500014-65f9-40da-9d9d-0c0fa01a4fbf", handler = JsonHandler)
print p