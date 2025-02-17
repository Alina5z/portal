from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Request, Category
from .forms import RequestForm, RequestStatusForm

# views.py
from django.http import JsonResponse
from .models import Request  # Импортируйте вашу модель Request


def is_admin(user):
    """Проверяет, является ли пользователь администратором."""
    return user.is_superuser or user.is_staff


@login_required
def request_list(request):
    """Отображает список заявок для пользователя или всех заявок для администратора."""
    if is_admin(request.user):
        requests = Request.objects.all()  # Все заявки для администраторов
    else:
        requests = Request.objects.filter(user=request.user)  # Заявки только для текущего пользователя
    return render(request, 'requests/request_list.html', {'requests': requests})


@login_required
def request_create(request):
    """Создает новую заявку."""
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)  # Создаем форму с данными POST
        if form.is_valid():
            request_obj = form.save(commit=False)  # Не сохраняем пока в БД
            request_obj.user = request.user  # Устанавливаем текущего пользователя как создателя заявки
            request_obj.save()  # Сохраняем заявку в БД
            messages.success(request, 'Заявка успешно создана')  # Успешное сообщение
            return redirect('request_list')  # Перенаправление на список заявок
    else:
        form = RequestForm()  # Пустая форма для GET-запроса
    return render(request, 'requests/request_form.html', {'form': form})  # Отображаем форму


@login_required
def request_detail(request, pk):
    """Отображает детали конкретной заявки."""
    request_obj = get_object_or_404(Request, pk=pk)  # Получаем заявку или 404 если не найдена
    if not is_admin(request.user) and request.user != request_obj.user:
        messages.error(request, 'У вас нет доступа к заявке')  # Ошибка доступа
        return redirect('request_list')  # Перенаправление на список заявок

    status_form = None
    if is_admin(request.user):
        if request.method == 'POST':
            status_form = RequestStatusForm(request.POST, instance=request_obj)  # Форма для изменения статуса
            if status_form.is_valid():
                status_form.save()  # Сохраняем изменения статуса
                messages.success(request, 'Статус заявки обновлен')  # Успешное сообщение
                return redirect('request_list')  # Перенаправление на список заявок
        else:
            status_form = RequestStatusForm(instance=request_obj)  # Заполняем форму текущими данными

    return render(request, 'requests/request_detail.html', {
        'request': request_obj,
        'status_form': status_form,
    })  # Отображаем детали заявки


@user_passes_test(is_admin)
def category_list(request):
    """Отображает список категорий для администраторов."""
    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'requests/category_list.html', {'categories': categories})  # Отображаем список категорий


@user_passes_test(is_admin)
def category_create(request):
    """Создает новую категорию."""
    if request.method == 'POST':
        name = request.POST.get('name')  # Получаем имя категории из POST-запроса
        if name:
            Category.objects.create(name=name)  # Создаем новую категорию
            messages.success(request, 'Категория создана')  # Успешное сообщение
        return redirect('category_list')  # Перенаправление на список категорий
    return render(request, 'requests/category_form.html')  # Отображаем форму создания категории


def get_resolved_count(request):
    """Возвращает количество разрешенных заявок в формате JSON."""
    resolved_count = Request.objects.filter(status='resolved').count()  # Подсчитываем разрешенные заявки
    return JsonResponse({'resolved_count': resolved_count})  # Возвращаем количество в формате JSON

