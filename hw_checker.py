import json
import cpuinfo
import psutil
import subprocess
import GPUtil
import platform

def load_compat_base(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def is_amd_ryzen_processor(cpu_brand):
    return "AMD Ryzen" in cpu_brand

def check_gpu_support(gpu_name, database):
    if "GPUs" in database:
        for item in database["GPUs"]:
            if item['model'].lower() in gpu_name.lower():
                return item
    return None

def get_system_hardware():
    cpu_info = cpuinfo.get_cpu_info()['brand_raw']
    gpus = GPUtil.getGPUs()
    gpu_info = gpus[0].name if gpus else "HWChecker: No discrete GPU found."

    integrated_gpu_info = None
    if platform.system() == "Windows":
        try:
            wmic_output = subprocess.check_output(['wmic', 'path', 'win32_videocontroller', 'get', 'name']).decode('utf-8')
            found_gpu = False
            for line in wmic_output.splitlines():
                line = line.strip()
                if "Radeon" in line:
                    integrated_gpu_info = line
                    found_gpu = True
                    break
            if found_gpu:
                print(f"Detected Integrated GPU: {integrated_gpu_info}")
            else:
                print("No compatible integrated GPU found.")
        except Exception as e:
            integrated_gpu_info = f"HWChecker: Error detecting Vega iGPU: {e}"
            print(integrated_gpu_info) 
    

    return {
        "CPU": cpu_info,
        "dGPU": gpu_info,
        "iGPU (Vega)": integrated_gpu_info,
    }

def main():
    database_path = 'compat_base.json'
    database = load_compat_base(database_path)

    hardware = get_system_hardware()
    print("############################### HW CHECKER ###############################")
    if is_amd_ryzen_processor(hardware['CPU']):
        print(f"AMD Ryzen CPU detected: {hardware['CPU']}")
        print(f"Your CPU is compatible with macOS 10.13 and up!")
    else:
        print(f"Non-AMD Ryzen CPU detected: {hardware['CPU']}")
    print("##########################################################################")

    dgpu_result = check_gpu_support(hardware["dGPU"], database)
    
   



    if dgpu_result:
        print(f"dGPU Supported: {gpu_result['model']}")
        print(f"macOS Compatibility: {gpu_result['macOS']}")
        print(f"Notes: {gpu_result['notes']}")
    else:
        print("dGPU not supported/not found.")


    integrated_gpu_detected = hardware.get("iGPU (Vega)")
    if isinstance(integrated_gpu_detected, str) and "Radeon" in integrated_gpu_detected:
        print(f"iGPU detected: {hardware['iGPU (Vega)']} (All Vega iGPUs are supported, use NootedRed!)")
        print("##########################################################################")
        print(f"WARNING: Don't take this as granted, currently there is no way to check for actual")
        print(f"Vega iGPU cause drivers are reporting generic Radeon GPU, check your manufacturer")
        print(f"site for more details!!!")
        print("##########################################################################")
    else:
        print("HWChecker: No Vega iGPU found.")

if __name__ == "__main__":
    main()