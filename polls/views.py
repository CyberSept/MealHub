from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from polls.models import Food, Poll


@login_required(login_url='login')
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
    #         temp_dict[Poll.objects.filter(meal=out_food_ids[i]).filter(out=True).distinct()] = Food.objects.get(
    #             id=out_food_ids[i])
    #
    # temp_list2 = []
    # for i in range(len(in_food_ids)):
    #     # print(Food.objects.get(id=food_ids[i]), Poll.objects.filter(meal=food_ids[i]))
    #     if Food.objects.get(id=out_food_ids[i]) not in temp_list2:
    #         temp_list2.append(Food.objects.get(id=out_food_ids[i]))
    #         temp_dict[Poll.objects.filter(meal=in_food_ids[i]).filter(out=False).distinct()] = Food.objects.get(
    #             id=in_food_ids[i])

    food_dict = {}
    food_ids = Poll.objects.values_list('meal', flat=True).distinct()

    for i in range(len(food_ids)):
        food_dict[Food.objects.get(id=food_ids[i])] = Poll.objects.filter(meal=food_ids[i])
        print(Poll.objects.filter(meal=food_ids[i], orderer=True))  # orderers lists-------------------------

    if request.method == 'POST':
        if request.POST.get('checkbox') == 'on':
            is_paying = True
        else:
            is_paying = False

        Poll.objects.update_or_create(user=request.user)
        query = Poll.objects.filter(user=request.user)
        query.update(meal=request.POST.get('food'), note=request.POST.get('text'), orderer=is_paying,
                     out=request.POST.get('out'))

    if Poll.objects.filter(user=request.user).exists():
        info = Poll.objects.get(user=request.user)
    else:
        info = None

    context = {'food': food_dict, 'info': info}
    return render(request, 'polls/home.html', context)


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

    context = {'info': info, 'food': food, 'errors': errors}
    return render(request, 'polls/review.html', context)


@login_required(login_url='login')
def clear(request):
    query = Poll.objects.filter(user=request.user)
    query.delete()
    return redirect('home')
