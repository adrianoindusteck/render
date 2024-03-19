from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Importando modelo do arquivo models.py
from .forms import CategoryForm, TaskForm

# Importando modelos para query de consultas
from .models import Category, Task

# Create your views here.

@login_required(login_url='/contas/login/')
def add_category(request):
    # nome do arquivo html que precisa ser renderizado
    template_name = 'tasks/add_category.html'

    # variáveis que são fornecidas ao template
    context = {}

    # verifica se o método é para salvar algo no banco de dados
    if request.method == 'POST':
        # Instacia valores que vem do request
        form = CategoryForm(request.POST)
        # Verifica se os dados passados não possuem erros
        if form.is_valid():
            # Instancia a classe para salva, mas segura um pouco antes de salvar
            f = form.save(commit=False)
            # Preenche a classe com o usuário que esta logado
            f.owner = request.user
            # Grava dados no banco de dados
            f.save()
            # atribui ao objeto messages o valor Categoria Adicionada com Sucesso 
            # para informar que a operação de salvamento foi realizada com sucesso.
            messages.success(request, "Categoria Adicionada com Sucesso.")
    form = CategoryForm() # Instancia o formulário temos acesso aos campos definidos em categoria
    context['form'] = form # contém todos os elementos a serem renderizados ao usuário
    # executa a resposta do request.
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def list_categories(request):
    template_name = 'tasks/list_categories.html'

    categories = Category.objects.filter(owner=request.user)
    context = {
        'categories': categories
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def edit_category(request, id_category):
    template_name = 'tasks/add_category.html'
    context = {}
    category = get_object_or_404(Category, id=id_category, owner=request.user)
    # category = Category.objects.get(id=id_category, owner=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('tasks:list_categories')
    form = CategoryForm(instance=category)
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def delete_category(request, id_category):
    category = Category.objects.get(id=id_category)
    if category.owner == request.user:
        category.delete()
        messages.success(request, "Categoria Deletada com Sucesso.")
    else:
        messages.error(request, 'Você não tem permissão para excluir esta categoria')
        return redirect('core:home')
    return redirect('tasks:list_categories')

@login_required(login_url='/contas/login/')
def add_task(request):

    template_name = 'tasks/add_task.html'
    context = {}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            form.save_m2m()
            messages.success(request, "Tarefa Adicionada com Sucesso.")
        else:
            print(form.erros)        
    form = TaskForm()
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def tasks_list(request):
    template_name = 'tasks/tasks_list.html'
    context = {}
    tasks = Task.objects.filter(owner=request.user).exclude(status='CD')
    context['tasks'] = tasks
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def edit_task(request, id_task):
    template_name = 'tasks/add_task.html'
    context = {}
    task = get_object_or_404(Task, pk=id_task, owner=request.user)    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:tasks_list')
    form = TaskForm(instance=task)
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def task_delete(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user:
        task.delete()
        messages.success(request, "Tarefa Deletada com Sucesso.")
    else:
        messages.error(request, 'Você não tem permissão para excluir esta Tarefa')
        return redirect('core:home')
    return redirect('tasks:tasks_list')
