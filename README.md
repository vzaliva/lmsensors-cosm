lmsensors-cosm
==============

Simple script to feed Linux lmsensors data to COSM.com.
Typical usage: to be regularly called from from cron(8).

Required:
  * Python 2.6+
  * Linux 'lm_sensors' package which provides libsensors.so version 2.x (API 3) or 3.x (API 4) (tested with lm_sensors-2.10.7-9.el5)
  * https://pypi.python.org/pypi/PySensors/

