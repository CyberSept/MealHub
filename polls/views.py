from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from polls.models import Food, Poll


@login_required(login_url='login')
def home(request):                                                                             # count may be optional
    result = (Poll.objects.values('meal', 'meal__food_item', 'out').annotate(count=Count('meal')).order_by('-count'))

    for i, dct in enumerate(result):
        users = Poll.objects.filter(out=dct['out'], meal=dct['meal'])
        dct['users'] = users
        dct['restaurant'] = dct.pop('meal__food_item')
        dct['id'] = i
    print(result)
    result.order_by('count')
    print(result)
    if Poll.objects.filter(user=request.user).exists():
        info = Poll.objects.get(user=request.user)
    else:
        info = None

    if request.method == 'POST':
        if request.POST.get('checkbox') == 'on':
            is_paying = True
        else:
            is_paying = False

        Poll.objects.update_or_create(user=request.user)
        query = Poll.objects.filter(user=request.user)
        query.update(meal=request.POST.get('food'), note=request.POST.get('text'), orderer=is_paying,
                     out=request.POST.get('out'))
        return redirect('home')

    context = {'food': result, 'info': info}
    return render(request, 'polls/home.html', context)


def random_orderer(request):
    result = (Poll.objects.values('meal', 'out').annotate(count=Count('meal')).order_by('-count'))
    ls = []
    for dct in result:
        users = Poll.objects.filter(out=dct['out'], meal=dct['meal'], orderer=True)
        if users.exists():
            ls.append(users.order_by('?').first())

    info = Poll.objects.get(user=request.user)
    rand = None
    for i in ls:
        if i.meal_id == info.meal_id and i.out == info.out:
           rand = i

    context = {'random': rand, 'info': info}
    return render(request, 'polls/random.html', context)


@login_required(login_url='login')
def review(request):
    food = Food.objects.all()

    if Poll.objects.filter(user=request.user).exists():
        info = Poll.objects.get(user=request.user)
    else:
        info = None

    errors = []
    if request.method == 'POST':
        if request.POST.get('checkbox') == 'on':
            is_paying = True
        else:
            is_paying = False

        if request.POST.get('in_or_out') == 'out':
            in_or_out = True
        else:
            in_or_out = False

        if request.POST.get('text') == '':
            errors.append('დაწერე დეტალური მენიუ!')
        else:
            note = request.POST.get('text')

        if request.POST.get('add-food') == '' and request.POST.get('food') == '':
            errors.append('აირჩიე საკვები ობიექტი')
        elif request.POST.get('add-food') != '' and not errors:
            users_food = Food.objects.create(food_item=request.POST.get('add-food'))
        elif not errors:
            users_food = Food.objects.get(id=request.POST.get('food'))

        if request.POST.get('action') == 'submit' and not errors:

            # info = Poll.objects.update_or_create(user=request.user, meal=users_food, orderer=is_paying,
            #                                      out=in_or_out, note=note)
            if Poll.objects.filter(user=request.user).exists():
                info = Poll.objects.filter(user=request.user)
                info.update(user=request.user, meal=users_food, orderer=is_paying, out=in_or_out, note=note)
                info = Poll.objects.get(user=request.user)
            else:
                info = Poll.objects.create(user=request.user, meal=users_food, orderer=is_paying, out=in_or_out,
                                           note=note)
            return redirect('home')

    context = {'info': info, 'food': food, 'errors': errors}
    return render(request, 'polls/review.html', context)


@login_required(login_url='login')
def clear(request):
    query = Poll.objects.filter(user=request.user)
    query.delete()
    return redirect('home')
