from django.core.management.utils import get_random_secret_key
skey = get_random_secret_key()
with open('downloader/settings.py','r') as setting_file:
    lines = setting_file.readlines()
    for i in range(len(lines)):
        if 'SECRET_KEY = ' in lines[i]:
            lines[i] = 'SECRET_KEY = "%s"\n'%skey
            break
        else:
            pass
    setting_file.close()
with open('downloader/settings.py','w') as setting_file:
    setting_file.writelines(lines)
    setting_file.close()