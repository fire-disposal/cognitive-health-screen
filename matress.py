import datetime

class MattressData:
    def __init__(self, hb=None, br=None, od=None, p=None, st=None, we=None, wt=None, sn=None, fv=None):
        self.hb = hb
        self.br = br
        self.od = od
        self.p = p
        self.st = st
        self.we = we
        self.wt = wt
        self.sn = sn
        self.fv = fv
        self.type = None
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sleepState = '0'

class HealthEventManager:
    """高级健康事件管理，包括心跳/呼吸报警、褥疮保护、翻身检测、数据起止统计"""
    def __init__(self):
        self.heart_threshold = {}
        self.breath_threshold = {}
        self.bedsore_flag = {}
        self.turn_time_count = {}
        self.judge_turn_record = {}
        self.drop_line_flag = {}
        self.abnormal_events = []

    def check_heart_alarm(self, data, heart_lower, heart_upper, heart_threshold):
        sn = data.sn
        if sn not in self.heart_threshold:
            self.heart_threshold[sn] = 0
        if data.hb is not None and (data.hb < heart_lower or data.hb > heart_upper):
            self.heart_threshold[sn] += 1
            if self.heart_threshold[sn] >= heart_threshold:
                data.type = 0  # 心跳报警
                self.abnormal_events.append(('heart', sn, data.time))
                return True
        else:
            self.heart_threshold[sn] = 0
        return False

    def check_breath_alarm(self, data, breath_lower, breath_upper, breath_threshold):
        sn = data.sn
        if sn not in self.breath_threshold:
            self.breath_threshold[sn] = 0
        if data.br is not None and (data.br < breath_lower or data.br > breath_upper):
            self.breath_threshold[sn] += 1
            if self.breath_threshold[sn] >= breath_threshold:
                data.type = 1  # 呼吸报警
                self.abnormal_events.append(('breath', sn, data.time))
                return True
        else:
            self.breath_threshold[sn] = 0
        return False

    def bedsore_check(self, data, bedsore_flag):
        sn = data.sn
        if bedsore_flag == 1:
            self.bedsore_flag[sn] = True
            self.judge_turn(data)
        else:
            self.bedsore_flag[sn] = False

    def judge_turn(self, data):
        sn = data.sn
        if sn not in self.turn_time_count:
            self.turn_time_count[sn] = 0
            self.judge_turn_record[sn] = {'time': data.time, 'p': data.p}
        else:
            last = self.judge_turn_record[sn]
            time_now = datetime.datetime.strptime(data.time, "%Y-%m-%d %H:%M:%S")
            time_last = datetime.datetime.strptime(last['time'], "%Y-%m-%d %H:%M:%S")
            diff_time = (time_now - time_last).total_seconds() / 60
            if diff_time > 120:
                data.type = 3  # 褥疮报警
                self.abnormal_events.append(('bedsore', sn, data.time))
            # 翻身判定（假设p为整数或可比较的体位参数）
            if data.p is not None and last['p'] is not None and abs(int(data.p) - int(last['p'])) >= 2:
                self.turn_time_count[sn] += 1
                self.judge_turn_record[sn] = {'time': data.time, 'p': data.p}

    def get_start_and_end(self, arr):
        """统计数据起止时间"""
        if not arr:
            return None
        start_time = arr[0].time
        end_time = arr[-1].time
        for d in arr:
            if d.st != 'off':
                start_time = d.time
                break
        for d in reversed(arr):
            if d.st != 'off':
                end_time = d.time
                break
        return {'startTime': start_time, 'endTime': end_time}

class WarningPushManager:
    """警告推送管理，模拟推送接口"""
    def __init__(self):
        self.push_records = []

    def push_warning(self, data):
        # 这里只做记录，实际可集成推送接口
        self.push_records.append({'sn': data.sn, 'type': data.type, 'time': data.time})

class MattressAnalyzer:
    def __init__(self, health_event_manager, warning_push_manager):
        self.sn_socket = []
        self.sleepRecordArr = []
        self.abnormal_judgect = 0
        self.health_event_manager = health_event_manager
        self.warning_push_manager = warning_push_manager

    def data_filter(self, data):
        temp = {
            'sn': data.sn,
            'sleepState': data.sleepState,
            'hb': data.hb,
            'br': data.br,
            'od': data.od,
            'p': data.p,
            'st': data.st,
            'we': data.we,
            'wt': data.wt
        }
        flag = 0
        for x in self.sn_socket:
            if x['sn'] == temp['sn']:
                if x == temp or (x['st'] == 'off' and temp['st'] == 'off'):
                    flag = 1
                else:
                    x.update(temp)
                    flag = 2
                break
        if flag == 0:
            self.sn_socket.append(temp)
        return flag

    def manage(self, content, thresholds, bedsore_flag=0):
        # thresholds: {'heart_lower': xx, 'heart_upper': xx, 'heart_threshold': xx, 'breath_lower': xx, 'breath_upper': xx, 'breath_threshold': xx}
        mydata = MattressData(**content)
        if self.abnormal_judgect == 10:
            mydata.type = 4
        if mydata.st == "off" and mydata.we and int(mydata.we) > 17:
            self.abnormal_judgect += 1
        else:
            self.abnormal_judgect = 0
        if mydata.type == 0 and mydata.st == 'off':
            mydata.type = None
        mydata.sleepState = self.get_sleep_state(mydata)
        # 心跳/呼吸报警
        heart_alarm = self.health_event_manager.check_heart_alarm(
            mydata, thresholds['heart_lower'], thresholds['heart_upper'], thresholds['heart_threshold']
        )
        breath_alarm = self.health_event_manager.check_breath_alarm(
            mydata, thresholds['breath_lower'], thresholds['breath_upper'], thresholds['breath_threshold']
        )
        # 褥疮保护与翻身检测
        self.health_event_manager.bedsore_check(mydata, bedsore_flag)
        # 推送警告
        if heart_alarm or breath_alarm or mydata.type in [3, 4]:
            self.warning_push_manager.push_warning(mydata)
        return mydata

    def get_sleep_state(self, params):
        sn = params.sn
        st = params.st
        result = '0'
        time = params.time
        flag = False
        for temp in self.sleepRecordArr:
            if temp['sn'] == sn:
                flag = True
                if temp['time'] != time:
                    if temp['st'] != st:
                        temp['st'] = st
                        temp['time'] = time
                    timeRecord = datetime.datetime.strptime(temp['time'], "%Y-%m-%d %H:%M:%S")
                    timeNow = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    timeDiff = (timeNow - timeRecord).total_seconds()
                    if st == "on":
                        if temp['sleepState'] == '0' and timeDiff >= 240:
                            temp['sleepState'] = '1'
                        elif temp['sleepState'] == '1' and timeDiff > 420:
                            temp['sleepState'] = '2'
                        elif temp['sleepState'] == '2' and timeDiff > 840:
                            temp['sleepState'] = '3'
                    elif st == 'mov':
                        if temp['sleepState'] == '2' and timeDiff >= 40:
                            temp['sleepState'] = '0'
                        elif temp['sleepState'] == '3':
                            temp['sleepState'] = '2'
                            if timeDiff >= 40:
                                temp['sleepState'] = '0'
                    elif st == 'off':
                        temp['sleepState'] = '0'
                        temp['time'] = time
                else:
                    temp['st'] = st
                result = temp['sleepState']
                break
        if not flag:
            temp = {
                'sn': sn,
                'st': st,
                'sleepState': '0',
                'time': time
            }
            self.sleepRecordArr.append(temp)
            result = '0'
        return result

# 示例用法
if __name__ == "__main__":
    health_event_manager = HealthEventManager()
    warning_push_manager = WarningPushManager()
    analyzer = MattressAnalyzer(health_event_manager, warning_push_manager)
    # 假设 raw_data 已经解析为字典
    raw_data = {
        'hb': 75,
        'br': 18,
        'od': 0,
        'p': 3,
        'st': 'on',
        'we': 20,
        'wt': 1,
        'sn': 'SN123456',
        'fv': 0
    }
    thresholds = {
        'heart_lower': 60,
        'heart_upper': 100,
        'heart_threshold': 3,
        'breath_lower': 12,
        'breath_upper': 20,
        'breath_threshold': 3
    }
    bedsore_flag = 1
    data = analyzer.manage(raw_data, thresholds, bedsore_flag)
    flag = analyzer.data_filter(data)
    print("分析结果:", vars(data))
    print("过滤标志:", flag)
    print("健康事件:", health_event_manager.abnormal_events)
    print("推送记录:", warning_push_manager.push_records)
    # 数据起止时间统计示例
    arr = [data]
    print("起止时间统计:", health_event_manager.get_start_and_end(arr))