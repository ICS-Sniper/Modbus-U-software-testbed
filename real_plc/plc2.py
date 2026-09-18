#this is the PLC 2 logic, it's about the very same thing as that in the real plc.
###### Existing emulator libraries ################
from devices import PLC
from utils import SCADA_ADDR, SCADA_TAGS
from utils import IP
import time
import multiprocessing
# from multiprocessing import Process
import threading

from logicblock.logicblock import SETD
from logicblock.logicblock import TONR
from controlblock.controlblock import *
from logicblock.logicblock import bit_2_signed_integer
from logicblock.logicblock import signed_integer_2_bit
from utils import getdata, setdata

interval = 60
timeout = 20
time_interval = 1


class plc2(PLC):
	'plc2 logic'


	def pre_loop(self):

		### Initialization block #######
		self.k = 0 # counter for number of iterations

		self.hmiait201ah = 0
		self.hmiait201al = 0
		self.hmiait202ah = 0
		self.hmiait202al = 0
		self.hmiait203ah = 0
		self.hmiait203al = 0
		self.hmiait402ah = 0
		self.hmiait503ah = 0
		self.hmifit201ah = 0
		self.hmifit201all = 0
		self.hmihclbothpmpnotavl = 0
		self.hmihclselectedpmpnotavl = 0
		self.hmilit301ah = 0
		self.hmilit301al = 0
		self.hmils201alarm = 0
		self.hmils201delay = 0
		self.hmils202alarm = 0
		self.hmils202delay = 0
		self.hmilsl203alarm = 0
		self.hmilsl203delay = 0
		self.hmilsll203alarm = 0
		self.hmilsll203delay = 0
		self.hmimv201auto = 1
		self.hmimv201avl = 1
		self.hmimv201close = 0
		self.hmimv201ftc = 0
		self.hmimv201fto = 0
		self.hmimv201open = 1
		self.hmimv201status = 1
		self.hmimv301status = 1
		self.hminaclbothpmpnotavl = 0
		self.hminaclselectedpmpnotavl = 0
		self.hminaoclbothpmpnotavl = 0
		self.hminaoclselectedpmpnotavl = 0
		self.hmip201auto = 1
		self.hmip201avl = 1
		self.hmip201fault = 0
		self.hmip201msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip201msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip201permissive = bit_2_signed_integer([1]*16)
		self.hmip201reset = 0
		self.hmip201sd = bit_2_signed_integer([0]*16)
		self.hmip201shutdown = bit_2_signed_integer([0]*16)
		self.hmip201status = 1
		self.hmip202auto = 1
		self.hmip202avl = 1
		self.hmip202fault = 0
		self.hmip202msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip202msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip202permissive = bit_2_signed_integer([1]*16)
		self.hmip202reset = 0
		self.hmip202sd = bit_2_signed_integer([0]*16)
		self.hmip202shutdown = bit_2_signed_integer([0]*16)
		self.hmip202status = 1
		self.hmip203auto = 1
		self.hmip203avl = 1
		self.hmip203fault = 0
		self.hmip203msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip203msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip203permissive = bit_2_signed_integer([1]*16)
		self.hmip203reset = 0
		self.hmip203sd = bit_2_signed_integer([0]*16)
		self.hmip203shutdown = bit_2_signed_integer([0]*16)
		self.hmip203status = 1
		self.hmip204auto = 1
		self.hmip204avl = 1
		self.hmip204fault = 0
		self.hmip204msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip204msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip204permissive = bit_2_signed_integer([1]*16)
		self.hmip204reset = 0
		self.hmip204sd = bit_2_signed_integer([0]*16)
		self.hmip204shutdown = bit_2_signed_integer([0]*16)
		self.hmip204status = 1
		self.hmip205auto = 1
		self.hmip205avl = 1
		self.hmip205fault = 0
		self.hmip205msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip205msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip205permissive = bit_2_signed_integer([1]*16)
		self.hmip205reset = 0
		self.hmip205sd = bit_2_signed_integer([0]*16)
		self.hmip205shutdown = bit_2_signed_integer([0]*16)
		self.hmip205status = 1
		self.hmip206auto = 1
		self.hmip206avl = 1
		self.hmip206fault = 0
		self.hmip206msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip206msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip206permissive = bit_2_signed_integer([1]*16)
		self.hmip206reset = 0
		self.hmip206sd = bit_2_signed_integer([0]*16)
		self.hmip206shutdown = bit_2_signed_integer([0]*16)
		self.hmip206status = 1
		self.hmip207avl = 1
		self.hmip207fault = 0
		self.hmip207msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip207msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip207permissive = bit_2_signed_integer([1]*16)
		self.hmip207sd = bit_2_signed_integer([0]*16)
		self.hmip207shutdown = bit_2_signed_integer([0]*16)
		self.hmip207status = 1
		self.hmip208avl = 1
		self.hmip208fault = 0
		self.hmip208msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip208msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip208permissive = bit_2_signed_integer([1]*16)
		self.hmip208sd = bit_2_signed_integer([0]*16)
		self.hmip208shutdown = bit_2_signed_integer([0]*16)
		self.hmip2permissiveon = 1
		self.hmip2shutdown = 1
		self.hmip2state = 1
		self.hmiphcldutyselection = 1
		self.hmiplantautooff = 0
		self.hmiplantautoon = 1
		self.hmiplantcriticalsdon = 0
		self.hmiplantreseton = 1
		self.hmiplantstart = 0
		self.hmiplantstop = 0
		self.hmipnacldutyselection = 1
		self.hmipnaoclfacdutyselection = 1
		self.hmiait201hty = 0
		self.hmiait201ahh = 0
		self.hmiait201ah = 0
		self.hmiait201al = 0
		self.hmiait201all = 0
		self.hmiait202hty = 0
		self.hmiait202ahh = 0
		self.hmiait202ah = 0
		self.hmiait202al = 0
		self.hmiait202all = 0
		self.hmiait203hty = 0
		self.hmiait203ahh = 0
		self.hmiait203ah = 0
		self.hmiait203al = 0
		self.hmiait203all = 0
		self.hmifit201hty = 0
		self.hmifit201ahh = 0
		self.hmifit201ah = 0
		self.hmifit201al = 0
		self.hmifit201all = 0
		self.hmimv201reset = 1
		self.hmip207reset = 1
		self.hmip208reset = 1
		self.hmip207auto = 1
		self.hmip208auto = 1
		self.hmip2ready = 0
		self.hminaclpumprunning = 0
		self.hminaoclpumprunning = 0
		self.hmihclpumprunning = 0
		self.hmip2state_prev = 0
		### End of Initialization block #######


		self.TON_FIT102_P1_TM	= TONR("FIT102_P1")
		self.TON_FIT102_P2_TM	= TONR("FIT102_P2")
		self.TON_FIT102_P3_TM	= TONR("FIT102_P3")
		self.TON_FIT102_P4_TM	= TONR("FIT102_P4")
		self.TON_FIT102_P5_TM	= TONR("FIT102_P5")
		self.TON_FIT102_P6_TM	= TONR("FIT102_P6")
		self.Mid_MV201_AutoInp  = self.hmimv201status-1
		self.Mid_P_NACL_DUTY_AutoInp = self.hmip201status-1
		self.Mid_P_HCL_DUTY_AutoInp = self.hmip203status-1
		self.Mid_P_NAOCL_FAC_DUTY_AutoInp = self.hmip205status-1
		self.Mid_FIT201_Tot_Enb = 0

		# self.MV201_FB = MV_FBD(HMI.MV201)
		self.MV201_FB = MV_FBD(self.hmimv201fto,self.hmimv201ftc,self.hmimv201open,self.hmimv201close)
#		print "MV201_FB Initialized"
		self.LS201_FB = SWITCH_FBD(self.hmils201delay)
#		print "LS201_FB Initialized"
		self.LS202_FB = SWITCH_FBD(self.hmils202delay)
#		print "LS201_FB Initialized"
		self.LS203_FB = SWITCH_FBD(self.hmilsl203delay)
#		print "LS203_FB Initialized"
		self.LSLL203_FB = SWITCH_FBD(self.hmilsll203delay)
#		print "LSLL203_FB Initialized"
		# self.P201_FB  = PMP_FBD(HMI.P201)
		self.P201_FB  = PMP_FBD(self.hmip201avl,self.hmip201fault,self.hmip201shutdown)
#		print "P201_FB Initialized"
		# self.P202_FB  = PMP_FBD(HMI.P202)
		self.P202_FB  = PMP_FBD(self.hmip202avl,self.hmip202fault,self.hmip202shutdown)
#		print "P202_FB Initialized"
		# self.P203_FB  = PMP_FBD(HMI.P203)
		self.P203_FB  = PMP_FBD(self.hmip203avl,self.hmip203fault,self.hmip203shutdown)
#		print "P203_FB Initialized"
		# self.P204_FB  = PMP_FBD(HMI.P204)
		self.P204_FB  = PMP_FBD(self.hmip204avl,self.hmip204fault,self.hmip204shutdown)
#		print "P204_FB Initialized"
		# self.P205_FB  = PMP_FBD(HMI.P205)
		self.P205_FB  = PMP_FBD(self.hmip205avl,self.hmip205fault,self.hmip205shutdown)
#		print "P205_FB Initialized"
		# self.P206_FB  = PMP_FBD(HMI.P206)
		self.P206_FB  = PMP_FBD(self.hmip206avl,self.hmip206fault,self.hmip206shutdown)
#		print "P206_FB Initialized"
		# self.P207_FB  = PMP_FBD(HMI.P207)
		self.P207_FB  = PMP_FBD(self.hmip207avl,self.hmip207fault,self.hmip207shutdown)
#		print "P207_FB Initialized"
		# self.P208_FB  = PMP_FBD(HMI.P208)
		self.P208_FB  = PMP_FBD(self.hmip208avl,self.hmip208fault,self.hmip208shutdown)
#		print "P208_FB Initialized"
		self.P_NACL_DUTY_FB = Duty2_FBD()
#		print "P_NACL_DUTY_FB Initialized"
		self.P_HCL_DUTY_FB  = Duty2_FBD()
#		print "P_HCL_DUTY_FB Initialized"
		self.P_NAOCL_FAC_DUTY_FB = Duty2_FBD()
#		print "P_NAOCL_FAC_DUTY_FB Initialized"
		self.FIT201_FB = FIT_FBD(self.hmifit201hty,self.hmifit201ahh,self.hmifit201ah,self.hmifit201al,self.hmifit201all)
#		print "FIT201_FB Initialized"
		self.AIT201_FB = AIN_FBD(self.hmiait201hty,self.hmiait201ahh,self.hmiait201ah,self.hmiait201al,self.hmiait201all)
#		print "AIT201_FB Initialized"
		self.AIT202_FB = AIN_FBD(self.hmiait202hty,self.hmiait202ahh,self.hmiait202ah,self.hmiait202al,self.hmiait202all)
#		print "AIT202_FB Initialized"
		self.AIT203_FB = AIN_FBD(self.hmiait203hty,self.hmiait203ahh,self.hmiait203ah,self.hmiait203al,self.hmiait203all)

		################## multiprocessing manager ###########
		manager = multiprocessing.Manager()
		self.shared = manager.dict({
            "hmiplantreseton": self.hmiplantreseton,
            "hmiplantautoon": self.hmiplantautoon,
            "hmiplantautooff": self.hmiplantautooff,
            "hmiait402ah": self.hmiait402ah,
            "hmiait503ah": self.hmiait503ah,
            "hmilit301ah": self.hmilit301ah,
            "hmilit301al": self.hmilit301al,
            "hmimv301status": self.hmimv301status,
            "hmiplantstart": self.hmiplantstart,
            "hmiplantstop": self.hmiplantstop,
			"hmiplantcriticalsdon": self.hmiplantcriticalsdon
        })
		#######################################################
		time.sleep(10)
		print ("	PLC2 started\n")

	def fetchData(self, state):

		self.shared["hmiplantreseton"] = getdata(self, 'HMI.PLANT.Reset_On',SCADA_ADDR,self.shared["hmiplantreseton"])
		self.shared["hmiplantautoon"] = getdata(self, 'HMI.PLANT.Auto_On',SCADA_ADDR,self.shared["hmiplantautoon"])
		self.shared["hmiplantautooff"] = getdata(self, 'HMI.PLANT.Auto_Off',SCADA_ADDR,self.shared["hmiplantautooff"])
		self.shared["hmimv301status"] = getdata(self, 'HMI.MV301.Status',SCADA_ADDR,self.shared["hmimv301status"])
		self.shared["hmiplantstop"] = getdata(self, 'HMI.PLANT.Stop',SCADA_ADDR,self.shared["hmiplantstop"])
		self.shared["hmiplantcriticalsdon"] = getdata(self, 'HMI.PLANT.Critical_SD_On',SCADA_ADDR,self.shared["hmiplantcriticalsdon"])
		if state==1:
			self.shared["hmiplantstart"] = getdata(self, 'HMI.PLANT.Start',SCADA_ADDR,self.shared["hmiplantstart"])
		if state==2:
			self.shared["hmiait402ah"] = getdata(self, 'HMI.AIT402.AH',SCADA_ADDR,self.shared["hmiait402ah"])
			self.shared["hmiait503ah"] = getdata(self, 'HMI.AIT503.AH',SCADA_ADDR,self.shared["hmiait503ah"])
			self.shared["hmilit301ah"] = getdata(self, 'HMI.LIT301.AH',SCADA_ADDR,self.shared["hmilit301ah"])
			self.shared["hmilit301al"] = getdata(self, 'HMI.LIT301.AL',SCADA_ADDR,self.shared["hmilit301al"])
		# print("self.hmilit301al> Inside fetchdata:", self.shared["hmilit301al"])


	def Actuator(self):
		self.IO.MV201.DI_ZSO = self.IO.MV201.DO_Open
		self.IO.MV201.DI_ZSC = self.IO.MV201.DO_Close

	def Plant(self):
		self.h_t101=0
		self.p = {"f_mv101":2.3*1000000000/3600,"S_t101":1.5*1000000,"S_t301":1.5*1000000,"S_t401":1.5*1000000,"S_t601":1.5*1000000,"S_t601":1.5*1000000,"S_t602":1.5*1000000,"f_p101":2.0*1000000000/3600,"f_mv201":2.0*1000000000/3600,"f_p301":2.0*1000000000/3600,"f_mv302":2.0*1000000000/3600,"f_p602":2.0*1000000000/3600,"f_p401":2.0*1000000000/36001,"f_mv501":2.0*1000000000/3600,"f_mv502":0.00006111,"f_mv503":0.00049,"f_p601":2.0*1000000000/36001,"LIT101_AL":0.2,"LIT101_AH":0.8,"LIT301_AL":0.2,"LIT301_AH":0.8,"LIT401_AL":0.2,"LIT401_AH":0.8,"LIT601_AL":0.2,"LIT601_AH":0.8,"LIT602_AL":0.2,"LIT602_AH":0.8,"cond_AIT201_AL":250,"cond_AIT201_AH":260,"ph_AIT202_AL":6.95,"ph_AIT202_AH":7.05,"orp_AIT203_AL":420,"orp_AIT203_AH":500,"cond_AIT503_AH":260,"h201_AL":50,"h202_AL":4,"h203_AL":15,"cond_AIT503_AL":250,"cond_AIT503_AH":260,"orp_AIT402_AL":420,"orp_AIT402_AH":500,"omega_inlet":0.001}  # critical plant parameters

		# No tank here, so nothing to be done
		self.k = self.k + 1

	def Iteration(self):
		p = multiprocessing.Process(target=self.fetchData, args=(self.hmip2state,))
		p.start()
		p.join(timeout)
		if p.is_alive():
			print("Timeout reached, could not fetch all recent data")
			p.terminate()
			p.join()
		else:
			print("Data fetching completed")

		self.hmiplantreseton = self.shared["hmiplantreseton"]
		self.hmiplantautoon = self.shared["hmiplantautoon"]
		self.hmiplantautooff = self.shared["hmiplantautooff"]
		self.hmiait402ah = self.shared["hmiait402ah"]
		self.hmiait503ah = self.shared["hmiait503ah"]
		self.hmilit301ah = self.shared["hmilit301ah"]
		self.hmilit301al = self.shared["hmilit301al"]
		# print("self.hmilit301al> Inside iteration:", self.hmilit301al)
		self.hmimv301status = self.shared["hmimv301status"]
		self.hmiplantstart = self.shared["hmiplantstart"]
		self.hmiplantstop = self.shared["hmiplantstop"]
		self.hmiplantcriticalsdon = self.shared["hmiplantcriticalsdon"]

		print("PLC2 State:", self.hmip2state)
		# iter_start = time.time()
		if self.hmiplantreseton:
			# setdata(self, 'HMI.MV201.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P201.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P202.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P203.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P204.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P205.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P206.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P207.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P208.Reset',SCADA_ADDR,1)
			self.hmimv201reset = 1
			self.hmip201reset = 1
			self.hmip202reset = 1
			self.hmip203reset = 1
			self.hmip204reset = 1
			self.hmip205reset = 1
			self.hmip206reset = 1
			self.hmip207reset = 1
			self.hmip208reset = 1

			# HMI.MV201.Reset	 =  1
			# HMI.P201.Reset 	 =  1
			# HMI.P202.Reset	 =  1
			# HMI.P203.Reset 	 =  1
			# HMI.P204.Reset	 =  1
			# HMI.P205.Reset	 =  1
			# HMI.P206.Reset	 =  1
			# HMI.P207.Reset 	 =  1
			# HMI.P208.Reset	 =  1

		if self.hmiplantautoon:
			# setdata(self, 'HMI.MV201.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P201.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P202.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P203.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P204.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P205.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P206.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P207.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P208.Auto',SCADA_ADDR,1)
			self.hmimv201auto = 1
			self.hmip201auto = 1
			self.hmip202auto = 1
			self.hmip203auto = 1
			self.hmip204auto = 1
			self.hmip205auto = 1
			self.hmip206auto = 1
			self.hmip207auto = 1
			self.hmip208auto = 1
			# HMI.P201.Auto 	=1
			# HMI.P202.Auto	=1
			# HMI.P203.Auto 	=1
			# HMI.P204.Auto	=1
			# HMI.P205.Auto	=1
			# HMI.P206.Auto	=1
			# HMI.P207.Auto 	=1
			# HMI.P208.Auto	=1

		if self.hmiplantautooff:
			# setdata(self, 'HMI.MV201.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P201.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P202.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P203.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P204.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P205.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P206.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P207.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P208.Auto',SCADA_ADDR,0)
			self.hmimv201auto = 0
			self.hmip201auto = 0
			self.hmip202auto = 0
			self.hmip203auto = 0
			self.hmip204auto = 0
			self.hmip205auto = 0
			self.hmip206auto = 0
			self.hmip207auto = 0
			self.hmip208auto = 0
			# HMI.MV201.Auto	=0
			# HMI.P201.Auto 	=0
			# HMI.P202.Auto	=0
			# HMI.P203.Auto 	=0
			# HMI.P204.Auto	=0
			# HMI.P205.Auto	=0
			# HMI.P206.Auto	=0
			# HMI.P207.Auto 	=0
			# HMI.P208.Auto	=0

		# setdata(self, 'HMI.P2.Permissive_On',SCADA_ADDR,(self.hmimv201avl and (self.hmip201avl or self.hmip202avl) and (self.hmip203avl or self.hmip204avl) and (self.hmip205avl or self.hmip206avl)))
		self.hmip2permissiveon = self.hmimv201avl and (self.hmip201avl or self.hmip202avl) and (self.hmip203avl or self.hmip204avl) and (self.hmip205avl or self.hmip206avl)
		# HMI.P2.Permissive_On 	= HMI.MV201.Avl	and (HMI.P201.Avl or HMI.P202.Avl) and (HMI.P203.Avl or HMI.P204.Avl) and (HMI.P205.Avl or HMI.P206.Avl)

		self.Mid_FIT201_Tot_Enb = self.hmimv201status == 2

		self.TON_FIT102_P1_TM.TONR( self.hmifit201all and self.hmimv201status == 2 and self.hmip201status == 2)
		self.TON_FIT102_P2_TM.TONR( self.hmifit201all and self.hmimv201status == 2 and self.hmip202status == 2)
		self.TON_FIT102_P3_TM.TONR( self.hmifit201all and self.hmimv201status == 2 and self.hmip203status == 2)
		self.TON_FIT102_P4_TM.TONR( self.hmifit201all and self.hmimv201status == 2 and self.hmip204status == 2)
		self.TON_FIT102_P5_TM.TONR( self.hmifit201all and self.hmimv201status == 2 and self.hmip205status == 2)
		self.TON_FIT102_P6_TM.TONR( self.hmifit201all and self.hmimv201status == 2 and self.hmip206status == 2)


		self.hmip201permissive_arr = signed_integer_2_bit(self.hmip201permissive)
		self.hmip201permissive_arr[0] = int(not self.hmils201alarm)
		self.hmip201permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip201permissive_arr[2] = int(self.hmifit201ah)
		self.hmip201permissive = bit_2_signed_integer(self.hmip201permissive_arr)
		# setdata(self, 'HMI.P201.Permissive',SCADA_ADDR,self.hmip201permissive)

		# HMI.P201.Permissive[0] 	= not HMI.LS201.Alarm
		# HMI.P201.Permissive[1] 	= HMI.MV201.Status == 2
		# HMI.P201.Permissive[2]	= HMI.FIT201.AH

		self.hmip201msgpermissive_arr = signed_integer_2_bit(self.hmip201msgpermissive)
		self.hmip201msgpermissive_arr[1] = int(self.hmip201permissive_arr[0])
		self.hmip201msgpermissive_arr[2] = int(self.hmip201permissive_arr[1])
		self.hmip201msgpermissive_arr[3] = int(self.hmip201permissive_arr[2])
		self.hmip201msgpermissive = bit_2_signed_integer(self.hmip201msgpermissive_arr)
		# setdata(self, 'HMI.P201.MSG_Permissive',SCADA_ADDR,self.hmip201msgpermissive)

		# HMI.P201.MSG_Permissive[1] = HMI.P201.Permissive[0]
		# HMI.P201.MSG_Permissive[2] = HMI.P201.Permissive[1]
		# HMI.P201.MSG_Permissive[3] = HMI.P201.Permissive[2]

		self.hmip202permissive_arr = signed_integer_2_bit(self.hmip202permissive)
		self.hmip202permissive_arr[0] = int(not self.hmils201alarm)
		self.hmip202permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip202permissive_arr[2] = int(self.hmifit201ah)
		self.hmip202permissive = bit_2_signed_integer(self.hmip202permissive_arr)
		# setdata(self, 'HMI.P202.Permissive',SCADA_ADDR,self.hmip202permissive)
		# HMI.P202.Permissive[0] 	= not HMI.LS201.Alarm
		# HMI.P202.Permissive[1] 	= HMI.MV201.Status == 2
		# HMI.P202.Permissive[2] 	= HMI.FIT201.AH

		self.hmip202msgpermissive_arr = signed_integer_2_bit(self.hmip202msgpermissive)
		self.hmip202msgpermissive_arr[1] = int(self.hmip202permissive_arr[0])
		self.hmip202msgpermissive_arr[2] = int(self.hmip202permissive_arr[1])
		self.hmip202msgpermissive_arr[3] = int(self.hmip202permissive_arr[2])
		self.hmip202msgpermissive = bit_2_signed_integer(self.hmip202msgpermissive_arr)
		# setdata(self, 'HMI.P202.MSG_Permissive',SCADA_ADDR,self.hmip202msgpermissive)
		# HMI.P202.MSG_Permissive[1] = HMI.P202.Permissive[0]
		# HMI.P202.MSG_Permissive[2] = HMI.P202.Permissive[1]
		# HMI.P202.MSG_Permissive[3] = HMI.P202.Permissive[2]

		self.hmip203permissive_arr = signed_integer_2_bit(self.hmip203permissive)
		self.hmip203permissive_arr[0] = int(not self.hmils202alarm)
		self.hmip203permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip203permissive_arr[2] = int(self.hmifit201ah)
		self.hmip203permissive = bit_2_signed_integer(self.hmip203permissive_arr)
		# setdata(self, 'HMI.P203.Permissive',SCADA_ADDR,self.hmip203permissive)
		# HMI.P203.Permissive[0] 	= not HMI.LS202.Alarm
		# HMI.P203.Permissive[1] 	= HMI.MV201.Status == 2
		# HMI.P203.Permissive[2] 	= HMI.FIT201.AH

		self.hmip203msgpermissive_arr = signed_integer_2_bit(self.hmip203msgpermissive)
		self.hmip203msgpermissive_arr[1] = int(self.hmip203permissive_arr[0])
		self.hmip203msgpermissive_arr[2] = int(self.hmip203permissive_arr[1])
		self.hmip203msgpermissive_arr[3] = int(self.hmip203permissive_arr[2])
		self.hmip203msgpermissive = bit_2_signed_integer(self.hmip203msgpermissive_arr)
		# setdata(self, 'HMI.P203.MSG_Permissive',SCADA_ADDR,self.hmip203msgpermissive)
		# HMI.P203.MSG_Permissive[1] = HMI.P203.Permissive[0]
		# HMI.P203.MSG_Permissive[2] = HMI.P203.Permissive[1]
		# HMI.P203.MSG_Permissive[3] = HMI.P203.Permissive[2]

		self.hmip204permissive_arr = signed_integer_2_bit(self.hmip204permissive)
		self.hmip204permissive_arr[0] = int(not self.hmils202alarm)
		self.hmip204permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip204permissive_arr[2] = int(self.hmifit201ah)
		self.hmip204permissive = bit_2_signed_integer(self.hmip204permissive_arr)
		# setdata(self, 'HMI.P204.Permissive',SCADA_ADDR,self.hmip204permissive)
		# HMI.P204.Permissive[0] 	= not HMI.LS202.Alarm
		# HMI.P204.Permissive[1] 	= HMI.MV201.Status == 2
		# HMI.P204.Permissive[2] 	= HMI.FIT201.AH

		self.hmip204msgpermissive_arr = signed_integer_2_bit(self.hmip204msgpermissive)
		self.hmip204msgpermissive_arr[1] = int(self.hmip204permissive_arr[0])
		self.hmip204msgpermissive_arr[2] = int(self.hmip204permissive_arr[1])
		self.hmip204msgpermissive_arr[3] = int(self.hmip204permissive_arr[2])
		self.hmip204msgpermissive = bit_2_signed_integer(self.hmip204msgpermissive_arr)
		# setdata(self, 'HMI.P204.MSG_Permissive',SCADA_ADDR,self.hmip204msgpermissive)
		# HMI.P204.MSG_Permissive[1] = HMI.P204.Permissive[0]
		# HMI.P204.MSG_Permissive[2] = HMI.P204.Permissive[1]
		# HMI.P204.MSG_Permissive[3] = HMI.P204.Permissive[2]

		self.hmip205permissive_arr = signed_integer_2_bit(self.hmip205permissive)
		self.hmip205permissive_arr[0] = int(not self.hmilsl203alarm)
		self.hmip205permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip205permissive_arr[2] = int(self.hmifit201ah)
		self.hmip205permissive = bit_2_signed_integer(self.hmip205permissive_arr)
		# setdata(self, 'HMI.P205.Permissive',SCADA_ADDR,self.hmip205permissive)
		# HMI.P205.Permissive[0] 	= not HMI.LSL203.Alarm
		# HMI.P205.Permissive[1] 	= HMI.MV201.Status == 2
		# HMI.P205.Permissive[2] 	= HMI.FIT201.AH

		self.hmip205msgpermissive_arr = signed_integer_2_bit(self.hmip205msgpermissive)
		self.hmip205msgpermissive_arr[1] = int(self.hmip205permissive_arr[0])
		self.hmip205msgpermissive_arr[2] = int(self.hmip205permissive_arr[1])
		self.hmip205msgpermissive_arr[3] = int(self.hmip205permissive_arr[2])
		self.hmip205msgpermissive = bit_2_signed_integer(self.hmip205msgpermissive_arr)
		# setdata(self, 'HMI.P205.MSG_Permissive',SCADA_ADDR,self.hmip205msgpermissive)
		# HMI.P205.MSG_Permissive[1] = HMI.P205.Permissive[0]
		# HMI.P205.MSG_Permissive[2] = HMI.P205.Permissive[1]
		# HMI.P205.MSG_Permissive[3] = HMI.P205.Permissive[2]

		self.hmip206permissive_arr = signed_integer_2_bit(self.hmip206permissive)
		self.hmip206permissive_arr[0] = int(not self.hmilsl203alarm)
		self.hmip206permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip206permissive_arr[2] = int(self.hmifit201ah)
		self.hmip206permissive = bit_2_signed_integer(self.hmip206permissive_arr)
		# setdata(self, 'HMI.P206.Permissive',SCADA_ADDR,self.hmip206permissive)
		# HMI.P206.Permissive[0] 	= not HMI.LSL203.Alarm
		# HMI.P206.Permissive[1] 	= HMI.MV201.Status == 2
		# HMI.P206.Permissive[2] 	= HMI.FIT201.AH

		self.hmip206msgpermissive_arr = signed_integer_2_bit(self.hmip206msgpermissive)
		self.hmip206msgpermissive_arr[1] = int(self.hmip206permissive_arr[0])
		self.hmip206msgpermissive_arr[2] = int(self.hmip206permissive_arr[1])
		self.hmip206msgpermissive_arr[3] = int(self.hmip206permissive_arr[2])
		self.hmip206msgpermissive = bit_2_signed_integer(self.hmip206msgpermissive_arr)
		# setdata(self, 'HMI.P206.MSG_Permissive',SCADA_ADDR,self.hmip206msgpermissive)
		# HMI.P206.MSG_Permissive[1] = HMI.P206.Permissive[0]
		# HMI.P206.MSG_Permissive[2] = HMI.P206.Permissive[1]
		# HMI.P206.MSG_Permissive[3] = HMI.P206.Permissive[2]

		self.hmip207permissive_arr = signed_integer_2_bit(self.hmip207permissive)
		self.hmip207permissive_arr[0] = int(not self.hmilsl203alarm)
		self.hmip207permissive_arr[1] = int(self.hmimv301status == 2)
		self.hmip207permissive = bit_2_signed_integer(self.hmip207permissive_arr)
		# setdata(self, 'HMI.P207.Permissive',SCADA_ADDR,self.hmip207permissive)
		# HMI.P207.Permissive[0] 	= not HMI.LSL203.Alarm
		# HMI.P207.Permissive[1] 	= HMI.MV301.Status == 2

		self.hmip207msgpermissive_arr = signed_integer_2_bit(self.hmip207msgpermissive)
		self.hmip207msgpermissive_arr[1] = int(self.hmip207permissive_arr[0])
		self.hmip207msgpermissive_arr[2] = int(self.hmip207permissive_arr[1])
		self.hmip207msgpermissive_arr[3] = int(self.hmip207permissive_arr[2])
		self.hmip207msgpermissive = bit_2_signed_integer(self.hmip207msgpermissive_arr)
		# setdata(self, 'HMI.P207.MSG_Permissive',SCADA_ADDR,self.hmip207msgpermissive)
		# HMI.P207.MSG_Permissive[1] = HMI.P207.Permissive[0]
		# HMI.P207.MSG_Permissive[2] = HMI.P207.Permissive[1]
		# HMI.P207.MSG_Permissive[3] = HMI.P207.Permissive[2]

		self.hmip208permissive_arr = signed_integer_2_bit(self.hmip208permissive)
		self.hmip208permissive_arr[0] = int(not self.hmilsl203alarm)
		self.hmip208permissive_arr[1] = int(self.hmimv301status == 2)
		self.hmip208permissive = bit_2_signed_integer(self.hmip208permissive_arr)
		# setdata(self, 'HMI.P208.Permissive',SCADA_ADDR,self.hmip208permissive)
		# HMI.P208.Permissive[0] 	= not HMI.LSL203.Alarm
		# HMI.P208.Permissive[1] 	= HMI.MV301.Status == 2

		self.hmip208msgpermissive_arr = signed_integer_2_bit(self.hmip208msgpermissive)
		self.hmip208msgpermissive_arr[1] = int(self.hmip208permissive_arr[0])
		self.hmip208msgpermissive_arr[2] = int(self.hmip208permissive_arr[1])
		self.hmip208msgpermissive_arr[3] = int(self.hmip208permissive_arr[2])
		self.hmip208msgpermissive = bit_2_signed_integer(self.hmip208msgpermissive_arr)
		# setdata(self, 'HMI.P208.MSG_Permissive',SCADA_ADDR,self.hmip208msgpermissive)
		# HMI.P208.MSG_Permissive[1] = HMI.P208.Permissive[0]
		# HMI.P208.MSG_Permissive[2] = HMI.P208.Permissive[1]
		# HMI.P208.MSG_Permissive[3] = HMI.P208.Permissive[2]

		self.hmip201sd_arr = signed_integer_2_bit(self.hmip201sd)
		self.hmip201sd_arr[0] = int(self.hmils201alarm)
		self.hmip201sd_arr[1] = int((self.hmip201status == 2) and (self.hmimv201status != 2))
		self.hmip201sd_arr[2] = int(self.TON_FIT102_P1_TM.DN)
		self.hmip201sd = bit_2_signed_integer(self.hmip201sd_arr)
		# setdata(self, 'HMI.P201.SD',SCADA_ADDR,self.hmip201sd)
		# HMI.P201.SD[0] 	= HMI.LS201.Alarm
		# HMI.P201.SD[1] 	= HMI.P201.Status  ==  2 and HMI.MV201.Status  !=  2
		# HMI.P201.SD[2] 	= self.TON_FIT102_P1_TM.DN

		self.hmip201msgshutdown_arr = signed_integer_2_bit(self.hmip201msgshutdown)
		self.hmip201shutdown_arr = signed_integer_2_bit(self.hmip201shutdown)
		self.hmip201msgshutdown_arr[1] = self.hmip201shutdown_arr[0]
		self.hmip201msgshutdown_arr[2] = self.hmip201shutdown_arr[1]
		self.hmip201msgshutdown_arr[3] = self.hmip201shutdown_arr[2]
		self.hmip201msgshutdown = bit_2_signed_integer(self.hmip201msgshutdown_arr)
		# setdata(self, 'HMI.P201.MSG_Shutdown',SCADA_ADDR,self.hmip201msgshutdown)
		# HMI.P201.MSG_Shutdown[1] = HMI.P201.Shutdown[0]
		# HMI.P201.MSG_Shutdown[2] = HMI.P201.Shutdown[1]
		# HMI.P201.MSG_Shutdown[3] = HMI.P201.Shutdown[2]

		self.hmip202sd_arr = signed_integer_2_bit(self.hmip202sd)
		self.hmip202sd_arr[0] = int(self.hmils201alarm)
		self.hmip202sd_arr[1] = int((self.hmip201status == 2) and (self.hmimv201status != 2))
		self.hmip202sd_arr[2] = int(self.TON_FIT102_P2_TM.DN)
		self.hmip202sd = bit_2_signed_integer(self.hmip202sd_arr)
		# setdata(self, 'HMI.P202.SD',SCADA_ADDR,self.hmip202sd)
		# HMI.P202.SD[0] 	= HMI.LS201.Alarm
		# HMI.P202.SD[1] 	= HMI.P201.Status  ==  2 and HMI.MV201.Status  !=  2
		# HMI.P202.SD[2] 	= self.TON_FIT102_P2_TM.DN

		self.hmip202msgshutdown_arr = signed_integer_2_bit(self.hmip202msgshutdown)
		self.hmip202shutdown_arr = signed_integer_2_bit(self.hmip202shutdown)
		self.hmip202msgshutdown_arr[1] = self.hmip202shutdown_arr[0]
		self.hmip202msgshutdown_arr[2] = self.hmip202shutdown_arr[1]
		self.hmip202msgshutdown_arr[3] = self.hmip202shutdown_arr[2]
		self.hmip202msgshutdown = bit_2_signed_integer(self.hmip202msgshutdown_arr)
		# setdata(self, 'HMI.P202.MSG_Shutdown',SCADA_ADDR,self.hmip202msgshutdown)
		# HMI.P202.MSG_Shutdown[1] = HMI.P202.Shutdown[0]
		# HMI.P202.MSG_Shutdown[2] = HMI.P202.Shutdown[1]
		# HMI.P202.MSG_Shutdown[3] = HMI.P202.Shutdown[2]

		self.hmip203sd_arr = signed_integer_2_bit(self.hmip203sd)
		self.hmip203sd_arr[0] = int(self.hmils202alarm)
		self.hmip203sd_arr[1] = int((self.hmip201status == 2) and (self.hmimv201status != 2))
		self.hmip203sd_arr[2] = int(self.TON_FIT102_P3_TM.DN)
		self.hmip203sd = bit_2_signed_integer(self.hmip203sd_arr)
		# setdata(self, 'HMI.P203.SD',SCADA_ADDR,self.hmip203sd)
		# HMI.P203.SD[0] 	= HMI.LS202.Alarm
		# HMI.P203.SD[1] 	= HMI.P201.Status  ==  2 and HMI.MV201.Status  !=  2
		# HMI.P203.SD[2] 	= self.TON_FIT102_P3_TM.DN

		self.hmip203msgshutdown_arr = signed_integer_2_bit(self.hmip203msgshutdown)
		self.hmip203shutdown_arr = signed_integer_2_bit(self.hmip203shutdown)
		self.hmip203msgshutdown_arr[1] = self.hmip203shutdown_arr[0]
		self.hmip203msgshutdown_arr[2] = self.hmip203shutdown_arr[1]
		self.hmip203msgshutdown_arr[3] = self.hmip203shutdown_arr[2]
		self.hmip203msgshutdown = bit_2_signed_integer(self.hmip203msgshutdown_arr)
		# setdata(self, 'HMI.P203.MSG_Shutdown',SCADA_ADDR,self.hmip203msgshutdown)
		# HMI.P203.MSG_Shutdown[1] = HMI.P203.Shutdown[0]
		# HMI.P203.MSG_Shutdown[2] = HMI.P203.Shutdown[1]
		# HMI.P203.MSG_Shutdown[3] = HMI.P203.Shutdown[2]

		self.hmip204sd_arr = signed_integer_2_bit(self.hmip204sd)
		self.hmip204sd_arr[0] = int(self.hmils202alarm)
		self.hmip204sd_arr[1] = int((self.hmip201status == 2) and (self.hmimv201status != 2))
		self.hmip204sd_arr[2] = int(self.TON_FIT102_P4_TM.DN)
		self.hmip204sd = bit_2_signed_integer(self.hmip204sd_arr)
		# setdata(self, 'HMI.P204.SD',SCADA_ADDR,self.hmip204sd)
		# HMI.P204.SD[0] 	= HMI.LS202.Alarm
		# HMI.P204.SD[1] 	= HMI.P201.Status == 2 and HMI.MV201.Status != 2
		# HMI.P204.SD[2] 	= self.TON_FIT102_P4_TM.DN

		self.hmip204msgshutdown_arr = signed_integer_2_bit(self.hmip204msgshutdown)
		self.hmip204shutdown_arr = signed_integer_2_bit(self.hmip204shutdown)
		self.hmip204msgshutdown_arr[1] = self.hmip204shutdown_arr[0]
		self.hmip204msgshutdown_arr[2] = self.hmip204shutdown_arr[1]
		self.hmip204msgshutdown_arr[3] = self.hmip204shutdown_arr[2]
		self.hmip204msgshutdown = bit_2_signed_integer(self.hmip204msgshutdown_arr)
		# setdata(self, 'HMI.P204.MSG_Shutdown',SCADA_ADDR,self.hmip204msgshutdown)
		# HMI.P204.MSG_Shutdown[1] = HMI.P204.Shutdown[0]
		# HMI.P204.MSG_Shutdown[2] = HMI.P204.Shutdown[1]
		# HMI.P204.MSG_Shutdown[3] = HMI.P204.Shutdown[2]

		self.hmip205sd_arr = signed_integer_2_bit(self.hmip205sd)
		self.hmip205sd_arr[0] = int(self.hmilsl203alarm)
		self.hmip205sd_arr[1] = int((self.hmip201status == 2) and (self.hmimv201status != 2))
		self.hmip205sd_arr[2] = int(self.TON_FIT102_P5_TM.DN)
		self.hmip205sd = bit_2_signed_integer(self.hmip205sd_arr)
		# setdata(self, 'HMI.P205.SD',SCADA_ADDR,self.hmip205sd)
		# HMI.P205.SD[0] 	= HMI.LSL203.Alarm
		# HMI.P205.SD[1] 	= HMI.P201.Status == 2 and HMI.MV201.Status != 2
		# HMI.P205.SD[2] 	= self.TON_FIT102_P5_TM.DN

		self.hmip205msgshutdown_arr = signed_integer_2_bit(self.hmip205msgshutdown)
		self.hmip205shutdown_arr = signed_integer_2_bit(self.hmip205shutdown)
		self.hmip205msgshutdown_arr[1] = self.hmip205shutdown_arr[0]
		self.hmip205msgshutdown_arr[2] = self.hmip205shutdown_arr[1]
		self.hmip205msgshutdown_arr[3] = self.hmip205shutdown_arr[2]
		self.hmip205msgshutdown = bit_2_signed_integer(self.hmip205msgshutdown_arr)
		# setdata(self, 'HMI.P205.MSG_Shutdown',SCADA_ADDR,self.hmip205msgshutdown)
		# HMI.P205.MSG_Shutdown[1] = HMI.P205.Shutdown[0]
		# HMI.P205.MSG_Shutdown[2] = HMI.P205.Shutdown[1]
		# HMI.P205.MSG_Shutdown[3] = HMI.P205.Shutdown[2]

		self.hmip206sd_arr = signed_integer_2_bit(self.hmip206sd)
		self.hmip206sd_arr[0] = int(self.hmilsl203alarm)
		self.hmip206sd_arr[1] = int((self.hmip201status == 2) and (self.hmimv201status != 2))
		self.hmip206sd_arr[2] = int(self.TON_FIT102_P6_TM.DN)
		self.hmip206sd = bit_2_signed_integer(self.hmip206sd_arr)
		# setdata(self, 'HMI.P206.SD',SCADA_ADDR,self.hmip206sd)
		# HMI.P206.SD[0] 	= HMI.LSL203.Alarm
		# HMI.P206.SD[1] 	= HMI.P201.Status == 2 and HMI.MV201.Status != 2
		# HMI.P206.SD[2] 	= self.TON_FIT102_P6_TM.DN

		self.hmip206msgshutdown_arr = signed_integer_2_bit(self.hmip206msgshutdown)
		self.hmip206shutdown_arr = signed_integer_2_bit(self.hmip206shutdown)
		self.hmip206msgshutdown_arr[1] = self.hmip206shutdown_arr[0]
		self.hmip206msgshutdown_arr[2] = self.hmip206shutdown_arr[1]
		self.hmip206msgshutdown_arr[3] = self.hmip206shutdown_arr[2]
		self.hmip206msgshutdown = bit_2_signed_integer(self.hmip206msgshutdown_arr)
		# setdata(self, 'HMI.P206.MSG_Shutdown',SCADA_ADDR,self.hmip206msgshutdown)
		# HMI.P206.MSG_Shutdown[1] = HMI.P206.Shutdown[0]
		# HMI.P206.MSG_Shutdown[2] = HMI.P206.Shutdown[1]
		# HMI.P206.MSG_Shutdown[3] = HMI.P206.Shutdown[2]

		self.hmip207sd_arr = signed_integer_2_bit(self.hmip207sd)
		self.hmip207sd_arr[0] = int(self.hmilsl203alarm)
		self.hmip207sd_arr[1] = int((self.hmip207status == 2) and (self.hmimv301status != 2))
		self.hmip207sd = bit_2_signed_integer(self.hmip207sd_arr)
		# setdata(self, 'HMI.P207.SD',SCADA_ADDR,self.hmip207sd)
		# HMI.P207.SD[0] 	= HMI.LSL203.Alarm
		# HMI.P207.SD[1] 	= HMI.P207.Status == 2 and HMI.MV301.Status != 2

		self.hmip207msgshutdown_arr = signed_integer_2_bit(self.hmip207msgshutdown)
		self.hmip207shutdown_arr = signed_integer_2_bit(self.hmip207shutdown)
		self.hmip207msgshutdown_arr[1] = self.hmip207shutdown_arr[0]
		self.hmip207msgshutdown_arr[2] = self.hmip207shutdown_arr[1]
		self.hmip207msgshutdown = bit_2_signed_integer(self.hmip207msgshutdown_arr)
		# setdata(self, 'HMI.P207.MSG_Shutdown',SCADA_ADDR,self.hmip207msgshutdown)
		# HMI.P207.MSG_Shutdown[1] = HMI.P207.Shutdown[0]
		# HMI.P207.MSG_Shutdown[2] = HMI.P207.Shutdown[1]

		self.hmip208sd_arr = signed_integer_2_bit(self.hmip208sd)
		self.hmip208sd_arr[0] = int(self.hmilsl203alarm)
		self.hmip208sd_arr[1] = int((self.hmip207status == 2) and (self.hmimv301status != 2))
		self.hmip208sd = bit_2_signed_integer(self.hmip208sd_arr)
		# setdata(self, 'HMI.P208.SD',SCADA_ADDR,self.hmip208sd)
		# HMI.P208.SD[0] 	= HMI.LSL203.Alarm
		# HMI.P208.SD[1] 	= HMI.P207.Status == 2 and HMI.MV301.Status != 2

		self.hmip208msgshutdown_arr = signed_integer_2_bit(self.hmip208msgshutdown)
		self.hmip208shutdown_arr = signed_integer_2_bit(self.hmip208shutdown)
		self.hmip208msgshutdown_arr[1] = self.hmip208shutdown_arr[0]
		self.hmip208msgshutdown_arr[2] = self.hmip208shutdown_arr[1]
		self.hmip208msgshutdown = bit_2_signed_integer(self.hmip208msgshutdown_arr)
		# setdata(self, 'HMI.P208.MSG_Shutdown',SCADA_ADDR,self.hmip208msgshutdown)
		# HMI.P208.MSG_Shutdown[1] = HMI.P208.Shutdown[0]
		# HMI.P208.MSG_Shutdown[2] = HMI.P208.Shutdown[1]

		if self.hmiplantstop or self.hmiplantcriticalsdon:# the HMI.PLANT.Critical_SD_On variable could be rethought, currently it's defined in HMI
			# setdata(self, 'HMI.P2.Shutdown',SCADA_ADDR,1)
			self.hmip2shutdown = 1

		if self.hmip2state == 1:
			self.hmip2state_prev = 1
			#PLANT IN STandBY
			self.Mid_MV201_AutoInp			=0
			self.Mid_P_NACL_DUTY_AutoInp		=0
			self.Mid_P_HCL_DUTY_AutoInp		=0
			self.Mid_P_NAOCL_FAC_DUTY_AutoInp	=0
			self.Mid_P_NAOCL_UF_DUTY_AutoInp	=0

			if self.hmip2permissiveon and self.hmiplantstart:
					# setdata(self, 'HMI.P2.State',SCADA_ADDR,2)
					self.hmip2state = 2

		elif self.hmip2state == 2:
			self.hmip2state_prev = 2
			#OPEN RAW WATER OUTLET VALVE, MV201
			#(*MV-201 , Raw Water Outlet Valve Control*)
			# print("self.hmilit301al> Before SETD:", self.hmilit301al)
			# print("self.hmilit301ah> Before SETD:", self.hmilit301ah)
			# print("self.Mid_MV201_AutoInp> Before SETD:", self.Mid_MV201_AutoInp)
			self.Mid_MV201_AutoInp = SETD(self.hmilit301al, self.hmilit301ah, self.Mid_MV201_AutoInp)

			#(*P-201/2 , Cond NACL Dosing Pump Control*)
			self.Mid_P_NACL_DUTY_AutoInp  = SETD(self.hmimv201status == 2 and (self.hmiait201al) and (not self.hmiait503ah), self.hmimv201status != 2 or (self.hmiait201ah) or (self.hmiait503ah) or  self.hmils201alarm or self.hmifit201all, self.Mid_P_NACL_DUTY_AutoInp)
			# print ("Mid_P_NACL_DUTY_AutoInp")
			# print (self.Mid_P_NACL_DUTY_AutoInp )
			#(*P-203/4 , PH HCL Dosing Pump Control*)
			self.Mid_P_HCL_DUTY_AutoInp = SETD(self.hmimv201status == 2 and (self.hmiait202ah),self.hmimv201status != 2 or (self.hmiait202al) or  self.hmils202alarm or self.hmifit201all, self.Mid_P_HCL_DUTY_AutoInp)
			#(*P-205/6 ,orP NAOCL FAC Dosing Pump Control*)
			self.Mid_P_NAOCL_FAC_DUTY_AutoInp = SETD( self.hmimv201status == 2 and (self.hmiait203al) and (not self.hmiait402ah),self.hmimv201status != 2 or (self.hmiait203ah) or (self.hmiait402ah) or self.hmilsl203alarm, self.Mid_P_NAOCL_FAC_DUTY_AutoInp)

			# setdata(self, 'HMI.P2.Ready',SCADA_ADDR,1)
			self.hmip2ready = 1

			if self.hmip2shutdown:
				if self.hmilit301ah:
					# setdata(self, 'HMI.P2.State',SCADA_ADDR,1)
					# setdata(self, 'HMI.P2.Shutdown',SCADA_ADDR,0)
					self.hmip2shutdown = 0
					self.hmip2state = 1
		else:
			# setdata(self, 'HMI.P2.State',SCADA_ADDR,1)
			self.hmip2state = 1


		# self.MV201_FB.MV_FBD(self.Mid_MV201_AutoInp, IO.MV201,HMI.MV201 )
		# print("self.IO.MV201.DO_Open> Before MV_FBD:", self.IO.MV201.DO_Open)
		# print("self.Mid_MV201_AutoInp> Before MV_FBD:", self.Mid_MV201_AutoInp)

		self.hmimv201status_upd, self.hmimv201avl = self.MV201_FB.MV_FBD(
			self.Mid_MV201_AutoInp, 
			self.IO.MV201, 
			self.hmimv201auto,
			self.hmimv201reset  # add reset input
		)
		if self.hmimv201status_upd!= -99:
			self.hmimv201status = self.hmimv201status_upd

		# print("self.IO.MV201.DO_Open> After MV_FBD:", self.IO.MV201.DO_Open)


		# self.hmils201alarm =
		self.LS201_FB.SWITCH_FBD(self.IO.LS201)

		# self.hmils202alarm =
		self.LS201_FB.SWITCH_FBD(self.IO.LS202)

		# self.hmilsl203alarm =
		self.LS203_FB.SWITCH_FBD(self.IO.LSL203)

		# self.hmilsll203alarm =
		self.LSLL203_FB.SWITCH_FBD(self.IO.LSL203)

		# self.P_NACL_DUTY_FB.Duty2_FBD(self.Mid_P_NACL_DUTY_AutoInp, HMI.P201,HMI.P202,HMI.P_NACL_DUTY)
		self.hminaclbothpmpnotavl, self.hminaclselectedpmpnotavl_upd, self.hminaclpumprunning = self.P_NACL_DUTY_FB.Duty2_FBD(self.Mid_P_NACL_DUTY_AutoInp, self.hmip201status, self.hmip201avl, self.hmip202status, self.hmip202avl, self.hmipnacldutyselection)
		if self.hminaclselectedpmpnotavl_upd != -99:
			self.hminaclselectedpmpnotavl = self.hminaclselectedpmpnotavl_upd


		# self.P_HCL_DUTY_FB.Duty2_FBD(self.Mid_P_HCL_DUTY_AutoInp, HMI.P203,HMI.P204,HMI.P_HCL_DUTY)
		self.hmihclbothpmpnotavl, self.hmihclselectedpmpnotavl_upd, self.hmihclpumprunning = self.P_HCL_DUTY_FB.Duty2_FBD(self.Mid_P_HCL_DUTY_AutoInp, self.hmip203status, self.hmip203avl, self.hmip204status, self.hmip204avl, self.hmiphcldutyselection)
		if self.hmihclselectedpmpnotavl_upd != -99:
			self.hmihclselectedpmpnotavl = self.hmihclselectedpmpnotavl_upd

		# self.P_NAOCL_FAC_DUTY_FB.Duty2_FBD(self.Mid_P_NAOCL_FAC_DUTY_AutoInp, HMI.P205,HMI.P206,HMI.P_NAOCL_FAC_DUTY)
		self.hminaoclbothpmpnotavl, self.hminaoclselectedpmpnotavl_upd, self.hminaoclpumprunning = self.P_NAOCL_FAC_DUTY_FB.Duty2_FBD(self.Mid_P_NAOCL_FAC_DUTY_AutoInp, self.hmip205status, self.hmip205avl, self.hmip206status, self.hmip206avl, self.hmipnaoclfacdutyselection)
		if self.hminaoclselectedpmpnotavl_upd != -99:
			self.hminaoclselectedpmpnotavl = self.hminaoclselectedpmpnotavl_upd

		# self.P201_FB.PMP_FBD(self.P_NACL_DUTY_FB.Start_Pmp1, IO.P201, HMI.P201)
		self.hmip201status_upd, self.hmip201fault, self.hmip201avl, self.hmip201shutdown = self.P201_FB.PMP_FBD(self.P_NACL_DUTY_FB.Start_Pmp1, self.IO.P201, self.hmip201auto, self.hmip201reset, self.hmip201permissive, self.hmip201sd)
		if self.hmip201status_upd != -99:
			self.hmip201status = self.hmip201status_upd


		# self.P202_FB.PMP_FBD(self.P_NACL_DUTY_FB.Start_Pmp2, IO.P202, HMI.P202)
		self.hmip202status_upd, self.hmip202fault, self.hmip202avl, self.hmip202shutdown = self.P202_FB.PMP_FBD(self.P_NACL_DUTY_FB.Start_Pmp2, self.IO.P202, self.hmip202auto, self.hmip202reset, self.hmip202permissive, self.hmip202sd)
		if self.hmip202status_upd != -99:
			self.hmip202status = self.hmip202status_upd

		# self.P203_FB.PMP_FBD(self.P_HCL_DUTY_FB.Start_Pmp1, IO.P203, HMI.P203)
		self.hmip203status_upd, self.hmip203fault, self.hmip203avl, self.hmip203shutdown = self.P203_FB.PMP_FBD(self.P_HCL_DUTY_FB.Start_Pmp1, self.IO.P203, self.hmip203auto, self.hmip203reset, self.hmip203permissive, self.hmip203sd)
		if self.hmip203status_upd != -99:
			self.hmip203status = self.hmip203status_upd

		# self.P204_FB.PMP_FBD(self.P_HCL_DUTY_FB.Start_Pmp2, IO.P204, HMI.P204)
		self.hmip204status_upd, self.hmip204fault, self.hmip204avl, self.hmip204shutdown = self.P204_FB.PMP_FBD(self.P_HCL_DUTY_FB.Start_Pmp2, self.IO.P204, self.hmip204auto, self.hmip204reset, self.hmip204permissive, self.hmip204sd)
		if self.hmip204status_upd != -99:
			self.hmip204status = self.hmip204status_upd

		# self.P205_FB.PMP_FBD(self.P_NAOCL_FAC_DUTY_FB.Start_Pmp1,IO.P205, HMI.P205 )
		self.hmip205status_upd, self.hmip205fault, self.hmip205avl, self.hmip205shutdown = self.P205_FB.PMP_FBD(self.P_NAOCL_FAC_DUTY_FB.Start_Pmp1, self.IO.P205, self.hmip205auto, self.hmip205reset, self.hmip205permissive, self.hmip205sd)
		if self.hmip205status_upd != -99:
			self.hmip205status = self.hmip205status_upd

		# self.P206_FB.PMP_FBD(self.P_NAOCL_FAC_DUTY_FB.Start_Pmp2,IO.P206, HMI.P206)
		self.hmip206status_upd, self.hmip206fault, self.hmip206avl, self.hmip206shutdown = self.P206_FB.PMP_FBD(self.P_NAOCL_FAC_DUTY_FB.Start_Pmp2, self.IO.P206, self.hmip206auto, self.hmip206reset, self.hmip206permissive, self.hmip206sd)
		if self.hmip206status_upd != -99:
			self.hmip206status = self.hmip206status_upd

		############# Physical process simulation code ################
		self.Actuator()
		self.Plant()

		############# Physical process simulation ends here ###########

		######## All setdata() calls start here #######################
		# if self.hmiplantreseton:
		setdata(self, 'HMI.MV201.Reset',SCADA_ADDR,self.hmimv201reset)
		setdata(self, 'HMI.P201.Reset',SCADA_ADDR,self.hmip201reset)
		setdata(self, 'HMI.P202.Reset',SCADA_ADDR,self.hmip202reset)
		setdata(self, 'HMI.P203.Reset',SCADA_ADDR,self.hmip203reset)
		setdata(self, 'HMI.P204.Reset',SCADA_ADDR,self.hmip204reset)
		setdata(self, 'HMI.P205.Reset',SCADA_ADDR,self.hmip205reset)
		setdata(self, 'HMI.P206.Reset',SCADA_ADDR,self.hmip206reset)
		setdata(self, 'HMI.P207.Reset',SCADA_ADDR,self.hmip207reset)
		setdata(self, 'HMI.P208.Reset',SCADA_ADDR,self.hmip208reset)
		# if self.hmiplantautoon:
		setdata(self, 'HMI.MV201.Auto',SCADA_ADDR,self.hmimv201auto)
		setdata(self, 'HMI.P201.Auto',SCADA_ADDR,self.hmip201auto)
		setdata(self, 'HMI.P202.Auto',SCADA_ADDR,self.hmip202auto)
		setdata(self, 'HMI.P203.Auto',SCADA_ADDR,self.hmip203auto)
		setdata(self, 'HMI.P204.Auto',SCADA_ADDR,self.hmip204auto)
		setdata(self, 'HMI.P205.Auto',SCADA_ADDR,self.hmip205auto)
		setdata(self, 'HMI.P206.Auto',SCADA_ADDR,self.hmip206auto)
		setdata(self, 'HMI.P207.Auto',SCADA_ADDR,self.hmip207auto)
		setdata(self, 'HMI.P208.Auto',SCADA_ADDR,self.hmip208auto)

		setdata(self, 'HMI.P2.Permissive_On',SCADA_ADDR,(self.hmimv201avl and (self.hmip201avl or self.hmip202avl) and (self.hmip203avl or self.hmip204avl) and (self.hmip205avl or self.hmip206avl)))
		setdata(self, 'HMI.P201.Permissive',SCADA_ADDR,self.hmip201permissive)
		setdata(self, 'HMI.P201.MSG_Permissive',SCADA_ADDR,self.hmip201msgpermissive)
		setdata(self, 'HMI.P202.Permissive',SCADA_ADDR,self.hmip202permissive)
		setdata(self, 'HMI.P202.MSG_Permissive',SCADA_ADDR,self.hmip202msgpermissive)
		setdata(self, 'HMI.P203.Permissive',SCADA_ADDR,self.hmip203permissive)
		setdata(self, 'HMI.P203.MSG_Permissive',SCADA_ADDR,self.hmip203msgpermissive)
		setdata(self, 'HMI.P204.Permissive',SCADA_ADDR,self.hmip204permissive)
		setdata(self, 'HMI.P204.MSG_Permissive',SCADA_ADDR,self.hmip204msgpermissive)
		setdata(self, 'HMI.P205.Permissive',SCADA_ADDR,self.hmip205permissive)
		setdata(self, 'HMI.P205.MSG_Permissive',SCADA_ADDR,self.hmip205msgpermissive)
		setdata(self, 'HMI.P206.Permissive',SCADA_ADDR,self.hmip206permissive)
		setdata(self, 'HMI.P206.MSG_Permissive',SCADA_ADDR,self.hmip206msgpermissive)
		setdata(self, 'HMI.P207.Permissive',SCADA_ADDR,self.hmip207permissive)
		setdata(self, 'HMI.P207.MSG_Permissive',SCADA_ADDR,self.hmip207msgpermissive)
		setdata(self, 'HMI.P208.Permissive',SCADA_ADDR,self.hmip208permissive)
		setdata(self, 'HMI.P208.MSG_Permissive',SCADA_ADDR,self.hmip208msgpermissive)
		setdata(self, 'HMI.P201.SD',SCADA_ADDR,self.hmip201sd)
		setdata(self, 'HMI.P201.MSG_Shutdown',SCADA_ADDR,self.hmip201msgshutdown)
		setdata(self, 'HMI.P202.SD',SCADA_ADDR,self.hmip202sd)
		setdata(self, 'HMI.P202.MSG_Shutdown',SCADA_ADDR,self.hmip202msgshutdown)
		setdata(self, 'HMI.P203.SD',SCADA_ADDR,self.hmip203sd)
		setdata(self, 'HMI.P203.MSG_Shutdown',SCADA_ADDR,self.hmip203msgshutdown)
		setdata(self, 'HMI.P204.SD',SCADA_ADDR,self.hmip204sd)
		setdata(self, 'HMI.P204.MSG_Shutdown',SCADA_ADDR,self.hmip204msgshutdown)
		setdata(self, 'HMI.P205.SD',SCADA_ADDR,self.hmip205sd)
		setdata(self, 'HMI.P205.MSG_Shutdown',SCADA_ADDR,self.hmip205msgshutdown)
		setdata(self, 'HMI.P206.SD',SCADA_ADDR,self.hmip206sd)
		setdata(self, 'HMI.P206.MSG_Shutdown',SCADA_ADDR,self.hmip206msgshutdown)
		setdata(self, 'HMI.P207.SD',SCADA_ADDR,self.hmip207sd)
		setdata(self, 'HMI.P207.MSG_Shutdown',SCADA_ADDR,self.hmip207msgshutdown)
		setdata(self, 'HMI.P208.SD',SCADA_ADDR,self.hmip208sd)
		setdata(self, 'HMI.P208.MSG_Shutdown',SCADA_ADDR,self.hmip208msgshutdown)
		if self.hmiplantstop or self.hmiplantcriticalsdon:# the HMI.PLANT.Critical_SD_On variable could be rethought, currently it's defined in HMI
			setdata(self, 'HMI.P2.Shutdown',SCADA_ADDR,1)
		if self.hmip2state_prev == 1:
			if self.hmip2permissiveon and self.hmiplantstart:
				setdata(self, 'HMI.P2.State',SCADA_ADDR,2)
				self.hmip2state_prev = 0
		elif self.hmip2state_prev == 2:
			setdata(self, 'HMI.P2.Ready',SCADA_ADDR,1)
			if self.hmip2shutdown:
				if self.hmilit301ah:
					setdata(self, 'HMI.P2.State',SCADA_ADDR,1)
					setdata(self, 'HMI.P2.Shutdown',SCADA_ADDR,0)
					self.hmip2state_prev = 0
		else:
			setdata(self, 'HMI.P2.State',SCADA_ADDR,1)

		setdata(self, 'HMI.MV201.Status',SCADA_ADDR,self.hmimv201status)
		setdata(self, 'HMI.MV201.Avl',SCADA_ADDR,self.hmimv201avl)

		setdata(self, 'HMI.LS201.Alarm',SCADA_ADDR,self.hmils201alarm)
		setdata(self, 'HMI.LS202.Alarm',SCADA_ADDR,self.hmils202alarm)
		setdata(self, 'HMI.LSL203.Alarm',SCADA_ADDR,self.hmilsl203alarm)
		setdata(self, 'HMI.LSLL203.Alarm',SCADA_ADDR,self.hmilsll203alarm)

		setdata(self, 'HMI.P_NACL_DUTY.Both_Pmp_Not_Avl',SCADA_ADDR,self.hminaclbothpmpnotavl)
		setdata(self, 'HMI.P_NACL_DUTY.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hminaclselectedpmpnotavl)
		setdata(self, 'HMI.P_NACL_DUTY.Pump_Running',SCADA_ADDR,self.hminaclpumprunning)


		setdata(self, 'HMI.P_HCL_DUTY.Both_Pmp_Not_Avl',SCADA_ADDR,self.hmihclbothpmpnotavl)
		setdata(self, 'HMI.P_HCL_DUTY.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hmihclselectedpmpnotavl)
		setdata(self, 'HMI.P_HCL_DUTY.Pump_Running',SCADA_ADDR,self.hmihclpumprunning)

		setdata(self, 'HMI.P_NAOCL_FAC_DUTY.Both_Pmp_Not_Avl',SCADA_ADDR,self.hminaoclbothpmpnotavl)
		setdata(self, 'HMI.P_NAOCL_FAC_DUTY.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hminaoclselectedpmpnotavl)
		setdata(self, 'HMI.P_NAOCL_FAC_DUTY.Pump_Running',SCADA_ADDR,self.hminaoclpumprunning)

		setdata(self, 'HMI.P201.Status',SCADA_ADDR,self.hmip201status)
		setdata(self, 'HMI.P201.Fault',SCADA_ADDR,self.hmip201fault)
		setdata(self, 'HMI.P201.Avl',SCADA_ADDR,self.hmip201avl)
		setdata(self, 'HMI.P201.Shutdown',SCADA_ADDR,self.hmip201shutdown)

		setdata(self, 'HMI.P202.Status',SCADA_ADDR,self.hmip202status)
		setdata(self, 'HMI.P202.Fault',SCADA_ADDR,self.hmip202fault)
		setdata(self, 'HMI.P202.Avl',SCADA_ADDR,self.hmip202avl)
		setdata(self, 'HMI.P202.Shutdown',SCADA_ADDR,self.hmip202shutdown)

		setdata(self, 'HMI.P203.Status',SCADA_ADDR,self.hmip203status)
		setdata(self, 'HMI.P203.Fault',SCADA_ADDR,self.hmip203fault)
		setdata(self, 'HMI.P203.Avl',SCADA_ADDR,self.hmip203avl)
		setdata(self, 'HMI.P203.Shutdown',SCADA_ADDR,self.hmip203shutdown)

		setdata(self, 'HMI.P204.Status',SCADA_ADDR,self.hmip204status)
		setdata(self, 'HMI.P204.Fault',SCADA_ADDR,self.hmip204fault)
		setdata(self, 'HMI.P204.Avl',SCADA_ADDR,self.hmip204avl)
		setdata(self, 'HMI.P204.Shutdown',SCADA_ADDR,self.hmip204shutdown)

		setdata(self, 'HMI.P205.Status',SCADA_ADDR,self.hmip205status)
		setdata(self, 'HMI.P205.Fault',SCADA_ADDR,self.hmip205fault)
		setdata(self, 'HMI.P205.Avl',SCADA_ADDR,self.hmip205avl)
		setdata(self, 'HMI.P205.Shutdown',SCADA_ADDR,self.hmip205shutdown)

		setdata(self, 'HMI.P206.Status',SCADA_ADDR,self.hmip206status)
		setdata(self, 'HMI.P206.Fault',SCADA_ADDR,self.hmip206fault)
		setdata(self, 'HMI.P206.Avl',SCADA_ADDR,self.hmip206avl)
		setdata(self, 'HMI.P206.Shutdown',SCADA_ADDR,self.hmip206shutdown)

		######### setadata() calls end here ##################

		# elapsed = time.time() - iter_start
		# print('Iteration time:', elapsed)

		# time.sleep(5)

	def _launch_next(self):
		# Schedule the next call
		threading.Timer(interval, self._launch_next).start()
		# Launch network_function in a thread
		t = threading.Thread(target=self.Iteration)
		t.daemon = True
		t.start()


	def Pre_Main_UF_Feed_Dosing(self,IO):

		self.IO = IO
		self._launch_next()
		while True:
			time.sleep(1)
