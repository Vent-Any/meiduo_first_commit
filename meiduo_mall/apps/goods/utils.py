def get_breadcrumb(category):
    """
    获取面包屑导航
    :param category: 商品类别
    :return: 面包屑导航字典
    """
    breadcrumb = dict(
        cat1='',
        cat2='',
        cat3=''
    )

    # 当前类别为三级
    breadcrumb['cat3'] = category.name
    breadcrumb['cat2'] = category.parent.name
    breadcrumb['cat1'] = category.parent.parent.name

    return breadcrumb