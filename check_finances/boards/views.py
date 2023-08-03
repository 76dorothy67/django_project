from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Category
from .models import Post
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.template import loader


def read_all(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'boards/all_records.html', context={'posts': posts})


def create(request):
    categories = Category.objects.all()
    error_sum = ""
    error_date = ""
    record = Post()
    record.date = request.POST.get('date')
    record.sum = request.POST.get('sum')
    record.category_id = request.POST.get('categories')
    if request.method == "POST":
        if record.sum and record.date:
            record.save()
            return redirect(reverse("read_all"))
        else:
            if not record.sum:
                error_sum = "Please, fill the sum field"
            if not record.date:
                error_date = "Please, fill the date field"

    return render(request, 'boards/create.html', context={'categories': categories, 'error_date': error_date, 'error_sum': error_sum})


def read_record(request, ind):

    try:
        record = Post.objects.get(id=ind)
    except:
        print("error")

    return render(request, 'boards/read.html', context={'record': record})


def select(request):
    error_records = ""
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    records = Post.objects.filter(date__range=[request.POST.get('date_from'), request.POST.get('date_to')]).order_by('date')
    result_days = Post.objects.raw('select date, id, SUM(`sum`) as `sum` from boards_post WHERE date >= %s and date <= %s GROUP by date', [date_from, date_to])
    result_category = Post.objects.raw('select id, SUM(`sum`) as `sum` from boards_post WHERE date >= %s and date <= %s GROUP by category_id', [date_from, date_to])
    if not records:
        error_records = "There are no records in the table for these dates"


    return render(request, 'boards/select.html', context={'records': records, "error_records": error_records, 'result_days': result_days, "result_category": result_category, 'date_from': request.POST.get('date_from'), 'date_to':request.POST.get('date_to')})


def delete(request, id):
    delete_record = Post.objects.get(id=id)
    delete_record.delete()
    return redirect(reverse("read_all"))

def update_record(request, id):

    categories = Category.objects.all()
    record = Post.objects.get(id=id)
    template = loader.get_template('boards/update_record.html')
    context = {'record': record, 'categories': categories}
    return HttpResponse(template.render(context, request))

def updaterecord(request, id):
    error_sum = ""
    error_date = ""
    categories = Category.objects.all()
    record = Post.objects.get(id=id)
    record.date = request.POST.get('date')
    record.sum = request.POST.get('sum')
    record.category_id = request.POST.get('categories')
    if request.method == "POST":
        if record.date and record.sum:
            record.save()
            return redirect(reverse("read_all"))
        else:
            if not record.sum:
                error_sum = "Please, fill the sum field"
                template = loader.get_template('boards/update_record.html')
                context = {'record': record, 'categories': categories, "error_sum": error_sum}
                return HttpResponse(template.render(context, request))
            if not record.date:
                error_date = "Please, fill the date field"
                template = loader.get_template('boards/update_record.html')
                context = {'record': record, 'categories': categories, "error_date": error_date}
                return HttpResponse(template.render(context, request))
    return render(request, 'boards/all_records.html', context={'categories': categories, 'error_date': error_date, 'error_sum': error_sum})


def imagine(request):

    fig, ax = plt.subplots()
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    result_bar = Post.objects.raw('select date, id, SUM(`sum`) as `sum` from boards_post WHERE date >= %s and date <= %s GROUP by date', [date_from, date_to])
    date_x = []
    sum_y = []

    for i in result_bar:
        date_x.append(i.date)
        sum_y.append(i.sum)

    myFmt = mdates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(myFmt)


    ax.bar(date_x, sum_y, color="#00A1FF", width=0.8)

    plt.grid(axis = 'y')
    ax.set_ylabel('Sum')
    plt.xticks(rotation=15)
    plt.savefig(r'C:\Users\zozul\PycharmProjects\FinalProject\check_finances\static\bar_diagram.png')


    result_pie = Post.objects.raw('select id, SUM(`sum`) as `sum` from boards_post WHERE date >= %s and date <= %s GROUP by category_id', [date_from, date_to])
    labels = []
    sum_m = []
    explode_list = []
    sizes = []
    all_costs = 0

    for i in result_pie:
        labels.append(i.category)
        sum_m.append(i.sum)
        explode_list.append(0)

    explode = tuple(explode_list)

    for j in sum_m:
        all_costs += j

    for k in sum_m:
        sizes.append(k/all_costs)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%',
            shadow=False, startangle=90)

    patches, texts = plt.pie(sizes, shadow=False, startangle=90)
    ax1.axis('equal')

    plt.savefig(r'C:\Users\zozul\PycharmProjects\FinalProject\check_finances\static\pie_diagram.png')

    return render(request, 'boards/imagine.html',  context={'date_from': request.POST.get('date_from'), 'date_to': request.POST.get('date_to')})


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'boards/all_categories.html', context={'categories': categories})


def delete_category(request, id):
    delete_category = Category.objects.get(id=id)
    delete_category.delete()
    return redirect(reverse("all_categories"))


def create_category(request):
    error_name = ""
    categories = Category.objects.all()
    record_category = Category()
    record_category.name = request.POST.get('name_of_category')
    if request.method == "POST":
        if record_category.name:
            record_category.save()
            return redirect(reverse("all_categories"))
        else:
            error_name = "Please, fill the name of category field"
    return render(request, 'boards/create_category.html', context={'categories': categories, "error_name": error_name})


def update_category(request, id):

    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    template = loader.get_template('boards/update_category.html')
    context = {
    'category': category, 'categories': categories
    }
    return HttpResponse(template.render(context, request))

def updatecategory(request, id):

    error_name = ""
    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    category.name = request.POST.get('name_of_category')
    if request.method == "POST":
        if category.name:
            category.save()
            return redirect(reverse("all_categories"))
        else:
            error_name = "Please, fill the name of category field"
            template = loader.get_template('boards/update_category.html')
            context = {
                'category': category, 'categories': categories, "error_name": error_name
            }
            return HttpResponse(template.render(context, request))

    return render(request, 'boards/all_categories.html', context={'categories': categories, "error_name": error_name})
