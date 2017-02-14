import myLib

product_id = "7924592"
product_infos ={}
product_infos["name"] = "Test"
product_infos["stock_dispo"] = "3"
product_infos["stock_cmd"] = "-3"
product_infos["product_category_id"] = "285696"

myLib.update_stock_movement("297973", "-3", product_id)#, "10267102")
myLib.update_stock_movement("297978", "3", product_id)#, "10267097")



