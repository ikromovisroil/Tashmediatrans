from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from users.models import *
from .models import *
from .forms import *
from django.db.models import Sum, Case, When, IntegerField
# Create your views here.

@login_required
def profil(request):
    if request.method == 'POST':
        form = Userprofilform(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = Userprofilform(instance=request.user)
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'main/profil.html',context)


@login_required
def index(request):
    if request.method == 'POST':
        form = NewIshchiForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            messages.info(request, "Saqlandi ")
            return redirect(reverse('index'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot.")
    else:
        form = NewIshchiForm()
    context = {
        'istemolchi': Istemolchi.objects.filter(author=request.user).annotate(
            summa=Sum(
                Case(
                    When(qarz__status=False, then='qarz__summa'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )[::-1],
        'form': form,
        'user': request.user,
    }
    return render(request, 'main/index.html',context)

@login_required
def detail(request,pk):
    istemolchi_id = get_object_or_404(Istemolchi, id=pk)
    if request.method == 'POST':
        form = QarzForm(request.POST)
        if form.is_valid():
            qarz = form.save(commit=False)
            qarz.istemolchi = istemolchi_id
            qarz.author = request.user
            qarz.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = QarzForm()
    context = {
        'form':form,
        'istemolchi_id':istemolchi_id,
        'qarzlar':Qarz.objects.filter(istemolchi=istemolchi_id,status=False)[::-1],
        'user': request.user,
    }
    return render(request, 'main/detail.html',context)

@login_required
def qarz_delete(request, pk):
    qarz = get_object_or_404(Qarz, id=pk)
    qarz.status = True
    qarz.save()
    messages.info(request, "O'chirildi!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def xodimlar(request):
    if request.method == 'POST':
        sana = request.POST.get('sana')
        istemolchi = Istemolchi.objects.filter(author=request.user, status=True, tolov__date=sana)
    else:
        istemolchi = Istemolchi.objects.filter(author=request.user, status=True)
    context = {
        'istemolchi': istemolchi,
        'user': request.user,
    }
    return render(request, 'main/xodimlar.html', context)

@login_required
def car(request,pk):
    istemolchi_id = get_object_or_404(Istemolchi, id=pk)
    context = {
        'istemolchi_id': istemolchi_id,
        'user': request.user,
    }
    return render(request, 'main/car.html',context)


@login_required
def payment(request,pk):
    istemolchi_id = get_object_or_404(Istemolchi, id=pk)
    if request.method == 'POST':
        form = TolovForm(request.POST)
        if form.is_valid():
            tolov = form.save(commit=False)
            tolov.istemolchi = istemolchi_id
            tolov.author = request.user
            tolov.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = TolovForm()
    context = {
        'form': form,
        'tolov': Tolov.objects.filter(author=request.user, istemolchi=istemolchi_id)[:60][::-1],
        'istemolchi_id': istemolchi_id,
        'user': request.user,
    }
    return render(request, 'main/payment.html',context)


@login_required
def payment_edit(request, pk):
    tolov_id = get_object_or_404(Tolov, id=pk)
    if request.method == 'POST':
        naxt = request.POST.get('naxt')
        karta = request.POST.get('karta')
        izox = request.POST.get('izox')
        if naxt and karta:
            tolov_id.karta = karta
            tolov_id.naxt = naxt
            tolov_id.izox = izox
            tolov_id.save()
            messages.info(request, "Saqlandi")
        elif karta:
            tolov_id.karta = karta
            tolov_id.izox = izox
            tolov_id.save()
            messages.info(request, "Saqlandi")
        elif naxt:
            tolov_id.naxt = naxt
            tolov_id.izox = izox
            tolov_id.save()
            messages.info(request, "Saqlandi")
        else:
            messages.error(request, "Yaroqsiz ma'lumot.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('login'))


    