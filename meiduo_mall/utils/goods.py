"""
分类数据
"""
from collections import OrderedDict
from apps.goods.models import GoodsCategory
from apps.goods.models import GoodsChannel


def get_categories():
    """
    提供商品频道和分类
    :return 菜单字典
    """
    # 查询商品频道和分类
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 构建当前类别的子类别
        for cat2 in cat1.subs.all():
            cat2.sub_cats = []
            for cat3 in cat2.subs.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)
    return categories


"""
首页广告数据
"""
from apps.contents.models import ContentCategory
def get_contents():
    # 定义字典
    contents = {}
    # 查询数据
    content_categories = ContentCategory.objects.all()
    # 遍历分类数据
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
    # 返回响应
    return contents


"""
面包屑
"""


def get_breadcrumb(category):
    dict = {
        'cat1': '',
        'cat2': '',
        'cat3': '',
    }

    dict['cat3'] = category.name
    dict['cat2'] = category.parent.name
    dict['cat1'] = category.parent.parent.name

    return dict


"""
规格选项
"""


def get_goods_specs(sku):
    # 构建当前商品的规格键
    sku_specs = sku.specs.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        sku_key.append(spec.option.id)

    # 获取当前商品的所有SKU
    skus = sku.spu.sku_set.all()
    # 构建不同规格参数（选项）的sku字典
    spec_sku_map = {}
    for s in skus:
        # 获取sku的规格参数
        s_specs = s.specs.order_by('spec_id')
        # 用于形成规格参数-sku字典的键
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        # 向规格参数-sku字典添加记录
        spec_sku_map[tuple(key)] = s.id

    # 以下代码为：在每个选项上绑定对应的sku_id值
    # 获取当前商品的规格信息
    goods_specs = sku.spu.specs.order_by('id')
    # 若当前sku的规格信息不完整，则不再继续
    if len(sku_key) < len(goods_specs):
        return
    for index, spec in enumerate(goods_specs):
        # 复制当前sku的规格键
        key = sku_key[:]
        # 该规格的选项
        spec_options = spec.options.all()
        for option in spec_options:
            # 在规格参数sku字典中查找符合当前规格的sku
            key[index] = option.id
            option.sku_id = spec_sku_map.get(tuple(key))
        spec.spec_options = spec_options

    return goods_specs
