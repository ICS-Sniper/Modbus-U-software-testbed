# this is the PLC 4 logic, it's about the very same thing as that in the real plc.
###### Existing emulator libraries ################
from devices import PLC
from utils import SCADA_ADDR, SCADA_TAGS
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

class plc4(PLC):
	'plc4 logic'


	def pre_loop(self):

		### Initialization block #######
		self.k = 0

		self.hmiait402ah = 0
		self.hmiait402al = 0
		self.hmifit401all = 0
		self.hmilit401all = 0
		self.hmils401alarm = 0
		self.hmimv501status = 1
		self.hmimv502status = 1
		self.hmimv503status = 1
		self.hmimv504status = 1
		self.hmip401auto = 1
		self.hmip401avl = 1
		self.hmip401fault = 0
		self.hmip401msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip401msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip401permissive = bit_2_signed_integer([1]*16)
		self.hmip401reset = 0
		self.hmip401sd = bit_2_signed_integer([0]*16)
		self.hmip401shutdown = bit_2_signed_integer([0]*16)
		self.hmip401status = 1
		self.hmip401status_upd = 0
		self.hmip402auto = 1
		self.hmip402avl = 1
		self.hmip402fault = 0
		self.hmip402msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip402msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip402permissive = bit_2_signed_integer([1]*16)
		self.hmip402reset = 0
		self.hmip402sd = bit_2_signed_integer([0]*16)
		self.hmip402shutdown = bit_2_signed_integer([0]*16)
		self.hmip402status = 1
		self.hmip402status_upd = 0
		self.hmip403auto = 1
		self.hmip403avl = 1
		self.hmip403fault = 0
		self.hmip403msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip403msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip403permissive = bit_2_signed_integer([1]*16)
		self.hmip403reset = 0
		self.hmip403sd = bit_2_signed_integer([0]*16)
		self.hmip403shutdown = bit_2_signed_integer([0]*16)
		self.hmip403status = 1
		self.hmip403status_upd = 0
		self.hmip404auto = 1
		self.hmip404avl = 1
		self.hmip404fault = 0
		self.hmip404msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip404msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip404permissive = bit_2_signed_integer([1]*16)
		self.hmip404reset = 0
		self.hmip404sd = bit_2_signed_integer([0]*16)
		self.hmip404shutdown = bit_2_signed_integer([0]*16)
		self.hmip404status = 1
		self.hmip404status_upd = 0
		self.hmip4permissiveon = 1
		self.hmip4state = 1
		self.hmiplantautooff = 0
		self.hmiplantautoon = 1
		self.hmiplantreseton =1
		self.hmiplantstart =0
		self.hmipnahso3orpduty = 1
		self.hmipnahso3orpdutybothpmpnotavl = 0
		self.hmipnahso3orpdutyselectedpmpnotavl = 0
		self.hmipnahso3orpdutyselectedpmpnotavl_upd = 0
		self.hmiprofeedduty = 1
		self.hmiprofeeddutybothpmpnotavl = 0
		self.hmiprofeeddutyselectedpmpnotavl = 0
		self.hmiprofeeddutyselectedpmpnotavl_upd = 0
		self.hmirohppsdon = 0
		self.hmiuv401auto = 1
		self.hmiuv401avl = 1
		self.hmiuv401avl_upd = 0
		self.hmiuv401fault = 0
		self.hmiuv401fault_upd = 0
		self.hmiuv401msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmiuv401msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmiuv401permissive = bit_2_signed_integer([1]*16)
		self.hmiuv401reset = 1
		self.hmiuv401resetrunhr = 0
		self.hmiuv401runhr = 0
		self.hmiuv401runhr_upd = 0
		self.hmiuv401sd = bit_2_signed_integer([0]*16)
		self.hmiuv401shutdown = bit_2_signed_integer([0]*16)
		self.hmiuv401shutdown_upd = 0
		self.hmiuv401status = 1
		self.hmiuv401status_upd = 0
		self.hmiuv401totalrunhr = 0
		self.hmiuv401totalrunhr_upd = 0
		self.hmilit401hty = 1
		self.hmilit401ahh = 0
		self.hmilit401ah = 0
		self.hmilit401al = 0
		self.hmilit401all = 0
		self.hmiait401hty = 1
		self.hmiait401ahh = 0
		self.hmiait401ah = 0
		self.hmiait401al = 0
		self.hmiait401all = 0
		self.hmiait402ah = 0
		self.hmiait402ahh = 0
		self.hmiait402al = 0
		self.hmiait402all = 0
		self.hmiait402hty = 1
		self.hmifit401ah = 0
		self.hmifit401ahh = 0
		self.hmifit401al = 0
		self.hmifit401all = 0
		self.hmifit401hty = 1
		self.hmipsh401delay = bit_2_signed_integer([0]*16)
		self.hmipnahso3orpdutypumprunning = 0
		self.hmiprofeeddutypumprunning = 0
		self.hmip301status = 1
		self.hmip302status = 1
		self.hmimv301close = 0
		self.hmimv302close = 0
		self.hmimv303close = 0
		self.hmimv304open = 0
		self.hmip602status = 1
		self.hmimv302open = 0
		self.hmimv304close = 0
		self.hmip4state_prev = 0


		self.Mid_UV401_AutoInp = self.hmiuv401status-1
		self.Mid_P_NAHSO3_ORP_DUTY_AutoInp = self.hmip401status-1
		self.Mid_FIT401_Tot_Enb = 0
		self.TON_FIT401_TM = TONR(6,"FIT401")
		self.TON_FIT401_P1_TM = TONR(6,"FIT401_p1")
		self.TON_FIT401_P2_TM = TONR(6,"FIT401_p2")
		self.Mid_P_RO_FEED_DUTY_AutoInp = 1
		self.Mid_P_NAHSO3_ORP_DUTY_AutoInp = 0

		self.LIT401_FB = AIN_FBD(self.hmilit401hty,self.hmilit401ahh,self.hmilit401ah,self.hmilit401al,self.hmilit401all)
		self.P_RO_FEED_DUTY_FB = Duty2_FBD()
		self.P401_FB = PMP_FBD(self.hmip401avl,self.hmip401fault,self.hmip401shutdown)
		self.P402_FB = PMP_FBD(self.hmip402avl,self.hmip402fault,self.hmip402shutdown)
		self.AIT401_FB = AIN_FBD(self.hmiait401hty,self.hmiait401ahh,self.hmiait401ah,self.hmiait401al,self.hmiait401all)
		self.FIT401_FB = FIT_FBD(self.hmifit401hty,self.hmifit401ahh,self.hmifit401ah,self.hmifit401al,self.hmifit401all)
		self.UV401_FB = UV_FBD(self.hmiuv401avl,self.hmiuv401runhr,0)
		self.AIT402_FB = AIN_FBD(self.hmiait402hty,self.hmiait402ahh,self.hmiait402ah,self.hmiait402al,self.hmiait402all)
		self.LS401_FB = SWITCH_FBD(self.hmipsh401delay)

		self.P_NAHSO3_ORP_DUTY_FB = Duty2_FBD()
		self.P403_FB = PMP_FBD(self.hmip403avl,self.hmip403fault,self.hmip403shutdown)
		self.P404_FB = PMP_FBD(self.hmip404avl,self.hmip404fault,self.hmip404shutdown)

		################## multiprocessing manager ###########
		manager = multiprocessing.Manager()
		self.shared = manager.dict({
            "hmiplantreseton": self.hmiplantreseton,
            "hmiplantautoon": self.hmiplantautoon,
            "hmiplantautooff": self.hmiplantautooff,
			"hmiplantstart": self.hmiplantstart,
			"hmimv501status": self.hmimv501status,
			"hmimv502status": self.hmimv502status,
			"hmimv503status": self.hmimv503status,
			"hmimv504status": self.hmimv504status,
			"hmip301status": self.hmip301status,
			"hmip302status": self.hmip302status,
			"hmimv301close": self.hmimv301close,
			"hmimv302close": self.hmimv302close,
			"hmimv303close": self.hmimv303close,
			"hmimv304open": self.hmimv304open,
			"hmip602status": self.hmip602status,
			"hmimv302open": self.hmimv302open,
			"hmimv304close": self.hmimv304close,
        })

		#######################################################

		time.sleep(10)
		print ("	PLC4 started\n")

	def fetchData(self, state):
		self.shared["hmimv501status"] = getdata(self, 'HMI.MV501.Status',SCADA_ADDR,self.shared["hmimv501status"])
		self.shared["hmimv502status"] = getdata(self, 'HMI.MV502.Status',SCADA_ADDR,self.shared["hmimv502status"])
		self.shared["hmimv503status"] = getdata(self, 'HMI.MV503.Status',SCADA_ADDR,self.shared["hmimv503status"])
		self.shared["hmimv504status"] = getdata(self, 'HMI.MV504.Status',SCADA_ADDR,self.shared["hmimv504status"])
		self.shared["hmiplantreseton"] = getdata(self, 'HMI.PLANT.Reset_On',SCADA_ADDR,self.shared["hmiplantreseton"])
		self.shared["hmiplantautoon"] = getdata(self, 'HMI.PLANT.Auto_On',SCADA_ADDR,self.shared["hmiplantautoon"])
		self.shared["hmiplantautooff"] = getdata(self, 'HMI.PLANT.Auto_Off',SCADA_ADDR,self.shared["hmiplantautooff"])
		self.shared["hmip301status"] = getdata(self, 'HMI.P301.Status',SCADA_ADDR,self.shared["hmip301status"])
		self.shared["hmip302status"] = getdata(self, 'HMI.P302.Status',SCADA_ADDR,self.shared["hmip302status"])
		self.shared["hmimv301close"] = getdata(self, 'HMI.MV301.Close',SCADA_ADDR,self.shared["hmimv301close"])
		self.shared["hmimv302close"] = getdata(self, 'HMI.MV302.Close',SCADA_ADDR,self.shared["hmimv302close"])
		self.shared["hmimv303close"] = getdata(self, 'HMI.MV303.Close',SCADA_ADDR,self.shared["hmimv303close"])
		self.shared["hmimv304open"] = getdata(self, 'HMI.MV304.Open',SCADA_ADDR,self.shared["hmimv304open"])
		self.shared["hmip602status"] = getdata(self, 'HMI.P602.Status',SCADA_ADDR,self.shared["hmip602status"])
		self.shared["hmimv302open"] = getdata(self, 'HMI.MV302.Open',SCADA_ADDR,self.shared["hmimv302open"])
		self.shared["hmimv304close"] = getdata(self, 'HMI.MV304.Close',SCADA_ADDR,self.shared["hmimv304close"])
		if state == 1:
			self.shared["hmiplantstart"] = getdata(self, 'HMI.PLANT.Start',SCADA_ADDR,self.shared["hmiplantstart"])


	def Actuator(self):
		self.IO.P401.DI_Run = self.IO.P401.DO_Start
		self.IO.P402.DI_Run = self.IO.P402.DO_Start

	def Plant(self):
		self.h_t401=0
		self.p = {"f_mv101":2.3*1000000000/3600,"S_t101":1.5*1000000,"S_t301":1.5*1000000,"S_t401":1.5*1000000,"S_t601":1.5*1000000,"S_t601":1.5*1000000,"S_t602":1.5*1000000,"f_p101":2.0*1000000000/3600,"f_mv201":2.0*1000000000/3600,"f_p301":2.0*1000000000/3600,"f_mv302":2.0*1000000000/3600,"f_p602":2.0*1000000000/3600,"f_p401":2.0*1000000000/36001,"f_mv501":2.0*1000000000/3600,"f_mv502":0.00006111,"f_mv503":0.00049,"f_p601":2.0*1000000000/36001,"LIT101_AL":0.2,"LIT101_AH":0.8,"LIT301_AL":0.2,"LIT301_AH":0.8,"LIT401_AL":0.2,"LIT401_AH":0.8,"LIT601_AL":0.2,"LIT601_AH":0.8,"LIT602_AL":0.2,"LIT602_AH":0.8,"cond_AIT201_AL":250,"cond_AIT201_AH":260,"ph_AIT202_AL":6.95,"ph_AIT202_AH":7.05,"orp_AIT203_AL":420,"orp_AIT203_AH":500,"cond_AIT503_AH":260,"h201_AL":50,"h202_AL":4,"h203_AL":15,"cond_AIT503_AL":250,"cond_AIT503_AH":260,"orp_AIT402_AL":420,"orp_AIT402_AH":500,"omega_inlet":0.001}  # critical plant parameters

		if self.hmip301status == 2 or self.hmip302status == 2 and self.hmimv301close==1 and  self.hmimv302close==1 and self.hmimv303close==1 and self.hmimv304open==1 and self.hmip602status == 1: #UF flushing procedure, 30 sec
			pass
		if self.hmip301status == 2 or self.hmip302status == 2 and self.hmimv301close==1 and  self.hmimv302open==1 and self.hmimv303close==1 and self.hmimv304close==1 and self.hmip602status == 1:   #UF ultra filtration procedure, 30 min
			self.h_t401=self.h_t401+ self.p['f_mv302'] / self.p['S_t401']

		if self.IO.P401.DI_Run == 1 or self.IO.P402.DI_Run == 1: #P401, drawing water from t401
			self.h_t401=self.h_t401- self.p['f_p401'] / self.p['S_t401']

		self.hmilit401pv=self.result[self.k]
		# setdata(self, 'HMI.LIT401.Pv',SCADA_ADDR,self.hmilit401pv)

        # HMI.LIT401.set_alarm()
		if type(self.hmilit401pv) != type('a'):
			self.hmilit401ahh, self.hmilit401ah, self.hmilit401al, self.hmilit401all = ALM(self.hmilit401pv, 1200, 1000, 800, 250)

			# setdata(self, 'HMI.LIT401.AHH',SCADA_ADDR,self.hmilit401ahh)
			# setdata(self, 'HMI.LIT401.AH',SCADA_ADDR,self.hmilit401ah)
			# setdata(self, 'HMI.LIT401.AL',SCADA_ADDR,self.hmilit401al)
			# setdata(self, 'HMI.LIT401.ALL',SCADA_ADDR,self.hmilit401all)

		self.result.append(self.result[self.k]+self.h_t401*time_interval)

		self.k = self.k + 1

	# def Pre_Main_RO_Feed_Dosing(self, IO,HMI):
	def Iteration(self):
		p = multiprocessing.Process(target=self.fetchData, args=(self.hmip4state,))
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
		self.hmiplantstart = self.shared["hmiplantstart"]
		self.hmimv501status = self.shared["hmimv501status"]
		self.hmimv502status = self.shared["hmimv502status"]
		self.hmimv503status = self.shared["hmimv503status"]
		self.hmimv504status = self.shared["hmimv504status"]
		self.hmip301status = self.shared["hmip301status"]
		self.hmip302status = self.shared["hmip302status"]
		self.hmimv301close = self.shared["hmimv301close"]
		self.hmimv302close = self.shared["hmimv302close"]
		self.hmimv303close = self.shared["hmimv303close"]
		self.hmimv304open = self.shared["hmimv304open"]
		self.hmip602status = self.shared["hmip602status"]
		self.hmimv302open = self.shared["hmimv302open"]
		self.hmimv304close = self.shared["hmimv304close"]

		print("PLC4 State:", self.hmip4state)


		if self.hmiplantreseton:
			# setdata(self, 'HMI.P401.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P402.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P403.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.P404.Reset',SCADA_ADDR,1)
			# setdata(self, 'HMI.UV401.Reset',SCADA_ADDR,1)
			self.hmip401reset =1
			self.hmip402reset	=1
			self.hmip403reset	=1
			self.hmip404reset =1
			self.hmiuv401reset	=1

		if self.hmiplantautoon:
			# setdata(self, 'HMI.P401.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P402.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P403.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.P404.Auto',SCADA_ADDR,1)
			# setdata(self, 'HMI.UV401.Auto',SCADA_ADDR,1)
			self.hmip401auto =1
			self.hmip402auto	=1
			self.hmip403auto	=1
			self.hmip404auto =1
			self.hmiuv401auto	=1

		if self.hmiplantautooff:
			# setdata(self, 'HMI.P401.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P402.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P403.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.P404.Auto',SCADA_ADDR,0)
			# setdata(self, 'HMI.UV401.Auto',SCADA_ADDR,0)
			self.hmip401auto =0
			self.hmip402auto	=0
			self.hmip403auto	=0
			self.hmip404auto =0
			self.hmiuv401auto	=0


		# HMI.P4.Permissive_On= (HMI.P401.Avl or HMI.P402.Avl) and (HMI.P403.Avl or HMI.P404.Avl) and HMI.UV401.Avl
		# setdata(self, 'HMI.P4.Permissive_On',SCADA_ADDR,(self.hmip401avl or self.hmip402avl) and (self.hmip403avl or self.hmip404avl) and self.hmiuv401avl)
		self.hmip4permissiveon = (self.hmip401avl or self.hmip402avl) and (self.hmip403avl or self.hmip404avl) and self.hmiuv401avl

		self.Mid_FIT401_Tot_Enb	= self.hmip401status==2 or self.hmip402status==2

		self.TON_FIT401_TM.TONR((self.hmip401status==2 or self.hmip402status==2)and self.hmifit401all)
		self.TON_FIT401_P1_TM.TONR(self.hmifit401all and self.hmip401status == 2)
		self.TON_FIT401_P2_TM.TONR(self.hmifit401all and self.hmip402status == 2)

		self.hmip401permissive_arr = signed_integer_2_bit(self.hmip401permissive)
		self.hmip401permissive_arr[0] 	= int(not self.hmilit401all)
		self.hmip401permissive_arr[1] 	= int(self.hmimv501status==2 or self.hmimv502status==2 or self.hmimv503status==2 or self.hmimv504status==2)
		self.hmip401permissive = bit_2_signed_integer(self.hmip401permissive_arr)
		# setdata(self, 'HMI.P401.Permissive',SCADA_ADDR,self.hmip401permissive)

		self.hmip401msgpermissive_arr = signed_integer_2_bit(self.hmip401msgpermissive)
		self.hmip401msgpermissive_arr[1] = self.hmip401permissive_arr[0]
		self.hmip401msgpermissive_arr[2] = 0
		self.hmip401msgpermissive = bit_2_signed_integer(self.hmip401msgpermissive_arr)
		# setdata(self, 'HMI.P401.MSG_Permissive',SCADA_ADDR,self.hmip401msgpermissive)

		self.hmip402permissive_arr = signed_integer_2_bit(self.hmip402permissive)
		self.hmip402permissive_arr[0] 	= int(not self.hmilit401all)
		self.hmip402permissive_arr[1] 	= int(self.hmimv501status==2 or self.hmimv502status==2 or self.hmimv503status==2 or self.hmimv504status==2)
		self.hmip402permissive = bit_2_signed_integer(self.hmip402permissive_arr)
		# setdata(self, 'HMI.P402.Permissive',SCADA_ADDR,self.hmip402permissive)

		self.hmip402msgpermissive_arr = signed_integer_2_bit(self.hmip402msgpermissive)
		self.hmip402msgpermissive_arr[1] = self.hmip402permissive_arr[0]
		self.hmip402msgpermissive = bit_2_signed_integer(self.hmip402msgpermissive_arr)
		# setdata(self, 'HMI.P402.MSG_Permissive',SCADA_ADDR,self.hmip402msgpermissive)

		self.hmip403permissive_arr = signed_integer_2_bit(self.hmip403permissive)
		self.hmip403permissive_arr[0] 	= int(not self.hmils401alarm)
		self.hmip403permissive_arr[1]	= int(self.hmip401status==2 or self.hmip402status==2)
		self.hmip403permissive = bit_2_signed_integer(self.hmip403permissive_arr)
		# setdata(self, 'HMI.P403.Permissive',SCADA_ADDR,self.hmip403permissive)

		self.hmip403msgpermissive_arr = signed_integer_2_bit(self.hmip403msgpermissive)
		self.hmip403msgpermissive_arr[1] = self.hmip403permissive_arr[0]
		self.hmip403msgpermissive_arr[2] = self.hmip403permissive_arr[1]
		self.hmip403msgpermissive = bit_2_signed_integer(self.hmip403msgpermissive_arr)
		# setdata(self, 'HMI.P403.MSG_Permissive',SCADA_ADDR,self.hmip403msgpermissive)
		# HMI.P403.MSG_Permissive[1] = HMI.P403.Permissive[0]
		# HMI.P403.MSG_Permissive[2] = HMI.P403.Permissive[1]

		self.hmip404permissive_arr = signed_integer_2_bit(self.hmip404permissive)
		self.hmip404permissive_arr[0] 	= int(not self.hmils401alarm)
		self.hmip404permissive_arr[1]	= int(self.hmip401status==2 or self.hmip402status==2)
		self.hmip404permissive = bit_2_signed_integer(self.hmip404permissive_arr)
		# setdata(self, 'HMI.P404.Permissive',SCADA_ADDR,self.hmip404permissive)
		# HMI.P404.Permissive[0] 	= not HMI.LS401.Alarm
		# HMI.P404.Permissive[1] 	= HMI.P401.Status==2 or HMI.P402.Status==2

		self.hmip404msgpermissive_arr = signed_integer_2_bit(self.hmip404msgpermissive)
		self.hmip404msgpermissive_arr[1] = self.hmip404permissive_arr[0]
		self.hmip404msgpermissive_arr[2] = self.hmip404permissive_arr[1]
		self.hmip404msgpermissive = bit_2_signed_integer(self.hmip404msgpermissive_arr)
		# setdata(self, 'HMI.P404.MSG_Permissive',SCADA_ADDR,self.hmip404msgpermissive)
		# HMI.P404.MSG_Permissive[1] = HMI.P404.Permissive[0]
		# HMI.P404.MSG_Permissive[2] = HMI.P404.Permissive[1]

		self.hmiuv401permissive_arr = signed_integer_2_bit(self.hmiuv401permissive)
		self.hmiuv401permissive_arr[0] 	= int(self.hmip401status==2 or self.hmip402status==2)
		self.hmiuv401permissive_arr[1]	= self.hmifit401all
		self.hmiuv401permissive = bit_2_signed_integer(self.hmiuv401permissive_arr)
		# setdata(self, 'HMI.UV401.Permissive',SCADA_ADDR,self.hmiuv401permissive)
		# HMI.UV401.Permissive[0] 	= HMI.P401.Status==2 or HMI.P402.Status==2
		# HMI.UV401.Permissive[1] 	= not HMI.FIT401.ALL

		self.hmiuv401msgpermissive_arr = signed_integer_2_bit(self.hmiuv401msgpermissive)
		self.hmiuv401msgpermissive_arr[1] = self.hmip403permissive_arr[0]
		self.hmiuv401msgpermissive_arr[2] = self.hmip403permissive_arr[1]
		self.hmiuv401msgpermissive = bit_2_signed_integer(self.hmiuv401msgpermissive_arr)
		# setdata(self, 'HMI.UV401.MSG_Permissive',SCADA_ADDR,self.hmiuv401msgpermissive)
		# HMI.UV401.MSG_Permissive[1] = HMI.P403.Permissive[0]
		# HMI.UV401.MSG_Permissive[2] = HMI.P403.Permissive[1]

		self.hmip401sd_arr = signed_integer_2_bit(self.hmip401sd)
		self.hmip401sd_arr[0] = int(self.hmilit401all)
		self.hmip401sd_arr[1] = int(self.TON_FIT401_P1_TM.DN)
		self.hmip401sd_arr[2] = int(self.hmip401status==2 and self.hmimv501status!=2 and self.hmimv502status!=2 and self.hmimv503status!=2 and self.hmimv504status!=2)
		self.hmip401sd = bit_2_signed_integer(self.hmip401sd_arr)
		# setdata(self, 'HMI.P401.SD',SCADA_ADDR,self.hmip401sd)
		# HMI.P401.SD[0]	= HMI.LIT401.ALL
		# HMI.P401.SD[1]	= self.TON_FIT401_P1_TM.DN
		# HMI.P401.SD[2]	= HMI.P401.Status==2 and HMI.MV501.Status!=2 and HMI.MV502.Status!=2 and HMI.MV503.Status!=2 and HMI.MV504.Status!=2

		self.hmip401msgshutdown_arr = signed_integer_2_bit(self.hmip401msgshutdown)
		self.hmip401shutdown_arr = signed_integer_2_bit(self.hmip401shutdown)
		self.hmip401msgshutdown_arr[1] = self.hmip401shutdown_arr[0]
		self.hmip401msgshutdown_arr[2] = self.hmip401shutdown_arr[1]
		self.hmip401msgshutdown_arr[3] = self.hmip401shutdown_arr[2]
		self.hmip401msgshutdown_arr[4] = self.hmip401shutdown_arr[3]
		self.hmip401msgshutdown_arr[5] = self.hmip401shutdown_arr[4]
		self.hmip401msgshutdown = bit_2_signed_integer(self.hmip401msgshutdown_arr)
		# setdata(self, 'HMI.P401.MSG_Shutdown',SCADA_ADDR,self.hmip401msgshutdown)

		self.hmip402sd_arr = signed_integer_2_bit(self.hmip402sd)
		self.hmip402sd_arr[0] = int(self.hmilit401all)
		self.hmip402sd_arr[1] = int(self.TON_FIT401_P2_TM.DN)
		self.hmip402sd_arr[2] = int(self.hmip402status==2 and self.hmimv501status!=2 and self.hmimv502status!=2 and self.hmimv503status!=2 and self.hmimv504status!=2)
		self.hmip402sd = bit_2_signed_integer(self.hmip402sd_arr)
		# setdata(self, 'HMI.P402.SD',SCADA_ADDR,self.hmip402sd)
		# HMI.P402.SD[0] 	= HMI.LIT401.ALL
		# HMI.P402.SD[1] 	= self.TON_FIT401_P2_TM.DN
		# HMI.P402.SD[2] 	= HMI.P402.Status==2 and HMI.MV501.Status!=2 and HMI.MV502.Status!=2 and HMI.MV503.Status!=2 and HMI.MV504.Status!=2

		self.hmip402msgshutdown_arr = signed_integer_2_bit(self.hmip402msgshutdown)
		self.hmip402shutdown_arr = signed_integer_2_bit(self.hmip402shutdown)
		self.hmip402msgshutdown_arr[1] = self.hmip402shutdown_arr[0]
		self.hmip402msgshutdown_arr[2] = self.hmip402shutdown_arr[1]
		self.hmip402msgshutdown_arr[3] = self.hmip402shutdown_arr[2]
		self.hmip402msgshutdown_arr[4] = self.hmip402shutdown_arr[3]
		self.hmip402msgshutdown_arr[5] = self.hmip402shutdown_arr[4]
		self.hmip402msgshutdown = bit_2_signed_integer(self.hmip402msgshutdown_arr)
		# setdata(self, 'HMI.P402.MSG_Shutdown',SCADA_ADDR,self.hmip402msgshutdown)

		self.hmip403sd_arr = signed_integer_2_bit(self.hmip403sd)
		self.hmip403sd_arr[0] = int(self.hmils401alarm)
		self.hmip403sd_arr[1] = int((self.hmip401status==2 or self.hmip402status==2 )and self.hmifit401all)
		self.hmip403sd = bit_2_signed_integer(self.hmip403sd_arr)
		# setdata(self, 'HMI.P403.SD',SCADA_ADDR,self.hmip403sd)
		# HMI.P403.SD[0] 	= HMI.LS401.Alarm
		# HMI.P403.SD[1] 	= (HMI.P401.Status==2 or HMI.P402.Status==2 )and HMI.FIT401.ALL

		self.hmip403msgshutdown_arr = signed_integer_2_bit(self.hmip403msgshutdown)
		self.hmip403shutdown_arr = signed_integer_2_bit(self.hmip403shutdown)
		self.hmip403msgshutdown_arr[1] = self.hmip403shutdown_arr[0]
		self.hmip403msgshutdown_arr[2] = self.hmip403shutdown_arr[1]
		self.hmip403msgshutdown_arr[3] = self.hmip403shutdown_arr[2]
		self.hmip403msgshutdown_arr[4] = self.hmip403shutdown_arr[3]
		self.hmip403msgshutdown_arr[5] = self.hmip403shutdown_arr[4]
		self.hmip403msgshutdown = bit_2_signed_integer(self.hmip403msgshutdown_arr)
		# setdata(self, 'HMI.P403.MSG_Shutdown',SCADA_ADDR,self.hmip403msgshutdown)

		self.hmip404sd_arr = signed_integer_2_bit(self.hmip404sd)
		self.hmip404sd_arr[0] = int(self.hmils401alarm)
		self.hmip404sd_arr[1] = int((self.hmip401status==2 or self.hmip402status==2 )and self.hmifit401all)
		self.hmip404sd = bit_2_signed_integer(self.hmip404sd_arr)
		# setdata(self, 'HMI.P404.SD',SCADA_ADDR,self.hmip404sd)

		self.hmip404msgshutdown_arr = signed_integer_2_bit(self.hmip404msgshutdown)
		self.hmip404shutdown_arr = signed_integer_2_bit(self.hmip404shutdown)
		self.hmip404msgshutdown_arr[1] = self.hmip404shutdown_arr[0]
		self.hmip404msgshutdown_arr[2] = self.hmip404shutdown_arr[1]
		self.hmip404msgshutdown_arr[3] = self.hmip404shutdown_arr[2]
		self.hmip404msgshutdown_arr[4] = self.hmip404shutdown_arr[3]
		self.hmip404msgshutdown_arr[5] = self.hmip404shutdown_arr[4]
		self.hmip404msgshutdown = bit_2_signed_integer(self.hmip404msgshutdown_arr)
		# setdata(self, 'HMI.P404.MSG_Shutdown',SCADA_ADDR,self.hmip404msgshutdown)

		self.hmiuv401sd_arr = signed_integer_2_bit(self.hmiuv401sd)
		self.hmiuv401sd_arr[0] 	= self.TON_FIT401_TM.DN
		self.hmiuv401sd = bit_2_signed_integer(self.hmiuv401sd_arr)
		# setdata(self, 'HMI.UV401.SD',SCADA_ADDR,self.hmiuv401sd)

		self.hmiuv401msgshutdown_arr = signed_integer_2_bit(self.hmiuv401msgshutdown)
		self.hmiuv401shutdown_arr = signed_integer_2_bit(self.hmiuv401shutdown)
		self.hmiuv401msgshutdown_arr[1] = self.hmiuv401shutdown_arr[0]
		self.hmiuv401msgshutdown_arr[2] = self.hmiuv401shutdown_arr[1]
		self.hmiuv401msgshutdown_arr[3] = self.hmiuv401shutdown_arr[2]
		self.hmiuv401msgshutdown_arr[4] = self.hmiuv401shutdown_arr[3]
		self.hmiuv401msgshutdown_arr[5] = self.hmiuv401shutdown_arr[4]
		self.hmiuv401msgshutdown = bit_2_signed_integer(self.hmiuv401msgshutdown_arr)
		# setdata(self, 'HMI.UV401.MSG_Shutdown',SCADA_ADDR,self.hmiuv401msgshutdown)

# Main
		if self.hmip4state == 1:
			self.hmip4state_prev = self.hmip4state
			self.Mid_UV401_AutoInp				=0
			self.Mid_P_RO_FEED_DUTY_AutoInp		=0
			self.Mid_P_NAHSO3_ORP_DUTY_AutoInp	=0
			print("PLC4 Debug:self.hmip4state, self.hmip4permissiveon, self.hmiplantstart", self.hmip4state, self.hmip4permissiveon, self.hmiplantstart)

			if self.hmip4permissiveon and self.hmiplantstart:
				# setdata(self, 'HMI.P4.State',SCADA_ADDR,2)
				self.hmip4state=2


		if self.hmip4state == 2:
			self.hmip4state_prev = self.hmip4state
			self.Mid_UV401_AutoInp				=0
			self.Mid_P_RO_FEED_DUTY_AutoInp		= self.hmimv503status==2 and self.hmimv504status==2
			self.Mid_P_NAHSO3_ORP_DUTY_AutoInp	=0

			if self.hmip401status ==2:
				# setdata(self, 'HMI.P4.State',SCADA_ADDR,3)
				self.hmip4state=3



		if self.hmip4state == 3:
			self.hmip4state_prev = self.hmip4state
			self.Mid_UV401_AutoInp				=1
			self.Mid_P_RO_FEED_DUTY_AutoInp		=1
			self.Mid_P_NAHSO3_ORP_DUTY_AutoInp	=0

			if self.hmiuv401status==2:
				# setdata(self, 'HMI.P4.State',SCADA_ADDR,4)
				self.hmip4state=4


		if self.hmip4state == 4:
			self.hmip4state_prev = self.hmip4state
			self.Mid_UV401_AutoInp				=1
			self.Mid_P_RO_FEED_DUTY_AutoInp		=1

			self.Mid_P_NAHSO3_ORP_DUTY_AutoInp = SETD((self.hmip401status==2 or self.hmip402status==2) and (self.hmiait402ah),(self.hmip401status!=2 and self.hmip402status!=2) or (self.hmiait402al),self.Mid_P_NAHSO3_ORP_DUTY_AutoInp)

			if self.hmirohppsdon: #(shutdown->stopping sequence)
				# setdata(self, 'HMI.P4.State',SCADA_ADDR,5)
				self.hmip4state=5


		if self.hmip4state == 5:
			self.hmip4state_prev = self.hmip4state
			self.Mid_UV401_AutoInp				=1
			self.Mid_P_RO_FEED_DUTY_AutoInp		= self.hmimv503status==1 and self.hmimv504status==1
			self.Mid_P_NAHSO3_ORP_DUTY_AutoInp	= 0

			if not self.hmip401status ==2:
				# setdata(self, 'HMI.P4.State',SCADA_ADDR,6)
				self.hmip4state=6
				# HMI.P4.State=6


		if self.hmip4state == 6:
			self.hmip4state_prev = self.hmip4state
			self.Mid_UV401_AutoInp				=0
			self.Mid_P_RO_FEED_DUTY_AutoInp		=0
			self.Mid_P_NAHSO3_ORP_DUTY_AutoInp	= 0

			if self.hmiuv401status==1:
				# setdata(self, 'HMI.P4.State',SCADA_ADDR,1)
				self.hmip4state=1

		if self.hmip4state > 6:
			# setdata(self, 'HMI.P4.State',SCADA_ADDR,1)
			self.hmip4state=1

# RO_Feed_Dosing
		# self.P_RO_FEED_DUTY_FB.Duty2_FBD(self.Mid_P_RO_FEED_DUTY_AutoInp, HMI.P401, HMI.P402, HMI.P_RO_FEED_DUTY)
		self.hmiprofeeddutybothpmpnotavl, self.hmiprofeeddutyselectedpmpnotavl_upd, self.hmiprofeeddutypumprunning = self.P_RO_FEED_DUTY_FB.Duty2_FBD(self.Mid_P_RO_FEED_DUTY_AutoInp, self.hmip401status, self.hmip401avl, self.hmip402status, self.hmip402avl, self.hmiprofeedduty)
		if self.hmiprofeeddutyselectedpmpnotavl_upd != -99:
			self.hmiprofeeddutyselectedpmpnotavl = self.hmiprofeeddutyselectedpmpnotavl_upd

		# self.P401_FB.PMP_FBD(self.P_RO_FEED_DUTY_FB.Start_Pmp1,self.IO.P401,HMI.P401)
		self.hmip401status_upd, self.hmip401fault, self.hmip401avl, self.hmip401shutdown = self.P401_FB.PMP_FBD(self.P_RO_FEED_DUTY_FB.Start_Pmp1, self.IO.P401, self.hmip401auto, self.hmip401reset, self.hmip401permissive, self.hmip401sd)
		if self.hmip401status_upd != -99:
			self.hmip401status = self.hmip401status_upd

		# self.P402_FB.PMP_FBD(self.P_RO_FEED_DUTY_FB.Start_Pmp2,self.IO.P402,HMI.P402)
		self.hmip402status_upd, self.hmip402fault, self.hmip402avl, self.hmip402shutdown = self.P402_FB.PMP_FBD(self.P_RO_FEED_DUTY_FB.Start_Pmp2, self.IO.P402, self.hmip402auto, self.hmip402reset, self.hmip402permissive, self.hmip402sd)
		if self.hmip402status_upd != -99:
			self.hmip402status = self.hmip402status_upd

		# self.UV401_FB.UV_FBD(self.Mid_UV401_AutoInp, self.IO.UV401, HMI.UV401)
		self.hmiuv401status_upd, self.hmiuv401fault_upd, self.hmiuv401avl_upd, self.hmiuv401runhr_upd, self.hmiuv401totalrunhr_upd, self.hmiuv401shutdown_upd = self.UV401_FB.UV_FBD(self.Mid_UV401_AutoInp, self.IO.UV401, self.hmiuv401auto, self.hmiuv401reset, self.hmiuv401resetrunhr, self.hmiuv401permissive, self.hmiuv401sd)
		if self.hmiuv401status_upd != -99:
			self.hmiuv401status = self.hmiuv401status_upd
		if self.hmiuv401fault_upd != -99:
			self.hmiuv401fault = self.hmiuv401fault_upd
		# if self.hmiuv401remote_upd != -99:
		# 	self.hmiuv401remote = self.hmiuv401remote_upd
		if self.hmiuv401avl_upd != -99:
			self.hmiuv401avl = self.hmiuv401avl_upd
		if self.hmiuv401runhr_upd != -99:
			self.hmiuv401runhr = self.hmiuv401runhr_upd
		if self.hmiuv401totalrunhr_upd != -99:
			self.hmiuv401totalrunhr = self.hmiuv401totalrunhr_upd
		if self.hmiuv401shutdown_upd != -99:
			self.hmiuv401shutdown = self.hmiuv401shutdown_upd


		# self.hmils401alarm =
		self.LS401_FB.SWITCH_FBD(self.IO.LS401)

		# self.P_NAHSO3_ORP_DUTY_FB.Duty2_FBD(self.Mid_P_NAHSO3_ORP_DUTY_AutoInp, HMI.P403, HMI.P404, HMI.P_NAHSO3_ORP_DUTY)
		self.hmipnahso3orpdutybothpmpnotavl, self.hmipnahso3orpdutyselectedpmpnotavl_upd, self.hmipnahso3orpdutypumprunning = self.P_RO_FEED_DUTY_FB.Duty2_FBD(self.Mid_P_NAHSO3_ORP_DUTY_AutoInp, self.hmip403status, self.hmip403avl, self.hmip404status, self.hmip404avl, self.hmipnahso3orpduty)
		if self.hmipnahso3orpdutyselectedpmpnotavl_upd != -99:
			self.hmipnahso3orpdutyselectedpmpnotavl = self.hmipnahso3orpdutyselectedpmpnotavl_upd

		# self.P403_FB.PMP_FBD(self.P_NAHSO3_ORP_DUTY_FB.Start_Pmp1,self.IO.P403,HMI.P403)
		self.hmip403status_upd, self.hmip403fault, self.hmip403avl, self.hmip403shutdown = self.P403_FB.PMP_FBD(self.P_NAHSO3_ORP_DUTY_FB.Start_Pmp1, self.IO.P403, self.hmip403auto, self.hmip403reset, self.hmip403permissive, self.hmip403sd)
		if self.hmip403status_upd != -99:
			self.hmip403status = self.hmip403status_upd

		# self.P404_FB.PMP_FBD(self.P_NAHSO3_ORP_DUTY_FB.Start_Pmp2,self.IO.P404,HMI.P404)
		self.hmip404status_upd, self.hmip404fault, self.hmip404avl, self.hmip404shutdown = self.P404_FB.PMP_FBD(self.P_NAHSO3_ORP_DUTY_FB.Start_Pmp2, self.IO.P404, self.hmip404auto, self.hmip404reset, self.hmip404permissive, self.hmip404sd)
		if self.hmip404status_upd != -99:
			self.hmip404status = self.hmip404status_upd

		############# Physical process simulation code ################
		self.Actuator()
		self.Plant()
		############# Physical process simulation ends here ###########

		## setdata() calls start here ###################
		setdata(self, 'HMI.P401.Reset',SCADA_ADDR,self.hmip401reset)
		setdata(self, 'HMI.P402.Reset',SCADA_ADDR,self.hmip402reset)
		setdata(self, 'HMI.P403.Reset',SCADA_ADDR,self.hmip403reset)
		setdata(self, 'HMI.P404.Reset',SCADA_ADDR,self.hmip404reset)
		setdata(self, 'HMI.UV401.Reset',SCADA_ADDR,self.hmiuv401reset)
		setdata(self, 'HMI.P401.Auto',SCADA_ADDR,self.hmip401auto)
		setdata(self, 'HMI.P402.Auto',SCADA_ADDR,self.hmip402auto)
		setdata(self, 'HMI.P403.Auto',SCADA_ADDR,self.hmip403auto)
		setdata(self, 'HMI.P404.Auto',SCADA_ADDR,self.hmip404auto)
		setdata(self, 'HMI.UV401.Auto',SCADA_ADDR,self.hmiuv401auto)
		setdata(self, 'HMI.P4.Permissive_On',SCADA_ADDR,self.hmip4permissiveon)
		setdata(self, 'HMI.P401.Permissive',SCADA_ADDR,self.hmip401permissive)
		setdata(self, 'HMI.P401.MSG_Permissive',SCADA_ADDR,self.hmip401msgpermissive)
		setdata(self, 'HMI.P402.Permissive',SCADA_ADDR,self.hmip402permissive)
		setdata(self, 'HMI.P402.MSG_Permissive',SCADA_ADDR,self.hmip402msgpermissive)
		setdata(self, 'HMI.P403.Permissive',SCADA_ADDR,self.hmip403permissive)
		setdata(self, 'HMI.P403.MSG_Permissive',SCADA_ADDR,self.hmip403msgpermissive)
		setdata(self, 'HMI.P404.Permissive',SCADA_ADDR,self.hmip404permissive)
		setdata(self, 'HMI.P404.MSG_Permissive',SCADA_ADDR,self.hmip404msgpermissive)
		setdata(self, 'HMI.UV401.Permissive',SCADA_ADDR,self.hmiuv401permissive)
		setdata(self, 'HMI.UV401.MSG_Permissive',SCADA_ADDR,self.hmiuv401msgpermissive)
		setdata(self, 'HMI.P401.SD',SCADA_ADDR,self.hmip401sd)
		setdata(self, 'HMI.P401.MSG_Shutdown',SCADA_ADDR,self.hmip401msgshutdown)
		setdata(self, 'HMI.P402.SD',SCADA_ADDR,self.hmip402sd)
		setdata(self, 'HMI.P402.MSG_Shutdown',SCADA_ADDR,self.hmip402msgshutdown)
		setdata(self, 'HMI.P403.SD',SCADA_ADDR,self.hmip403sd)
		setdata(self, 'HMI.P403.MSG_Shutdown',SCADA_ADDR,self.hmip403msgshutdown)
		setdata(self, 'HMI.P404.SD',SCADA_ADDR,self.hmip404sd)
		setdata(self, 'HMI.P404.MSG_Shutdown',SCADA_ADDR,self.hmip404msgshutdown)
		setdata(self, 'HMI.UV401.SD',SCADA_ADDR,self.hmiuv401sd)
		setdata(self, 'HMI.UV401.MSG_Shutdown',SCADA_ADDR,self.hmiuv401msgshutdown)
		if self.hmip4state_prev == 1:
			if self.hmip4state == 2:
				setdata(self, 'HMI.P4.State',SCADA_ADDR,2)
				self.hmip4state_prev = 0
		if self.hmip4state_prev == 2:
			if self.hmip4state == 3:
				setdata(self, 'HMI.P4.State',SCADA_ADDR,3)
				self.hmip4state_prev = 0
		if self.hmip4state_prev == 3:
			if self.hmip4state == 4:
				setdata(self, 'HMI.P4.State',SCADA_ADDR,4)
				self.hmip4state_prev = 0
		if self.hmip4state_prev == 4:
			if self.hmip4state == 5:
				setdata(self, 'HMI.P4.State',SCADA_ADDR,5)
				self.hmip4state_prev = 0
		if self.hmip4state_prev == 5:
			if self.hmip4state == 6:
				setdata(self, 'HMI.P4.State',SCADA_ADDR,6)
				self.hmip4state_prev = 0
		if self.hmip4state_prev == 6:
			if self.hmip4state == 1:
				setdata(self, 'HMI.P4.State',SCADA_ADDR,1)
				self.hmip4state_prev = 0
		if self.hmip4state_prev > 6:
			setdata(self, 'HMI.P4.State',SCADA_ADDR,1)

		setdata(self, 'HMI.LIT401.Pv',SCADA_ADDR,self.hmilit401pv)
		setdata(self, 'HMI.LIT401.AHH',SCADA_ADDR,self.hmilit401ahh)
		setdata(self, 'HMI.LIT401.AH',SCADA_ADDR,self.hmilit401ah)
		setdata(self, 'HMI.LIT401.AL',SCADA_ADDR,self.hmilit401al)
		setdata(self, 'HMI.LIT401.ALL',SCADA_ADDR,self.hmilit401all)


		setdata(self, 'HMI.P_RO_FEED_DUTY.Both_Pmp_Not_Avl',SCADA_ADDR,self.hmiprofeeddutybothpmpnotavl)
		setdata(self, 'HMI.P_RO_FEED_DUTY.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hmiprofeeddutyselectedpmpnotavl)
		setdata(self, 'HMI.P_RO_FEED_DUTY.Pump_Running',SCADA_ADDR,self.hmiprofeeddutypumprunning)
		setdata(self, 'HMI.P401.Status',SCADA_ADDR,self.hmip401status)
		setdata(self, 'HMI.P401.Fault',SCADA_ADDR,self.hmip401fault)
		setdata(self, 'HMI.P401.Avl',SCADA_ADDR,self.hmip401avl)
		setdata(self, 'HMI.P401.Shutdown',SCADA_ADDR,self.hmip401shutdown)
		setdata(self, 'HMI.P402.Status',SCADA_ADDR,self.hmip402status)
		setdata(self, 'HMI.P402.Fault',SCADA_ADDR,self.hmip402fault)
		setdata(self, 'HMI.P402.Avl',SCADA_ADDR,self.hmip402avl)
		setdata(self, 'HMI.P402.Shutdown',SCADA_ADDR,self.hmip402shutdown)
		setdata(self, 'HMI.UV401.Status',SCADA_ADDR,self.hmiuv401status)
		setdata(self, 'HMI.UV401.Avl',SCADA_ADDR,self.hmiuv401avl)
		setdata(self, 'HMI.UV401.RunHr',SCADA_ADDR,self.hmiuv401runhr)
		setdata(self, 'HMI.UV401.Shutdown',SCADA_ADDR,self.hmiuv401shutdown)
		setdata(self, 'HMI.LS401.Alarm',SCADA_ADDR,self.hmils401alarm)
		setdata(self, 'HMI.P_NAHSO3_ORP_DUTY.Both_Pmp_Not_Avl',SCADA_ADDR,self.hmipnahso3orpdutybothpmpnotavl)
		setdata(self, 'HMI.P_NAHSO3_ORP_DUTY.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hmipnahso3orpdutyselectedpmpnotavl)
		setdata(self, 'HMI.P_NAHSO3_ORP_DUTY.Pump_Running',SCADA_ADDR,self.hmipnahso3orpdutypumprunning)
		setdata(self, 'HMI.P403.Status',SCADA_ADDR,self.hmip403status)
		setdata(self, 'HMI.P403.Fault',SCADA_ADDR,self.hmip403fault)
		setdata(self, 'HMI.P403.Avl',SCADA_ADDR,self.hmip403avl)
		setdata(self, 'HMI.P403.Shutdown',SCADA_ADDR,self.hmip403shutdown)
		setdata(self, 'HMI.P404.Status',SCADA_ADDR,self.hmip404status)
		setdata(self, 'HMI.P404.Fault',SCADA_ADDR,self.hmip404fault)
		setdata(self, 'HMI.P404.Avl',SCADA_ADDR,self.hmip404avl)
		setdata(self, 'HMI.P404.Shutdown',SCADA_ADDR,self.hmip404shutdown)

		# print("PLC4 Debug: HMI.LIT401.Pv, HMI.P301.Status, HMI.P302.Status, HMI.MV301.Close, HMI.MV302.Open, HMI.MV303.Close, HMI.MV304.Close, HMI.P602.Status, IO_P4.P401.DI_Run, IO_P4.P402.DI_Run", self.hmilit401pv, self.hmip301status, HMI.P302.Status, HMI.MV301.Close, HMI.MV302.Open, HMI.MV303.Close, HMI.MV304.Close, HMI.P602.Status, IO_P4.P401.DI_Run, IO_P4.P402.DI_Run)
		## setdata() calls end here ###################


	def _launch_next(self):
		# Schedule the next call
		threading.Timer(interval, self._launch_next).start()
		# Launch network_function in a thread
		t = threading.Thread(target=self.Iteration)
		t.daemon = True
		t.start()


	def Pre_Main_RO_Feed_Dosing(self,IO):
		self.IO = IO
		self.result=[900]
		self._launch_next()
		while True:
			time.sleep(1)
