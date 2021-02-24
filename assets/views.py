from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from assets import models
from assets import asset_handler
from django.shortcuts import get_object_or_404


# Create your views here.
@csrf_exempt
def report(request):
    """
    通过csrf_exempt 装饰器，跳过Django的csrf安全机制，让post的数据能够接收，但这又会带来安全问题。
    可以再客户端，使用自定义认证token，进行身份验证，这部分工作，根据实际情况，自己进行
    :param request:
    :return:
    """
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据！')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须是字典格式')
        sn = data.get('sn', None)
        if not sn:
            return HttpResponse('没有资产sn序列号，请检查数据！')
        else:
            # 进入审批流程
            # 首先判断是否在上线资产存在该sn
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                # 进入已经上线资产的数据更新流程
                return HttpResponse('资产数据已更新！')
            else:
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
    return HttpResponse('200 ok')


def index(request):
    assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())


def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()
    up_rate = round(upline/total*100)
    o_rate = round(offline/total*100)
    un_rate = round(unknown/total*100)
    bd_rate = round(breakdown/total*100)
    bu_rate = round(backup/total*100)
    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()
    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详情为例，安全设备，存储设备，网络设备等参照此例
    :param request:
    :return:
    """

    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assets/detail.html', locals())
