from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from social.models import MyProfile, PostLike, PostComment, FollowUser, MyPost


class HomeView(TemplateView):
    template_name = "social/home.html"


class AboutView(TemplateView):
    template_name = "social/about.html"


class ContactView(TemplateView):
    template_name = "social/contact.html"


@method_decorator(login_required, name="dispatch")
class MyPostListView(ListView):
    model = MyPost

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        if self.request.user.is_superuser:
            return MyPost.objects.order_by('-id')
        else:
            return MyPost.objects.filter(uploaded_by=self.request.user.myprofile).filter(
                Q(subject__icontains=si) | Q(msg__icontains=si)).order_by('-id')


@method_decorator(login_required, name="dispatch")
class MyPostDetailView(DetailView):
    model = MyPost


@method_decorator(login_required, name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost


@method_decorator(login_required, name="dispatch")
class MyProfileListView(ListView):
    model = MyProfile

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return MyProfile.objects.filter(Q(name__icontains=si) | Q(address__icontains=si) | Q(gender__icontains=si) | Q(
            status__icontains=si)).order_by('-id')


@method_decorator(login_required, name="dispatch")
class MyProfileDetailView(DetailView):
    model = MyProfile


#
#
@method_decorator(login_required, name="dispatch")
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age", "address", "status", "gender", "phone_no", "description", "pic"]


#
#
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["pic", "subject", "msg"]

    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# for following profiles

def follow(req, pk):
    # id = req.GET.get("id")
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile/")

# class MyList(TemplateView):
#     template_name = 'college/mylist.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(MyList,self).get_context_data(**kwargs)
#         context["notices"] = Notice.objects.order_by("-id")[:3]
#         context["questions"] = Question.objects.order_by("-id")[:3]
#         return context
#
#
