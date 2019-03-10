from django.shortcuts import render
from .models import New


def news_list(request):
    context = {'new': New.objects.order_by('entry_type', 'date')}

    return render(request, 'archive/news_list.html', context)
