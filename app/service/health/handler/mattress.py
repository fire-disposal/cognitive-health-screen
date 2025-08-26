from typing import Any, Dict, List,Optional
from app.service.health.handler.base import EventHandler, HealthDataEvent

class MattressHandler(EventHandler):
    """
    床垫数据插件：解析-分析-告警一体化
    支持参数化阈值与事件管理，风格统一

    示例:
    原始数据 raw_data:
        {
            "sn": "设备序列号",
            "d": {
                "hb": 72,
                "br": 18,
                "st": 1,
                "we": 65,
                "wt": 3600,
                "od": 0,
                "fv": 0,
                "p": 1
            }
        }
    解析后数据 parsed_data:
        {
            "sn": "设备序列号",
            "hb": 72,
            "br": 18,
            "st": 1,
            "we": 65,
            "wt": 3600,
            "od": 0,
            "fv": 0,
            "p": 1,
            "raw": {...}
        }
    分析结果 analysis_result:
        {
            "risk": "正常",
            "hb": 72,
            "br": 18
        }
    告警 alerts:
        [
            {
                "rule_name": "床垫异常",
                "level": "info",
                "message": "离床或心率异常",
                "event_type": "mattress",
                "description": "自动检测床垫数据异常",
                "extra": {"hb": 72, "od": 1},
                "status": "active"
            }
        ]
    """

    def __init__(self, thresholds: Dict[str, Any] = None):
        self.name = "床垫支持"
        self.thresholds = thresholds or {
            "heart_lower": 40,
            "heart_upper": 120,
            "heart_threshold": 3,
            "breath_lower": 8,
            "breath_upper": 30,
            "breath_threshold": 3,
        }
        self.event_manager = MattressEventManager()

    async def can_handle(self, event: HealthDataEvent) -> bool:
        return event.event_type == "mattress_received"

    async def handle(self, event: HealthDataEvent) -> Optional[Dict[str, Any]]:
        # 解析数据
        d = event.data
        hb = d.get("hb")
        br = d.get("br")
        we = d.get("we")
        # 异常值过滤
        if hb is not None and (hb < 20 or hb > 250):
            return None
        if br is not None and (br < 4 or br > 100):
            return None
        if we is not None and (we < 10 or we > 300):
            return None

        # 分析逻辑
        patient_id = event.patient_id
        history_records = None
        # 可集成历史查询服务
        # if self.history_query and patient_id:
        #     history_records = await self.history_query(patient_id, "mattress", limit=10)

        analysis_result = self.event_manager.analyze(d, self.thresholds, history_records=history_records)
        alerts = self.event_manager.generate_alert(analysis_result)
        return {
            "analysis_result": analysis_result,
            "alerts": alerts
        }


class MattressEventManager:
    """
    床垫事件管理器，封装 matress.py 的核心分析与告警逻辑
    """

    def __init__(self):
        self.heart_threshold = {}
        self.breath_threshold = {}
        self.bedsore_flag = {}
        self.turn_time_count = {}
        self.judge_turn_record = {}
        self.abnormal_events = []
        self.max_history_minutes = 1440  # 默认保留24小时历史

    def analyze(self, data: Dict[str, Any], thresholds: Dict[str, Any], history_records=None) -> Dict[str, Any]:
        import datetime
        hb = data.get("hb")
        br = data.get("br")
        sn = data.get("sn")
        st = data.get("st")
        p = data.get("p")
        time_str = data.get("time") or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bedsore_flag = data.get("bedsore_flag", 0)
        risk = "正常"
        type_code = None

        # 历史数据辅助分析（如连续异常、趋势判断等）
        if history_records and isinstance(history_records, list) and len(history_records) > 0:
            abnormal_count = sum(1 for r in history_records if r.get("risk") and r.get("risk") != "正常")
            if abnormal_count >= 3:
                risk = "历史连续异常"
                type_code = 99

        # 清理历史数据，只保留 max_history_minutes 内的
        self._cleanup_history(time_str)

        # 心率报警
        if hb is not None and (hb < thresholds["heart_lower"] or hb > thresholds["heart_upper"]):
            self.heart_threshold[sn] = self.heart_threshold.get(sn, 0) + 1
            if self.heart_threshold[sn] >= thresholds["heart_threshold"]:
                risk = "心率异常"
                type_code = 0
                self.abnormal_events.append(("heart", sn, time_str))
        else:
            self.heart_threshold[sn] = 0

        # 呼吸报警
        if br is not None and (br < thresholds["breath_lower"] or br > thresholds["breath_upper"]):
            self.breath_threshold[sn] = self.breath_threshold.get(sn, 0) + 1
            if self.breath_threshold[sn] >= thresholds["breath_threshold"]:
                risk = "呼吸异常"
                type_code = 1
                self.abnormal_events.append(("breath", sn, time_str))
        else:
            self.breath_threshold[sn] = 0

        # 褥疮报警与翻身检测
        if bedsore_flag == 1:
            self.bedsore_flag[sn] = True
            if sn not in self.turn_time_count:
                self.turn_time_count[sn] = 0
                self.judge_turn_record[sn] = {'time': time_str, 'p': p}
            else:
                last = self.judge_turn_record[sn]
                try:
                    time_now = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    time_last = datetime.datetime.strptime(last['time'], "%Y-%m-%d %H:%M:%S")
                    diff_time = (time_now - time_last).total_seconds() / 60
                    if diff_time > 120:
                        risk = "褥疮风险"
                        type_code = 3
                        self.abnormal_events.append(("bedsore", sn, time_str))
                    if p is not None and last['p'] is not None and abs(int(p) - int(last['p'])) >= 2:
                        self.turn_time_count[sn] += 1
                        self.judge_turn_record[sn] = {'time': time_str, 'p': p}
                except Exception:
                    pass
        else:
            self.bedsore_flag[sn] = False

        return {
            "risk": risk,
            "hb": hb,
            "br": br,
            "type": type_code,
            "sleepState": "0",
            "bedsore_flag": bedsore_flag,
            "turn_count": self.turn_time_count.get(sn, 0)
        }

    def _cleanup_history(self, now_time_str):
        import datetime
        now = datetime.datetime.strptime(now_time_str, "%Y-%m-%d %H:%M:%S")
        # judge_turn_record
        keys_to_del = []
        for sn, record in self.judge_turn_record.items():
            try:
                t = datetime.datetime.strptime(record['time'], "%Y-%m-%d %H:%M:%S")
                if (now - t).total_seconds() > self.max_history_minutes * 60:
                    keys_to_del.append(sn)
            except Exception:
                keys_to_del.append(sn)
        for sn in keys_to_del:
            self.judge_turn_record.pop(sn, None)
            self.turn_time_count.pop(sn, None)
            self.heart_threshold.pop(sn, None)
            self.breath_threshold.pop(sn, None)
            self.bedsore_flag.pop(sn, None)

    def generate_alert(self, analysis_result: Dict[str, Any]) -> List[Dict]:
        alerts = []
        risk = analysis_result.get("risk")
        if risk != "正常":
            alerts.append(
                {
                    "rule_name": "床垫异常",
                    "level": "info",
                    "message": f"{risk}",
                    "event_type": "mattress",
                    "description": "自动检测床垫数据异常",
                    "extra": {
                        "hb": analysis_result.get("hb"),
                        "br": analysis_result.get("br"),
                        "type": analysis_result.get("type"),
                        "sleepState": analysis_result.get("sleepState"),
                    },
                    "status": "active",
                }
            )
        return alerts