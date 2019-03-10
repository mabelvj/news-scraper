from django.core.paginator import Paginator
from django.shortcuts import render
from .models import New


def news_list(request):
    news_list_ = New.objects.order_by('entry_type', 'date')
    # .filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(news_list_, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    news = paginator.get_page(page)
    return render(request, 'archive/news_list.html', {'news': news})
