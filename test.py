catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
for product in products_actual:
    print product