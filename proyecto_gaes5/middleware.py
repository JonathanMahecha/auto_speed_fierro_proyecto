# from django.shortcuts import redirect

# class RedirectIfAuthenticatedMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if request.path in ['/login/', '/registro/', '/index/']:
#                 # Si el usuario ya está autenticado y trata de acceder a las páginas de login, registro o index,
#                 # lo redirigimos a una página apropiada, por ejemplo, el panel de administración.
#                 return redirect('Menu')  # Cambiar 'Menu' por la URL a la que deseas redirigir al usuario
#         return self.get_response(request)

