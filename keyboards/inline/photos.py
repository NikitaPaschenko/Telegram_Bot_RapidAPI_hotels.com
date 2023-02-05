from keyboa import Keyboa
from config_data.my_config import max_photos_amount

photos_markup = Keyboa(items=list(range(max_photos_amount + 1)),
                       items_in_row=6)
