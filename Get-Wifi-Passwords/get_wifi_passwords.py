import subprocess

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode().split("\n")
profile_names = [name.split(":")[1][1:-1] for name in command_output if "All User Profile" in name]
wifi_list = list()

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        if "Security key           : Absent" in profile_info:
            continue
        else:
            wifi_profile["SSID"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode().split("\n")
            password = [passw.split(":")[1][1:-1] for passw in profile_info_pass if "Key Content" in passw]
            if password == None:
                wifi_profile["Password"] = None
            else:
                wifi_profile["Password"] = password[0]
            wifi_list.append(wifi_profile)

for x in range(len(wifi_list)):
    print(wifi_list[x])
