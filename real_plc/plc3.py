# this is the PLC 3 logic, it's about the very same thing as that in the real plc.
###### Existing emulator libraries ################
from devices import PLC
from utils import SCADA_ADDR, SCADA_TAGS
from utils import IP
import time
import multiprocessing
import threading


# from logicblock.logicblock import SETD
from logicblock.logicblock import *
# from logicblock.logicblock import TONR
from controlblock.controlblock import *
from logicblock.logicblock import bit_2_signed_integer
from logicblock.logicblock import signed_integer_2_bit
from utils import getdata, setdata

interval = 60
timeout = 20
time_interval = 1

class plc3(PLC):
	'plc3 logic'


	def pre_loop(self):

		### Initialization block #######
		self.k = 0 # counter for number of iterations

		self.hmiplantreseton = 1
		self.hmiplantautoon = 1
		self.hmiplantautooff = 0
		self.hmiplantstart = 0
		self.hmiplantstop = 0
		self.hmiplantcriticalsdon = 0

		self.hmimv301status = 1
		self.hmimv302status = 1
		self.hmimv303status = 1
		self.hmimv304status = 1
		self.hmip602status = 1
		self.hmilit301hty = 1
		self.hmilit301ahh = 0
		self.hmilit301ah = 0
		self.hmilit301al=0
		self.hmilit301all=0
		self.hmip301avl=1
		self.hmip301fault=0
		self.hmip301shutdown = bit_2_signed_integer([0]*16)
		self.hmip302avl=1
		self.hmip302fault=0
		self.hmip302shutdown=bit_2_signed_integer([0]*16)
		self.hmifit301hty=0
		self.hmifit301ahh=0
		self.hmifit301ah=0
		self.hmifit301al=0
		self.hmifit301all=0
		self.hmipsh301delay=0
		self.hmidpsh301delay=0
		self.hmidpit301hty=1
		self.hmidpit301ahh=0
		self.hmidpit301ah=0
		self.hmidpit301al=0
		self.hmidpit301all=0
		self.hmimv301fto=0
		self.hmimv301ftc=0
		self.hmimv301open=1
		self.hmimv301close=0
		self.hmimv302fto=0
		self.hmimv302ftc=0
		self.hmimv302open=1
		self.hmimv302close=0
		self.hmimv303fto=0
		self.hmimv303ftc=0
		self.hmimv303open=1
		self.hmimv303close=0
		self.hmimv304fto=0
		self.hmimv304ftc=0
		self.hmimv304open=1
		self.hmimv304close=0

		self.hmip3state=1
		self.hmimv301reset=1
		self.hmimv302reset=1
		self.hmimv303reset=1
		self.hmimv304reset=1
		self.hmip301reset=0
		self.hmip302reset=0
		self.hmimv301auto=1
		self.hmimv302auto=1
		self.hmimv303auto=1
		self.hmimv304auto=1
		self.hmip301auto=1
		self.hmip302auto=1
		self.hmip3permissiveon=1
		self.hmimv301avl=1
		self.hmimv302avl=1
		self.hmimv303avl=1
		self.hmimv304avl=1
		self.hmip301status=1
		self.hmip302status=1
		self.hmip301permissive=bit_2_signed_integer([1]*16)
		self.hmip301msgpermissive=bit_2_signed_integer([0] * 6)
		self.hmilit401ahh=0
		self.hmip302permissive=bit_2_signed_integer([1]*16)
		self.hmip302msgpermissive=bit_2_signed_integer([0] * 6)
		self.hmip301sd=bit_2_signed_integer([0]*16)
		self.hmipsh301alarm=0
		self.hmip301msgshutdown=bit_2_signed_integer([0] * 6)
		self.hmip302msgshutdown=bit_2_signed_integer([0] * 6)
		self.hmip302sd= bit_2_signed_integer([0]*16)
		self.hmip3shutdown=1
		self.hmiplantstop=0
		self.hmiplantcriticalsdon=0
		self.hmiplanttmphigh=0
		self.hmidpsh301alarm=0
		self.hmilit401ah=0
		self.hmicyp3ufrefillsec=0
		self.hmicyp3uffiltrationmin=0
		self.hmicyp3backwashsec=0
		self.hmicyp3cipcleaningsec=0
		self.hmicyp3drainsec=0

		self.hmicyp3ufrefillsecsp=30
		self.hmimv302status=1
		self.hmip3tmphigh=0
		self.hmicyp3uffiltrationminsp=3
		self.hmicyp3backwashsecsp=30
		self.hmicyp3bwcnt=0
		self.hmicyp3drainsecsp=30
		self.hmip205status=1
		self.hmicyp3cipcleaningsecsp=0
		self.hmilit401al=0
		self.hmipufdutyselection=1
		self.hmiufbothpmpnotavl=0
		self.hmiufselectedpmpnotavl_upd=0
		self.hmiufselectedpmpnotavl=0
		# self.hmip301status_upd=0
		# self.hmip302status_upd=0
		# self.hmimv301status_upd=0
		# self.hmimv302status_upd=0
		# self.hmimv303status_upd=0
		# self.hmimv304status_upd=0
		self.hmiufpumprunning = 0
		### End of Initialization block #######
		self.TON_FIT301_P1_TM = TONR(6,'FIT301_P1')
		self.TON_FIT301_P2_TM = TONR(6,'FIT301_P2')
		self.SEC_TEST = 0
		self.MIN_TEST = 0
		self.Mid_NEXT = 0
		self.Mid_MV301_AutoInp			= self.hmimv301status-1
		self.Mid_MV302_AutoInp			= self.hmimv302status-1
		self.Mid_MV303_AutoInp			= self.hmimv303status-1
		self.Mid_MV304_AutoInp			= self.hmimv304status-1
		self.Mid_P_UF_FEED_DUTY_AutoInp	=0
		self.Mid_P602_AutoInp			= self.hmip602status-1
		self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
		self.hmimv201open = 0
		self.hmip101status = 1
		self.hmip3state_prev = 0


		self.LIT301_FB = AIN_FBD(self.hmilit301hty,self.hmilit301ahh,self.hmilit301ah,self.hmilit301al,self.hmilit301all)
		self.P_UF_FEED_DUTY_FB = Duty2_FBD()
		self.P301_FB = PMP_FBD(self.hmip301avl,self.hmip301fault,self.hmip301shutdown)
		self.P302_FB = PMP_FBD(self.hmip302avl,self.hmip302fault,self.hmip302shutdown)
		self.FIT301_FB = FIT_FBD(self.hmifit301hty,self.hmifit301ahh,self.hmifit301ah,self.hmifit301al,self.hmifit301all)
		self.PSH301_FB = SWITCH_FBD(self.hmipsh301delay)
		self.DPSH301_FB = SWITCH_FBD(self.hmidpsh301delay)
		self.DPIT301_FB = AIN_FBD(self.hmidpit301hty,self.hmidpit301ahh,self.hmidpit301ah,self.hmidpit301al,self.hmidpit301all)
		self.MV301_FB = MV_FBD(self.hmimv301fto,self.hmimv301ftc,self.hmimv301open,self.hmimv301close)
		self.MV302_FB = MV_FBD(self.hmimv302fto,self.hmimv302ftc,self.hmimv302open,self.hmimv302close)
		self.MV303_FB = MV_FBD(self.hmimv303fto,self.hmimv303ftc,self.hmimv303open,self.hmimv303close)
		self.MV304_FB = MV_FBD(self.hmimv304fto,self.hmimv304ftc,self.hmimv304open,self.hmimv304close)

		################## multiprocessing manager ###########
		manager = multiprocessing.Manager()
		self.shared = manager.dict({
            "hmiplantreseton": self.hmiplantreseton,
            "hmiplantautoon": self.hmiplantautoon,
            "hmiplantautooff": self.hmiplantautooff,
			"hmilit401ahh": self.hmilit401ahh,
			"hmilit401ah": self.hmilit401ah,
			"hmiplantstart": self.hmiplantstart,
			"hmiplantstop": self.hmiplantstop,
			"hmiplantcriticalsdon": self.hmiplantcriticalsdon,
			"hmilit401al": self.hmilit401al,
			"hmip205status": self.hmip205status,
			"hmimv201open": self.hmimv201open,
			"hmip101status": self.hmip101status,
			"hmip602status": self.hmip602status,
        })

		#######################################################
		time.sleep(10)
		print ("	PLC3 started\n")


	def fetchData(self, state):
		self.shared["hmiplantreseton"] = getdata(self, 'HMI.PLANT.Reset_On',SCADA_ADDR,self.shared["hmiplantreseton"])
		self.shared["hmiplantautoon"] = getdata(self, 'HMI.PLANT.Auto_On',SCADA_ADDR,self.shared["hmiplantautoon"])
		self.shared["hmiplantautooff"] = getdata(self, 'HMI.PLANT.Auto_Off',SCADA_ADDR,self.shared["hmiplantautooff"])
		self.shared["hmilit401ahh"] = getdata(self, 'HMI.LIT401.AHH',SCADA_ADDR,self.shared["hmilit401ahh"])
		self.shared["hmiplantstop"] = getdata(self, 'HMI.PLANT.Stop',SCADA_ADDR,self.shared["hmiplantstop"])
		self.shared["hmiplantcriticalsdon"] = getdata(self, 'HMI.PLANT.Critical_SD_On',SCADA_ADDR,self.shared["hmiplantcriticalsdon"])
		if state>1:
			self.shared["hmilit401ah"] = getdata(self, 'HMI.LIT401.AH',SCADA_ADDR,self.shared["hmilit401ah"])
		if state == 1 or state == 99:
			self.shared["hmiplantstart"] = getdata(self, 'HMI.PLANT.Start',SCADA_ADDR,self.shared["hmiplantstart"])
		if state == 11 or state == 13:
			self.shared["hmip602status"] = getdata(self, 'HMI.P602.Status',SCADA_ADDR,self.shared["hmip602status"])
		if state==17 or state==19:
			self.shared["hmip205status"] = getdata(self, 'HMI.P205.Status',SCADA_ADDR,self.shared["hmip205status"])
		if state==99:
			self.shared["hmilit401al"] = getdata(self, 'HMI.LIT401.AL',SCADA_ADDR,self.shared["hmilit401al"])

		self.shared["hmimv201open"] = getdata(self, 'HMI.MV201.Open',SCADA_ADDR,self.shared["hmimv201open"])
		self.shared["hmip101status"] = getdata(self, 'HMI.P101.Status',SCADA_ADDR,self.shared["hmip101status"])

	def Actuator(self):
		self.IO.MV301.DI_ZSO = self.IO.MV301.DO_Open
		self.IO.MV301.DI_ZSC = self.IO.MV301.DO_Close
		self.IO.MV302.DI_ZSO = self.IO.MV302.DO_Open
		self.IO.MV302.DI_ZSC = self.IO.MV302.DO_Close
		self.IO.MV303.DI_ZSO = self.IO.MV303.DO_Open
		self.IO.MV303.DI_ZSC = self.IO.MV303.DO_Close
		self.IO.MV304.DI_ZSO = self.IO.MV304.DO_Open
		self.IO.MV304.DI_ZSC = self.IO.MV304.DO_Close
		self.IO.P301.DI_Run = self.IO.P301.DO_Start
		self.IO.P302.DI_Run = self.IO.P302.DO_Start

	def Plant(self):
		self.h_t301=0
		self.p = {"f_mv101":2.3*1000000000/3600,"S_t101":1.5*1000000,"S_t301":1.5*1000000,"S_t401":1.5*1000000,"S_t601":1.5*1000000,"S_t601":1.5*1000000,"S_t602":1.5*1000000,"f_p101":2.0*1000000000/3600,"f_mv201":2.0*1000000000/3600,"f_p301":2.0*1000000000/3600,"f_mv302":2.0*1000000000/3600,"f_p602":2.0*1000000000/3600,"f_p401":2.0*1000000000/36001,"f_mv501":2.0*1000000000/3600,"f_mv502":0.00006111,"f_mv503":0.00049,"f_p601":2.0*1000000000/36001,"LIT101_AL":0.2,"LIT101_AH":0.8,"LIT301_AL":0.2,"LIT301_AH":0.8,"LIT401_AL":0.2,"LIT401_AH":0.8,"LIT601_AL":0.2,"LIT601_AH":0.8,"LIT602_AL":0.2,"LIT602_AH":0.8,"cond_AIT201_AL":250,"cond_AIT201_AH":260,"ph_AIT202_AL":6.95,"ph_AIT202_AH":7.05,"orp_AIT203_AL":420,"orp_AIT203_AH":500,"cond_AIT503_AH":260,"h201_AL":50,"h202_AL":4,"h203_AL":15,"cond_AIT503_AL":250,"cond_AIT503_AH":260,"orp_AIT402_AL":420,"orp_AIT402_AH":500,"omega_inlet":0.001}  # critical plant parameters

		if self.hmimv201open == 1 and self.hmip101status == 2:#mv201, feeding water to tank301
			self.h_t301=self.h_t301+self.p['f_mv201'] / self.p['S_t301']

		if self.IO.P301.DI_Run == 1 or self.IO.P302.DI_Run == 1: #p301, drawing water from tank301
			self.h_t301=self.h_t301-self.p['f_p301'] / self.p['S_t301']

		self.hmilit301pv=self.result[self.k]
		# setdata(self, 'HMI.LIT301.Pv',SCADA_ADDR,self.hmilit301pv)
        # HMI.LIT301.set_alarm()
		if type(self.hmilit301pv) != type('a'):
			self.hmilit301ahh, self.hmilit301ah, self.hmilit301al, self.hmilit301all = ALM(self.hmilit301pv, 1200, 1000, 800, 250)

			# setdata(self, 'HMI.LIT301.AHH',SCADA_ADDR,self.hmilit301ahh)
			# setdata(self, 'HMI.LIT301.AH',SCADA_ADDR,self.hmilit301ah)
			# setdata(self, 'HMI.LIT301.AL',SCADA_ADDR,self.hmilit301al)
			# setdata(self, 'HMI.LIT301.ALL',SCADA_ADDR,self.hmilit301all)


		self.result.append(self.result[self.k]+self.h_t301*time_interval)

		self.k = self.k + 1

	def Iteration(self,time):
		p = multiprocessing.Process(target=self.fetchData, args=(self.hmip3state,))
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
		self.hmilit401ahh = self.shared["hmilit401ahh"]
		self.hmilit401ah = self.shared["hmilit401ah"]
		self.hmiplantstart = self.shared["hmiplantstart"]
		self.hmiplantstop = self.shared["hmiplantstop"]
		self.hmiplantcriticalsdon = self.shared["hmiplantcriticalsdon"]
		self.hmilit401al = self.shared["hmilit401al"]
		self.hmip205status = self.shared["hmip205status"]
		self.hmimv201open = self.shared["hmimv201open"]
		self.hmip101status = self.shared["hmip101status"]
		self.hmip602status = self.shared["hmip602status"]

		print("PLC3 State:", self.hmip3state)

		Sec_P = not bool(time%(1/time_interval))
		Min_P = not bool(time%(60/time_interval))

		if self.hmiplantreseton:

			# setdata(self, 'HMI.MV301.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV302.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV303.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV304.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P301.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P302.Reset',SCADA_ADDR,1)
			self.hmimv301reset  = 1
			self.hmimv302reset = 1
			self.hmimv303reset = 1
			self.hmimv304reset = 1
			self.hmip301reset  = 1
			self.hmip302reset  = 1

		if self.hmiplantautoon:
			# setdata(self, 'HMI.MV301.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV302.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV303.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.MV304.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P301.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P302.Auto',SCADA_ADDR,1)
			self.hmimv301auto  = 1
			self.hmimv302auto = 1
			self.hmimv303auto = 1
			self.hmimv304auto = 1
			self.hmip301auto  = 1
			self.hmip302auto  = 1

		if self.hmiplantautooff:
			# setdata(self, 'HMI.MV301.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.MV302.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.MV303.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.MV304.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P301.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P302.Auto',SCADA_ADDR,0)
			self.hmimv301auto  = 0
			self.hmimv302auto = 0
			self.hmimv303auto = 0
			self.hmimv304auto = 0
			self.hmip301auto  = 0
			self.hmip302auto  = 0


		# setdata(self, 'HMI.P3.Permissive_On',SCADA_ADDR,self.hmimv301avl and self.hmimv302avl and self.hmimv303avl and self.hmimv304avl and (self.hmip301avl or self.hmip302avl))
		self.hmip3permissiveon = self.hmimv301avl and self.hmimv302avl and self.hmimv303avl and self.hmimv304avl and (self.hmip301avl or self.hmip302avl)
		# HMI.P3.Permissive_On 	=  HMI.MV301.Avl and HMI.MV302.Avl and HMI.MV303.Avl and HMI.MV304.Avl and (HMI.P301.Avl or HMI.P302.Avl)

		self.Mid_FIT301_Tot_Enb	= self.hmimv301status==2 or self.hmimv302status==2


		self.TON_FIT301_P1_TM.TONR(self.hmifit301all and self.hmip301status == 2)

		self.TON_FIT301_P2_TM.TONR(self.hmifit301all and self.hmip302status == 2)

		self.hmip301permissive_arr = signed_integer_2_bit(self.hmip301permissive)
		self.hmip301permissive_arr[0] 	= not self.hmilit301all
		self.hmip301permissive_arr[1] 	= not self.hmilit401ahh
		self.hmip301permissive_arr[2] 	= self.hmimv302status==2 or self.hmimv304status==2
		self.hmip301permissive = bit_2_signed_integer(self.hmip301permissive_arr)
		# setdata(self, 'HMI.P301.Permissive',SCADA_ADDR,self.hmip301permissive)

		self.hmip301msgpermissive_arr = signed_integer_2_bit(self.hmip301msgpermissive)
		self.hmip301msgpermissive_arr[1] = int(self.hmip301permissive_arr[0])
		self.hmip301msgpermissive_arr[2] = int(self.hmip301permissive_arr[1])
		self.hmip301msgpermissive_arr[3] = int(self.hmip301permissive_arr[2])
		self.hmip301msgpermissive = bit_2_signed_integer(self.hmip301msgpermissive_arr)
		# setdata(self, 'HMI.P301.MSG_Permissive',SCADA_ADDR,self.hmip301msgpermissive)

		# HMI.P301.MSG_Permissive[1] = HMI.P301.Permissive[0]
		# HMI.P301.MSG_Permissive[2] = HMI.P301.Permissive[1]
		# HMI.P301.MSG_Permissive[3] = HMI.P301.Permissive[2]

		self.hmip302permissive_arr = signed_integer_2_bit(self.hmip302permissive)
		self.hmip302permissive_arr[0] 	= not self.hmilit301all
		self.hmip302permissive_arr[1] 	= not self.hmilit401ahh
		self.hmip302permissive_arr[2] 	= self.hmimv302status==2 or self.hmimv304status==2
		self.hmip302permissive = bit_2_signed_integer(self.hmip302permissive_arr)
		# setdata(self, 'HMI.P302.Permissive',SCADA_ADDR,self.hmip302permissive)
		# HMI.P302.Permissive[0] 	= not HMI.LIT301.ALL
		# HMI.P302.Permissive[1] 	= not HMI.LIT401.AHH
		# HMI.P302.Permissive[2] 	= HMI.MV302.Status==2 or HMI.MV304.Status==2

		self.hmip302msgpermissive_arr = signed_integer_2_bit(self.hmip302msgpermissive)
		self.hmip302msgpermissive_arr[1] = int(self.hmip302permissive_arr[0])
		self.hmip302msgpermissive_arr[2] = int(self.hmip302permissive_arr[1])
		self.hmip302msgpermissive_arr[3] = int(self.hmip302permissive_arr[2])
		self.hmip302msgpermissive = bit_2_signed_integer(self.hmip302msgpermissive_arr)
		# setdata(self, 'HMI.P302.MSG_Permissive',SCADA_ADDR,self.hmip302msgpermissive)
		# HMI.P302.MSG_Permissive[1] = HMI.P302.Permissive[0]
		# HMI.P302.MSG_Permissive[2] = HMI.P302.Permissive[1]
		# HMI.P302.MSG_Permissive[3] = HMI.P302.Permissive[2]

		self.hmip301sd_arr = signed_integer_2_bit(self.hmip301sd)
		self.hmip301sd_arr[0] = int(self.hmilit301all)
		self.hmip301sd_arr[1] = int(self.hmilit401ahh)
		self.hmip301sd_arr[2] = int(self.hmipsh301alarm)
		self.hmip301sd_arr[3] = 0
		self.hmip301sd_arr[4] = int(self.hmip301status==2 and self.hmimv302status!=2 and self.hmimv304status!=2)
		self.hmip301sd = bit_2_signed_integer(self.hmip301sd_arr)
		# setdata(self, 'HMI.P301.SD',SCADA_ADDR,self.hmip301sd)

		# HMI.P301.SD[0] 	= HMI.LIT301.ALL
		# HMI.P301.SD[1] 	= HMI.LIT401.AHH
		# HMI.P301.SD[2] 	= HMI.PSH301.Alarm
		# HMI.P301.SD[3] 	= 0
		# HMI.P301.SD[4] 	= HMI.P301.Status ==2 and HMI.MV302.Status!=2 and HMI.MV304.Status!=2

		self.hmip301msgshutdown_arr = signed_integer_2_bit(self.hmip301msgshutdown)
		self.hmip301shutdown_arr = signed_integer_2_bit(self.hmip301shutdown)
		self.hmip301msgshutdown_arr[1] = self.hmip301shutdown_arr[0]
		self.hmip301msgshutdown_arr[2] = self.hmip301shutdown_arr[1]
		self.hmip301msgshutdown_arr[3] = self.hmip301shutdown_arr[2]
		self.hmip301msgshutdown_arr[4] = self.hmip301shutdown_arr[3]
		self.hmip301msgshutdown_arr[5] = self.hmip301shutdown_arr[4]
		self.hmip301msgshutdown = bit_2_signed_integer(self.hmip301msgshutdown_arr)
		# setdata(self, 'HMI.P301.MSG_Shutdown',SCADA_ADDR,self.hmip301msgshutdown)
		# HMI.P301.MSG_Shutdown[1] = HMI.P301.Shutdown[0]
		# HMI.P301.MSG_Shutdown[2] = HMI.P301.Shutdown[1]
		# HMI.P301.MSG_Shutdown[3] = HMI.P301.Shutdown[2]
		# HMI.P301.MSG_Shutdown[4] = HMI.P301.Shutdown[3]
		# HMI.P301.MSG_Shutdown[5] = HMI.P301.Shutdown[4]

		self.hmip302sd_arr = signed_integer_2_bit(self.hmip302sd)
		self.hmip302sd_arr[0] = int(self.hmilit301all)
		self.hmip302sd_arr[1] = int(self.hmilit401ahh)
		self.hmip302sd_arr[2] = int(self.hmipsh301alarm)
		self.hmip302sd_arr[3] = 0
		self.hmip302sd_arr[4] = int(self.hmip302status==2 and self.hmimv302status!=2 and self.hmimv304status!=2)
		self.hmip302sd = bit_2_signed_integer(self.hmip302sd_arr)
		# setdata(self, 'HMI.P302.SD',SCADA_ADDR,self.hmip302sd)
		# HMI.P302.SD[0] 	= HMI.LIT301.ALL
		# HMI.P302.SD[1] 	= HMI.LIT401.AHH
		# HMI.P302.SD[2] 	= HMI.PSH301.Alarm
		# HMI.P302.SD[3] 	= 0
		# HMI.P302.SD[4] 	= HMI.P302.Status ==2 and HMI.MV302.Status!=2 and HMI.MV304.Status!=2

		self.hmip302msgshutdown_arr = signed_integer_2_bit(self.hmip302msgshutdown)
		self.hmip302shutdown_arr = signed_integer_2_bit(self.hmip302shutdown)
		self.hmip302msgshutdown_arr[1] = self.hmip302shutdown_arr[0]
		self.hmip302msgshutdown_arr[2] = self.hmip302shutdown_arr[1]
		self.hmip302msgshutdown_arr[3] = self.hmip302shutdown_arr[2]
		self.hmip302msgshutdown_arr[4] = self.hmip302shutdown_arr[3]
		self.hmip302msgshutdown_arr[5] = self.hmip302shutdown_arr[4]
		self.hmip302msgshutdown = bit_2_signed_integer(self.hmip302msgshutdown_arr)
		# setdata(self, 'HMI.P302.MSG_Shutdown',SCADA_ADDR,self.hmip302msgshutdown)
		# HMI.P302.MSG_Shutdown[1] = HMI.P302.Shutdown[0]
		# HMI.P302.MSG_Shutdown[2] = HMI.P302.Shutdown[1]
		# HMI.P302.MSG_Shutdown[3] = HMI.P302.Shutdown[2]
		# HMI.P302.MSG_Shutdown[4] = HMI.P302.Shutdown[3]
		# HMI.P302.MSG_Shutdown[5] = HMI.P302.Shutdown[4]


		if self.hmiplantstop or self.hmiplantcriticalsdon:
			# setdata(self, 'HMI.P3.Shutdown',SCADA_ADDR,1)
			self.hmip3shutdown = 1

		if self.hmidpit301hty:
			# setdata(self, 'HMI.PLANT.TMP_High',SCADA_ADDR,self.hmidpit301ah)
			self.hmiplanttmphigh = self.hmidpit301ah
		else:
			# setdata(self, 'HMI.PLANT.TMP_High',SCADA_ADDR,self.hmidpsh301alarm)
			self.hmiplanttmphigh = self.hmidpsh301alarm
			# HMI.PLANT.TMP_High= HMI.DPSH301.Alarm


		if self.hmilit401ah and self.hmip3state > 1:
			self.hmip3state=99
			# setdata(self, 'HMI.P3.State',SCADA_ADDR,self.hmip3state)
		#(*-----------WRITE FAULT COnDITIOn--------------*)
		while switch(self.hmip3state):
			if case(1):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.P3.Shutdown',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				self.hmip3shutdown = 0
				if self.hmip3permissiveon and self.hmiplantstart:
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,2)
					self.hmip3state = 2
				break
			if case(2):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=not self.hmilit301all and not self.hmilit401ah
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				# HMI.Cy_P3.UF_REFILL_SEC		=0
				# HMI.Cy_P3.UF_FILTRATION_MIN	=0
				# HMI.Cy_P3.BACKWASH_SEC		=0
				# HMI.Cy_P3.CIP_CLEANING_SEC	=0
				# HMI.Cy_P3.DRAIN_SEC			=0
				if  self.hmimv304status==2 or self.Mid_NEXT:
					self.Mid_NEXT = 0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,3)
					self.hmip3state = 3
					# HMI.P3.State=3
				break
			if case(3):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=1
				self.Mid_P_UF_FEED_DUTY_AutoInp	=1
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if  self.hmip301status ==2 or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,4)
					self.hmip3state = 4
				break
			if case(4):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=1
				self.Mid_P_UF_FEED_DUTY_AutoInp	=1
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				# self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				# HMI.Cy_P3.UF_FILTRATION_MIN	=0
				# HMI.Cy_P3.BACKWASH_SEC		=0
				# HMI.Cy_P3.CIP_CLEANING_SEC	=0
				# HMI.Cy_P3.DRAIN_SEC			=0
				if Sec_P:
					self.hmicyp3ufrefillsec = self.hmicyp3ufrefillsec + 1
					# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,self.hmicyp3ufrefillsec)
				if self.hmicyp3ufrefillsec>self.hmicyp3ufrefillsecsp or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,5)
					self.hmip3state = 5
				break
				# timer
			if case(5):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=1
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=1
				self.Mid_P_UF_FEED_DUTY_AutoInp	=1
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmimv302status ==2 or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,6)
					self.hmip3state = 6
				break
			if case(6):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=1
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=1
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmimv304status or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,7)
					self.hmip3state = 7
				break
			if case(7):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=1
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=1
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# # setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				# self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmip3tmphigh:
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,8)
					self.hmip3state = 8
				else:
					if Min_P:
						self.hmicyp3uffiltrationmin += 1
						# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,self.hmicyp3uffiltrationmin)
				if self.hmicyp3uffiltrationmin>=self.hmicyp3uffiltrationminsp or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,8)
					self.hmip3state = 8
				if  self.hmip3shutdown and self.hmilit401ah:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,8)
					self.hmip3state = 8
				break
			if case(8):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=1
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if not self.hmip301status == 2 or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,9)
					self.hmip3state = 9
				break
			if case(9):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmip3shutdown:
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,1)
					self.hmip3state = 1
				elif self.hmimv302status==1 or self.Mid_NEXT and not self.hmip3shutdown:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,10)
					self.hmip3state = 10
				break
			if case(10):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=1
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmimv301status==2 and self.hmimv303status==2 or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,11)
					self.hmip3state = 11
				break
			if case(11):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=1
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=1
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmip602status==2 or self.Mid_NEXT:
					self.Mid_NEXT =0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,12)
					self.hmip3state = 12
				break
			if case(12):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=1
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=1
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# # setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				# self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if Sec_P:
					self.hmicyp3backwashsec = self.hmicyp3backwashsec + 1
					# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,self.hmicyp3backwashsec)
				if self.hmicyp3backwashsec> self.hmicyp3backwashsecsp or self.Mid_NEXT:
					self.Mid_NEXT =0
					self.hmicyp3bwcnt +=1
					# setdata(self, 'HMI.Cy_P3.BW_CNT',SCADA_ADDR,self.hmicyp3bwcnt)
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,13)
					self.hmip3state = 13
				break
			if case(13):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=1
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmip602status==1 or self.Mid_NEXT:
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,14)
					self.hmip3state = 14
				break
			if case(14):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmimv301status==1 or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,15)
					self.hmip3state = 15
				break
			if case(15):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=1
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmimv304status==2 or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,16)
					self.hmip3state = 16
				break
			if case(16):
				self.hmip3state_prev = self.hmip3state
				self.Mid_Last_State= self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=1
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				# self.hmicyp3drainsec = 0
				if Sec_P:
					self.hmicyp3drainsec = self.hmicyp3drainsec + 1
					# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,self.hmicyp3drainsec)
				if self.hmicyp3drainsec>self.hmicyp3drainsecsp or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,4)
					self.hmip3state = 4
				break
			if case(17):
				self.hmip3state_prev = self.hmip3state
				self.Mid_MV301_AutoInp			=1
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=1
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if self.hmip205status == 2 or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,18)
					self.hmip3state = 18
				break
			if case(18):
				self.hmip3state_prev = self.hmip3state
				self.Mid_MV301_AutoInp			=1
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=1
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# # setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				# self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if Sec_P:
					self.hmicyp3cipcleaningsec=self.hmicyp3cipcleaningsec+1
					# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,self.hmicyp3cipcleaningsec)
				if self.hmicyp3cipcleaningsec>self.hmicyp3cipcleaningsecsp or self.Mid_NEXT:
					self.Mid_NEXT=0
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,19)
					self.hmip3state = 19
				break
			if case(19):
				self.hmip3state_prev = self.hmip3state
				self.Mid_MV301_AutoInp			=1
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=1
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# # setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				# self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if not self.hmip205status == 2 or self.Mid_NEXT:
						self.Mid_NEXT=0
						# setdata(self, 'HMI.P3.State',SCADA_ADDR,14)
						self.hmip3state = 14
				break
			if case(99):
				self.hmip3state_prev = self.hmip3state
				self.Mid_MV301_AutoInp			=0
				self.Mid_MV302_AutoInp			=0
				self.Mid_MV303_AutoInp			=0
				self.Mid_MV304_AutoInp			=0
				self.Mid_P_UF_FEED_DUTY_AutoInp	=0
				self.Mid_P602_AutoInp			=0
				self.Mid_P_NAOCL_UF_DUTY_AutoInp=0
				# setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
				# setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
				self.hmicyp3ufrefillsec = 0
				self.hmicyp3uffiltrationmin = 0
				self.hmicyp3backwashsec = 0
				self.hmicyp3cipcleaningsec = 0
				self.hmicyp3drainsec = 0
				if  (self.hmilit401al and not self.hmip3shutdown) or self.hmiplantstart:
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,2)
					self.hmip3state = 2
				elif self.hmilit401ah and self.hmip3shutdown:
					# setdata(self, 'HMI.P3.State',SCADA_ADDR,1)
					self.hmip3state = 1
				break
			# setdata(self, 'HMI.P3.State',SCADA_ADDR,1)
			self.hmip3state = 1
			break
#end of case structure
		# setdata(self, 'HMI.Mid_P602_AutoInp',SCADA_ADDR,self.Mid_P602_AutoInp)

#	def UF_Feed(self):
		# self.P_UF_FEED_DUTY_FB.Duty2_FBD(self.Mid_P_UF_FEED_DUTY_AutoInp, HMI.P301, HMI.P302, HMI.P_UF_FEED_DUTY)
		self.hmiufbothpmpnotavl, self.hmiufselectedpmpnotavl_upd, self.hmiufpumprunning = self.P_UF_FEED_DUTY_FB.Duty2_FBD(self.Mid_P_UF_FEED_DUTY_AutoInp, self.hmip301status, self.hmip301avl, self.hmip302status, self.hmip302avl, self.hmipufdutyselection)
		if self.hmiufselectedpmpnotavl_upd != -99:
			self.hmiufselectedpmpnotavl = self.hmiufselectedpmpnotavl_upd

		# self.P301_FB.PMP_FBD(self.P_UF_FEED_DUTY_FB.Start_Pmp1, self.IO.P301, HMI.P301)
		self.hmip301status_upd, self.hmip301fault, self.hmip301avl, self.hmip301shutdown = self.P301_FB.PMP_FBD(self.P_UF_FEED_DUTY_FB.Start_Pmp1, self.IO.P301, self.hmip301auto, self.hmip301reset, self.hmip301permissive, self.hmip301sd)
		if self.hmip301status_upd != -99:
			self.hmip301status = self.hmip301status_upd

		# self.P302_FB.PMP_FBD(self.P_UF_FEED_DUTY_FB.Start_Pmp2, self.IO.P302, HMI.P302)
		self.hmip302status_upd, self.hmip302fault, self.hmip302avl, self.hmip302shutdown = self.P302_FB.PMP_FBD(self.P_UF_FEED_DUTY_FB.Start_Pmp1, self.IO.P302, self.hmip302auto, self.hmip302reset, self.hmip302permissive, self.hmip302sd)
		if self.hmip302status_upd != -99:
			self.hmip302status = self.hmip302status_upd

		# self.hmipsh301alarm =  # Note: Bug in code - should be assigned to Status, but HMI_PSH class has no status variable
		self.PSH301_FB.SWITCH_FBD(self.IO.PSH301)

		# self.hmidpsh301alarm = # Same note as above
		self.DPSH301_FB.SWITCH_FBD(self.IO.DPSH301)

		# self.MV301_FB.MV_FBD(self.Mid_MV301_AutoInp, self.IO.MV301, HMI.MV301)
		self.hmimv301status_upd, self.hmimv301avl = self.MV301_FB.MV_FBD(
			self.Mid_MV301_AutoInp,
			self.IO.MV301,
			self.hmimv301auto,
			self.hmimv301reset)
		if self.hmimv301status_upd!= -99:
			self.hmimv301status = self.hmimv301status_upd

		# self.MV302_FB.MV_FBD(self.Mid_MV302_AutoInp, self.IO.MV302, HMI.MV302)
		self.hmimv302status_upd, self.hmimv302avl = self.MV302_FB.MV_FBD(self.Mid_MV302_AutoInp, self.IO.MV302, self.hmimv302auto, self.hmimv302reset)
		if self.hmimv302status_upd!= -99:
			self.hmimv302status = self.hmimv302status_upd

		# self.MV303_FB.MV_FBD(self.Mid_MV303_AutoInp, self.IO.MV303, HMI.MV303)
		self.hmimv303status_upd, self.hmimv303avl = self.MV303_FB.MV_FBD(self.Mid_MV303_AutoInp, self.IO.MV303, self.hmimv303auto, self.hmimv303reset)
		if self.hmimv303status_upd!= -99:
			self.hmimv303status = self.hmimv303status_upd

		# self.MV304_FB.MV_FBD(self.Mid_MV304_AutoInp, self.IO.MV304, HMI.MV304)
		self.hmimv304status_upd, self.hmimv304avl = self.MV304_FB.MV_FBD(self.Mid_MV304_AutoInp, self.IO.MV304, self.hmimv304auto, self.hmimv304reset)
		if self.hmimv304status_upd!= -99:
			self.hmimv304status = self.hmimv304status_upd

		############# Physical process simulation code ################
		self.Actuator()
		self.Plant()

		############# Physical process simulation ends here ###########

		####### setdata() calls start here ###############
		# if self.hmiplantreseton:

		setdata(self, 'HMI.MV301.Reset',SCADA_ADDR,self.hmimv301reset)
		setdata(self, 'HMI.MV302.Reset',SCADA_ADDR,self.hmimv302reset)
		setdata(self, 'HMI.MV303.Reset',SCADA_ADDR,self.hmimv303reset)
		setdata(self, 'HMI.MV304.Reset',SCADA_ADDR,self.hmimv304reset)
		setdata(self, 'HMI.P301.Reset',SCADA_ADDR,self.hmip301reset)
		setdata(self, 'HMI.P302.Reset',SCADA_ADDR,self.hmip302reset)

		# if self.hmiplantautoon:
		setdata(self, 'HMI.MV301.Auto',SCADA_ADDR,self.hmimv301auto)
		setdata(self, 'HMI.MV302.Auto',SCADA_ADDR,self.hmimv302auto)
		setdata(self, 'HMI.MV303.Auto',SCADA_ADDR,self.hmimv303auto)
		setdata(self, 'HMI.MV304.Auto',SCADA_ADDR,self.hmimv304auto)
		setdata(self, 'HMI.P301.Auto',SCADA_ADDR,self.hmip301auto)
		setdata(self, 'HMI.P302.Auto',SCADA_ADDR,self.hmip302auto)

		# if self.hmiplantautooff:
		# 	setdata(self, 'HMI.MV301.Auto',SCADA_ADDR,0)
		# 	setdata(self, 'HMI.MV302.Auto',SCADA_ADDR,0)
		# 	setdata(self, 'HMI.MV303.Auto',SCADA_ADDR,0)
		# 	setdata(self, 'HMI.MV304.Auto',SCADA_ADDR,0)
		# 	setdata(self, 'HMI.P301.Auto',SCADA_ADDR,0)
		# 	setdata(self, 'HMI.P302.Auto',SCADA_ADDR,0)
		setdata(self, 'HMI.P3.Permissive_On',SCADA_ADDR,self.hmip3permissiveon)

		setdata(self, 'HMI.P301.Permissive',SCADA_ADDR,self.hmip301permissive)
		setdata(self, 'HMI.P301.MSG_Permissive',SCADA_ADDR,self.hmip301msgpermissive)
		setdata(self, 'HMI.P302.Permissive',SCADA_ADDR,self.hmip302permissive)
		setdata(self, 'HMI.P302.MSG_Permissive',SCADA_ADDR,self.hmip302msgpermissive)
		setdata(self, 'HMI.P301.SD',SCADA_ADDR,self.hmip301sd)
		setdata(self, 'HMI.P301.MSG_Shutdown',SCADA_ADDR,self.hmip301msgshutdown)
		setdata(self, 'HMI.P302.SD',SCADA_ADDR,self.hmip302sd)
		setdata(self, 'HMI.P302.MSG_Shutdown',SCADA_ADDR,self.hmip302msgshutdown)
		# if self.hmiplantstop or self.hmiplantcriticalsdon:
		setdata(self, 'HMI.P3.Shutdown',SCADA_ADDR,1)
		if self.hmidpit301hty:
			setdata(self, 'HMI.PLANT.TMP_High',SCADA_ADDR,self.hmidpit301ah)
		else:
			setdata(self, 'HMI.PLANT.TMP_High',SCADA_ADDR,self.hmidpsh301alarm)
		if self.hmilit401ah and self.hmip3state > 1:
			setdata(self, 'HMI.P3.State',SCADA_ADDR,self.hmip3state)
		if self.hmip3state_prev == 1:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.P3.Shutdown',SCADA_ADDR,0)
			if self.hmip3state == 2:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,2)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 2:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if  self.hmip3state == 3:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,3)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 3:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if  self.hmip3state == 4:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,4)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 4:
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if Sec_P:
				setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,self.hmicyp3ufrefillsec)
			if self.hmip3state == 5:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,5)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 5:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 6:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,6)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 6:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 7:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,7)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 7:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			# setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 8:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,8)
				self.hmip3state_prev = 0
			else:
				if Min_P:
					setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,self.hmicyp3uffiltrationmin)
			if self.hmip3state == 8:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,8)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 8:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 9:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,9)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 9:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 1:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,1)
				self.hmip3state_prev = 0
			elif self.hmip3state == 10:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,10)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 10:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 11:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,11)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 11:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 12:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,12)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 12:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			# setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if Sec_P:
				setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,self.hmicyp3backwashsec)
			if self.hmip3state == 13:
				setdata(self, 'HMI.Cy_P3.BW_CNT',SCADA_ADDR,self.hmicyp3bwcnt)
				setdata(self, 'HMI.P3.State',SCADA_ADDR,13)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 13:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 14:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,14)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 14:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 15:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,15)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 15:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 16:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,16)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 16:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			if Sec_P:
				setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,self.hmicyp3drainsec)
			if self.hmip3state == 4:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,4)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 17:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 18:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,18)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 18:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if Sec_P:
				setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,self.hmicyp3cipcleaningsec)
			if self.hmip3state == 19:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,19)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 19:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			# setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 14:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,14)
				self.hmip3state_prev = 0
		if self.hmip3state_prev == 99:
			setdata(self, 'HMI.Cy_P3.UF_REFILL_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.UF_FILTRATION_MIN',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.BACKWASH_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.CIP_CLEANING_SEC',SCADA_ADDR,0)
			setdata(self, 'HMI.Cy_P3.DRAIN_SEC',SCADA_ADDR,0)
			if self.hmip3state == 1:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,1)
				self.hmip3state_prev = 0
			if self.hmip3state == 2:
				setdata(self, 'HMI.P3.State',SCADA_ADDR,2)
				self.hmip3state_prev = 0
		if self.hmip3state_prev > 19 and self.hmip3state_prev != 99:
			setdata(self, 'HMI.P3.State',SCADA_ADDR,1)
			self.hmip3state_prev = 0	

		setdata(self, 'HMI.Mid_P602_AutoInp',SCADA_ADDR,self.Mid_P602_AutoInp)
		setdata(self, 'HMI.P_UF_FEED_DUTY.Both_Pmp_Not_Avl',SCADA_ADDR,self.hmiufbothpmpnotavl)
		setdata(self, 'HMI.P_UF_FEED_DUTY.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hmiufselectedpmpnotavl)
		setdata(self, 'HMI.P_UF_FEED_DUTY.Pump_Running',SCADA_ADDR,self.hmiufpumprunning)

		setdata(self, 'HMI.P301.Status',SCADA_ADDR,self.hmip301status)
		setdata(self, 'HMI.P301.Fault',SCADA_ADDR,self.hmip301fault)
		setdata(self, 'HMI.P301.Avl',SCADA_ADDR,self.hmip301avl)
		setdata(self, 'HMI.P301.Shutdown',SCADA_ADDR,self.hmip301shutdown)
		setdata(self, 'HMI.P302.Status',SCADA_ADDR,self.hmip302status)
		setdata(self, 'HMI.P302.Fault',SCADA_ADDR,self.hmip302fault)
		setdata(self, 'HMI.P302.Avl',SCADA_ADDR,self.hmip302avl)
		setdata(self, 'HMI.P302.Shutdown',SCADA_ADDR,self.hmip302shutdown)
		# setdata(self, 'HMI.PSH301.Alarm',SCADA_ADDR,self.hmipsh301alarm)
		# setdata(self, 'HMI.DPSH301.Alarm',SCADA_ADDR,self.hmidpsh301alarm)
		setdata(self, 'HMI.MV301.Status',SCADA_ADDR,self.hmimv301status)
		setdata(self, 'HMI.MV301.Avl',SCADA_ADDR,self.hmimv301avl)
		setdata(self, 'HMI.MV302.Status',SCADA_ADDR,self.hmimv302status)
		setdata(self, 'HMI.MV302.Avl',SCADA_ADDR,self.hmimv302avl)
		setdata(self, 'HMI.MV303.Status',SCADA_ADDR,self.hmimv303status)
		setdata(self, 'HMI.MV303.Avl',SCADA_ADDR,self.hmimv303avl)
		setdata(self, 'HMI.MV304.Status',SCADA_ADDR,self.hmimv304status)
		setdata(self, 'HMI.MV304.Avl',SCADA_ADDR,self.hmimv304avl)
		setdata(self, 'HMI.LIT301.Pv',SCADA_ADDR,self.hmilit301pv)
		setdata(self, 'HMI.LIT301.AHH',SCADA_ADDR,self.hmilit301ahh)
		setdata(self, 'HMI.LIT301.AH',SCADA_ADDR,self.hmilit301ah)
		setdata(self, 'HMI.LIT301.AL',SCADA_ADDR,self.hmilit301al)
		setdata(self, 'HMI.LIT301.ALL',SCADA_ADDR,self.hmilit301all)

		####### setdata() calls end here ###############

		# print("PLC3 Debug: self.Mid_P_UF_FEED_DUTY_AutoInp,self.hmip301avl,self.hmip301sd_arr, self.hmip301status_upd, self.P_UF_FEED_DUTY_FB.Start_Pmp1, self.IO.P301, self.hmip301auto, self.hmip301reset, self.hmip301permissive, self.hmip301sd, self.hmimv302status, self.hmimv304status, self.hmimv201open, self.hmip101status, self.IO.P301.DI_Run, self.IO.P302.DI_Run:", self.Mid_P_UF_FEED_DUTY_AutoInp, self.hmip301avl,self.hmip301sd_arr,self.hmip301status_upd,self.P_UF_FEED_DUTY_FB.Start_Pmp1, self.IO.P301, self.hmip301auto, self.hmip301reset, self.hmip301permissive, self.hmip301sd, self.hmimv302status, self.hmimv304status, self.hmimv201open, self.hmip101status, self.IO.P301.DI_Run, self.IO.P302.DI_Run)
		# print("PLC3 Debug: self.hmip301status_upd, self.P_UF_FEED_DUTY_FB.Start_Pmp1, self.IO.P301, self.hmip301auto, self.hmip301reset, self.hmip301permissive, self.hmip301sd: ",self.hmip301status_upd,self.P_UF_FEED_DUTY_FB.Start_Pmp1, self.IO.P301, self.hmip301auto, self.hmip301reset, self.hmip301permissive, self.hmip301sd)



	def _launch_next(self,counter):
		# Schedule the next call

		threading.Timer(interval, self._launch_next, args=(counter+1,)).start()
		# Launch network_function in a thread
		t = threading.Thread(target=self.Iteration, args=(counter,))
		t.daemon = True
		t.start()

	def Pre_Main_UF_Feed(self,IO):
	# def main_loop(self):
		self.IO = IO
		self.result=[890] # original value: 890
		counter = 0
		self._launch_next(counter)
		while True:
			time.sleep(1)
