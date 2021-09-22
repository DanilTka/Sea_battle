from django.shortcuts import redirect
from users.forms import AddShopForm
from django.contrib.auth.models import User
from users.models import Shop, Seller
from django.contrib import messages


def add_shop(request):
    """Делает последний добавленный магазин в профиле продавца активным"""
    form = AddShopForm(request.POST)
    if form.is_valid():
        shop = form.save(commit=False)
        shop.user = User.objects.get(username=request.user)
        shop.save()
    else:
        messages.error(request, f'Введены некорректные данные.')
    seller = Seller.objects.get(user_id=request.user)
    shop_from_form = request.POST.__getitem__('client_id')
    try:
        shop = Shop.objects.get(user_id=seller.user_id, client_id=shop_from_form)
        seller.current_shop = shop.client_id
        seller.save()
        messages.success(request, f'Магазин успешно добавлен.')
    except:
        messages.error(request, f'Невозможно добавить магазин: {shop_from_form}. Возможно он уже привязан к другому аккаунту.')

    return redirect('home')


def select_shop(request):
    """Делает активным выбранный пользователем магазин"""
    queryset = list(request.POST.items())[1]
    if queryset[0].startswith('<QuerySet'):
        current_shop = queryset[1]
        seller = Seller.objects.get(user_id=request.user)
        seller.current_shop = current_shop
        seller.save()
        messages.info(request, f'Текущий магазин: {current_shop}')


def del_shop(request):
    """Удаляет данные выбранного магазина продавца"""
    queryset = list(request.POST.items())[1]
    if queryset[0].startswith('<QuerySet'):
        try:
            current_shop = queryset[1]
            del_shop = Shop.objects.get(user_id=request.user, client_id=current_shop)
            del_shop.delete()
            seller = Seller.objects.get(user_id=request.user)
            seller.current_shop = 0
            seller.save()
        except:
            messages.error(request, f'Не удалось удалить магазин: {current_shop}')
