import myLib

ID_USER=387394

url="https://www.incwo.com/customer_product_categories/list/387394.xml"
response = myLib.send_request("get", url)
for l in response.splitlines():
    if "<id>" in l:
        id = l[8:-5]
        print url
        url="https://www.incwo.com/customer_product_categories/destroy/"+str(ID_USER)+"/"+id+".xml"
        myLib.send_request("post", url)
