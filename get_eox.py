from cisco import Cisco
c = Cisco(config='apiconsole')

date_start = '2000-01-01'
date_end = '2040-12-31'
data = c.get_eox_date_range(date_start, date_end)
data_dict = c.json_to_dict(data['result'])

# upload to MySQL
from mysql.mysql import MySQL
m = MySQL(config='stage')

headers = m.get_headers(data_dict)
column_params = {k:'TEXT' for k in headers}
m.recreate_table('cisco_eox',column_params)
m.populate_table('cisco_eox',data_dict,headers,rows_per_send=300)
m.close()
