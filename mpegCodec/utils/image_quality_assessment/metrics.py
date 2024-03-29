﻿import scipy.ndimage
from scipy import signal, ndimage
import scipy
import numpy as np

def psnr(l, k):

    # RFZ: o cálculo de n deve ser parametrizado, para imagens de diferentes dimensões
	r, c, d = l.shape
	n = float(r*c) #len(l)  
	L = 2**8 - 1
	PSNRaleat = []
	for i in range (d):
		aa = (l[:,:,i] - k[:,:,i])**2
		ba = np.sum(aa)
		MSE1 = (1/n)*ba
	
		if MSE1==0:
			PSNRaleat += [float('inf')]
		else:
			PSNRaleat += [10.0 * np.log10(((L**2.0)/MSE1))]
    
	return PSNRaleat

def mae(a, b):
	r, c, d = a.shape
	mae = []
	for i in range (d):
		n = float(r*c)
		mae += [np.sum(np.abs((b[:,:,i]-a[:,:,i])))*(1/n)]
	return mae

def mse(a, b):
	r, c, d = a.shape
	n = float(r*c)
	mse = []
	for i in range (d):
		mse += [np.sum((b[:,:,i]-a[:,:,i])**2)*(1/n)]
	return mse

def snrNo(a):
	r, c, d = a.shape
	snr = []
	for i in range (d):
		snr += [np.mean(a[:,:,i])/np.std(a[:,:,i])]
	return snr

def snrFull(l,k):
	r, c, d = l.shape
	N = float(r*c)
	snr = []
	for i in range (d):
		mse = np.sum(np.abs((k-l)))*(1/N)
		snr += [10*np.log10(np.sum((l**2))/(N*mse))]
	return snr

def cc(l,k):
	r, c, d = l.shape
	cc = []
	cc = pearson(l,k)
	return cc
	
def pearson(x,y):
	r, c, d = x.shape
	resp = []
	for i in range (d):
		xb = np.mean(x[:,:,i])
		yb = np.mean(y[:,:,i])
	
		x1 = xb -x[:,:,i]
	    
		y1 = yb - y[:,:,i]
	
		a = x1*y1
	
		num = np.sum(a)
	
		x2 = x1**2
		y2 = y1**2
	
		b = np.sum(x2)
		c = np.sum(y2)
		d = c*b
		den = d**0.5
	
		resp += [num/den]

	return resp

#def ag (img):
#	r, c, d = img.shape
#	resp = []
#	for w in range (d):
#		x = 0.
#		for i in range (r-1):
#			for j in range (c-1):
#				x += sqrt ((img[i,j,w]-img[i+1,j,w])**2+(img[i,j,w]-img[i,j+1,w])**2)
#		resp += [x/float((r-1)*(c-1))]
#	return resp

def msim(img_mat_1, img_mat_2):

	# RFZ: # L e window dever ser passados como parâmetros da função. Valores default devem ser fornecidos
	# Valores default devem ser fornecidos
	r, c, d = img_mat_1.shape
	index = []
	for i in range(d):
		std =3
		L = 6*std +1 # comprimento do filtro
		window = signal.gaussian(L, std) # vetor Gaussiano unidimensional
		#x = misc.lena()                  # imagem de entrada
	
		# kernel 2d (usando fft)
		w = window.reshape((L,1))
		wt = np.transpose(w)
		h = w * wt
		soma = np.sum(h)
		h = h/soma
	
		#convertere para float
		img_mat_1=img_mat_1.astype(np.float)
		img_mat_2=img_mat_2.astype(np.float)
	
		#Squares of input matrices
		img_mat_1_sq=img_mat_1[:,:,i]**2
		img_mat_2_sq=img_mat_2[:,:,i]**2
		img_mat_12=img_mat_1[:,:,i]*img_mat_2[:,:,i]
	    
		#Means obtained by Gaussian filtering of inputs
		img_mat_mu_1=ndimage.filters.convolve(img_mat_1[:,:,i],h)
		img_mat_mu_2=ndimage.filters.convolve(img_mat_2[:,:,i],h)
	        
		#Squares of means
		img_mat_mu_1_sq=img_mat_mu_1**2
		img_mat_mu_2_sq=img_mat_mu_2**2
		img_mat_mu_12=img_mat_mu_1*img_mat_mu_2
	    
		#Variances obtained by Gaussian filtering of inputs' squares
		img_mat_sigma_1_sq=scipy.ndimage.filters.convolve(img_mat_1_sq,h)
		img_mat_sigma_2_sq=scipy.ndimage.filters.convolve(img_mat_2_sq,h)
	    
		#Covariance
		img_mat_sigma_12=scipy.ndimage.filters.convolve(img_mat_12,h)
	
		#Centered squares of variances
		img_mat_sigma_1_sq=img_mat_sigma_1_sq-img_mat_mu_1_sq
		img_mat_sigma_2_sq=img_mat_sigma_2_sq-img_mat_mu_2_sq
		img_mat_sigma_12=img_mat_sigma_12-img_mat_mu_12;
	
	    
		#c1/c2 constants
		#First use: manual fitting
		c_1=6.5025
		c_2=58.5225
	    
		#Second use: change k1,k2 & c1,c2 depend on L (width of color map)
		l=255
		k_1=0.01
		c_1=(k_1*l)**2
		k_2=0.03
		c_2=(k_2*l)**2
	    
		#Numerator of SSIM
		num_ssim=(2*img_mat_mu_12+c_1)*(2*img_mat_sigma_12+c_2)
		#Denominator of SSIM
		den_ssim=(img_mat_mu_1_sq+img_mat_mu_2_sq+c_1)*\
		(img_mat_sigma_1_sq+img_mat_sigma_2_sq+c_2)
		#SSIM
		ssim_map=num_ssim/den_ssim
		#print ssim_map
		index+=[np.average(ssim_map)]
		
	return index