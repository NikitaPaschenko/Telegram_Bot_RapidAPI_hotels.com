from keyboa import Keyboa
from config_data.my_config import max_hotels_amount

hotels_markup = Keyboa(items=list(range(1, max_hotels_amount + 1)),
                       items_in_row=6)
