from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from forms import LoginForm,addStudForm,addFacForm,addPerForm
from django.views.generic  import TemplateView
from .models import Student,UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


def User_login(request):
	form = LoginForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			return HttpResponseRedirect("/home")  # Redirect to a success page.
	return render(request, 'log/login.html', {'form': form})

class User_logout(LoginRequiredMixin,TemplateView):
	login_url = '/log/login'

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect('/')


class addStud(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to access this site. Please log in with a valid Profile".format(self.request.user))
		return isAdmin(self.request.user)


	def get(self, request, *args, **kwargs):
		form = addStudForm()
		return render(request,'log/addStud.html',{'form':form})

	def post(self,request):
		form = addStudForm(data=request.POST)
		if form.is_valid():
			stud = form.save(commit=False)
			print stud.usn
			passw = request.POST['password']
			print passw
			try:
				user =User.objects.create_user(username=stud.usn,password=passw,first_name=stud.name)
				print "here"
				stud.save()
				UserProfile.objects.create(user=user, student=stud, userType='S', priorityLevel=2)
				messages.success(request,"Sucessfully Added Student {0}".format(user))
				return HttpResponseRedirect('/home')
			except Exception as e :

				form.add_error('usn',e.args[1])

		return render(request, 'log/addStud.html', {'form': form})

class addFac(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to Access This Site. Please Log in with a Valid Profile to Proceed ".format(self.request.user))
		return isAdmin(self.request.user)

	def get(self, request, *args, **kwargs):
		form = addFacForm()
		return render(request,'log/addFac.html',{'form':form})

	def post(self,request):
		form = addFacForm(data=request.POST)
		if form.is_valid():
			faculty = form.save(commit=False)
			#print faculty.usn
			passw = request.POST['password']
			#print passw
			try:
				user =User.objects.create_user(username=faculty.facultyid,password=passw,first_name=faculty.name)
				print "here"
				faculty.save()
				UserProfile.objects.create(user=user,faculty=faculty,userType='F',priorityLevel=1)
				messages.success(request,"Sucessfully Added Faculty {0}".format(user))
				return HttpResponseRedirect('/home')
			except Exception as e:

				form.add_error('facultyid',e.args[1])

		return render(request, 'log/addFac.html', {'form': form})


def isAdmin(user):
	return user.userprofile.userType == 'SA'


class addPer(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
	login_url = '/log/login/'

	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to Access This Site. Please Log in with a Valid Profile to Proceed ".format(self.request.user))
		return isAdmin(self.request.user)

	def get(self, request, *args, **kwargs):
		form = addPerForm()
		return render(request,'log/addPer.html',{'form':form})

	def post(self,request):
		form = addPerForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		name = request.POST['name']
		if form.is_valid():
			try:
				user =User.objects.create_user(username=username,password=password,first_name=name)
				UserProfile.objects.create(user=user,userType='P',priorityLevel=0)
				messages.success(request,"Sucessfully Added Personnel {0}".format(user))
				return HttpResponseRedirect('/home')
			except :
				form.add_error('username',"Username Already Exists")
				print form

		return render(request, 'log/addPer.html', {'form': form})



class viewUsers(LoginRequiredMixin,UserPassesTestMixin,TemplateView):

	login_url = '/log/login/'
	def test_func(self):
		if not isAdmin(self.request.user):
			messages.error(self.request," Profile {0} Does Not Have The Priviliges to Access This Site. Please Log in with a Valid Profile to Proceed ".format(self.request.user))
		return isAdmin(self.request.user)

	def get(self, request, *args, **kwargs):
		users = UserProfile.objects.filter(~Q(userType='SA'))
		return render(request,'log/viewUser.html',{'users':users})

	def post(self,request):
		users = UserProfile.objects.filter(~Q(userType='SA'))
		list = User.objects.filter(~Q(userprofile__userType='SA'))
		for person in list:
			if person.username in request.POST:
				print request.POST[person.username].strip(), request.POST[person.username] == u'ACTIVATE'
				print u'ACTIVATE'
				if request.POST[person.username] == 'DEACTIVATE':
					person.is_active = False
					person.save()
					messages.success(request,"Successfully Deactivated User {0}".format(person))
					return HttpResponseRedirect('/home')

				elif request.POST[person.username] == 'ACTIVATE':
					print "going to activaete"
					person.is_active = True
					person.save()
					messages.success(request,"Successfully Activated User {0}".format(person))
					return HttpResponseRedirect('/home')


		return render(request,'log/viewUser.html',{'users':users})


