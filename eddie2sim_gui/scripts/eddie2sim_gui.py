#!/usr/bin/env python

# Import necessary package 
import sys
import rospy
import roslaunch
from functools import partial
from std_msgs.msg import Int32MultiArray
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from os.path import expanduser

# Initialize home directory
home = expanduser("~")

# Class for operating the obstacle detection graphic user interface
class MainWindow(QtWidgets.QMainWindow):

	# Initial state
	def __init__(self):
		super(MainWindow,self).__init__()
		# Load ui
		uic.loadUi("{}/eddie2sim_ws/src/eddie2sim_gui/ui/eddie2sim.ui".format(home),self)
		self.setWindowTitle('EDDIE2')
		# Load val2 image
		pixmap_val2 = QtGui.QPixmap('{}/eddie2sim_ws/src/eddie2sim_gui/picture/eddie2sim.png'.format(home))
		self.label_val2_pic.setPixmap(pixmap_val2)
		# Define back end for each buttons
		self.enterButton.clicked.connect(self.buttonEnter_clicked)
		self.goal1_checkBox.stateChanged.connect(self.checkBox1)
		self.goal2_checkBox.stateChanged.connect(self.checkBox2)
		self.goal3_checkBox.stateChanged.connect(self.checkBox3)
		self.goal4_checkBox.stateChanged.connect(self.checkBox4)
		self.goal5_checkBox.stateChanged.connect(self.checkBox5)
		self.allgoal_checkBox.stateChanged.connect(self.checkBoxAll)
		# Block user to check these 2 boxes
		self.goal3_checkBox.blockSignals(True)
		self.goal4_checkBox.blockSignals(True)
		# Initialize goal variable
		self.goal_list = []
		self.num_goal = 5
		# Define node name
		rospy.init_node('eddie2sim_gui_node', anonymous=True)

	# Backend for enter button
	def buttonEnter_clicked(self): 
		if len(self.goal_list) > 0:
			adding_round = self.num_goal - len(self.goal_list)
			for index in range(adding_round):
				self.goal_list.append(None)
			# Robot moving in term of obstacle detection state machine process
			fsm_node = roslaunch.core.Node(	package='eddie2sim_fsm', 
											node_type='eddie2sim_fsm.py', 
											name='eddie2sim_fsm_node',
											output='screen')
			fsm_node.args = "_goal1:={} _goal2:={} _goal3:={} _goal4:={} _goal5:={}".format(self.goal_list[0], 
																	   						self.goal_list[1],
																							self.goal_list[2],
																							self.goal_list[3],
																							self.goal_list[4])
			fsm_launch = roslaunch.scriptapi.ROSLaunch()
			fsm_launch.start()
			fsm_process = fsm_launch.launch(fsm_node)
			while fsm_process.is_alive():
				if fsm_process.is_alive() == False:
					break
			for data in self.goal_list:
				if None in self.goal_list:
					self.goal_list.remove(None)
		else: 
			print("Please select the goal before click 'Enter' button")

	# Get text function
	def getText(self):
		doc = QtGui.QTextDocument()

		doc.setHtml(self.label_goal1.text())
		self.label1_text = doc.toPlainText()

		doc.setHtml(self.label_goal2.text())
		self.label2_text = doc.toPlainText()

		doc.setHtml(self.label_goal3.text())
		self.label3_text = doc.toPlainText()
		
		doc.setHtml(self.label_goal4.text())
		self.label4_text = doc.toPlainText()
		
		doc.setHtml(self.label_goal5.text())
		self.label5_text = doc.toPlainText()
	
	# Sequencing text function
	def textIn(self, text):
		self.getText()
		if self.label1_text == "":
			self.label_goal1.setText(text)
		elif self.label2_text == "":
			self.label_goal2.setText(text)
		elif self.label3_text == "":
			self.label_goal3.setText(text)
		elif self.label4_text == "":
			self.label_goal4.setText(text)
		elif self.label5_text == "":
			self.label_goal5.setText(text)

	# Reorder text function
	def textOut(self,text):
		self.getText()
		if self.label1_text == text:
			self.label_goal1.setText(self.label2_text)
			self.label_goal2.setText(self.label3_text)
			self.label_goal3.setText(self.label4_text)
			self.label_goal4.setText(self.label5_text)
			self.label_goal5.setText("")
		elif self.label2_text == text:
			self.label_goal2.setText(self.label3_text)
			self.label_goal3.setText(self.label4_text)
			self.label_goal4.setText(self.label5_text)
			self.label_goal5.setText("")
		elif self.label3_text == text:
			self.label_goal3.setText(self.label4_text)
			self.label_goal4.setText(self.label5_text)
			self.label_goal5.setText("")
		elif self.label4_text == text:
			self.label_goal4.setText(self.label5_text)
			self.label_goal5.setText("")

		elif self.label5_text == text:
			self.label_goal5.setText("")

	# Backend for check box 1
	def checkBox1(self, state):
		if state == QtCore.Qt.Checked:
			self.goal_list.append("station1")
			self.textIn("Station1")
		else:
			self.goal_list.remove("station1")
			self.textOut("Station1")
	
	# Backend for check box 2
	def checkBox2(self, state):
		if state == QtCore.Qt.Checked:
			self.goal_list.append("station2")
			self.textIn("Station2")
		else:
			self.goal_list.remove("station2")
			self.textOut("Station2")

	# Backend for check box 3
	def checkBox3(self, state):
		if state == QtCore.Qt.Checked:
			self.goal_list.append("station3")
			self.textIn("Station3")
		else:
			self.goal_list.remove("station3")
			self.textOut("Station3")

	# Backend for check box 4
	def checkBox4(self, state):
		if state == QtCore.Qt.Checked:
			self.goal_list.append("station4")
			self.textIn("Station4")
		else:
			self.goal_list.remove("station4")
			self.textOut("Station4")

	# Backend for check box 5
	def checkBox5(self, state):
		if state == QtCore.Qt.Checked:
			self.goal_list.append("base_station")
			self.textIn("Base Station")
		else:
			self.goal_list.remove("base_station")
			self.textOut("Base Station")

	# Backend for check box all
	def checkBoxAll(self, state):
		if state == QtCore.Qt.Checked:
			self.goal1_checkBox.setChecked(True)
			self.goal2_checkBox.setChecked(True)
			self.goal3_checkBox.setChecked(True)
			self.goal4_checkBox.setChecked(True)
			self.goal5_checkBox.setChecked(True)

			self.label_goal1.setText("Station1")
			self.label_goal2.setText("Station2")
			self.label_goal3.setText("Base Station")
			self.label_goal4.setText("")
			self.label_goal5.setText("")

			self.goal_list = ["station1","station2","base_station",None,None]

		else:
			self.goal1_checkBox.setChecked(False)
			self.goal2_checkBox.setChecked(False)
			self.goal3_checkBox.setChecked(False)
			self.goal4_checkBox.setChecked(False)
			self.goal5_checkBox.setChecked(False)

			self.label_goal1.setText("")
			self.label_goal2.setText("")
			self.label_goal3.setText("")
			self.label_goal4.setText("")
			self.label_goal5.setText("")

			self.goal_list = []
			 
			 
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	Window = MainWindow()
	Window.show()
	sys.exit(app.exec_())
