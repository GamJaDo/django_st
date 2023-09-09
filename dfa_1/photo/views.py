from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo
from .forms import PhotoForm

def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})

def photo_post(request):
    if request.method == "POST":
        form = PhotoForm(request.POST)
        if form.is_valid():
            # 'commit=False' 데이터베이스에 저장하지 않고 임시로 모델 객체를 생성
            photo = form.save(commit=False)
            # 'commit=False'로 생성된 모델 객체를 데이터베이스에 저장
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        # 빈 'PhotoForm'을 생성하여 사용자에게 업로드 양식을 제공
        form = PhotoForm()
    return render(request, 'photo/photo_post.html', {'form': form})

def photo_edit(request, pk):
    #예외 처리 없이 한다면
    # photo = Photo.objects.get(pk=pk) or photo = Photo.objects.filter(pk=pk).first()
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        # instance=photo 기존에 작성했던 데이터가 입력칸에 들어 있음
        form = PhotoForm(request.POST, instance=photo)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'photo/photo_post.html', {'form': form})