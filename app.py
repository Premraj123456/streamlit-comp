import streamlit as st
import psutil
import GPUtil
import platform
import os
import pandas as pd
import time

# Function to get CPU information
def get_cpu_info():
    cpu_info = {
        "CPU Name": platform.processor() if platform.system() == "Windows" else os.popen("cat /proc/cpuinfo | grep 'model name' | uniq").read().strip().split(": ")[1],
        "Physical cores": psutil.cpu_count(logical=False),
        "Total threads": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f}Mhz",
        "Min Frequency": f"{psutil.cpu_freq().min:.2f}Mhz",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f}Mhz",
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
    }
    return cpu_info

# Function to get RAM information
def get_ram_info():
    svmem = psutil.virtual_memory()
    ram_info = {
        "Total": f"{svmem.total / (1024 ** 3):.2f} GB",
        "Available": f"{svmem.available / (1024 ** 3):.2f} GB",
        "Used": f"{svmem.used / (1024 ** 3):.2f} GB",
        "Percentage": f"{svmem.percent}%",
    }
    return ram_info

# Function to get GPU information
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        info = {
            "GPU Name": gpu.name,
            "Total Memory": f"{gpu.memoryTotal}MB",
            "Free Memory": f"{gpu.memoryFree}MB",
            "Used Memory": f"{gpu.memoryUsed}MB",
            "GPU Load": f"{gpu.load * 100}%",
            "Temperature": f"{gpu.temperature} °C",
        }
        gpu_info.append(info)
    return gpu_info

# Function to get process information
def get_process_info():
    process_info = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        process_info.append(proc.info)
    return process_info

# Streamlit app
st.title("System Information and Activity Tracker")

# CPU Information
st.header("CPU Information")
cpu_info = get_cpu_info()
st.table(cpu_info.items())

# RAM Information
st.header("RAM Information")
ram_info = get_ram_info()
st.table(ram_info.items())

# GPU Information
st.header("GPU Information")
gpu_info = get_gpu_info()
if gpu_info:
    for idx, gpu in enumerate(gpu_info):
        st.subheader(f"GPU {idx + 1}")
        st.table(gpu.items())
else:
    st.write("No GPU found")

# Process Information
st.header("Process Information")
refresh_rate = st.sidebar.slider('Refresh Rate (seconds)', min_value=1, max_value=60, value=5)

process_placeholder = st.empty()

# Function to display process information
def display_process_info():
    process_info = get_process_info()
    df = pd.DataFrame(process_info)
    process_placeholder.table(df)

while True:
    display_process_info()
    time.sleep(refresh_rate)
