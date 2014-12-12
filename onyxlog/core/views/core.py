from django.shortcuts import render

def error403(request):
    """
    Renderiza o template de erro 403
    """
    return render(request,'error403.html',{},status=403)

def error404(request):
    """
    Renderiza o template de erro 404
    """
    return render(request,'error404.html',{},status=404)

def error500(request):
    """
    Renderiza o template de erro 500
    """
    return render(request,'error500.html',{},status=500)