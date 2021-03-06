# -*- coding: utf-8 -
import time
from selenium import webdriver as selenium_webdriver
from appium import webdriver as appium_webdriver
from selenium.webdriver.chrome.options import Options
from common import *
from common.log.logger import Log
log = Log(logs_path, '%s.log' % time.strftime('%Y-%m-%d'))
cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class GetDriverWeb():
    def __init__(self, form):
        self.form = form

    def get_driver_web(self):
        if self.form == 'chrome':
            log.info('开始启动chrome浏览器')
            driver = selenium_webdriver.Chrome()
            driver.implicitly_wait(20)  # 隐性等待,最长等20秒
            # 将浏览器窗口最大化
            driver.maximize_window()
            return driver
        elif self.form == 'h5':
            log.info('开始启动chrome浏览器-phone')
            mobile_emulation = {"deviceName": "iPhone 8"}
            chrome_options = Options()
            chrome_options.add_argument('disable-infobars')
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            driver = selenium_webdriver.Chrome(chrome_options=chrome_options)
            driver.implicitly_wait(20)  # 隐性等待,最长等20秒
            return driver


class GetDriverAndroid:
    def __init__(self, reset):
        self.reset = reset  # 是否重启，目前支持'Reset'\'noReset'

    # 把启动android_app的功能封闭成方法
    def get_driver_android(self, reset):

        app_apk_path = os.path.join(cur_path, 'app', app_info['appName'])
        start_info = {
            # 平台名称
            "platformName": 'Android',
            # 平台版本号
            "platformVersion": device_info['platformVersion'],
            # 设备名称
            'deviceName': device_info['deviceName'],
            # app文件地址
            'app': app_apk_path,
            # app包名
            'appPackage': app_info['appPackage'],
            # app程序名
            'appActivity': app_info['appActivity'],
            # 是否不每次重新安装
            'noReset': reset,
            # 是否启用unicode键盘，启动可以输入中文
            'unicodeKeyboard': True,
            # 是否每次重新安装键盘
            'resetKeyboard': True,
            # 如果达到超时时间仍未接收到新的命令时appium会自动结束会话/秒
            'newCommandTimeout': 600}

        log.info('开始启动' + app_info['appName'])
        driver = appium_webdriver.Remote(appium_info['appiumIp'], start_info)
        driver.implicitly_wait(20)  # 隐性等待,最长等20秒
        return driver

    def get_driver_android_app(self):
        if self.reset == 'Reset':
            no_reset = False
        elif self.reset == 'noReset':
            no_reset = True

        driver = self.get_driver_android(no_reset)
        return driver
        

# 封装所有driver获取，因此命名为get_driver
def get_driver(form, *parm):

    if form == 'Chrome':
        driver = GetDriverWeb('chrome').get_driver_web()
    elif form == 'H5':
        driver = GetDriverWeb('h5').get_driver_web()
    elif form == 'Android':
        reset = parm[0]  # 是否重启，目前支持'Reset'\'noReset'
        driver = GetDriverAndroid(reset).get_driver_android_app()
    else:
        print('参数错误请检查')
    return driver


if __name__ == "__main__":
    get_driver('Chrome')
    get_driver('H5')
    get_driver('Android', 'Reset')
    get_driver('Android', 'noReset')
