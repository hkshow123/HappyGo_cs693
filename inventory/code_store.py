# def inventory_edit(request):
#     error_message = None
#     # id is an instance
#     id = request.POST.get("obj_id")
#     print("-post--id:", id)
#     # Get the product object with the given 'id'
#     inventory_obj = get_object_or_404(ProductInventory, id=id)
#     # product = Product.objects.get(id=id)
#     print("----second0000---- and id-")
#
#     if request.method == "POST":
#         print("----first POST-----")
#         form = ProductInventoryForm(request.POST, instance=inventory_obj)
#         print(form)
#         print("----second POST---form created--")
#         print("----third POST-----", request.POST)
#         upc = request.POST.get("upc")
#
#         print("----third POST-----",upc)
#
#         retail_price = request.POST.get("retail_price")
#         print("----third POST----", retail_price)
#         retail_price = form.cleaned_data["retail_price"]
#         store_price = form.cleaned_data["store_price"]
#         total = form.cleaned_data["total"]
#         location = form.cleaned_data["location"]
#         is_active = form.cleaned_data["is_active"]
#         print(upc, retail_price, store_price, total, location, is_active)
#         if form.is_valid():
#             print("----second1111-----")
#             # fields = ['upc', 'retail_price', 'store_price', 'total', 'location', 'is_active']
#             upc = form.cleaned_data["upc"]
#             retail_price = form.cleaned_data["retail_price"]
#             store_price = form.cleaned_data["store_price"]
#             total = form.cleaned_data["total"]
#             location = form.cleaned_data["location"]
#             is_active = form.cleaned_data["is_active"]
#
#             # Update the product object with new data
#             inventory_obj.upc = upc
#             inventory_obj.retail_price = retail_price
#             inventory_obj.total = total
#             inventory_obj.store_price = store_price
#             inventory_obj.location = location
#             inventory_obj.is_active = is_active
#             inventory_obj.update_at = formatted_time
#             inventory_obj.save()
#
#             print("----inventory_obj_saved")
#             return redirect("inventory:inventory_mg")
#
#         else:
#             print(form.errors)
#             print("----second33333-----")
#             error_message = "Invalid data. Please check your input."
#     else:
#         form = ProductForm(instance=inventory_obj)
#     category_list = Category.objects.all()
#     type_list = ProductType.objects.all()
#     brand_list = Brand.objects.all()
#     product_list = Product.objects.all().order_by("name")
#     inventory_list = ProductInventory.objects.all()
#     print("-----five-----")
#     content = {
#         "category_list": category_list,
#         "type_list": type_list,
#         "brand_list": brand_list,
#         "product_list": product_list,
#         "inventory_list": inventory_list,
#         "form": form,
#         "error_message": error_message,
#         # "product":product,
#     }
#
#     return render(request, "inventory.html", content)





# def search(request):
#     print("-------search page-------")
#     error_message = None
#     category_list = Category.objects.all()
#     type_list = ProductType.objects.all()
#     brand_list = Brand.objects.all()
#     product_list = Product.objects.all().order_by("product_id")
#     location_list = Location.objects.filter(is_active=True)
#
#     def sub_search(request,inventory_list):
#         for obj in inventory_list:
#             obj.product_obj = Product.objects.get(upc=obj.upc)
#
#         content = {
#             "category_list": category_list,
#             "type_list": type_list,
#             "brand_list": brand_list,
#             "product_list": product_list,
#             "inventory_list": inventory_list,
#             "location_list": location_list,
#         }
#         return render(request, "inventory.html", content)
#
#     inventory = ProductInventory.objects.all()
#     if request.method == "POST":
#         doc_type = request.POST.get("doc_type")
#         keywords = request.POST.get("keyword")
#         print("doc_type and keyword",doc_type, keywords)
#         if doc_type == "Name":
#             inventory_list = inventory.filter(product_name__name__icontains=keywords).order_by("product_id")
#             sub_search(request,inventory_list)
#         elif doc_type == "ID":
#             if keywords.isdigit():
#                 inventory_list = inventory.filter(product_name__id__icontains=keywords).order_by("product_id")
#                 sub_search(request,inventory_list)
#         else:
#             inventory_list = inventory.filter(upc=keywords).order_by("product_id")
#             sub_search(request,inventory_list)
#
#     return sub_search(request, inventory)

