from celery_tasks.main import app

@app.task
def sms(mobile, sms_code):
    from ronglian_sms_sdk import SmsSDK

    accId = '容联云通讯分配的主账号ID'
    accToken = '容联云通讯分配的主账号TOKEN'
    appId = '容联云通讯分配的应用ID'
    sdk = SmsSDK(accId, accToken, appId)

    tid = '1'
    mobile = mobile
    datas = (sms_code, 10)
    sdk.sendMessage(tid, mobile, datas)
