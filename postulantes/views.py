from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime

from django.urls import reverse
from .forms import PostulanteForm
from .models import Postulante
from .utils import generar_pdf_postulante, enviar_pdf_por_correo

from reportlab.lib.pagesizes import A4
from django.http import HttpResponse


def registro_postulante(request):
    if request.method == 'POST':
        form = PostulanteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                postulante = form.save()  # Se guarda el registro
                pdf = generar_pdf_postulante(postulante)
                enviar_pdf_por_correo(postulante, pdf)
                return redirect(reverse('postulantes:registro_exitoso'))
            except Exception as e:
                # Registra o imprime el error para saber qué falla
                print("Error en el proceso de registro:", e)
                form.add_error(None, "Ocurrió un error durante el registro. Inténtelo nuevamente.")
        else:
            print(form.errors)
    else:
        form = PostulanteForm()
    return render(request, 'postulantes/formulario.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'postulantes/registro_exitoso.html')


def listar_postulantes(request):
    postulantes = Postulante.objects.all()
    return render(request, 'postulantes/listar.html', {'postulantes': postulantes})


def postulante_print(self, pk=None):  
    import io  
    from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle  
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
    from reportlab.lib import colors  
    from reportlab.lib.pagesizes import letter  
    from reportlab.platypus import Table, Image, SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Frame
    from reportlab.lib.units import cm, inch, mm
    from reportlab.rl_settings import canvas_basefontname
    from reportlab.lib.fonts import tt2ps
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
  
    
    response = HttpResponse(content_type='application/pdf')  
    buff = io.BytesIO()  
    doc = SimpleDocTemplate(
        buff,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
        title='Ficha de inscripción',
        author='IESTP - ARIB',
    ) 
    elements = []  
    styles = getSampleStyleSheet()
    titulo1 = ParagraphStyle(name='Titulo1',
                             parent=styles['Heading3'],
                             fontName=tt2ps(canvas_basefontname, 1, 0),
                             fontSize=12,
                             leading=14,
                             spaceBefore=10,
                             spaceAfter=1,
                             alignment=TA_CENTER
                             )
    titulo2 = ParagraphStyle(name='Titulo2',
                             parent=styles['Heading3'],
                             fontName=tt2ps(canvas_basefontname, 1, 0),
                             fontSize=12,
                             leading=14,
                             spaceBefore=0,
                             spaceAfter=20,
                             alignment=TA_CENTER
                             )

    secciones = styles['Heading4']
    cabecera = ParagraphStyle(name='Cabecera',
                              parent=styles['Normal'],
                              alignment=TA_CENTER,
                              fontSize=8,
                              leading=10
                              )

    paragraph = styles['Normal']
    paragraph.alignment = TA_JUSTIFY

    firma = ParagraphStyle(name='firma',
                           fontName=styles['Normal'],
                           alignment=TA_CENTER,
                           fontSize=10,
                           leading=10)

    lugar_fecha = styles['Italic']
    lugar_fecha.alignment = TA_RIGHT
    image1 = Image('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAB7CAMAAAB6t7bCAAACBFBMVEX+/v5YWFriABr///9UVFZPT1HgAACxsbJ/f4DZECPiABXyr7KUlJXlIjP3zdD40tWGhogAfqhKSkzr6+v29vbd3d7uiI7bACThAAn52dzX19eNjY6enp+3t7fjFCMAcpPRAADqbHNxcXLq3qt5eXplZWb77u7f16zMzM30trtZiXFCQkXrdnvXvADAwMCoqKnZERXoUFrHAADoywDcwAA+OzzpXGTKDyHKsQA0MTKfva1qamsAfa7p5OXfsbTxpanRghkAgKjHWRPs0wDDqwC9AAArJygaFRcBAADI186Otp3c5+FjoH4AYR5GjGNWkG8rckskf02bwKp3p4xchG8xdlMAbjKqubFymIQFeT8AaTeElo64xr9xiX0ofU9LhmePqZs3ilvf3c3PyqpOlG7Ku2Xq6Nu3p0zNxZDFuXTs5sbOukuznAC9hivg1MK4jjcbhU/Uk5fEnnjCNQC7ZADISlK7SADKiY4AUADEqFy/JzOsgUCsrErezoGCpJO9ro7IYWvGqKpXgjqXpVp+lV8AbHmzbRU9g4nUf4c+g3d4VB+VZia9Mzxcg1jFmWGhnIzXfwBFcoGHdVV6cVuIlXqXcEOtKRiCgUvDjUmrbiHKi0D228Hls35tho+TtMUAaIqkgwZFjKqeln6QeDvIMgDDnjvQlwzGUQDQowfQjQ/GmYe4DR4+0OfAAAAV30lEQVR4nO2di0MTV77HJ5yZJEOjJvPoQB4YMdHUyCQEMJAQRERbCKJCi+halK51ka2tloCre+vi3l5qu1Ztd+3t3t3a2su17fWfvL/fOZN3AugNj3t7vmqYzJwZ5Hz4Pc7vnJkIAhcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcX18uLEGK94CtZr+1maVMvvhO1AS5azIRXUScCUWMROKX+SWRP067NUdMeQvzOX5FCsTXZAAU9I/RFnF5i2kLwzmyP9RCi10VKdtubN0d2QOOWxF+PJNcaFkAEjZCAT3eiddn0k/DOZZJ2r94n+rXacABN0+aIohFtvx6JddGg34q54PWkdpJoIa3Pl4Z3NpX0aW4fiQimt9aZHE3DVBcNUZ3RGDmJ5qLGJCUSMYnggzfpsI/0mbYIOalyNJuq2mjAYMib3owi+AIZl8NBNJqf0RwJfFykB1IBl58lbBzNZqkmGuLSYsTscZpR9U23bkEp8XNqLKyepKC8gYrTOZqGqTYanbTHSI/uD5FquxBYPu0KI7Men7P8OEfTMNVCQ9QoIX06+q26IxhCVPBqYRuRvGXwOJqGqQYaohIwF922znAUDvvd3r524ihN1TiahqkaDXH3tJOwO2yuXyeg2UEsbNNLQhFH0yhVoSFOF6bMgcy6ZDBdg4xBcRJJKzTmaBqmSjQQQ3rC3trRvxYc9S1iuolQGONwNA1TBRoS8QObyMa40BN0RYO0Qcmj5GgapnI0RFNIiGi+qvhTv1RNdK/jrYDXydE0WhVoQj6Xqbore5+kRoTRrKbBi5qqrGsSvV3rC5y09nI0DVMZGjAJ11uqVF4cAzBjp8ZHTx86c+jM3bMTp8YnK9kQb7tDJQwZR9MwlaIhQthJ9JNmJZk/zE6Oj7z9zpXT77ydmpg8MzWmVbDxmSTSFzBxN0fTMJWhcUdCpqlXkJk8dWHk3LnpS+cvXJh65/RvLl58Z2qmnA2Mb8Jhlag6R9NIlaAh+pua5PRVuLPxM2dG3r00c2rm/OjFmdmpC5fejly6MJOtyOtCMBIKc4fWUJVZjXkyVJGBkezU5OVL78xcybLsTJ08P3PpN9NTqQrTUhw9To2jaagq0gCHUhFGRmcvvz0+Ppu3EiKMjc9cunx6poKgGlPZHo6mYaoccrL+LQwgs1PA4ezsSNHrqeOz49OpU3mzIZVnbCEaSVEUqXRLzL8v+fkUpQqnWA8wXKYhndoYVYxr2Ot7B69aW9rM3XOjZ0dLLWvk7OTFy1PZfIODvyUlp24lGiWjaVoGO1NRYUtXxJCgecs7V/JrmqMCl9Qeqs1G8WpC+86xy3KHZo1NtN5h1tVk5Mp06vz5yTI056fuTk9atMj7vfNlE9FbiUbF6BeGrTANg4CGEL0CTQzyk3I0koP46qDRCdmxaN7vpeZCrh78HWVD1LOpyzOz5WiuTKVS50cYkLlrjIzw+w+0rY41ikor3yKYBm5sEI0UIf8n0Vzt/T1DIpy4ziCNTU5PTJU7NMjZ7s7SbhGundjDgMz17t/yQg1DY0rY2xQN9LuEDSQJ/9FNm2h9lSRFooiigMatsEMKO0ZPw3+iZFGUCoe2URWxhnz4EZ2F8SbacmgPJDWTunyj3GrOXkpNn6YgPwombtKVyNc+3oY0ANBoOhKBDZ2iCfv9YBDtfn+74o9E/ABADPn9TuhzMWZGIjEbnO4C0wj403C604yYDJLf77aZEZfk8/vRP0q2WCTiSG93SlCZoWWCK4CEDCRkY2EOPPjk1N3Lp+mohsV6IkxOnbt89izwmM+1yclF3HU7eHN7Yo0QIAT6GzqbOjQnOjRwb8RPwxA4N+bQxHardu4URbaq3ScqEboH0wYIVSacoPUwh6b4WePANrOpRmMsHSRkMS7LRuI2ZARjM6fPjF4YIbRABtn0oelLh8ZngNXcgiHLyaBG5lfiLQPbhMZHiEtxwYFiGoBoABT8fyEOMTSYMOiRDOwXJQuNAlBJBrYiCqJBdIEoRSO5rLmP7WZTjUY2Vq9ptxZlUBwCTnbqyvTdy6dmxlOEZC9M/uHu9PQkFgNuJ4CMfOe+fnDIkIPbhQYMxoyahIhlaATii/Z44ZBE0ShoFn1Kj1fzglHg8kZwW9D36SgyC4thXHTfDl6QolEgTTWVKF4lva3xpgYa2Yj/kQjBNuj5tqF/mScjY6mLh6ZHzuz/5MuRQ3dTF8dSmvb+9TiSCbaSP63CRsPRtLQ0bwQNiapE7VPp6qxSq9GjNvzljygFNILplKJRMAN0ZD4Jj5pRCQ0uJiGatCSKFI0EhqhGWboQqBzAbqkq0ahBtJZlQu4lwae1/dFz6Nr85NkLU3/+10//bf/Ba38+deHG+G/n5oQ5aNcWvKWSgRa58Whajuw7UsmmNhroQLQcpRxNRLKJvgIaiY2ABK8rj0aUwJ95Yw68b8hEciRqs5Jn9HQ4SMXz9W31aDXRQOggurYcNFb2evr7Pzv06aeHPvP0791PYMAzN7d/Hkye3I4338kIGWpmjUZj303I65XXqYkGQzZ0r18qRwMZteguohHTKosfuphHY5L8rLoX0Wi0qEDRmGhImNtBLNp5aILwf4SgOZD7zIPq7++Hfx5EA0rBH/wdvH4fkgT4kV80HE1zJyFvVF2mJhopTUdfYXFNNDZR8UWw0gH2UEBDIjGUwwUOjQ6KKqzGvSOtJnl/8Sb8N+c/7/dY+v6LvyAaNJcJnIGGLe0TeL23vPyg4WjAaGpcpSYaDNrwGxJdG40UdqcVJR1BE7HQ+DEjgwPhKM3QimgwCkGosqH1mDsv1iTjcejs+S8LZDz9D69+/P1+khpNpWbPjY+OTACe9+bAm8XjycaigfhvP0q9WXN5KlAHDa6ZiyhrolHgxRuVomwPZmhRmjDbFBzJVFgNjnyIIxqFULPNVZvaaCATuCl8WiTj8Qw+OrZ3vzAxPTumfahN3picAAM6eBADzdpo7AU1V7yne1qK71rY8cOddmiEZJoO72peF43kwJvnpHUcGsSVTMAU8AJSgFbeMH8QInizgyiWo4FTwA7RP5g7a1yjWWjaFj+kRoNxBnTs8VeQBmRHs4/Gbvw4e+VRdmIEHN7c/ThrXReN/XUr2Gq7d+EBe2txPduB5uaWzsISt9Z99PhRQjotSK1EsK+JBrpPxAoA+1UvrQaYLEPz5tMAp/VNHIqNbTskKcN2hcRyhwaJQoAdiUS3CwpTLTTJZFI2kvLDzz2evV9//df2r/b2tz/+CmONemP00d++/tuj0RtARvvdg4QB7RDN7jpoWgSWCeHLkZamln2kZL3hkRb77pL3R+FM+wH2FYymjZ1SH40UCzjgvcOBw49AANKqdCDgB1iBAJaW20veiGLMq+tmOwKQ3F494gQCrojudWBZjZ2MkzuBANbQlHQAGjt3Wg1NADQvcoMrS0m57e+eY4OPqVYeD3oQTVadvJJ6cm52Mpsl5FqiLfnNyuDKN4Yc3FMbDfRvvuvh0i3NYERFMgeamtEyCmtC0VwQzWsMzS44tG8tNFhdrnoVS4vNpW9wHpSdLVpbYnGSVCr/KkrKjqs8UzTG0JC8kFuRjdXP2x8PUv3jqh/RZCcmR7LkiZAdGRvLajnDWBpckBdW1kZD9kEg6YQGMFRB/2Z5qbY2iDXo317DQGMcheOQML8Umv/nqrpTICHLqytJ6HWIN//e/+3Dh48fD/6TqB5EM3E6dWMy+yQ7emN0bHQ+IUMjIzmENbTWNdActmO4F3CswtBYz2iwQg8dwaD9kAMcTalqoTEWBoeSBnz9e/+7//H0w398+E/1O4qGXPE+mpx9cuXKI+8VbQ6L0/LSyhCrpa2BpsXq2N2lVpMP9dbgEuM/R1OmWmigx4cQjpE79t3HT/uPvfun7/dSNNnUjZHAj09+DIzMTmRvx43k0kpu1dgYmt3roHmDo6lQTTQMTi6ZO/ZX/1NP/7sROrTBDG1kdvLck0djs6kseSjnwWwATZlDKw5kGBrULnqcoylRFZq4LBfg/OB59PSZp/9HM48GMuZR4Qt1IouTziu5pGE1XhMNpgG7CmlAIUMTIDNGNK1HQbtxT2czR1OiajRJuQDnuufps2Mez3dPi2gAzhesjHstkQezDpoDBw4IJclzgQ0aSWtJMv26Na55WTRinSV/JQ9JWr/xOr1UOKvGKsTNUhWaB4m83cht/9n/3bFnHs9Xz8rRsHH0wWCRzIvMOuMaa8hZNq5hVmMd1t5g1YKXRyM6XThrWaWwq6jiXperzkqntTspf5aY1r3elz7/1VSFRtWX40lmOfEv+5/tfebZ++zYs1I0f2Fo5lmcgbYvMtp6aIhACzUs1rRQ5WPNnsOvo83tY9nAy6NRvDX3Yw2toOJh+P4v/1uPCwpYbQDr0XXWfjZcVWh0LZJHs/pZf/9enKjB6Zr+fguN/iNbiyLkLDTBW0RdAw15fVdn5y5W3rTGNRUZmh3TN1aUeRU0kdponCUGWjgsgn2+EhrNKtvg7PVLn/9qqoFGVV/EsTBm5E4fKtWlTw6W6b8oGTkxoK2N5rCdjS8LaJoq0DQ1N0MvajgHUMymmzuJkK90viIaosUsFfe+EhoxYrKpG9Hn9W9Zaa0WGhK5jxVOORevULBMS6sGgFkeIKqwNppi/9Yb19AYhNaC9tPKXNth2FU6K1ADjYhz/VELDbwJS8V+QzRqVGLCHXhMYWisWJ4P6XimyG4ogC9hW/4q9AzaoqeHVaEVRRTz5+AmXnFr0aha5k7CvrpgpWBGcuH58+Gu57litkw11JIAkxG0l0XDYk2ZkdhxsrKtmTHCqEQftbn2pIBNateh+0MMjRTCyZeIrZBKOa1SvyUFH0kZsSEa0a2qOCsdUlU0BsWH9wbpIVyO69TRfiP0AqIJZ9D7DERVxbloMYyz2GoMN+ESrhCcp7o3zb/VQiMgnd27v82DeX68q6Orq+N4x/Hewfw+SK2N3MC9jKC+NJpOS7vsJWgQyVE7izAHOu32ptdYvXMNNGI7CyQq7s9PyWiFo4imT6HC/newthQNXWxDW3gVG86BUoVEnItjzbC/NbYNTVisyX8/3EMvwd5t2mK1mlZD0HCEFWoixlB3dy+A6eru7oDXnyma6x3DS4axOo8MaeuNoyl5PMS+lpJCDcR/jXk063Gs8GXtWc4ofmt/DO3NLUpoE64IWylroSn8TDFJTOM8tQufiVyBhna46Uf7UxTIPU1XTEBMGMK0mEPAGWqGBr+FFkAgAbwEQPZj001bQFCNhrAHBWrzq5TMNx3dXV2UTQei6cqBvSSHl4aHk3J8DgDS1kSvg6aJlM2H0am0wrc6asfuZgkZhdbZDBnBgfyjJGnJuj4a7FMB4kE7oqELAqMSLo0Nl6CxfgdiEl13BscDVWhwbU0AjmhES4uxCDTqMRGHjS7DxTWEJkODs6eqIimYlNtwISG84lor72blBTXQWMIhpZEc7LCMBsyG/u0Y/sYwBuUfhhfktm/zbYU6VoP9qbVU9G9eWidWB/LkwGwE3Gq2H2U92tpZscqgAg1dCqgw43HTNC2Ky2HxhpsCGpVK89OFmTjbGa5Cw9bWwlgSg7qkRBXRB7bjV1gbmy0N7pCiwfETELNF6VIPtoCQTXlvOZrbcdlY6jreBWQ6wGzAeKhHA7/2PDf0Q2/vgmHk1kXTZN/XVr4upnzZhv1IHkBzi9Wy2W7v3LfvSJu9pan8SpVoHGzlK6MC/20NxRaR2cpjjUiXeOD6GLEq1qCbKlxTCeEtA2CGfoxABVfF0KjMItEAHRa5GjdbbSKaTL67r0Og7+1g7gxMpwP+dNN4A7vgHzg046ereQOo/9Ct6sXL9Q4XN5tbNrDmuRJN3nsFStAUem0NNAJDg1UyvCQRvGgeBTQ4Eb3T0EAWYDwHKL1gLQinA2MNwKGcOrohszYWNoCmYarn0NBXuengRhLxRrP8D1aORmcnlzk0uuYG1+WgQ3O70tTdORUMSPTOELy6GHPm0ViXQMfm3yY0gpZHI/cOdw13DKMr6wUhHyvm9H6Ds6AWGo3ezbLVaDAN0BSRrvN3Y24ciEKKbLqKaQBRexTLo9GFtFERbYGh0aM2ROClIcQRFdEjun14+wC9R8AlpbHaJkkhGvtpGkAzCfx+wFLaJqvBO7QE8m2bnOwCHl3dw8Po1ro/eP4zs5ze52zsafwE4026nA4zta1GQ52UHnKqNEPDDnPRkma6iEbzMulOCR+L7Ej7WfKMmbQr7KdDFJoGx5wm9r4bx0VRF8YaendBxo2jUQfL0NCmSMTtwixdEbcFDXQ0pjZkDtfWdHT0dveCD+uFqPOLAWnzEvyRDVYUgAwN2mn4dxusxpYfZWasRZlM+acElJU3faLCbg3A/6xEb5oidPyJQ06v1cgliRr1AfjUEakwwNSsDI3efEilirbtQaNiTQz+Xv0JSFCPBtGmG+wnl1saWpCTCx3PrXJN4qBglQ4yxfO38mkbPvrE3BjNi63hviPfUWWTAnicDjfTKk4KiGlk4BVZv9IjRPBjT+MFdbaaUwqxG0JtYn5SgFZ0sNojWnGK/nZs2p0eNaxGQDgaM5tfhiHmDw9/AMbT9fPxjuMsQ7NqaB9hHUAtKwZs7TNqJMntsxUyXNHpAusp/dnKJjmVsMuZL0aKitOVLlQmJZvb5aQ1UFFy437RKnW2u3xh1vH5xYWwx1aOYgvLm1pG1Wj9RdWuQ6D/oOMDyNHgD4xtMBeASDPIZnOM3HsQaohaVnje6scHlU0nrze5XH8iumSCee3Z6lebv341VT/nWdeI997ArQcngjIuFUzKzzvAq3X3gmPr6Or6+ZdelgIYudXgiTv3B+55NS1Tcjp/slOjVI1GWzwRDCbiuMzcyA0ZoGRyCP788rz3+PACwMK02VgAbNAinggmgndKnlzP0TRMNR5cP5Bg05c40ZnMQeRHFCh5wcrNVodySwZrAo1OLJfWLDmaRqnWxz0sF9fKyMBjCJQDRIZxAr+C8ojobU9tSY2j2QzVQiMs2ksnM6nFNMv/nfvp4zv2Nmo+JYonyz59gKNpmGp+fo1wnz7Qodj9weRNrTWxcJ8MLAbjpUfk4GLFY1Q5mkap9qc+kVZAwBjE48H48h7YtZg0gjBSy9y/EwzGKbk2QDZQ+TxujqZRqvMJg4Dg5nIynpAfLN9spQWPTILdsombA/cXk4lEcvH+nqpP7OBoGqb6H/5YInx7K/FiUb7DHmRXfoij2RzV/8jUii5/ICdfJBM1P4uTo9kUbRjNsvwCRjFrfDA3R9NgbRANuRWUF2/FLY/G0WyFNoomsygnTsiJyLoNOZpGacNoEndu3ltMDHCHtmXaKBr60BZ85Wi2ShtOA0jxlaPZEm0UzUbF0TRMHM2OFUezY7UJaDZLgMapSL8eKVUfj/q/RHPg6Gubo6MHCDEdvya9xIcKb4zN5mlTL74T1VgyXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXK+i/wEd6PBbk7FWzQAAAABJRU5ErkJggg==', (291 / 8) * mm, (58 / 8) * mm)
    image2 = Image('https://drive.google.com/uc?export=download&id=1Ku7Ecjc-zFkoRSHFfExAdf1oxVSj-yyO', (669 / 20) * mm, (280 / 20) * mm)
    # elements.append(image1)
    logobj = [
        (
            image1,
            Paragraph("""INSTITUTO DE EDUCACIÓN SUPERIOR TECNOLÓGICO PÚBLICO<br/>
            "Alianza Renovada Ichuña Bélgica"<br/>
            Resolución Ministerial N° 0353-2004-ED<br/>
            Provincia General Sanchez Cerro - Distrito de Ichuña - Calle Tacna S/N
            """, cabecera),
            image2
        )
    ]
    logo_table = Table(logobj, [1.6 * inch, 3.7 * inch, 1.3 * inch])
    # logo_table.setStyle(PIE_TABLE)
    logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                    ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                                    ('ALIGN', (0, 1), (0, 1), 'CENTER'),
                                    # ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                    # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ]))
    elements.append(logo_table)

    elements.append(Paragraph("FICHA DE POSTULANTE", titulo1))
    elements.append(Paragraph("PROCESO DE ADMISIÓN IESTP ARIB - 2025", titulo2))
    elements.append(Paragraph("<u>I. DATOS PERSONALES:</u>", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.id, p.dni, p.apellido_paterno, p.apellido_materno, 
                          p.nombres, p.genero)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.id, p.dni, p.apellido_paterno, p.apellido_materno, 
                          p.nombres, p.genero)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Id','DNI', 'Apellido Paterno', 'Apellido Materno', 'Nombres', 'Sexo')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.correo, p.celular, p.fecha_nacimiento)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.correo, p.celular, p.fecha_nacimiento)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Correo','N° de Celular', 'Fecha de Nacimiento')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)

    elements.append(Paragraph("<u>II. LUGAR DE NACIMIENTO:</u>", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.id, p.lugar_nacimiento, p.lugar_nacimiento_distrito, p.lugar_nacimiento_provincia, 
                          p.lugar_nacimiento_departamento)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.id, p.lugar_nacimiento, p.lugar_nacimiento_distrito, p.lugar_nacimiento_provincia, 
                          p.lugar_nacimiento_departamento)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Id','Lugar', 'Distrito', 'Provincia', 'Departamento')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)

    elements.append(Paragraph("<u>III. INFORMACIÓN DE PROCEDENCIA ACADÉMICA:</u>", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.nombre_ies, p.tipo_institucion, p.anio_egreso, p.direccion_institucion, p.institucion_distrito, p.institucion_provincia, p.institucion_departamento)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.nombre_ies, p.tipo_institucion, p.anio_egreso, p.direccion_institucion, p.institucion_distrito, p.institucion_distrito, p.institucion_departamento)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Colegio Procedencia', 'Tipo', 'Año egreso', 'Dirección', 'Distrito', 'Provincia', 'Departamento')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)


    elements.append(Paragraph("<u>IV. PROGRAMA DE ESTUDIOS AL CUAL POSTULAR:</u>", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.programa_postula_primera_opcion, p.programa_postula_segunda_opcion, p.enterado_proceso_admision, p.codigo_voucher)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.programa_postula_primera_opcion, p.programa_postula_segunda_opcion, p.enterado_proceso_admision, p.codigo_voucher)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('1ra Opcion Carrera', '2da Opcion Carrera', '¿Cómo se entero del proceso de admisión?', 'Cod. de Pago')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)


    elements.append(Paragraph("<u>IV. DATOS DEL PADRE O PODERADO:</u>", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.tutor_apellidos, p.tutor_nombres, p.tutor_parentesco)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.tutor_apellidos, p.tutor_nombres, p.tutor_parentesco)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Apellidos', 'Nombres','Parentesco')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)

    elements.append(Spacer(20, 40))
    elements.append(Paragraph("""Declaro bajo juramento que los datos que consigno en la presente FICHA DE POSTULANTE, son verídicos y me remito para la confrontación con los documentos originales.
                De no ser correctos pierdo la vacante de admisión y renuncio a todo derecho que pueda
                obtener.""", paragraph))
    elements.append(Spacer(5, 10))
    today = timezone.now()

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Formatear la fecha en el formato deseado
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
    #locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    #elements.append(Paragraph(f"Ichuña, {today.strftime('%d de ')} Marzo del 2024", lugar_fecha))
    elements.append(Paragraph(f"Fecha: {fecha_formateada}"))
    elements.append(Spacer(20, 40))

    firma = [['__________________'],
             ['Firma']]
    firma_table = Table(firma)
    firma_table.setStyle(TableStyle([('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
                                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                     # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                     # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                     ]))
    elements.append(firma_table)

     # Agregar un recuadro para la imagen del postulante
    #recuadro_para_imagen = Frame(x=100, y=500, width=200, height=200, showBoundary=1)
    #elements.append(recuadro_para_imagen)

    doc.build(elements)  
    response.write(buff.getvalue())  
    buff.close()  
    return response

from django.shortcuts import render
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os
from pathlib import Path
from django.conf import settings

def storage_quota(request):
    BASE_DIR = Path(settings.BASE_DIR)
    JSON_KEYFILE = os.path.join(BASE_DIR, 'client_secrets.json')
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, SCOPES)
    service = build('drive', 'v3', credentials=creds)
    about = service.about().get(fields="storageQuota").execute()
    quota = about.get('storageQuota', {})
    limit = int(quota.get('limit', 0))
    usage = int(quota.get('usage', 0))
    remaining = limit - usage

    context = {
        'limit': limit,
        'usage': usage,
        'remaining': remaining,
    }
    return render(request, 'postulantes/storage_quota.html', context)