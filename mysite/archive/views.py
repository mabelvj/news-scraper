from django.shortcuts import render
from .models import New


def news_list(request):
    news = New.objects.order_by('entry_type', 'date')
    # .filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'archive/news_list.html', {'news': news})
