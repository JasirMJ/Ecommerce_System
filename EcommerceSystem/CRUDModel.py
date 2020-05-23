#
# class PagesView(ListAPIView):
#     serializer_class = SerializerClass
#     def get_queryset(self):
#         queryset = ModelName.objects.all()
#         return queryset
#
#     def post(self,request):
#         try:
#             serializer = SerializerClass(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             # serializer.is_valid(raise_exception=True)
#             obj = serializer.save()
#             print("Data id or object : ",obj.id)
#             return Response(
#                 {
#                     STATUS: True,
#                     MESSAGE:"Data created "+str(obj.id)
#                 }
#             )
#         except Exception as e:
#             printLineNo()
#             return Response(
#                 {
#                     STATUS: False,
#                     MESSAGE: e.detail,
#                     "line_no": printLineNo()
#                 }
#             )
#
#     def put(self,request):
#         id = self.request.POST.get("id")
#         if not id or id =="":
#             return Response({
#                 STATUS:False,
#                 MESSAGE:"Required object id as id"
#             })
#         serializer = SerializerClass(ModelName.objects.filter(id=id).first(), data=request.data,partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 STATUS: True,
#                 MESSAGE: "Data updated",
#                 # "Data": request.data
#             }
#         )
#
#     def delete(self,request):
#         try:
#             id = self.request.POST.get('id', "")
#             if id == "" or not id:
#                 ModelName.objects.all().delete()
#                 return Response(
#                     {
#                         STATUS: True,
#                         MESSAGE: "Deleted all data",
#                     }
#                 )
#             else:
#                 id = json.loads(id)
#                 print(id)
#                 ModelName.objects.filter(id__in=id).delete()
#                 return Response(
#                     {
#                         STATUS: True,
#                         MESSAGE: "Deleted data having id " + str(id),
#                     }
#                 )
#         except Exception as e:
#             printLineNo()
#             return Response(
#                 {
#                     STATUS: False,
#                     MESSAGE: str(e),
#                     "line_no": printLineNo()
#                 }
#             )
