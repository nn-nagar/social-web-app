from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from social.models import MyProfile, PostLike, PostComment, FollowUser, MyPost

@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "social/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        followList = FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        followList2 = []
        for e in followList:
            followList2.append(e.profile)
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        # if self.request.user.is_superuser:
        #     return MyPost.objects.order_by('-id')

        postList = MyPost.objects.filter(Q(uploaded_by__in=followList2)).filter(
            Q(subject__icontains=si) | Q(msg__icontains=si)).order_by('-id')
        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True
            ob = PostLike.objects.filter(post=p1)
            p1.likecount = ob.count()
        context["mypost_list"] = postList
        return context


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
        profList = MyProfile.objects.filter(
            Q(name__icontains=si) | Q(address__icontains=si) | Q(gender__icontains=si) | Q(
                status__icontains=si)).order_by('-id')
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile=p1, followed_by=self.request.user.myprofile)
            if ob:
                p1.followed = True
        return profList


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


def unfollow(req, pk):
    # id = req.GET.get("id")
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by=req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile/")


def like(req, pk):
    # id = req.GET.get("id")
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/home/")


def unlike(req, pk):
    # id = req.GET.get("id")
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by=req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/home/")

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
