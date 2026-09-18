
from logicblock.logicblock import TONR
from logicblock.logicblock import bit_2_signed_integer
from logicblock.logicblock import signed_integer_2_bit
# 8 Classes in this file
class AIN_FBD:

	def __init__(self,hmihty,hmiahh,hmiah,hmial,hmiall):
		self.Hty = hmihty
		self.AHH = hmiahh
		self.AH = hmiah
		self.AL = hmial
		self.ALL = hmiall

	# def AIN_FBD(self,IO,HMI):
	# 	SAHH = HMI.SAHH
	# 	SAH  = HMI.SAHH
	# 	SAL  = HMI.SAL
	# 	SALL = HMI.SALL
	#
	# 	self.AHH, self.AH, self.AL, self.ALL = ALM(HMI.Pv,SAHH,SAH,SAL,SALL)
	# 	HMI.Hty = self.Hty
	# 	HMI.AHH = self.AHH
	# 	HMI.AH  = self.AH
	# 	HMI.AL  = self.AL
	# 	HMI.ALL = self.ALL


class MV_FBD:
	def __init__(self,hmifto,hmiftc,hmiopen,hmiclose):
		self.FTO = hmifto
		self.FTC = hmiftc
		self.Cmd_Open = hmiopen
		self.Cmd_Close = hmiclose

	def MV_FBD(self, AutoInp, IO, hmiauto, hmireset):
		ZSO = IO.DI_ZSO
		ZSC = IO.DI_ZSC
		Auto = hmiauto
		Reset = hmireset
		hmistatus = -99
		
		# Reset fault logic (same pattern as PMP_FBD)
		if Reset:
			self.FTO = 0
			self.FTC = 0
		
		if ZSC:
			hmistatus = 1
		elif ZSO:
			hmistatus = 2
		else:
			hmistatus = 0
		# transfer
		hmiavl = Auto
		if AutoInp:
			self.Cmd_Close = 0
			self.Cmd_Open  = 1
		else:
			self.Cmd_Close = 1
			self.Cmd_Open  = 0
		IO.DO_Open = self.Cmd_Open
		IO.DO_Close= self.Cmd_Close
		return hmistatus, hmiavl

class FIT_FBD:
	def __init__(self,hmihty,hmiahh,hmiah,hmial,hmiall):
		self.Hty = hmihty
		self.AHH = hmiahh
		self.AH = hmiah
		self.AL = hmial
		self.ALL = hmiall

	# def FIT_FBD(self, WRIO_Enb, Totaliser_Enb, IO,HMI,Sec_P):
	# 	Raw_RIO = IO.AI_Value
	# 	Raw_WRIO = IO.W_AI_Value
	# 	RIO_Hty = IO.AI_Hty
	# 	WRIO_Hty = IO.W_AI_Hty
	#
	# 	SAHH = HMI.SAHH
	# 	SAH  = HMI.SAH
	# 	SAL  = HMI.SAL
	# 	SALL = HMI.SALL
	# 	Simulation = HMI.Sim
	# 	Rst_Totaliser = HMI.Rst_Totaliser
	#
	# 	if WRIO_Enb:
	# 		self.Wifi_Enb = 1
	# 		Mid_Raw = Raw_WRIO
	# 		Mid_H_Raw = self.H_Raw_WRIO
	# 		Mid_L_Raw = self.L_Raw_WRIO
	# 		Mid_Inst_Hty = WRIO_Hty
	# 	else:
	# 		self.Wifi_Enb = 0
	# 		Mid_Raw = Raw_RIO
	# 		Mid_H_Raw = self.H_Raw_RIO
	# 		Mid_L_Raw = self.L_Raw_RIO
	# 		Mid_Inst_Hty = RIO_Hty
	# 	if Simulation:
	# 	   	HMI.Pv = HMI.Sim_PV
	# 	else:
	# 		Scale_Out = SCL( Mid_Raw, Mid_H_Raw, Mid_L_Raw, self.HEU, self.LEU)
	# 		if Scale_Out > 0:
	# 			HMI.Pv = Scale_Out
	# 		elif Scale_Out <= 0:
	# 			HMI.Pv = 0.0
	# 		HMI.Sim_Pv = HMI.Pv
	# 	self.AHH, self.AH, self.AL, self.ALL = ALM(HMI.Pv, SAHH, SAH, SAL, SALL)
	# 	if Totaliser_Enb:
	# 		if Sec_P:
	# 			HMI.Totaliser = HMI.Totaliser + abs(HMI.Pv)/3600
	# 	if Rst_Totaliser:
	# 		HMI.Totaliser = 0
	# 	self.Hty = Mid_Inst_Hty and (Mid_Raw > Mid_L_Raw) and (Mid_Raw > Mid_H_Raw)
	#
	# 	HMI.Hty = self.Hty
	# 	HMI.Wifi_Enb = self.Wifi_Enb
	# 	HMI.AHH = self.AHH
	# 	HMI.AH  = self.AH
	# 	HMI.AL  = self.AL
	# 	HMI.ALL = self.AHH

class PMP_FBD:
	def __init__(self,hmiavl,hmifault,hmishutdown):
		self.Cmd_Start = 0
		self.Avl = hmiavl
		self.Fault = hmifault
		self.SD = hmishutdown
		self.Fault = 0
		self.RunMin = 0
		self.Total_RunMin = 0
	def PMP_FBD(self, AutoInp,IO, hmiauto, hmireset, hmipermissive, hmisd):
		Auto = hmiauto
		Remote = IO.DI_Auto
		Run    = IO.DI_Run
		Trip   = IO.DI_Fault
		hmistatus = -99

		Rst = hmireset
		Permissive = hmipermissive
		self.a = Permissive
		Shutdown   = hmisd

		if not Run:
			hmistatus = 1
		else:
			hmistatus = 2
		if self.Fault:
			hmifault = 1
		else:
			hmifault = 0
		if hmireset:
			self.SD = 0
		self.Fault = Trip or self.SD != 0
		hmiremote = Remote

		self.Avl = Auto and Remote and not self.Fault and self.SD == 0
		if Remote:
			if not Auto:
				pass
			else:
				if Run:
					self.Cmd = 2
				if not Run or self.Fault:
					self.Cmd = 1
				if AutoInp:
					if not self.Fault and Permissive == -1 and hmisd== 0:
						self.Cmd_Start = 1
					elif self.Cmd_Start or hmisd != 0 or self.Fault:
						self.SD = hmisd
						self.Cmd_Start = 0
				else:
					self.Cmd_Start = 0
		else:
			self.Cmd_Start = 0
			self.Cmd = 1

		hmiavl = self.Avl
		hmifault = self.Fault
		hmishutdown = self.SD

		IO.DO_Start = self.Cmd_Start
		return hmistatus, hmifault, hmiavl, hmishutdown


class Duty2_FBD:
	def __init__(self):
		self.Start_Pmp1 = 0
		self.Start_Pmp2 = 0
	def Duty2_FBD(self, AutoInp, pmp1status, pmp1avl, pmp2status, pmp2avl, hmiprawwaterdutyselection): #PMP1 and PMP2 should be the class of pump1 and pump2
		Selection = hmiprawwaterdutyselection
		hmipmprunning = 0
		hmiselectedpmpnotavl = -99

		if pmp1status == 2 or pmp2status ==2:
			hmipmprunning = 1
		else:
			hmipmprunning =0
		hmibothpmpnotavl = not pmp1avl and not pmp2avl
		if AutoInp:
			if Selection == 1:
				if pmp1avl:
					self.Start_Pmp1 = 1
					self.Start_Pmp2 = 0
					hmiselectedpmpnotavl = 0
				elif not pmp1avl and pmp2avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 1
					hmiselectedpmpnotavl = 1
				elif not pmp1avl and not pmp2avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 0
				else:
					hmiselectedpmpnotavl = 0
			if Selection == 2:
				if pmp2avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 1
					hmiselectedpmpnotavl = 0
				elif not pmp1avl and pmp2avl:
					self.Start_Pmp1 = 1
					self.Start_Pmp2 = 0
					hmiselectedpmpnotavl = 1
				elif not pmp1avl and not pmp2avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 0
				else:
					hmiselectedpmpnotavl = 0
		else:
			self.Start_Pmp1 = 0
			self.Start_Pmp2 = 0
		return hmibothpmpnotavl, hmiselectedpmpnotavl, hmipmprunning

class SWITCH_FBD:
	def __init__(self,hmidelay):
		Delay = hmidelay
		self.TON_Delay = TONR(Delay)
	def SWITCH_FBD(self, IO):
		Alarm = IO.DI_LS
		self.TON_Delay.TONR(Alarm)
		hmistatus = self.TON_Delay.DN
		self.Status = self.TON_Delay.DN
		return hmistatus


class UV_FBD:
	def __init__(self,hmiavl,hmirunhr,hmishutdown):
		self.Cmd_Start  = 0
		self.Fault = 0
		self.Avl = hmiavl
		self.RunHr = hmirunhr
		self.Total_RunHr = hmirunhr
		self.SD = hmishutdown

	def UV_FBD(self, AutoInp,IO, hmiauto, hmireset,hmiresetrunhr,hmipermissive,hmisd):

		hmistatus = -99
		hmifault = -99
		hmiremote = -99
		hmiavl = -99
		hmirunhr = -99
		hmitotalrunhr = -99
		hmishutdown = -99

		Remote = IO.DI_Auto
		Run    = IO.DI_Run
		Trip   = IO.DI_Fault

		Auto = hmiauto
		Rst  = hmireset
		Rst_RunHr = hmiresetrunhr
		Permissive = hmipermissive
		Shutdown = hmisd

		if not Run:
			hmistatus = 1
		else:
			hmistatus = 2
		if self.Fault:
			hmifault = 1
		else:
			hmifault = 0
		if hmireset:

			self.SD = 0
		self.Fault = Trip
		hmiremote = Remote
		self.Avl = Auto and Remote and not self.Fault and  self.SD == 0
		if Remote:
			if Run:
				self.Cmd = 2
			if not Run or self.Fault:
				self.Cmd = 1
			if AutoInp:
				if not self.Fault and Permissive == -1 and hmisd == 0:
					self.Cmd_Start = 1
				elif self.Cmd_Start or hmisd != 0 or self.Fault:
					self.SD = hmisd
					self.Cmd_Start = 0
			else:
				self.Cmd_Start = 0
		else:
			self.Cmd_Start = 0
			self.Cmd = 1


		hmiavl = self.Avl
		hmifault = self.Fault

		hmirunhr = self.RunHr
		hmitotalrunhr = self.Total_RunHr
		hmishutdown = self.SD
		IO.Start = self.Cmd_Start

		return hmistatus, hmifault, hmiavl, hmirunhr, hmitotalrunhr, hmishutdown

class VSD_FBD:
	def __init__(self, hmifault,hmishutdown,hmispeed,hmidriveready):
		self.Fault = hmifault

		self.SD = hmishutdown
		self.RunMin = 0
		self.Total_RunMin = 0
		self.Speed = hmispeed
		self.Rdy = hmidriveready


	def VSD_FBD(self, AutoInp, AutoSpeed, VSD_In, VSD_Out,IO, hmiauto, hmireset, hmiresetrunhr, hmispeedcommand, hmipermissive, hmisd):

		hmistatus = -99
		hmiremote = -99
		hmifault = -99
		hmicmd = -99

		Remote = IO.DI_Auto
		Run    = IO.DI_Run
		Start_PB = IO.DI_VSD_PB

		Trip = VSD_In.Faulted

		Auto = hmiauto
		Rst  = hmireset
		Rst_RunHr = hmiresetrunhr
		Speed_Cmd = hmispeedcommand
		Permissive = hmipermissive
		Shutdown = hmisd

		if not VSD_In.Active:
			hmistatus = 1
		else:
			hmistatus = 2
		self.Rdy = VSD_In.Ready
		self.Speed = VSD_In.OutputFreq
		hmiremote = Remote
		self.Avl = Auto and Remote and not self.Fault and self.SD == 0
		hmifault = VSD_In.Faulted or Trip or self.SD
		if VSD_In.Active:
			hmicmd = 2  # Cmd or HMI.Cmd, the original code is realy ambiguous
		if not VSD_In.Active or VSD_In.Faulted:
			hmicmd = 1
		if AutoInp:
			if not VSD_In.Faulted and Permissive == -1 and hmisd == 0:
				VSD_Out.Start = 1
				VSD_Out.Stop = 0
				VSD_Out.FreqCommand = AutoSpeed * 100
			elif VSD_Out.Start or hmisd != 0 or self.Fault:
				self.SD = hmisd
				VSD_Out.Start = 0
				VSD_Out.Stop = 0
				hmicmd = 1
			if not VSD_In.Active:
				VSD_Out.Start = 0
				VSD_Out.Stop = 1
				VSD_Out.FreqCommand = AutoSpeed * 100
				hmicmd = 1
		else:
			VSD_Out.Start = 0
			VSD_Out.Stop = 1


		hmiavl = self.Avl
		hmifault = self.Fault
		hmispeed = self.Speed
		hmidriveready = self.Rdy
		hmishutdown = self.SD

		return hmistatus, hmifault, hmiavl, hmispeed, hmidriveready, hmishutdown
