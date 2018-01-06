# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.db import models
from django.views import View
from webapp.models import Miner
from forms import MinerForm
from d3_miner_scraper import *
from time import sleep
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['inputUsername']
        password = request.POST['inputPassword']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
    return render(request,'webapp/login.html')

def thanks(request):
	return render(request, 'webapp/logout.html')


@login_required(login_url='/login/')
def index(request):
	template_dict = {}
	query_list = Miner.objects.all()
	sum = 0.0
	counter = 0.0
	average_hash = 0.0
	high_hash = 0.0
	low_hash = 10000000000000000000.0
	for miner in query_list:
		if miner.hash_rate > high_hash:
			high_hash = miner.hash_rate
		if miner.hash_rate < low_hash:
			low_hash = miner.hash_rate

		sum = sum + miner.hash_rate
		counter = counter + 1.0
	if counter != 0.0:
		average_hash = str(sum/counter)

	template_dict['eff'] = "{0:.2f}".format((float(average_hash)/15000)*100)
	template_dict['object_list'] = query_list
	template_dict['avg_hash'] = average_hash
	template_dict['min_hash'] = low_hash
	template_dict['max_hash'] = high_hash
	template_dict['miners'] = query_list
	template_dict['user'] = request.user.get_short_name()
	# if elements != None:
	# 	template_dict['deleted'] = True
	# else:
	# 	template_dict['deleted'] = False

	return render(request,'webapp/template.html',template_dict)

@login_required(login_url='/login/')
def addminer(request):
	return render(request,'webapp/addminer.html')

@login_required(login_url='/login/')
def minerform(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
		form = MinerForm(request.POST)
		if form.is_valid():
			final_form = form.save(commit=False)
			update_one_db(final_form.ip, final_form.username, final_form.password, final_form.sshpassword)
			return redirect('/')
		else:
			return render(request, 'webapp/minerform.html', {'form': form,'invalid':True})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MinerForm()

    return render(request, 'webapp/minerform.html', {'form': form})

@login_required(login_url='/login/')
def copyright(request):
	return render(request,'webapp/copyright.html')

@login_required(login_url='/login/')
def force_refresh(request):
	update_db()
	return redirect('/')

@login_required(login_url='/login/')
def refresh_one(request):
	update_one_entry()
	return redirect('/')

@login_required(login_url='/login/')
def delete_miner(request):
	result = None
	if request.method == 'POST':
		for i in range(30):
			title = str(i) + 'delete'
			if title in request.POST:
				result = i

		if result != None:
			print "deleting " + str(result)
			delete_one_db(result)
	return redirect('/',{'delete':"true"})

@login_required(login_url='/login/')
def change_pools(request):
	if request.method == 'POST':
		target_miner = None
		target_id = None
		for i in range(30):
			title = str(i) + 'changepool'
			if title in request.POST:
				target_id = i

		query_list = Miner.objects.all()
		for miner in query_list:
			if miner.id == target_id:
				target_miner = miner

		target_id = str(target_id)
		pool_num = request.POST['pool']
		pool_arg = request.POST[target_id+'pool']
		pool_user = request.POST[target_id+'poolworker']
		pool_pass = request.POST[target_id+'poolpassword']
		set_miner_conf(target_miner.ip,'root',target_miner.sshpassword,pool_num,pool_arg,pool_user,pool_pass)

	return redirect('/')
