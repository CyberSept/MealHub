from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from polls.models import Food, Poll


def home(request):
    # out_food_ids = Poll.objects.filter(out=True).values_list('meal', flat=True)
    # in_food_ids = Poll.objects.filter(out=False).values_list('meal', flat=True)
    #
    # temp_dict = {}
    # temp_list = []
    #
    # for i in range(len(out_food_ids)):
    #     # print(Food.objects.get(id=food_ids[i]), Poll.objects.filter(meal=food_ids[i]))
    #     if Food.objects.get(id=out_food_ids[i]) not in temp_list:
    #         temp_list.append(Food.objects.get(id=out_food_ids[i]))
    #         temp_dict[Poll.objects.filter(meal=out_food_ids[i]).filter(out=True).distinct()] = Food.objects.get(id=out_food_ids[i])
    #
    # temp_list2 = []
    # for i in range(len(in_food_ids)):
    #     # print(Food.objects.get(id=food_ids[i]), Poll.objects.filter(meal=food_ids[i]))
    #     if Food.objects.get(id=out_food_ids[i]) not in temp_list2:
    #         temp_list2.append(Food.objects.get(id=out_food_ids[i]))
    #         temp_dict[Poll.objects.filter(meal=in_food_ids[i]).filter(out=False).distinct()] = Food.objects.get(id=in_food_ids[i])


    food_dict = {}
    food_ids = Poll.objects.values_list('meal', flat=True).distinct()

    print(food_dict)
    for i in range(len(food_ids)):
        food_dict[Food.objects.get(id=food_ids[i])] = Poll.objects.filter(meal=food_ids[i])

    if request.method == 'POST':
        Poll.objects.update_or_create(user=request.user)
        query = Poll.objects.filter(user=request.user)
        if query[0].meal_id != int(request.POST.get('food')):
            query.update(meal=request.POST.get('food'), note='', out=request.POST.get('out'))
            return redirect('orderer')

    context = {'food': food_dict}
    return render(request, 'polls/home.html', context)


def hungry(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'yes':
            if not Poll.objects.filter(user_id=request.user.id) and request.user.id is not None:
                Poll.objects.create(user_id=request.user.id)
            return redirect('out_or_in')
        else:
            return redirect('home')
    context = {}
    return render(request, 'polls/hungry.html', context)


@login_required(login_url='login')
def out_or_in(request):
    query = Poll.objects.get(user=request.user)

    if query.out is not None:
        return redirect('orderer')

    if request.method == 'POST':
        poll = Poll.objects.filter(user=request.user.id)
        if request.POST.get('action') == 'out':
            poll.update(out=1)
        else:
            poll.update(out=0)
        return redirect('orderer')
    context = {}
    return render(request, 'polls/out_or_in.html', context)


@login_required(login_url='login')
def orderer(request):
    query = Poll.objects.get(user=request.user)

    if query.orderer is not None:
        return redirect('food_choice')

    if request.method == 'POST':
        poll = Poll.objects.filter(user=request.user.id)
        if request.POST.get('action') == 'yes':
            poll.update(orderer=1)
        else:
            poll.update(orderer=0)
        return redirect('food_choice')
    context = {}
    return render(request, 'polls/orderer.html', context)


@login_required(login_url='login')
def food_choice(request):
    query = Poll.objects.get(user=request.user)

    if query.meal is not None:
        return redirect('order_menu')

    order = query.out
    food = Food.objects.all()
    context = {'food': food, 'order': order}

    if request.method == 'POST':
        food_input = request.POST.get('add-food')
        poll = Poll.objects.filter(user=request.user)
        if food_input != '' and food_input is not None:
            food_list = Food.objects.create(food_item=food_input)
            poll.update(meal=food_list.id)
        else:
            poll.update(meal=request.POST.get('food'))

        return redirect('order_menu')

    return render(request, 'polls/food_choice.html', context)


@login_required(login_url='login')
def order_menu(request):
    query = Poll.objects.filter(user=request.user)

    if query[0].note is not None:
        return redirect('review')

    food = query[0].meal.food_item
    if request.method == 'POST':
        query.update(note=request.POST.get('text'))
        return redirect('review')
    context = {'food': food}
    return render(request, 'polls/order_menu.html', context)


@login_required(login_url='login')
def review(request):
    query = Poll.objects.filter(user=request.user)
    edit = request.POST.get('edit')
    error = None
    if edit == 'food':
        query.update(meal=None, note=None)
        return redirect('food_choice')
    elif edit == 'menu':
        query.update(note=None)
        return redirect('order_menu')
    elif edit == 'out':
        query.update(out=None)
        return redirect('out_or_in')
    elif edit == 'orderer':
        query.update(orderer=None)
        return redirect('orderer')

    if request.POST.get('action') == 'submit':
        if query[0].meal is not None and query[0].note is not None and \
                query[0].out is not None and query[0].orderer is not None:
            return redirect('home')
        else:
            error = 'Some info is missing! Please complete!'
    context = {'order_details': query[0], 'error': error}
    return render(request, 'polls/review.html', context)


@login_required(login_url='login')
def clear(request):
    query = Poll.objects.filter(user=request.user)
    query.update(meal=None, note=None, out=None, orderer=None)
    return redirect('home')
