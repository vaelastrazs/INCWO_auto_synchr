from lxml import etree

catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
for product in catalog_actual.xpath("/customer_products/customer_product"):
    print product