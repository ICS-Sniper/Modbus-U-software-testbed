# this is the PLC 5 logic, it's about the very same thing as that in the real plc.
###### Existing emulator libraries ################
from devices import PLC
from utils import SCADA_ADDR, SCADA_TAGS
from utils import IP
import time
import multiprocessing
import threading


from logicblock.logicblock import SETD
from logicblock.logicblock import *
from logicblock.logicblock import TONR
from controlblock.controlblock import *
from logicblock.logicblock import bit_2_signed_integer
from logicblock.logicblock import signed_integer_2_bit
from utils import getdata, setdata

interval = 70
timeout = 20
time_interval = 1


class plc5(PLC):
	'plc5 logic'

	# def getdata(self,tag,addr,oldval):
	# 	suffix = 2
	# 	data_type_lookup = {tag[0]: tag[2] for tag in SCADA_TAGS}
	# 	data_type = data_type_lookup[tag]
	# 	val = 0
	# 	print('Fetching tag:', tag)
	# 	try:
	# 		if data_type == 'INT':
	# 			val = int(self.receive((tag, suffix),addr))
	# 		elif data_type == 'REAL':
	# 			val = float(self.receive((tag, suffix),addr))
	# 		print('Fetched value:', val)
	# 	except:
	# 		print('Could not fetch the value of', tag)
	# 		val = oldval
	# 		print('Keeping stale value:', val)
	# 	return val
	#
	# def setdata(self, tag,addr,value):
	# 	suffix = 2
	# 	data_type_lookup = {tag[0]: tag[2] for tag in SCADA_TAGS}
	# 	data_type = data_type_lookup[tag]
	# 	print('Setting tag:', tag, 'to', value)
	# 	try:
	# 		if data_type == 'INT':
	# 			self.send((tag,suffix), int(value), addr)
	# 		elif data_type == 'REAL':
	# 			self.send((tag,suffix), float(value), addr)
	# 	except:
	# 		print('Could not set the value of', tag, 'to', value)

	def pre_loop(self):

		### Initialization block #######
		self.k = 0 # counter for number of iterations

		self.hmiait501ah = 0
		self.hmiait501ahh = 0
		self.hmiait501al = 0
		self.hmiait501all = 0
		self.hmiait501hty = 0
		self.hmiait502ah = 0
		self.hmiait502ahh = 0
		self.hmiait502al = 0
		self.hmiait502all = 0
		self.hmiait502hty = 0
		self.hmiait503ah = 0
		self.hmiait503ahh = 0
		self.hmiait503al = 0
		self.hmiait503all = 0
		self.hmiait503hty = 0
		self.hmiait504ah = 0
		self.hmiait504ahh= 0
		self.hmiait504al= 0
		self.hmiait504all= 0
		self.hmiait504hty= 0
		self.hmiait504pv= 0
		self.hmiait504sah= 0
		self.hmicyp5flushingmin = 0
		self.hmicyp5hppqmaxm3h= 0
		self.hmicyp5hppqsetm3h= 0
		self.hmicyp5minrovsdspeed = 0
		self.hmicyp5mv501timeouttm= 0
		self.hmicyp5mv502timeouttm= 0
		self.hmicyp5mv503timeouttm= 0
		self.hmicyp5mv504timeouttm= 0
		self.hmicyp5rampingratepersec= 0
		self.hmicyp5rohighpumpshutdown= 0
		self.hmicyp5rohppsdon = 0
		self.hmicyp5rosdflushingmin = 0
		self.hmicyp5rosdflushingminsp = 2
		self.hmicyp5rotmp = 0
		self.hmicyp5sdflushingdoneon = 0
		self.hmicyp5vsdhighspeed = 0
		self.hmicyp5vsdminspeed = 0
		self.hmifit401all = 0
		self.hmifit501ah = 0
		self.hmifit501ahh= 0
		self.hmifit501al=0
		self.hmifit501all= 0
		self.hmifit501hty= 0
		self.hmifit501pv= 0
		self.hmifit502ah= 0
		self.hmifit502ahh= 0
		self.hmifit502al= 0
		self.hmifit502all= 0
		self.hmifit502hty= 0
		self.hmifit503ah= 0
		self.hmifit503ahh= 0
		self.hmifit503al= 0
		self.hmifit503all= 0
		self.hmifit503hty= 0
		self.hmifit504ah= 0
		self.hmifit504ahh= 0
		self.hmifit504al= 0
		self.hmifit504all= 0
		self.hmifit504hty= 0
		self.hmimv501auto =1
		self.hmimv501avl= 1
		self.hmimv501close= 0
		self.hmimv501ftc= 0
		self.hmimv501fto= 0
		self.hmimv501open= 1
		self.hmimv501reset= 1
		self.hmimv501status= 1
		self.hmimv502auto =1
		self.hmimv502avl= 1
		self.hmimv502close= 0
		self.hmimv502ftc= 0
		self.hmimv502fto= 0
		self.hmimv502open= 1
		self.hmimv502reset= 1
		self.hmimv502status= 1
		self.hmimv503auto =1
		self.hmimv503avl= 1
		self.hmimv503close= 0
		self.hmimv503ftc= 0
		self.hmimv503fto= 0
		self.hmimv503open= 1
		self.hmimv503reset= 1
		self.hmimv503status= 1
		self.hmimv504auto =1
		self.hmimv504avl= 1
		self.hmimv504close= 0
		self.hmimv504ftc= 0
		self.hmimv504fto= 0
		self.hmimv504open= 1
		self.hmimv504reset= 1
		self.hmimv504status= 1
		# self.hmip3state= 1
		self.hmip401status= 1
		self.hmip402status= 1

		self.hmip501auto= 1
		self.hmip501avl= 1
		self.hmip501driveready= 0
		self.hmip501fault = 0
		self.hmip501msgpermissive= 1
		self.hmip501msgshutdown= 1
		self.hmip501permissive= 1
		self.hmip501reset= 0
		self.hmip501resetrunhr= 1
		self.hmip501sd= 0
		self.hmip501shutdown= 0
		self.hmip501speed= 0
		self.hmip501speedcommand= 7710
		self.hmip501status= 2

		self.hmip502auto= 1
		self.hmip502avl= 1
		self.hmip502driveready= 0
		self.hmip502fault = 0
		self.hmip502msgpermissive= 1
		self.hmip502msgshutdown= 1
		self.hmip502permissive= 1
		self.hmip502reset= 0
		self.hmip502resetrunhr= 1
		self.hmip502sd= 0
		self.hmip502shutdown= 0
		self.hmip502speed= 0
		self.hmip502speedcommand= 7710
		self.hmip502status= 2

		self.hmip5permissiveon= 1
		self.hmip5state= 1

		self.hmipit501ah= 0
		self.hmipit501ahh= 0
		self.hmipit501al= 0
		self.hmipit501all= 0
		self.hmipit501hty= 1
		self.hmipit501pv= 0

		self.hmipit502ah= 0
		self.hmipit502ahh= 0
		self.hmipit502al= 0
		self.hmipit502all= 0
		self.hmipit502hty= 1
		self.hmipit502pv= 0

		self.hmipit503ah= 0
		self.hmipit503ahh= 0
		self.hmipit503al= 0
		self.hmipit503all= 0
		self.hmipit503hty= 1
		self.hmipit503pv= 0

		self.hmiplantautooff = 0
		self.hmiplantautoon = 1
		self.hmiplantreseton = 1
		self.hmiplantstart = 0
		self.hmiplantstop = 0
		self.hmiprofeeddutypumprunning = 1
		self.hmiprohighdutybothpmpnotavl= 0
		self.hmiprohighdutypumprunning = 1
		self.hmiprohighdutyselectedpmpnotavl = 0
		self.hmiprohighdutyselection = 1
		self.hmiuv401status = 1
		self.hmip5state_prev = 0
		### End of Initialization block #######
		self.Mid_Stop = 0
		self.Mid_NEXT = 0
		self.TON_FIT401_TM=TONR(3,"FIT401_TM")
		self.SEC_TEST = 0
		self.TEST_MIN = 0
		self.Mid_FIT501_Tot_Enb = 1
		self.Mid_FIT502_Tot_Enb = 1
		self.Mid_FIT503_Tot_Enb = 1
		self.Mid_FIT504_Tot_Enb = 1
		self.Mid_MV501_AutoInp = self.hmimv501status-1
		self.Mid_MV502_AutoInp = self.hmimv502status-1
		self.Mid_MV503_AutoInp = self.hmimv503status-1
		self.Mid_MV504_AutoInp = self.hmimv504status-1
		self.Mid_P50X_AutoSpeed = 0
		self.Mid_P_RO_HIGH_AutoInp = 1

		self.AIT501_FB = AIN_FBD(self.hmiait501hty,self.hmiait501ahh,self.hmiait501ah,self.hmiait501al,self.hmiait501all)
		self.AIT502_FB = AIN_FBD(self.hmiait502hty,self.hmiait502ahh,self.hmiait502ah,self.hmiait502al,self.hmiait502all)
		self.AIT503_FB = AIN_FBD(self.hmiait503hty,self.hmiait503ahh,self.hmiait503ah,self.hmiait503al,self.hmiait503all)
		self.AIT504_FB = AIN_FBD(self.hmiait504hty,self.hmiait504ahh,self.hmiait504ah,self.hmiait504al,self.hmiait504all)
		self.PIT501_FB = AIN_FBD(self.hmipit501hty,self.hmipit501ahh,self.hmipit501ah,self.hmipit501al,self.hmipit501all)
		self.PIT502_FB = AIN_FBD(self.hmipit502hty,self.hmipit502ahh,self.hmipit502ah,self.hmipit502al,self.hmipit502all)
		self.PIT503_FB = AIN_FBD(self.hmipit503hty,self.hmipit503ahh,self.hmipit503ah,self.hmipit503al,self.hmipit503all)

		self.FIT501_FB = FIT_FBD(self.hmifit501hty,self.hmifit501ahh,self.hmifit501ah,self.hmifit501al,self.hmifit501all)
		self.FIT502_FB = FIT_FBD(self.hmifit502hty,self.hmifit502ahh,self.hmifit502ah,self.hmifit502al,self.hmifit502all)
		self.FIT503_FB = FIT_FBD(self.hmifit503hty,self.hmifit503ahh,self.hmifit503ah,self.hmifit503al,self.hmifit503all)
		self.FIT504_FB = FIT_FBD(self.hmifit504hty,self.hmifit504ahh,self.hmifit504ah,self.hmifit504al,self.hmifit504all)

		self.MV501_FB  = MV_FBD(self.hmimv501fto,self.hmimv501ftc,self.hmimv501open,self.hmimv501close)
		self.MV502_FB  = MV_FBD(self.hmimv502fto,self.hmimv502ftc,self.hmimv502open,self.hmimv502close)
		self.MV503_FB  = MV_FBD(self.hmimv503fto,self.hmimv503ftc,self.hmimv503open,self.hmimv503close)
		self.MV504_FB  = MV_FBD(self.hmimv504fto,self.hmimv504ftc,self.hmimv504open,self.hmimv504close)
		self.P501_FB   = VSD_FBD(self.hmip501fault,self.hmip501shutdown,self.hmip501speed,self.hmip501driveready)
		self.P502_FB   = VSD_FBD(self.hmip502fault,self.hmip502shutdown,self.hmip502speed,self.hmip502driveready)
		self.P_RO_HIGH_DUTY_FB = Duty2_FBD()

		################## multiprocessing manager ###########
		manager = multiprocessing.Manager()
		self.shared = manager.dict({
			"hmifit401all": self.hmifit401all,
			# "hmip3state": self.hmip3state,
			"hmip401status": self.hmip401status,
			"hmip402status": self.hmip402status,
			"hmiplantautooff": self.hmiplantautooff,
			"hmiplantautoon": self.hmiplantautoon,
			"hmiplantreseton": self.hmiplantreseton,
			"hmiplantstart": self.hmiplantstart,
			"hmiplantstop": self.hmiplantstop,
			"hmiuv401status": self.hmiuv401status,
			"hmiprofeeddutypumprunning": self.hmiprofeeddutypumprunning,

        })

		#######################################################

		time.sleep(10)
		print ("	PLC5 started\n")

	def fetchData(self, state):
		if state==1:
			self.shared["hmiplantstart"] = getdata(self, 'HMI.PLANT.Start',SCADA_ADDR,self.shared["hmiplantstart"])
		self.shared["hmifit401all"] = getdata(self, 'HMI.FIT401.ALL',SCADA_ADDR,self.shared["hmifit401all"])
		# self.shared["hmip3state"] = getdata(self, 'HMI.P3.State',SCADA_ADDR,self.shared["hmip3state"])
		self.shared["hmip401status"] = getdata(self, 'HMI.P401.Status',SCADA_ADDR,self.shared["hmip401status"])
		self.shared["hmip402status"] = getdata(self, 'HMI.P402.Status',SCADA_ADDR,self.shared["hmip402status"])
		self.shared["hmiplantautooff"]= getdata(self, 'HMI.PLANT.Auto_Off',SCADA_ADDR,self.shared["hmiplantautooff"])
		self.shared["hmiplantautoon"]= getdata(self, 'HMI.PLANT.Auto_On',SCADA_ADDR,self.shared["hmiplantautoon"])
		self.shared["hmiplantreseton"]= getdata(self, 'HMI.PLANT.Reset_On',SCADA_ADDR,self.shared["hmiplantreseton"])

		self.shared["hmiplantstop"] = getdata(self, 'HMI.PLANT.Stop',SCADA_ADDR,self.shared["hmiplantstop"])
		self.shared["hmiuv401status"] = getdata(self, 'HMI.UV401.Status',SCADA_ADDR,self.shared["hmiuv401status"])
		self.shared["hmiprofeeddutypumprunning"] = getdata(self, 'HMI.P_RO_FEED_DUTY.Pump_Running',SCADA_ADDR,self.shared["hmiprofeeddutypumprunning"])

	def Actuator(self):
		self.IO.MV501.DI_ZSO = self.IO.MV501.DO_Open
		self.IO.MV501.DI_ZSC = self.IO.MV501.DO_Close
		self.IO.MV502.DI_ZSO = self.IO.MV502.DO_Open
		self.IO.MV502.DI_ZSC = self.IO.MV502.DO_Close
		self.IO.MV503.DI_ZSO = self.IO.MV503.DO_Open
		self.IO.MV503.DI_ZSC = self.IO.MV503.DO_Close
		self.IO.MV504.DI_ZSO = self.IO.MV504.DO_Open
		self.IO.MV504.DI_ZSC = self.IO.MV504.DO_Close
		self.IO.P501.DI_Run = self.IO.P501_VSD_Out.Start or not self.IO.P501_VSD_Out.Stop
		self.IO.P502.DI_Run = self.IO.P502_VSD_Out.Start or not self.IO.P502_VSD_Out.Stop


	def Plant(self):

		self.p = {"f_mv101":2.3*1000000000/3600,"S_t101":1.5*1000000,"S_t301":1.5*1000000,"S_t401":1.5*1000000,"S_t601":1.5*1000000,"S_t601":1.5*1000000,"S_t602":1.5*1000000,"f_p101":2.0*1000000000/3600,"f_mv201":2.0*1000000000/3600,"f_p301":2.0*1000000000/3600,"f_mv302":2.0*1000000000/3600,"f_p602":2.0*1000000000/3600,"f_p401":2.0*1000000000/36001,"f_mv501":2.0*1000000000/3600,"f_mv502":0.00006111,"f_mv503":0.00049,"f_p601":2.0*1000000000/36001,"LIT101_AL":0.2,"LIT101_AH":0.8,"LIT301_AL":0.2,"LIT301_AH":0.8,"LIT401_AL":0.2,"LIT401_AH":0.8,"LIT601_AL":0.2,"LIT601_AH":0.8,"LIT602_AL":0.2,"LIT602_AH":0.8,"cond_AIT201_AL":250,"cond_AIT201_AH":260,"ph_AIT202_AL":6.95,"ph_AIT202_AH":7.05,"orp_AIT203_AL":420,"orp_AIT203_AH":500,"cond_AIT503_AH":260,"h201_AL":50,"h202_AL":4,"h203_AL":15,"cond_AIT503_AL":250,"cond_AIT503_AH":260,"orp_AIT402_AL":420,"orp_AIT402_AH":500,"omega_inlet":0.001}  # critical plant parameters

		# no tank so nothing to be done
		self.k = self.k + 1

	# def Pre_Main_High_Pressure_RO(self,IO,HMI,Sec_P,Min_P):
	def Iteration(self,time):
		p = multiprocessing.Process(target=self.fetchData, args=(self.hmip5state,))
		p.start()
		p.join(timeout)
		if p.is_alive():
			print("Timeout reached, could not fetch all recent data")
			p.terminate()
			p.join()
		else:
			print("Data fetching completed")

		self.hmifit401all = self.shared["hmifit401all"]
		# self.hmip3state = self.shared["hmip3state"]
		self.hmip401status = self.shared["hmip401status"]
		self.hmip402status = self.shared["hmip402status"]
		self.hmiplantautooff= self.shared["hmiplantautooff"]
		self.hmiplantautoon= self.shared["hmiplantautoon"]
		self.hmiplantreseton= self.shared["hmiplantreseton"]
		self.hmiplantstart = self.shared["hmiplantstart"]
		self.hmiplantstop = self.shared["hmiplantstop"]
		self.hmiuv401status = self.shared["hmiuv401status"]
		self.hmiprofeeddutypumprunning = self.shared["hmiprofeeddutypumprunning"]


		print("PLC5 State:", self.hmip5state)

		Sec_P = not bool(time%(1/time_interval))
		Min_P = not bool(time%(60/time_interval))

		if self.hmiplantreseton:
			# setdata(self, 'HMI.P501.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P502.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV501.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV502.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV503.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV504.Reset',SCADA_ADDR,1)
			self.hmip501reset  = 1
			self.hmip502reset  = 1
			self.hmimv501reset  = 1
			self.hmimv502reset = 1
			self.hmimv503reset = 1
			self.hmimv504reset = 1

		if self.hmiplantautoon:
			# setdata(self, 'HMI.P501.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P502.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV501.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV502.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV503.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV504.Auto',SCADA_ADDR,1)
			self.hmip501auto  = 1
			self.hmip502auto  = 1
			self.hmimv501auto  = 1
			self.hmimv502auto = 1
			self.hmimv503auto = 1
			self.hmimv504auto = 1


		if self.hmiplantautooff:
			# setdata(self, 'HMI.P501.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P502.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.MV501.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.MV502.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.MV503.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.MV504.Auto',SCADA_ADDR,0)
			self.hmip501auto  = 0
			self.hmip502auto  = 0
			self.hmimv501auto  = 0
			self.hmimv502auto = 0
			self.hmimv503auto = 0
			self.hmimv504auto = 0

		# HMI.P5_Permissive_On= (HMI.P501.Avl or HMI.P502.Avl) and HMI.MV501.Avl and HMI.MV502.Avl and HMI.MV503.Avl and HMI.MV504.Avl
		# setdata(self, 'HMI.P5.Permissive_On',SCADA_ADDR,self.hmimv501avl and self.hmimv502avl and self.hmimv503avl and self.hmimv504avl and (self.hmip501avl or self.hmip502avl))
		self.hmip5permissiveon = self.hmimv501avl and self.hmimv502avl and self.hmimv503avl and self.hmimv504avl and (self.hmip501avl or self.hmip502avl)

		self.Mid_FIT501_Tot_Enb	= self.hmip501status==2 or self.hmip502status==2
		self.Mid_FIT502_Tot_Enb	= self.hmimv501status==2
		self.Mid_FIT503_Tot_Enb	= self.hmip401status==2 or self.hmip402status==2
		self.Mid_FIT504_Tot_Enb	= self.hmip401status==2 or self.hmip402status==2

		self.TON_FIT401_TM.TONR(self.hmifit401all and self.hmiprofeeddutypumprunning)

		# HMI.P501.Permissive[0] 	= HMI.P_RO_FEED_DUTY.Pump_Running
		# HMI.P501.Permissive[1] 	= not HMI.FIT401.ALL
		# HMI.P501.Permissive[2] 	= HMI.UV401.Status==2
		self.hmip501permissive_arr = signed_integer_2_bit(self.hmip501permissive)
		self.hmip501permissive_arr[0] 	= self.hmiprofeeddutypumprunning
		self.hmip501permissive_arr[1] 	= not self.hmifit401all
		self.hmip501permissive_arr[2] 	= self.hmiuv401status==2
		self.hmip501permissive = bit_2_signed_integer(self.hmip501permissive_arr)
		# setdata(self, 'HMI.P501.Permissive',SCADA_ADDR,self.hmip501permissive)

		# HMI.P501.MSG_Permissive[1] = HMI.P501.Permissive[0]
		# HMI.P501.MSG_Permissive[2] = HMI.P501.Permissive[1]
		# HMI.P501.MSG_Permissive[3] = HMI.P501.Permissive[2]
		self.hmip501msgpermissive_arr = signed_integer_2_bit(self.hmip501msgpermissive)
		self.hmip501msgpermissive_arr[1] = int(self.hmip501permissive_arr[0])
		self.hmip501msgpermissive_arr[2] = int(self.hmip501permissive_arr[1])
		self.hmip501msgpermissive_arr[3] = int(self.hmip501permissive_arr[2])
		self.hmip501msgpermissive = bit_2_signed_integer(self.hmip501msgpermissive_arr)
		# setdata(self, 'HMI.P501.MSG_Permissive',SCADA_ADDR,self.hmip501msgpermissive)

		# HMI.P502.Permissive[0]	= HMI.P_RO_FEED_DUTY.Pump_Running
		# HMI.P502.Permissive[1]	= not HMI.FIT401.ALL
		# HMI.P502.Permissive[2]	= HMI.UV401.Status==2
		self.hmip502permissive_arr = signed_integer_2_bit(self.hmip502permissive)
		self.hmip502permissive_arr[0] 	= int(self.hmiprofeeddutypumprunning)
		self.hmip502permissive_arr[1] 	= int(not self.hmifit401all)
		self.hmip502permissive_arr[2] 	= int(self.hmiuv401status==2)
		self.hmip502permissive = bit_2_signed_integer(self.hmip502permissive_arr)
		# setdata(self, 'HMI.P502.Permissive',SCADA_ADDR,self.hmip502permissive)

		# HMI.P502.MSG_Permissive[1] = HMI.P502.Permissive[0]
		# HMI.P502.MSG_Permissive[2] = HMI.P502.Permissive[1]
		# HMI.P502.MSG_Permissive[3] = HMI.P502.Permissive[2]
		self.hmip502msgpermissive_arr = signed_integer_2_bit(self.hmip502msgpermissive)
		self.hmip502msgpermissive_arr[1] = int(self.hmip502permissive_arr[0])
		self.hmip502msgpermissive_arr[2] = int(self.hmip502permissive_arr[1])
		self.hmip502msgpermissive_arr[3] = int(self.hmip502permissive_arr[2])
		self.hmip502msgpermissive = bit_2_signed_integer(self.hmip502msgpermissive_arr)
		# setdata(self, 'HMI.P502.MSG_Permissive',SCADA_ADDR,self.hmip502msgpermissive)

		# HMI.P501.SD[0] 	= not HMI.P_RO_FEED_DUTY.Pump_Running
		# HMI.P501.SD[1] 	= self.TON_FIT401_TM.DN
		# HMI.P501.SD[2] 	= HMI.UV401.Status!=2
		# HMI.P501.SD[3] 	= 0
		# HMI.P501.SD[4] 	= 0
		self.hmip501sd_arr = signed_integer_2_bit(self.hmip501sd)
		self.hmip501sd_arr[0] = int(not self.hmiprofeeddutypumprunning)
		self.hmip501sd_arr[1] = int(self.TON_FIT401_TM.DN)
		self.hmip501sd_arr[2] = int(self.hmiuv401status!=2)
		self.hmip501sd_arr[3] = 0
		self.hmip501sd_arr[4] = 0
		self.hmip501sd = bit_2_signed_integer(self.hmip501sd_arr)
		# setdata(self, 'HMI.P501.SD',SCADA_ADDR,self.hmip501sd)

		# HMI.P501.MSG_Shutdown[1] = HMI.P501.Shutdown[0]
		# HMI.P501.MSG_Shutdown[2] = HMI.P501.Shutdown[1]
		# HMI.P501.MSG_Shutdown[3] = HMI.P501.Shutdown[2]
		# HMI.P501.MSG_Shutdown[4] = HMI.P501.Shutdown[3]
		# HMI.P501.MSG_Shutdown[5] = HMI.P501.Shutdown[4]
		self.hmip501msgshutdown_arr = signed_integer_2_bit(self.hmip501msgshutdown)
		self.hmip501shutdown_arr = signed_integer_2_bit(self.hmip501shutdown)
		self.hmip501msgshutdown_arr[1] = self.hmip501shutdown_arr[0]
		self.hmip501msgshutdown_arr[2] = self.hmip501shutdown_arr[1]
		self.hmip501msgshutdown_arr[3] = self.hmip501shutdown_arr[2]
		self.hmip501msgshutdown_arr[4] = self.hmip501shutdown_arr[3]
		self.hmip501msgshutdown_arr[5] = self.hmip501shutdown_arr[4]
		self.hmip501msgshutdown = bit_2_signed_integer(self.hmip501msgshutdown_arr)
		# setdata(self, 'HMI.P501.MSG_Shutdown',SCADA_ADDR,self.hmip501msgshutdown)

		# HMI.P502.SD[0] 	= not HMI.P_RO_FEED_DUTY.Pump_Running
		# HMI.P502.SD[1] 	= self.TON_FIT401_TM.DN
		# HMI.P502.SD[2] 	= HMI.UV401.Status!=2
		# HMI.P502.SD[3] 	= 0
		# HMI.P502.SD[4] 	= 0
		self.hmip502sd_arr = signed_integer_2_bit(self.hmip502sd)
		self.hmip502sd_arr[0] = int(not self.hmiprofeeddutypumprunning)
		self.hmip502sd_arr[1] = int(self.TON_FIT401_TM.DN)
		self.hmip502sd_arr[2] = int(self.hmiuv401status!=2)
		self.hmip502sd_arr[3] = 0
		self.hmip502sd_arr[4] = 0
		self.hmip502sd = bit_2_signed_integer(self.hmip502sd_arr)
		# setdata(self, 'HMI.P502.SD',SCADA_ADDR,self.hmip502sd)

		# HMI.P502.MSG_Shutdown[1]= HMI.P502.Shutdown[0]
		# HMI.P502.MSG_Shutdown[2]= HMI.P502.Shutdown[1]
		# HMI.P502.MSG_Shutdown[3]= HMI.P502.Shutdown[2]
		# HMI.P502.MSG_Shutdown[4]= HMI.P502.Shutdown[3]
		# HMI.P502.MSG_Shutdown[5]= HMI.P502.Shutdown[4]
		self.hmip502msgshutdown_arr = signed_integer_2_bit(self.hmip502msgshutdown)
		self.hmip502shutdown_arr = signed_integer_2_bit(self.hmip502shutdown)
		self.hmip502msgshutdown_arr[1] = self.hmip502shutdown_arr[0]
		self.hmip502msgshutdown_arr[2] = self.hmip502shutdown_arr[1]
		self.hmip502msgshutdown_arr[3] = self.hmip502shutdown_arr[2]
		self.hmip502msgshutdown_arr[4] = self.hmip502shutdown_arr[3]
		self.hmip502msgshutdown_arr[5] = self.hmip502shutdown_arr[4]
		self.hmip502msgshutdown = bit_2_signed_integer(self.hmip502msgshutdown_arr)
		# setdata(self, 'HMI.P502.MSG_Shutdown',SCADA_ADDR,self.hmip502msgshutdown)
#Main

		if self.hmiplantstop:
			# setdata(self, 'HMI.P5.State',SCADA_ADDR,13)
			self.hmip5state = 13


		# HMI.Cy_P5.RO_TMP	=((HMI.PIT501.Pv+ HMI.PIT503.Pv)/2)-HMI.PIT502.Pv
		self.hmicyp5rotmp = ((self.hmipit501pv+self.hmipit503pv)/2)-self.hmipit502pv
		# HMI.Cy_P5.HPP_Q_MAX_M3H = 2
		self.hmicyp5hppqmaxm3h = 2
		# HMI.Cy_P5.HPP_Q_SET_M3H = 1.25
		self.hmicyp5hppqsetm3h = 1.25
		# HMI.Cy_P5.MIN_RO_VSD_SPEED		= HMI.Cy_P5.HPP_Q_SET_M3H/ HMI.Cy_P5.HPP_Q_MAX_M3H *50 *0.1
		self.hmicyp5minrovsdspeed = self.hmicyp5hppqsetm3h / self.hmicyp5hppqmaxm3h *50 *0.1
		# HMI.Cy_P5.RAMPING_RATE_PER_SEC	= 1.5
		self.hmicyp5rampingratepersec = 1.5
		# HMI.Cy_P5.VSD_MIN_SPEED			= 10
		self.hmicyp5vsdminspeed = 10
		# HMI.Cy_P5.VSD_HIGH_SPEED			= 30
		self.hmicyp5vsdhighspeed = 30

		while switch(self.hmip5state):
			if case(1):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp		= 0
				self.Mid_MV501_AutoInp			= 0
				self.Mid_MV502_AutoInp			= 0
				self.Mid_MV503_AutoInp			= 0
				self.Mid_MV504_AutoInp			= 0
				self.Mid_P50X_AutoSpeed			= self.hmicyp5vsdminspeed
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)

				if self.hmip5permissiveon and self.hmiplantstart:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,3)
					self.hmip5state = 3
				break

			if case(2):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 0
				self.Mid_P50X_AutoSpeed		= self.hmicyp5vsdminspeed
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)

				if self.hmiprofeeddutypumprunning and self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,3)
					self.hmip5state = 3
				break

			if case(3):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.Mid_P50X_AutoSpeed		= self.hmicyp5vsdminspeed
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmimv503status==2 and self.hmimv504status==2 and self.hmiprofeeddutypumprunning or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,4)
					self.hmip5state = 4
				break

			if case(4):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.Mid_P50X_AutoSpeed		= self.hmicyp5vsdminspeed
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				self.hmicyp5rohppsdon = 0
				# self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				# self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				break


			if case(5):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.Mid_P50X_AutoSpeed		= self.hmicyp5vsdminspeed
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if (self.hmip501speed >= self.Mid_P50X_AutoSpeed) or (self.hmip502speed >= self.Mid_P50X_AutoSpeed) or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,6)
					self.hmip5state = 6
				break

			if case(6):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if  self.Mid_P50X_AutoSpeed <  self.hmicyp5vsdhighspeed:
					if Sec_P:
						if (self.hmipit502pv<self.hmipit503pv) and self.hmipit501pv<250:
							self.Mid_P50X_AutoSpeed =  self.Mid_P50X_AutoSpeed + 0.5
				if ((self.hmifit501pv > self.hmicyp5hppqsetm3h) and (self.hmipit502pv<self.hmipit503pv)) and self.hmipit501pv>250 or self.Mid_NEXT:
						self.Mid_NEXT=0
						# setdata(self, 'HMI.P5.State',SCADA_ADDR,7)
						self.hmip5state = 7
				break

			if case(7):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmiait504pv < self.hmiait504sah or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,8)
					self.hmip5state = 8
				break

			if case(8):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmimv501status==2 or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,9)
					self.hmip5state = 9
				break

			if case(9):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmimv503status==1 or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,10)
					self.hmip5state = 10
				break

			if case(10):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 1
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmimv502status==2 or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,11)
					self.hmip5state = 11
				break

			if case(11):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 1
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 0
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmimv504status==1 or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,12)
					self.hmip5state = 12
				break

			if case(12):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 1
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 0
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmiplantstop or self.Mid_Stop :
					self.Mid_Stop=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,13)
					self.hmip5state = 13
				break

			if case(13):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 1
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 1
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 0
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if  self.Mid_P50X_AutoSpeed >  self.hmicyp5vsdminspeed:
					if Sec_P:
						self.Mid_P50X_AutoSpeed =  self.Mid_P50X_AutoSpeed - 0.5
				if  (self.hmip501speed <= self.hmicyp5vsdminspeed) and  (self.hmip502speed <= self.hmicyp5vsdminspeed) or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,14)
					self.hmip5state = 14
				break

			if case(14):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 1
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 0
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if not self.hmiprohighdutypumprunning or self.Mid_NEXT :
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,15)
					self.hmip5state = 15
				break

			if case(15):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 1
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				# self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				if Sec_P:
					self.hmicyp5mv504timeouttm= self.hmicyp5mv504timeouttm+1
				if self.hmimv504status==2 or self.Mid_NEXT or self.hmicyp5mv504timeouttm >120:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,16)
					self.hmip5state = 16
				break

			if case(16):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				# self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if Sec_P:
					self.hmicyp5mv502timeouttm= self.hmicyp5mv502timeouttm+1
				if self.hmimv502status==1 or self.Mid_NEXT or self.hmicyp5mv502timeouttm >120:
					self.Mid_NEXT=0
					setdata(self, 'HMI.P5.State',SCADA_ADDR,17)
					self.hmip5state = 17
				break

			if case(17):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 1
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				# self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# # setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if Sec_P:
					self.hmicyp5mv503timeouttm= self.hmicyp5mv503timeouttm+1
				if self.hmimv503status==2 or self.Mid_NEXT or self.hmicyp5mv503timeouttm >120 :
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,18)
					self.hmip5state = 18
				break

			if case(18):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				# self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# # setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmicyp5mv501timeouttm==1 or self.Mid_NEXT or self.hmicyp5mv501timeouttm >120 :
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,19)
					self.hmip5state = 19
				break

			if case(19):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.Mid_P50X_AutoSpeed		= self.hmicyp5vsdminspeed
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				# self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# # setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if self.hmicyp5rosdflushingmin>self.hmicyp5rosdflushingminsp or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,20)
					self.hmip5state = 20
				break

			if case(20):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 1
				self.Mid_MV504_AutoInp		= 1
				self.Mid_P50X_AutoSpeed		= self.hmicyp5vsdminspeed
				self.hmicyp5rohppsdon = 1
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				self.hmicyp5mv503timeouttm = 0
				self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,1)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On			=1
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV503_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV504_TIMEOUT_TM		=0
				if (not self.hmiprofeeddutypumprunning ) or self.Mid_NEXT:
					self.Mid_NEXT=0
					setdata(self, 'HMI.P5.State',SCADA_ADDR,21)
					self.hmip5state = 21
				break

			if case(21):
				self.hmip5state_prev = self.hmip5state
				self.Mid_P_RO_HIGH_AutoInp	= 0
				self.Mid_MV501_AutoInp		= 0
				self.Mid_MV502_AutoInp		= 0
				self.Mid_MV503_AutoInp		= 0
				self.Mid_MV504_AutoInp		= 0
				self.Mid_P50X_AutoSpeed		= self.hmicyp5vsdminspeed
				self.hmicyp5rohppsdon = 0
				self.hmicyp5flushingmin = 0
				self.hmicyp5rosdflushingmin = 0
				self.hmicyp5rohighpumpshutdown = 0
				self.hmicyp5sdflushingdoneon = 0
				self.hmicyp5mv501timeouttm = 0
				self.hmicyp5mv502timeouttm = 0
				# self.hmicyp5mv503timeouttm = 0
				# self.hmicyp5mv504timeouttm = 0
				# setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
				# HMI.Cy_P5.RO_HPP_SD_On=0
				# HMI.Cy_P5.FLUSHING_MIN			=0
				# HMI.Cy_P5.RO_SD_FLUSHING_MIN		=0
				# HMI.Cy_P5.RO_HIGH_PUMP_Shutdown	=0
				# HMI.Cy_P5.SD_FLUSHING_DONE_On	=0
				# HMI.Cy_P5.MV501_TIMEOUT_TM		=0
				# HMI.Cy_P5.MV502_TIMEOUT_TM		=0
				if self.hmimv503status==1 and self.hmimv504status==1 or self.Mid_NEXT or self.hmicyp5mv503timeouttm >120 or self.hmicyp5mv504timeouttm >120 :
					# setdata(self, 'HMI.P5.State',SCADA_ADDR,1)
					self.hmip5state = 1
				break
			# self.setdata('HMI.P5.State',SCADA_ADDR,1)
			self.hmip5state = 1
			break

		# self.MV501_FB.MV_FBD(self.Mid_MV501_AutoInp,self.IO.MV501,HMI.MV501)
		self.hmimv501status_upd, self.hmimv501avl = self.MV501_FB.MV_FBD(self.Mid_MV501_AutoInp, self.IO.MV501, self.hmimv501auto, self.hmimv501reset)
		if self.hmimv501status_upd!= -99:
			self.hmimv501status = self.hmimv501status_upd

		# self.MV502_FB.MV_FBD(self.Mid_MV502_AutoInp,self.IO.MV502,HMI.MV502)
		self.hmimv502status_upd, self.hmimv502avl = self.MV502_FB.MV_FBD(self.Mid_MV502_AutoInp, self.IO.MV502, self.hmimv502auto, self.hmimv502reset)
		if self.hmimv502status_upd!= -99:
			self.hmimv502status = self.hmimv502status_upd

		# self.MV503_FB.MV_FBD(self.Mid_MV503_AutoInp,self.IO.MV503,HMI.MV503)
		self.hmimv503status_upd, self.hmimv503avl = self.MV503_FB.MV_FBD(self.Mid_MV503_AutoInp, self.IO.MV503, self.hmimv503auto, self.hmimv503reset)
		if self.hmimv503status_upd!= -99:
			self.hmimv503status = self.hmimv503status_upd

		# self.MV504_FB.MV_FBD(self.Mid_MV504_AutoInp,self.IO.MV504,HMI.MV504)
		self.hmimv504status_upd, self.hmimv504avl = self.MV504_FB.MV_FBD(self.Mid_MV504_AutoInp, self.IO.MV504, self.hmimv504auto, self.hmimv504reset)
		if self.hmimv504status_upd!= -99:
			self.hmimv504status = self.hmimv504status_upd

		self.hmip501status, self.hmip501fault, self.hmip501avl, self.hmip501speed, self.hmip501driveready, self.hmip501shutdown = self.P501_FB.VSD_FBD(self.P_RO_HIGH_DUTY_FB.Start_Pmp1,self.Mid_P50X_AutoSpeed, self.IO.P501_VSD_In, self.IO.P501_VSD_Out, self.IO.P501,self.hmip501auto, self.hmip501reset, self.hmip501resetrunhr, self.hmip501speedcommand, self.hmip501permissive, self.hmip501sd)


		# self.P502_FB.VSD_FBD(self.P_RO_HIGH_DUTY_FB.Start_Pmp2,self.Mid_P50X_AutoSpeed, self.IO.P502_VSD_In, self.IO.P502_VSD_Out, self.IO.P502,HMI.P502)
		self.hmip502status, self.hmip502fault, self.hmip502avl, self.hmip502speed, self.hmip502driveready, self.hmip502shutdown = self.P502_FB.VSD_FBD(self.P_RO_HIGH_DUTY_FB.Start_Pmp2,self.Mid_P50X_AutoSpeed, self.IO.P502_VSD_In, self.IO.P502_VSD_Out, self.IO.P502,self.hmip502auto, self.hmip502reset, self.hmip502resetrunhr, self.hmip502speedcommand, self.hmip502permissive, self.hmip502sd)

		# self.P_RO_HIGH_DUTY_FB.Duty2_FBD(self.Mid_P_RO_HIGH_AutoInp,HMI.P501,HMI.P502,HMI.P_RO_HIGH_DUTY)
		self.hmiprohighdutybothpmpnotavl, self.hmiprohighdutyselectedpmpnotavl_upd, self.hmiprohighdutypumprunning = self.P_RO_HIGH_DUTY_FB.Duty2_FBD(self.Mid_P_RO_HIGH_AutoInp, self.hmip501status, self.hmip501avl, self.hmip502status, self.hmip502avl, self.hmiprohighdutyselection)
		if self.hmiprohighdutyselectedpmpnotavl_upd != -99:
			self.hmiprohighdutyselectedpmpnotavl = self.hmiprohighdutyselectedpmpnotavl_upd

		############# Physical process simulation code ################
		self.Actuator()
		self.Plant()

		############# Physical process simulation ends here ###########

		###### setdata() calls start here ###########
		setdata(self, 'HMI.P501.Reset',SCADA_ADDR,self.hmip501reset)
		setdata(self, 'HMI.P502.Reset',SCADA_ADDR,self.hmip502reset)
		setdata(self, 'HMI.MV501.Reset',SCADA_ADDR,self.hmimv501reset)
		setdata(self, 'HMI.MV502.Reset',SCADA_ADDR,self.hmimv502reset)
		setdata(self, 'HMI.MV503.Reset',SCADA_ADDR,self.hmimv503reset)
		setdata(self, 'HMI.MV504.Reset',SCADA_ADDR,self.hmimv504reset)
		setdata(self, 'HMI.P501.Auto',SCADA_ADDR,self.hmip501auto)
		setdata(self, 'HMI.P502.Auto',SCADA_ADDR,self.hmip502auto)
		setdata(self, 'HMI.MV501.Auto',SCADA_ADDR,self.hmimv501auto)
		setdata(self, 'HMI.MV502.Auto',SCADA_ADDR,self.hmimv502auto)
		setdata(self, 'HMI.MV503.Auto',SCADA_ADDR,self.hmimv503auto)
		setdata(self, 'HMI.MV504.Auto',SCADA_ADDR,self.hmimv504auto)
		setdata(self, 'HMI.P5.Permissive_On',SCADA_ADDR,self.hmip5permissiveon)
		setdata(self, 'HMI.P501.Permissive',SCADA_ADDR,self.hmip501permissive)
		setdata(self, 'HMI.P501.MSG_Permissive',SCADA_ADDR,self.hmip501msgpermissive)
		setdata(self, 'HMI.P502.Permissive',SCADA_ADDR,self.hmip502permissive)
		setdata(self, 'HMI.P502.MSG_Permissive',SCADA_ADDR,self.hmip502msgpermissive)
		setdata(self, 'HMI.P501.SD',SCADA_ADDR,self.hmip501sd)
		setdata(self, 'HMI.P501.MSG_Shutdown',SCADA_ADDR,self.hmip501msgshutdown)
		setdata(self, 'HMI.P502.SD',SCADA_ADDR,self.hmip502sd)
		setdata(self, 'HMI.P502.MSG_Shutdown',SCADA_ADDR,self.hmip502msgshutdown)
		if self.hmiplantstop:
			setdata(self, 'HMI.P5.State',SCADA_ADDR,13)
		if self.hmip5state_prev == 1:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 3:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,3)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 2:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 3:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,3)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 3:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 4:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,4)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 4:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)

		if self.hmip5state_prev == 5:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 6:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,6)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 6:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 7:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,7)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 7:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 8:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,8)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 8:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 9:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,9)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 9:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 10:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,10)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 10:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 11:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,11)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 11:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 12:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,12)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 12:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 13:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,13)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 13:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 14:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,14)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 14:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 15:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,15)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 15:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 16:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,16)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 16:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 17:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,17)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 17:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			# setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 18:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,18)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 18:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			# setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 19:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,19)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 19:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			# setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 20:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,20)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 20:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,1)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV503_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV504_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 21:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,21)
				self.hmip5state_prev = 0

		if self.hmip5state_prev == 21:
			setdata(self, 'HMI.Cy_P5.RO_HPP_SD_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_SD_FLUSHING_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.RO_HIGH_PUMP_Shutdown',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.SD_FLUSHING_DONE_On',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV501_TIMEOUT_TM',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P5.MV502_TIMEOUT_TM',SCADA_ADDR,0)
			if self.hmip5state == 1:
				setdata(self, 'HMI.P5.State',SCADA_ADDR,1)
				self.hmip5state_prev = 0

		if self.hmip5state_prev > 21:
			self.setdata('HMI.P5.State',SCADA_ADDR,1)
		setdata(self, 'HMI.MV501.Status',SCADA_ADDR,self.hmimv501status)
		setdata(self, 'HMI.MV501.Avl',SCADA_ADDR,self.hmimv501avl)
		setdata(self, 'HMI.MV502.Status',SCADA_ADDR,self.hmimv502status)
		setdata(self, 'HMI.MV502.Avl',SCADA_ADDR,self.hmimv502avl)
		setdata(self, 'HMI.MV503.Status',SCADA_ADDR,self.hmimv503status)
		setdata(self, 'HMI.MV503.Avl',SCADA_ADDR,self.hmimv503avl)
		setdata(self, 'HMI.MV504.Status',SCADA_ADDR,self.hmimv504status)
		setdata(self, 'HMI.MV504.Avl',SCADA_ADDR,self.hmimv504avl)
		setdata(self, 'HMI.P501.Status',SCADA_ADDR,self.hmip501status)
		setdata(self, 'HMI.P501.Fault',SCADA_ADDR,self.hmip501fault)
		setdata(self, 'HMI.P501.Avl',SCADA_ADDR,self.hmip501avl)
		setdata(self, 'HMI.P501.Shutdown',SCADA_ADDR,self.hmip501shutdown)
		setdata(self, 'HMI.P501.Speed',SCADA_ADDR,self.hmip501speed)
		setdata(self, 'HMI.P501.Drive_Ready',SCADA_ADDR,self.hmip501driveready)
		setdata(self, 'HMI.P502.Status',SCADA_ADDR,self.hmip501status)
		setdata(self, 'HMI.P502.Fault',SCADA_ADDR,self.hmip501fault)
		setdata(self, 'HMI.P502.Avl',SCADA_ADDR,self.hmip501avl)
		setdata(self, 'HMI.P502.Shutdown',SCADA_ADDR,self.hmip501shutdown)
		setdata(self, 'HMI.P502.Speed',SCADA_ADDR,self.hmip501speed)
		setdata(self, 'HMI.P502.Drive_Ready',SCADA_ADDR,self.hmip501driveready)
		setdata(self, 'HMI.P_RO_HIGH_DUTY.Both_Pmp_Not_Avl',SCADA_ADDR,self.hmiprohighdutybothpmpnotavl)
		setdata(self, 'HMI.P_RO_HIGH_DUTY.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hmiprohighdutyselectedpmpnotavl)

		###### setdata() calls end here ###########


	def _launch_next(self, counter):
		# Schedule the next call

		threading.Timer(interval, self._launch_next, args=(counter+1,)).start()
		# Launch network_function in a thread
		t = threading.Thread(target=self.Iteration, args=(counter,))
		t.daemon = True
		t.start()

	def Pre_Main_High_Pressure_RO(self,IO):
	# def main_loop(self):
		self.IO = IO
		counter = 0
		self._launch_next(counter)
		while True:
			time.sleep(1)
