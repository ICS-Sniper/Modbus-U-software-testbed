#this is the PLC 6 logic, it's about the very same thing as that in the real plc.
###### Existing emulator libraries ################
from devices import PLC
from utils import PLC1_DATA, PLC1_PROTOCOL, PLC1_ADDR, SCADA_ADDR, SCADA_TAGS
from utils import IP
import time
import multiprocessing
# from multiprocessing import Process
import threading

# from logicblock.logicblock import SETD
from logicblock.logicblock import *
from controlblock.controlblock import *
from logicblock.logicblock import bit_2_signed_integer
from logicblock.logicblock import signed_integer_2_bit
from utils import getdata, setdata

interval = 70
timeout = 20
time_interval = 1

class plc6(PLC):
	'plc6 logic'


	def pre_loop(self):
		### Initialization block #######
		self.k = 0

		self.hmiait202pv = 0
		self.hmilit101ahh = 0
		self.hmilsh601alarm = 0
		self.hmilsh601delay = 0
		self.hmilsh602alarm = 0
		self.hmilsh602delay = 0
		self.hmilsh603alarm = 0
		self.hmilsh603delay= 0
		self.hmilsl601alarm= 0
		self.hmilsl601delay= 0
		self.hmilsl602alarm= 0
		self.hmilsl602delay= 0
		self.hmilsl603alarm= 0
		self.hmilsl603delay= 0
		self.hmimidp602autoinp = 0
		self.hmimidp603autoinp= 0
		self.hmip601auto = 1
		self.hmip601avl = 1
		self.hmip601fault = 0
		self.hmip601msgpermissive=bit_2_signed_integer([0] * 6)
		self.hmip601msgshutdown=bit_2_signed_integer([0] * 6)
		self.hmip601permissive=bit_2_signed_integer([1]*16)
		self.hmip601reset = 0
		self.hmip601sd=bit_2_signed_integer([0]*16)
		self.hmip601shutdown= bit_2_signed_integer([0]*16)
		self.hmip601status= 1
		self.hmip602auto = 1
		self.hmip602avl = 1
		self.hmip602fault = 0
		self.hmip602msgpermissive=bit_2_signed_integer([0] * 6)
		self.hmip602msgshutdown=bit_2_signed_integer([0] * 6)
		self.hmip602permissive=bit_2_signed_integer([1]*16)
		self.hmip602reset = 0
		self.hmip602sd=bit_2_signed_integer([0]*16)
		self.hmip602shutdown= bit_2_signed_integer([0]*16)
		self.hmip602status= 1
		self.hmip603auto = 1
		self.hmip603avl = 1
		self.hmip603fault = 0
		self.hmip603msgpermissive=bit_2_signed_integer([0] * 6)
		self.hmip603msgshutdown=bit_2_signed_integer([0] * 6)
		self.hmip603permissive=bit_2_signed_integer([1]*16)
		self.hmip603reset = 0
		self.hmip603sd=bit_2_signed_integer([0]*16)
		self.hmip603shutdown= bit_2_signed_integer([0]*16)
		self.hmip603status= 1
		self.hmip6permissiveon = 1
		self.hmip6state = 1
		self.hmiplantautooff= 0
		self.hmiplantautoon= 1
		self.hmiplantcriticalsdon= 0
		self.hmiplantreseton= 1
		self.hmiplantstart= 1
		self.hmiplantstop= 0
		self.hmip301status = 1
		self.hmip302status = 1
		self.hmimv301open = 1
		self.hmimv301close = 0
		self.hmimv302close = 0
		self.hmimv303open = 1
		self.hmimv303close = 0
		self.hmimv304close = 0
		self.hmimv304open = 1
		self.hmip401status = 1
		self.hmip402status = 1
		self.hmip501status = 1
		self.hmip502status = 1
		self.hmimv501open = 1
		self.hmimv501close = 0
		self.hmimv502open = 1
		self.hmimv502close = 0
		self.hmimv503open = 1
		self.hmimv503close = 0
		self.hmimv504open = 1
		self.hmimv504close = 0
		self.hmip6state_prev = 0

		# End of Initialization block #######

		self.Mid_P601_AutoInp = self.hmip601status-1
		self.Mid_P_PERMEATE_SR = self.Mid_P601_AutoInp
		self.Mid_P602_AutoInp = self.hmimidp602autoinp
		self.Mid_P603_AutoInp = self.hmip603status-1


		self.LSL601_FB = SWITCH_FBD(self.hmilsl601delay)
		self.LSL602_FB = SWITCH_FBD(self.hmilsl602delay)
		self.LSL603_FB = SWITCH_FBD(self.hmilsl603delay)
		self.LSH601_FB = SWITCH_FBD(self.hmilsh601delay)
		self.LSH602_FB = SWITCH_FBD(self.hmilsh602delay)
		self.LSH603_FB = SWITCH_FBD(self.hmilsh603delay)
		self.P601 = PMP_FBD(self.hmip601avl,self.hmip601fault,self.hmip601shutdown)
		self.P602 = PMP_FBD(self.hmip602avl,self.hmip602fault,self.hmip602shutdown)
		self.P603 = PMP_FBD(self.hmip603avl,self.hmip603fault,self.hmip603shutdown)

		################## multiprocessing manager ###########
		manager = multiprocessing.Manager()
		self.shared = manager.dict({
			"hmiait202pv": self.hmiait202pv,
			"hmilit101ahh": self.hmilit101ahh,
			"hmip301status": self.hmip301status,
			"hmip302status": self.hmip302status,
			"hmimv301open": self.hmimv301open,
			"hmimv301close": self.hmimv301close,
			"hmimv302close": self.hmimv302close,
			"hmimv303open": self.hmimv303open,
			"hmimv303close": self.hmimv303close,
			"hmimv304close": self.hmimv304close,
			"hmimv304open": self.hmimv304open,
			"hmip401status": self.hmip401status,
			"hmip402status": self.hmip402status,
			"hmip501status": self.hmip501status,
			"hmip502status": self.hmip502status,
			"hmimv501open": self.hmimv501open,
			"hmimv501close": self.hmimv501close,
			"hmimv502open": self.hmimv502open,
			"hmimv502close": self.hmimv502close,
			"hmimv503open": self.hmimv503open,
			"hmimv503close": self.hmimv503close,
			"hmimv504open": self.hmimv504open,
			"hmimv504close": self.hmimv504close,
			"hmiplantautooff": self.hmiplantautooff,
			"hmiplantautoon": self.hmiplantautoon,
			"hmiplantcriticalsdon": self.hmiplantcriticalsdon,
			"hmiplantreseton": self.hmiplantreseton,
			"hmiplantstart": self.hmiplantstart,
			"hmiplantstop": self.hmiplantstop,
			"hmimidp602autoinp": self.hmimidp602autoinp,

		})

		#######################################################

		time.sleep(10)
		print ("	PLC6 started\n")

	def fetchData(self,state):
		if state == 1:
			self.shared["hmiplantstart"]= getdata(self, 'HMI.PLANT.Start',SCADA_ADDR,self.shared["hmiplantstart"])
		if state == 2:
			self.shared["hmiait202pv"] =getdata(self, 'HMI.AIT202.Pv',SCADA_ADDR,self.shared["hmiait202pv"])
			self.shared["hmilit101ahh"] = getdata(self, 'HMI.LIT101.AHH',SCADA_ADDR,self.shared["hmilit101ahh"])
			self.shared["hmimidp602autoinp"] = getdata(self, 'HMI.Mid_P602_AutoInp',SCADA_ADDR,self.shared["hmimidp602autoinp"])
			# self.shared["hmimidp603autoinp"] = getdata(self, 'HMI.Mid_P603_AutoInp',SCADA_ADDR,self.shared["hmimidp603autoinp"])
		self.shared["hmip301status"] = getdata(self, 'HMI.P301.Status',SCADA_ADDR,self.shared["hmip301status"])
		self.shared["hmip302status"] = getdata(self, 'HMI.P302.Status',SCADA_ADDR,self.shared["hmip302status"])
		self.shared["hmimv301open"] = getdata(self, 'HMI.MV301.Open',SCADA_ADDR,self.shared["hmimv301open"])
		self.shared["hmimv301close"] = getdata(self, 'HMI.MV301.Close',SCADA_ADDR,self.shared["hmimv301close"])
		self.shared["hmimv302close"] = getdata(self, 'HMI.MV302.Close',SCADA_ADDR,self.shared["hmimv302close"])
		self.shared["hmimv303open"] = getdata(self, 'HMI.MV303.Open',SCADA_ADDR,self.shared["hmimv303open"])
		self.shared["hmimv303close"] = getdata(self, 'HMI.MV303.Close',SCADA_ADDR,self.shared["hmimv303close"])
		self.shared["hmimv304close"] = getdata(self, 'HMI.MV304.Close',SCADA_ADDR,self.shared["hmimv304close"])
		self.shared["hmimv304open"] = getdata(self, 'HMI.MV304.Open',SCADA_ADDR,self.shared["hmimv304open"])
		self.shared["hmip401status"] = getdata(self, 'HMI.P401.Status',SCADA_ADDR,self.shared["hmip401status"])
		self.shared["hmip402status"] = getdata(self, 'HMI.P402.Status',SCADA_ADDR,self.shared["hmip402status"])
		self.shared["hmip501status"] = getdata(self, 'HMI.P501.Status',SCADA_ADDR,self.shared["hmip501status"])
		self.shared["hmip502status"] = getdata(self, 'HMI.P502.Status',SCADA_ADDR,self.shared["hmip502status"])
		self.shared["hmimv501open"] = getdata(self, 'HMI.MV501.Open',SCADA_ADDR,self.shared["hmimv501open"])
		self.shared["hmimv501close"] = getdata(self, 'HMI.MV501.Close',SCADA_ADDR,self.shared["hmimv501close"])
		self.shared["hmimv502open"] = getdata(self, 'HMI.MV502.Open',SCADA_ADDR,self.shared["hmimv502open"])
		self.shared["hmimv502close"] = getdata(self, 'HMI.MV502.Close',SCADA_ADDR,self.shared["hmimv502close"])
		self.shared["hmimv503open"] = getdata(self, 'HMI.MV503.Open',SCADA_ADDR,self.shared["hmimv503open"])
		self.shared["hmimv503close"] = getdata(self, 'HMI.MV503.Close',SCADA_ADDR,self.shared["hmimv503close"])
		self.shared["hmimv504open"] = getdata(self, 'HMI.MV504.Open',SCADA_ADDR,self.shared["hmimv504open"])
		self.shared["hmimv504close"] = getdata(self, 'HMI.MV504.Close',SCADA_ADDR,self.shared["hmimv504close"])
		self.shared["hmiplantautooff"]= getdata(self, 'HMI.PLANT.Auto_Off',SCADA_ADDR,self.shared["hmiplantautooff"])
		self.shared["hmiplantautoon"]= getdata(self, 'HMI.PLANT.Auto_On',SCADA_ADDR,self.shared["hmiplantautoon"])
		self.shared["hmiplantcriticalsdon"]= getdata(self, 'HMI.PLANT.Critical_SD_On',SCADA_ADDR,self.shared["hmiplantcriticalsdon"])
		self.shared["hmiplantreseton"]= getdata(self, 'HMI.PLANT.Reset_On',SCADA_ADDR,self.shared["hmiplantreseton"])

		self.shared["hmiplantstop"]= getdata(self, 'HMI.PLANT.Stop',SCADA_ADDR,self.shared["hmiplantstop"])

	def Actuator(self):
		# pass
		self.IO.P601.DI_Run = self.IO.P601.DO_Start
		self.IO.P602.DI_Run = self.IO.P602.DO_Start

	def Plant(self):
		# pass
		self.h_t601=0
		self.h_t602=0
		self.p = {"f_mv101":2.3*1000000000/3600,"S_t101":1.5*1000000,"S_t301":1.5*1000000,"S_t401":1.5*1000000,"S_t601":1.5*1000000,"S_t601":1.5*1000000,"S_t602":1.5*1000000,"f_p101":2.0*1000000000/3600,"f_mv201":2.0*1000000000/3600,"f_p301":2.0*1000000000/3600,"f_mv302":2.0*1000000000/3600,"f_p602":2.0*1000000000/3600,"f_p401":2.0*1000000000/36001,"f_mv501":2.0*1000000000/3600,"f_mv502":0.00006111,"f_mv503":0.00049,"f_p601":2.0*1000000000/36001,"LIT101_AL":0.2,"LIT101_AH":0.8,"LIT301_AL":0.2,"LIT301_AH":0.8,"LIT401_AL":0.2,"LIT401_AH":0.8,"LIT601_AL":0.2,"LIT601_AH":0.8,"LIT602_AL":0.2,"LIT602_AH":0.8,"cond_AIT201_AL":250,"cond_AIT201_AH":260,"ph_AIT202_AL":6.95,"ph_AIT202_AH":7.05,"orp_AIT203_AL":420,"orp_AIT203_AH":500,"cond_AIT503_AH":260,"h201_AL":50,"h202_AL":4,"h203_AL":15,"cond_AIT503_AL":250,"cond_AIT503_AH":260,"orp_AIT402_AL":420,"orp_AIT402_AH":500,"omega_inlet":0.001}  # critical plant parameters

		if self.hmip301status == 1 and self.hmip302status == 1 and self.hmimv301open==1 and  self.hmimv302close == 1 and self.hmimv303open == 1 and self.hmimv304close == 1 and self.IO.P602.DI_Run == 1:   #UF back wash procedure, 45 sec
			self.h_t602=self.h_t602- self.p['f_p602'] / self.p['S_t602']

		if self.hmip301status == 1 and self.hmip302status == 1 and self.hmimv301close == 1 and  self.hmimv302close == 1 and self.hmimv303close == 1 and self.hmimv304open == 1 and self.IO.P602.DI_Run == 0:   #UF feed tank draining procedure, 1 min
			pass

		if self.hmip401status == 2 or self.hmip402status == 2 and self.hmip501status == 2 or self.hmip502status == 2 and self.hmimv501open == 1 and self.hmimv502open == 1 and self.hmimv503close == 1 and self.hmimv504close == 1:#procedure for RO normal functioning with product of permeate 60% and backwash 40%
			self.h_t601=self.h_t601+self.p['f_mv501'] / self.p['S_t601']
			self.h_t602=self.h_t602+self.p['f_mv502'] / self.p['S_t602']

		elif self.hmip401status == 2 or self.hmip402status == 2 and self.hmip501status == 2 or self.hmip502status == 2 and self.hmimv501close == 1 and self.hmimv502close == 1 and self.hmimv503open == 1 and self.hmimv504open == 1:#procedure for RO flushing with product of backwash 60% and drain 40%
			self.h_t602=self.h_t602+self.p['f_mv503'] / self.p['S_t602']

		if self.IO.P601.DI_Run == 1: # Pumping water out of tank601
			self.h_t601=self.h_t601-self.p['f_p601'] / self.p['S_t601']

		self.result1.append(self.result1[self.k] + self.h_t601 * time_interval)
		self.result2.append(self.result2[self.k] + self.h_t602 * time_interval)

		if self.result1[self.k]>700:
			self.hmilsh601alarm = True
			# setdata(self, 'HMI.LSH601.Alarm',SCADA_ADDR,1)

		if self.result1[self.k]<200:
			self.hmilsl601alarm =True
			# setdata(self, 'HMI.LSL601.Alarm',SCADA_ADDR,1)

		if self.result2[self.k]>700:
			self.hmilsh602alarm = True
			# setdata(self, 'HMI.LSH602.Alarm',SCADA_ADDR,1)
		if self.result2[self.k]<200:
			self.hmilsl602alarm = True
			# setdata(self, 'HMI.LSL602.Alarm',SCADA_ADDR,1)

		self.k = self.k + 1

	# def Pre_Main_Product(self,IO,HMI):
	def Iteration(self):
		p = multiprocessing.Process(target=self.fetchData, args=(self.hmip6state,))
		p.start()
		p.join(timeout)
		if p.is_alive():
			print("Timeout reached, could not fetch all recent data")
			p.terminate()
			p.join()
		else:
			print("Data fetching completed")

		self.hmiait202pv =self.shared["hmiait202pv"]
		self.hmilit101ahh = self.shared["hmilit101ahh"]
		self.hmip301status = self.shared["hmip301status"]
		self.hmip302status = self.shared["hmip302status"]
		self.hmimv301open = self.shared["hmimv301open"]
		self.hmimv301close = self.shared["hmimv301close"]
		self.hmimv302close = self.shared["hmimv302close"]
		self.hmimv303open = self.shared["hmimv303open"]
		self.hmimv303close = self.shared["hmimv303close"]
		self.hmimv304close = self.shared["hmimv304close"]
		self.hmimv304open = self.shared["hmimv304open"]
		self.hmip401status = self.shared["hmip401status"]
		self.hmip402status = self.shared["hmip402status"]
		self.hmip501status = self.shared["hmip501status"]
		self.hmip502status = self.shared["hmip502status"]
		self.hmimv501open = self.shared["hmimv501open"]
		self.hmimv501close = self.shared["hmimv501close"]
		self.hmimv502open = self.shared["hmimv502open"]
		self.hmimv502close = self.shared["hmimv502close"]
		self.hmimv503open = self.shared["hmimv503open"]
		self.hmimv503close = self.shared["hmimv503close"]
		self.hmimv504open = self.shared["hmimv504open"]
		self.hmimv504close = self.shared["hmimv504close"]
		self.hmiplantautooff= self.shared["hmiplantautooff"]
		self.hmiplantautoon= self.shared["hmiplantautoon"]
		self.hmiplantcriticalsdon= self.shared["hmiplantcriticalsdon"]
		self.hmiplantreseton= self.shared["hmiplantreseton"]
		self.hmiplantstart= self.shared["hmiplantstart"]
		self.hmiplantstop= self.shared["hmiplantstop"]
		self.hmimidp602autoinp = self.shared["hmimidp602autoinp"]
		# self.hmimidp603autoinp = self.shared["hmimidp603autoinp"]

		print("PLC6 State:", self.hmip6state)

		if self.hmiplantreseton:
			# setdata(self, 'HMI.P601.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P602.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P603.Reset',SCADA_ADDR,1)
			self.hmip601reset =1
			self.hmip602reset	=1
			self.hmip603reset	=1

		if self.hmiplantautoon:
			# setdata(self, 'HMI.P601.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P602.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P603.Auto',SCADA_ADDR,1)
			self.hmip601auto =1
			self.hmip602auto	=1
			self.hmip603auto	=1

		if self.hmiplantautooff:
			# setdata(self, 'HMI.P601.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P602.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P603.Auto',SCADA_ADDR,0)
			self.hmip601auto =0
			self.hmip602auto	=0
			self.hmip603auto	=0

		# HMI.P6.Permissive_On= HMI.P601.Avl and HMI.P602.Avl
		# setdata(self, 'HMI.P6.Permissive_On',SCADA_ADDR,(self.hmip601avl and self.hmip602avl))
		self.hmip6permissiveon = (self.hmip601avl and self.hmip602avl)

		self.Mid_FIT601_Tot_Enb	= self.hmip602status==2

		# HMI.P601.Permissive[0] 	= not HMI.LSL601.Alarm
		self.hmip601permissive_arr = signed_integer_2_bit(self.hmip601permissive)
		self.hmip601permissive_arr[0] 	= int(not self.hmilsl601alarm)
		self.hmip601permissive = bit_2_signed_integer(self.hmip601permissive_arr)
		# setdata(self, 'HMI.P601.Permissive',SCADA_ADDR,self.hmip601permissive)

		# HMI.P601.MSG_Permissive[0] = HMI.P601.Permissive[0]
		self.hmip601msgpermissive_arr = signed_integer_2_bit(self.hmip601msgpermissive)
		self.hmip601msgpermissive_arr[0] = self.hmip601permissive_arr[0]
		self.hmip601msgpermissive = bit_2_signed_integer(self.hmip601msgpermissive_arr)
		# setdata(self, 'HMI.P601.MSG_Permissive',SCADA_ADDR,self.hmip601msgpermissive)

		# HMI.P601.SD[0] 	= HMI.LSL601.Alarm
		self.hmip601sd_arr = signed_integer_2_bit(self.hmip601sd)
		self.hmip601sd_arr[0] = int(self.hmilsl601alarm)
		self.hmip601sd = bit_2_signed_integer(self.hmip601sd_arr)
		# setdata(self, 'HMI.P601.SD',SCADA_ADDR,self.hmip601sd)

		self.hmip601msgshutdown_arr = signed_integer_2_bit(self.hmip601msgshutdown)
		self.hmip601shutdown_arr = signed_integer_2_bit(self.hmip601shutdown)
		self.hmip601msgshutdown_arr[1] = self.hmip601shutdown_arr[0]
		self.hmip601msgshutdown_arr[2] = self.hmip601shutdown_arr[1]
		self.hmip601msgshutdown_arr[3] = self.hmip601shutdown_arr[2]
		self.hmip601msgshutdown_arr[4] = self.hmip601shutdown_arr[3]
		self.hmip601msgshutdown_arr[5] = self.hmip601shutdown_arr[4]
		self.hmip601msgshutdown = bit_2_signed_integer(self.hmip601msgshutdown_arr)
		# setdata(self, 'HMI.P601.MSG_Shutdown',SCADA_ADDR,self.hmip601msgshutdown)

		# HMI.P602.Permissive[0] 	= not HMI.LSL602.Alarm
		self.hmip602permissive_arr = signed_integer_2_bit(self.hmip602permissive)
		self.hmip602permissive_arr[0] 	= int(not self.hmilsl602alarm)
		self.hmip602permissive = bit_2_signed_integer(self.hmip602permissive_arr)
		# setdata(self, 'HMI.P602.Permissive',SCADA_ADDR,self.hmip602permissive)

		# HMI.P602.MSG_Permissive[0] = HMI.P602.Permissive[0]
		self.hmip602msgpermissive_arr = signed_integer_2_bit(self.hmip602msgpermissive)
		self.hmip602msgpermissive_arr[0] = self.hmip602permissive_arr[0]
		self.hmip602msgpermissive = bit_2_signed_integer(self.hmip602msgpermissive_arr)
		# setdata(self, 'HMI.P602.MSG_Permissive',SCADA_ADDR,self.hmip602msgpermissive)

		# HMI.P602.SD[0] 	= 0
		self.hmip602sd_arr = signed_integer_2_bit(self.hmip602sd)
		self.hmip602sd_arr[0] = 0
		self.hmip602sd = bit_2_signed_integer(self.hmip602sd_arr)
		# setdata(self, 'HMI.P602.SD',SCADA_ADDR,self.hmip602sd)

		self.hmip602msgshutdown_arr = signed_integer_2_bit(self.hmip602msgshutdown)
		self.hmip602shutdown_arr = signed_integer_2_bit(self.hmip602shutdown)
		self.hmip602msgshutdown_arr[1] = self.hmip602shutdown_arr[0]
		self.hmip602msgshutdown_arr[2] = self.hmip602shutdown_arr[1]
		self.hmip602msgshutdown_arr[3] = self.hmip602shutdown_arr[2]
		self.hmip602msgshutdown_arr[4] = self.hmip602shutdown_arr[3]
		self.hmip602msgshutdown_arr[5] = self.hmip602shutdown_arr[4]
		self.hmip602msgshutdown = bit_2_signed_integer(self.hmip602msgshutdown_arr)
		# setdata(self, 'HMI.P602.MSG_Shutdown',SCADA_ADDR,self.hmip602msgshutdown)

		# HMI.P603.Permissive[0] 	= not HMI.LSL603.Alarm
		self.hmip603permissive_arr = signed_integer_2_bit(self.hmip603permissive)
		self.hmip603permissive_arr[0] 	= int(not self.hmilsl603alarm)
		self.hmip603permissive = bit_2_signed_integer(self.hmip603permissive_arr)
		# setdata(self, 'HMI.P603.Permissive',SCADA_ADDR,self.hmip603permissive)

		# HMI.P603.MSG_Permissive[0] = HMI.P603.Permissive[0]
		self.hmip603msgpermissive_arr = signed_integer_2_bit(self.hmip603msgpermissive)
		self.hmip603msgpermissive_arr[0] = self.hmip603permissive_arr[0]
		self.hmip603msgpermissive = bit_2_signed_integer(self.hmip603msgpermissive_arr)
		# setdata(self, 'HMI.P603.MSG_Permissive',SCADA_ADDR,self.hmip603msgpermissive)

		# HMI.P603.SD[0] 	= HMI.LSL603.Alarm
		self.hmip603sd_arr = signed_integer_2_bit(self.hmip603sd)
		self.hmip603sd_arr[0] = int(self.hmilsl603alarm)
		self.hmip603sd = bit_2_signed_integer(self.hmip603sd_arr)
		# setdata(self, 'HMI.P603.SD',SCADA_ADDR,self.hmip603sd)

		self.hmip603msgshutdown_arr = signed_integer_2_bit(self.hmip603msgshutdown)
		self.hmip603shutdown_arr = signed_integer_2_bit(self.hmip603shutdown)
		self.hmip603msgshutdown_arr[1] = self.hmip603shutdown_arr[0]
		self.hmip603msgshutdown_arr[2] = self.hmip603shutdown_arr[1]
		self.hmip603msgshutdown_arr[3] = self.hmip603shutdown_arr[2]
		self.hmip603msgshutdown_arr[4] = self.hmip603shutdown_arr[3]
		self.hmip603msgshutdown_arr[5] = self.hmip603shutdown_arr[4]
		self.hmip603msgshutdown = bit_2_signed_integer(self.hmip603msgshutdown_arr)
		# setdata(self, 'HMI.P603.MSG_Shutdown',SCADA_ADDR,self.hmip603msgshutdown)
#Main
		if self.hmiplantstop or self.hmiplantcriticalsdon:
			# setdata(self, 'HMI.P6.State',SCADA_ADDR,1)
			self.hmip6state = 1

		#self.Mid_P602_AutoInp = P6_P602_AutoInp.On

		if self.hmip6state == 1:
			self.hmip6state_prev = self.hmip6state
			self.Mid_P601_AutoInp	= 0
			self.Mid_P602_AutoInp	= 0
			self.Mid_P603_AutoInp	= 0

			if self.hmip6permissiveon and self.hmiplantstart:
				# setdata(self, 'HMI.P6.State',SCADA_ADDR,2)
				self.hmip6state = 2

		elif self.hmip6state == 2:
			self.hmip6state_prev = self.hmip6state
			self.Mid_P_PERMEATE_SR = SETD(self.hmilsh601alarm and self.hmiait202pv >= 7 and not self.hmilit101ahh and 0 ,self.hmilit101ahh or self.hmilsl601alarm or self.hmiait202pv < 7,self.Mid_P_PERMEATE_SR)
			self.Mid_P601_AutoInp	= self.Mid_P_PERMEATE_SR

			self.Mid_P602_AutoInp	= self.hmimidp602autoinp #(*SIGNAL FROM P3, UF*)
			self.Mid_P603_AutoInp	= self.hmimidp603autoinp #(*SIGNAL FROM P5, RO*), fixed to 0

		else:
			# setdata(self, 'HMI.P6.State',SCADA_ADDR,1)
			self.hmip6state = 1

#Product
		# self.hmilsl601alarm=
		self.LSL601_FB.SWITCH_FBD(self.IO.LSL601)
		# self.hmilsl602alarm=
		self.LSL602_FB.SWITCH_FBD(self.IO.LSL602)
		# self.hmilsl603alarm=
		self.LSL603_FB.SWITCH_FBD(self.IO.LSL603)
		# self.hmilsh601alarm=
		self.LSH601_FB.SWITCH_FBD(self.IO.LSH601)
		# self.hmilsh602alarm=
		self.LSH602_FB.SWITCH_FBD(self.IO.LSH602)
		# self.hmilsh603alarm=
		self.LSH603_FB.SWITCH_FBD(self.IO.LSH603)

		# self.P601.PMP_FBD(self.Mid_P601_AutoInp, self.IO.P601,HMI.P601)
		self.hmip601status_upd, self.hmip601fault, self.hmip601avl, self.hmip601shutdown = self.P601.PMP_FBD(self.Mid_P601_AutoInp, self.IO.P601, self.hmip601auto, self.hmip601reset, self.hmip601permissive, self.hmip601sd)
		if self.hmip601status_upd != -99:
			self.hmip601status = self.hmip601status_upd

		# self.P602.PMP_FBD(self.Mid_P602_AutoInp, self.IO.P602,HMI.P602)
		self.hmip602status_upd, self.hmip602fault, self.hmip602avl, self.hmip602shutdown = self.P602.PMP_FBD(self.Mid_P602_AutoInp, self.IO.P602, self.hmip602auto, self.hmip602reset, self.hmip602permissive, self.hmip602sd)
		if self.hmip602status_upd != -99:
			self.hmip602status = self.hmip602status_upd

		# self.P603.PMP_FBD(self.Mid_P603_AutoInp, self.IO.P603,HMI.P603)
		self.hmip603status_upd, self.hmip603fault, self.hmip603avl, self.hmip603shutdown = self.P603.PMP_FBD(self.Mid_P603_AutoInp, self.IO.P603, self.hmip603auto, self.hmip603reset, self.hmip603permissive, self.hmip603sd)
		if self.hmip603status_upd != -99:
			self.hmip603status = self.hmip603status_upd

		############# Physical process simulation code ################
		self.Actuator()
		self.Plant()

		############# Physical process simulation ends here ###########

		#### setdata() calls start here########
		setdata(self, 'HMI.P601.Reset',SCADA_ADDR,self.hmip601reset)
		setdata(self, 'HMI.P602.Reset',SCADA_ADDR,self.hmip602reset)
		setdata(self, 'HMI.P603.Reset',SCADA_ADDR,self.hmip603reset)
		setdata(self, 'HMI.P601.Auto',SCADA_ADDR,self.hmip601auto)
		setdata(self, 'HMI.P602.Auto',SCADA_ADDR,self.hmip602auto)
		setdata(self, 'HMI.P603.Auto',SCADA_ADDR,self.hmip603auto)
		setdata(self, 'HMI.P6.Permissive_On',SCADA_ADDR,self.hmip6permissiveon)
		setdata(self, 'HMI.P601.Permissive',SCADA_ADDR,self.hmip601permissive)
		setdata(self, 'HMI.P601.MSG_Permissive',SCADA_ADDR,self.hmip601msgpermissive)
		setdata(self, 'HMI.P601.SD',SCADA_ADDR,self.hmip601sd)
		setdata(self, 'HMI.P601.MSG_Shutdown',SCADA_ADDR,self.hmip601msgshutdown)
		setdata(self, 'HMI.P602.Permissive',SCADA_ADDR,self.hmip602permissive)
		setdata(self, 'HMI.P602.MSG_Permissive',SCADA_ADDR,self.hmip602msgpermissive)
		setdata(self, 'HMI.P602.SD',SCADA_ADDR,self.hmip602sd)
		setdata(self, 'HMI.P602.MSG_Shutdown',SCADA_ADDR,self.hmip602msgshutdown)
		setdata(self, 'HMI.P603.Permissive',SCADA_ADDR,self.hmip603permissive)
		setdata(self, 'HMI.P603.MSG_Permissive',SCADA_ADDR,self.hmip603msgpermissive)
		setdata(self, 'HMI.P603.SD',SCADA_ADDR,self.hmip603sd)
		setdata(self, 'HMI.P603.MSG_Shutdown',SCADA_ADDR,self.hmip603msgshutdown)
		if self.hmiplantstop or self.hmiplantcriticalsdon:
			setdata(self, 'HMI.P6.State',SCADA_ADDR,1)

		if self.hmip6state_prev == 1:
			if self.hmip6state == 2:
				setdata(self, 'HMI.P6.State',SCADA_ADDR,2)
				self.hmip6state_prev= 0
		if self.hmip6state_prev > 2:
			setdata(self, 'HMI.P6.State',SCADA_ADDR,1)
			self.hmip6state_prev = 0

		setdata(self, 'HMI.LSL601.Alarm',SCADA_ADDR,self.hmilsl601alarm)
		setdata(self, 'HMI.LSL602.Alarm',SCADA_ADDR,self.hmilsl602alarm)
		setdata(self, 'HMI.LSL603.Alarm',SCADA_ADDR,self.hmilsl603alarm)
		setdata(self, 'HMI.LSH601.Alarm',SCADA_ADDR,self.hmilsh601alarm)
		setdata(self, 'HMI.LSH602.Alarm',SCADA_ADDR,self.hmilsh602alarm)
		setdata(self, 'HMI.LSH603.Alarm',SCADA_ADDR,self.hmilsh603alarm)
		setdata(self, 'HMI.P601.Status',SCADA_ADDR,self.hmip601status)
		setdata(self, 'HMI.P601.Fault',SCADA_ADDR,self.hmip601fault)
		setdata(self, 'HMI.P601.Avl',SCADA_ADDR,self.hmip601avl)
		setdata(self, 'HMI.P601.Shutdown',SCADA_ADDR,self.hmip601shutdown)
		setdata(self, 'HMI.P602.Status',SCADA_ADDR,self.hmip602status)
		setdata(self, 'HMI.P602.Fault',SCADA_ADDR,self.hmip602fault)
		setdata(self, 'HMI.P602.Avl',SCADA_ADDR,self.hmip602avl)
		setdata(self, 'HMI.P602.Shutdown',SCADA_ADDR,self.hmip602shutdown)
		setdata(self, 'HMI.P603.Status',SCADA_ADDR,self.hmip603status)
		setdata(self, 'HMI.P603.Fault',SCADA_ADDR,self.hmip603fault)
		setdata(self, 'HMI.P603.Avl',SCADA_ADDR,self.hmip603avl)
		setdata(self, 'HMI.P603.Shutdown',SCADA_ADDR,self.hmip603shutdown)
		setdata(self, 'HMI.LSH601.Alarm',SCADA_ADDR,self.hmilsh601alarm)
		setdata(self, 'HMI.LSL601.Alarm',SCADA_ADDR,self.hmilsl601alarm)
		setdata(self, 'HMI.LSH602.Alarm',SCADA_ADDR,self.hmilsh602alarm)
		setdata(self, 'HMI.LSL602.Alarm',SCADA_ADDR,self.hmilsl602alarm)
		#### setdata() calls end here ########


	def _launch_next(self):
		# Schedule the next call
		threading.Timer(interval, self._launch_next).start()
		# Launch network_function in a thread
		t = threading.Thread(target=self.Iteration)
		t.daemon = True
		t.start()


	def Pre_Main_Product(self,IO):
		self.IO = IO
		self.result1=[200]
		self.result2=[200]
		self._launch_next()
		while True:
			time.sleep(1)
