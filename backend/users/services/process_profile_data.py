from users.forms import AddShopForm
from users.models import Shop
from users.services.saving_seller_data import add_shop, select_shop, del_shop
import logging
logger = logging.getLogger(__name__)

def process_data_from_profile(request) -> tuple:
    if request.method == 'POST':
        if "add_shop" in request.POST:
            add_shop(request=request)
        elif "select_shop" in request.POST:
            select_shop(request=request)
        elif "delete_shop" in request.POST:
            del_shop(request=request)
    try:
        shops = Shop.objects.filter(user_id=request.user)
    except Exception as ex:
        logger.error(ex)
    form = AddShopForm()
    return form, shops

