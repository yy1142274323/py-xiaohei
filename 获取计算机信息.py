'''
python中，platform模块给我们提供了很多方法去获取操作系统的信息

platform.platform()#获取操作系统名称及版本号，'Windows-7-6.1.7601-SP1'
platform.version()#获取操作系统版本号，'6.1.7601'
platform.architecture()#获取操作系统的位数，('64bit','WindowsPE')
platform.machine()#计算机类型，'AMD64'
platform.node()#计算机的网络名称，'PC-20200627RNBJ'
platform.processor()#计算机处理器信息，'Intel64Family6Model58Stepping9,GenuineIntel'
platform.system()#计算机操作系统，'Windows'
platform.uname()#包含上面所有的信息汇总，uname_result(system='Windows',node='PC-20200627RNBJ',release='7',
                    version='6.1.7601',machine='AMD64',processor='Intel64Family6
                    Model58Stepping9,GenuineIntel')

platform.python_build()
platform.python_compiler()
platform.python_branch()
platform.python_implementation()
platform.python_revision()
platform.python_version()
platform.python_version_tuple()
'''
#
import platform
import pynvml
import wmi
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0) # 0表示第一块显卡
meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)



def get_platform():
  '''获取操作系统名称及版本号'''
  return platform.platform()


def get_version():
  '''获取操作系统版本号'''
  return platform.version()


def get_architecture():
  '''获取操作系统的位数'''
  return platform.architecture()


def get_machine():
  '''计算机类型'''
  return platform.machine()


def get_node():
  '''计算机的网络名称'''
  return platform.node()


def get_processor():
  '''计算机处理器信息'''
  return platform.processor()


def get_system():
  '''获取操作系统类型'''
  return platform.system()


def get_uname():
  '''汇总信息'''
  return platform.uname()


def get_python_build():
  '''thePythonbuildnumberanddateasstrings'''
  return platform.python_build()


def get_python_compiler():
  '''ReturnsastringidentifyingthecompilerusedforcompilingPython'''
  return platform.python_compiler()


def get_python_branch():
  '''ReturnsastringidentifyingthePythonimplementationSCMbranch'''
  return platform.python_branch()


def get_python_implementation():
  '''ReturnsastringidentifyingthePythonimplementation.Possiblereturnvaluesare:‘CPython’,‘IronPython’,‘Jython’,‘PyPy’.'''
  return platform.python_implementation()


def get_python_version():
  '''ReturnsthePythonversionasstring'major.minor.patchlevel'''
  return platform.python_version()


def get_python_revision():
  '''ReturnsastringidentifyingthePythonimplementationSCMrevision.'''
  return platform.python_revision()


def get_python_version_tuple():
  '''ReturnsthePythonversionastuple(major,minor,patchlevel)ofstrings'''
  return platform.python_version_tuple()



def get_fs_info():
    """
    获取文件系统信息
    包含分区的大小、已用量、可用量、使用率、挂载点信息
    """
    tmplist = []
    c = wmi.WMI()
    for physical_disk in c.Win32_DiskDrive():
        # print(physical_disk)
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            # print(partition)
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                # print(logical_disk)
                tmpdict = {}
                tmpdict["Caption"] = logical_disk.Caption
                tmpdict["DiskTotal"] = int(logical_disk.Size) / 1024 / 1024 / 1024
                tmpdict["UseSpace"] = (int(logical_disk.Size) - int(logical_disk.FreeSpace)) / 1024 / 1024 / 1024
                tmpdict["FreeSpace"] = int(logical_disk.FreeSpace) / 1024 / 1024 / 1024
                tmpdict["Percent"] = int(
                    100.0 * (int(logical_disk.Size) - int(logical_disk.FreeSpace)) / int(logical_disk.Size))
                tmplist.append(tmpdict)
    return tmplist


def show_os_info():
  '''打印os的全部信息'''
  print('获取操作系统名称及版本号:[{}]'.format(get_platform()))
  print('获取操作系统版本号:[{}]'.format(get_version()))
  print('获取操作系统的位数:[{}]'.format(get_architecture()))
  print('计算机类型:    [{}]'.format(get_machine()))
  print('计算机的网络名称:[{}]'.format(get_node()))
  print('计算机处理器信息:[{}]'.format(get_processor()))
  print('获取操作系统类型:[{}]'.format(get_system()))
  print('汇总信息:    [{}]'.format(get_uname()))
  print('显卡大小：[{}]'.format(meminfo.total / 1024 ** 2) )  # 第二块显卡总的显存大小
  print('显卡[{}]'.format(pynvml.nvmlDeviceGetName(handle)))



# def show_python_info():
#   '''打印python的全部信息'''
#   print('ThePythonbuildnumberanddateasstrings:[{}]'.format(get_python_build()))
#   print('ReturnsastringidentifyingthecompilerusedforcompilingPython:[{}]'.format(get_python_compiler()))
#   print('ReturnsastringidentifyingthePythonimplementationSCMbranch:[{}]'.format(get_python_branch()))
#   print('ReturnsastringidentifyingthePythonimplementation:[{}]'.format(get_python_implementation()))
#   print('TheversionofPython：[{}]'.format(get_python_version()))
#   print('PythonimplementationSCMrevision:[{}]'.format(get_python_revision()))
#   print('Pythonversionastuple:[{}]'.format(get_python_version_tuple()))


def testPlatform():

  print("操作系统信息：")
  show_os_info()

  # print('-'*100)
  # print("计算机中的Python信息：")

  # show_python_info()


def main():
  testPlatform()
  # 获取磁盘信息
  fs = get_fs_info()
  for f in fs:
      disk_name = f['Caption']  # 磁盘名
      DiskTotal = f['DiskTotal']  # 磁盘大小 单位G
      disk_UseSpace = f['UseSpace']  # 已用磁盘大小 单位G
      disk_FreeSpace = f['FreeSpace']  # 剩余可用磁盘大小 单位G
      print('磁盘名：{}  磁盘大小：{}G   已用空间：{}G  剩余可用空间：{}G !!'.format(disk_name, round(DiskTotal, 2), round(disk_UseSpace, 2),
                                                                round(disk_FreeSpace, 2)))


if __name__ == '__main__':
    main()



# -----------------------------------------------------------------------------------------------------------------------------------------------------






















# # -----------------------------------------------------------------------------------
# # GPU information
# import GPUtil
# from tabulate import tabulate
#
# print("=" * 40, "GPU Details", "=" * 40)
# gpus = GPUtil.getGPUs()
#
# list_gpus = []
# print(list_gpus)
# for gpu in gpus:
#     # get the GPU id
#     gpu_id = gpu.id
#     # name of GPU
#     gpu_name = gpu.name
#     # get % percentage of GPU usage of that GPU
#     gpu_load = f"{gpu.load * 100}%"
#     # get free memory in MB format
#     gpu_free_memory = f"{gpu.memoryFree}MB"
#     # get used memory
#     gpu_used_memory = f"{gpu.memoryUsed}MB"
#     # get total memory
#     gpu_total_memory = f"{gpu.memoryTotal}MB"
#     # get GPU temperature in Celsius
#     gpu_temperature = f"{gpu.temperature} °C"
#     gpu_uuid = gpu.uuid
#     list_gpus.append((
#         gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
#         gpu_total_memory, gpu_temperature, gpu_uuid
#     ))
#
# print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
#                                    "temperature", "uuid")))
#
#
# # print(gpu.name).












#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @author: kun
# from PyQt5.Qt import *
# import sys
# """
# setIcon(QIcon)  # 设置图标
# setIconSize(ASize)  # 设置图标大小
# icon()  # 获取图标
# iconSize()  # 获取图标大小
# # 当一直摁下不松开触发重复
# setAutoRepeat(bool)  # 设置自动重复
# setAutoRepeatInterval(ms)  # 设置自动重复检测间隔
# setAutoRepeatDelay(ms)  # 设置初次检测延迟
# autoRepeat()  # 获取是否自动重复
# autoRepeatInterval()  # 获取自动重复检测间隔
# autoRepeatDelay()  # 获取初次检测延迟时长
# """
# app = QApplication(sys.argv)
# w = QWidget()
# w.resize(500, 500)
# btn = QPushButton(w)
# btn.move(50, 0)
# btn1 = QPushButton(w)
# btn1.move(150, 0)
#
#
#
#
# btn.setText("Button")  # 设置初始文本
# icon = QIcon(r"d:\61434\Desktop\t01753453b660de14e9.jpg")  # 设置图片
# btn.setIcon(icon)  # 设置图标
# size = QSize(20, 20)  # 输入图标大小
# btn.setIconSize(size)  # 设置图标大小
# w.setVisible(True)  # 设置为可见
#
#
#
#
#
# btn1.setText("点我")
# btn1.clicked.connect(lambda: print("点击一次"))
# btn1.setAutoRepeat(True)  # 开启重复
# btn1.setAutoRepeatInterval(1000)  # 设置 1 秒间隔
# btn1.setAutoRepeatDelay(2000)  # 摁下两秒后触发重复
# # 获取值
# # print(btn.autoRepeat())
# # print(btn.autoRepeatInterval())
# # print(btn.autoRepeatDelay())
# w.show()
# sys.exit(app.exec_())






