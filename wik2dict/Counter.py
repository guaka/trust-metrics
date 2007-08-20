# -*- coding: utf-8 -*-
"""
Copyright (c) 2004 Guaka

wik2dict is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""

import sys
import time

class Counter:
	"""Counter, with and without ETA."""
	def __init__(self, length = 0, msg = ""):
		self.msg = msg
		if length:
			self.length = length
			self.show = self.show_eta
		else:
			self.show = self.show_no_eta
		self.starttime = time.time()

	def minsec(self, sec):
		"""Seconds to string with h:m:s, h:m or sec."""
	   	minutes, sec = divmod(sec, 60)
		hour, minutes = divmod(minutes, 60)
		if hour:
			return "%i:%02i:%02i" % (hour, minutes, sec)
		if minutes:
			return "%i:%02i" % (minutes, sec)
		return "%.1fs" % (sec)

	def show_no_eta(self, message, finished = False):
		"""Counter without ETA."""
		dif = time.time() - self.starttime
		show = self.msg + "  Time: " + self.minsec(dif) + "  " + str(message)
		if finished:
			print show + " " * 20
		else:
			sys.stdout.write(show + " " * 20 + "\r")
			sys.stdout.flush()

	def show_eta(self, counter, finished = False):
		"""Counter with ETA."""
		ratio = 1.0 * counter / self.length
		dif = time.time() - self.starttime
		show = self.msg + "  %.2f" % (100.0 * ratio) + "%  time: " + self.minsec(dif)
		if finished:
			print show + " " * 20
		else:
			eta = (dif / (ratio or 1)) - dif
			show += "  ETA: " + self.minsec(eta) + " " * 20
			sys.stdout.write(show + "\r")
			sys.stdout.flush()

	def finish(self, show = ""):
		"""Finalize counter."""
		if hasattr(self, "length"):
			self.show(self.length, True)
		else:
			self.show(show, True)
