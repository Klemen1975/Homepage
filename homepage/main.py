#!/usr/bin/env python

import os
import jinja2
import webapp2
import datetime
from eurojack import sp1, sp2, sp3, sp4, sp5, d1, d2
from models import Vnos
from models_users import Uporabnik



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class HomeHandler(BaseHandler):
    def get(self):

        return self.render_template("base_hp.html")

class AboutHandler(BaseHandler):
    def get(self):

        return self.render_template("me.html")

class ProjektiHandler(BaseHandler):
    def get(self):

        return self.render_template("projekti.html")

class CasHandler(BaseHandler):
    def get(self):

        params={"dan":datetime.datetime.now().strftime("%A"),
                "datum":datetime.datetime.now().strftime("%d"),
                "mesec":datetime.datetime.now().strftime("%B"),
                "leto":datetime.datetime.now().strftime("%Y"),
                "ura":datetime.datetime.now().strftime("%H:%M:%S"),
                }

        return self.render_template("cas.html", params=params)

class LotoHandler(BaseHandler):
    def get(self):

        params = {"ena": sp1,
                  "dva": sp2,
                  "tri": sp3,
                  "stiri": sp4,
                  "pet": sp5,
                  "dod1": d1,
                  "dod2": d2,
                  }

        return self.render_template("loto.html", params=params)

class KalkulatorHandler(BaseHandler):
    def get(self):

        f = {'+': lambda x, y: str(float(x) + float(y)),
             '-': lambda x, y: str(float(x) - float(y)),
             '*': lambda x, y: str(float(x) * float(y)),
             '/': lambda x, y: str(float(x) / float(y)),
             'C': lambda x, y: "",
            }

        x = self.request.get('x')
        y = self.request.get('y')
        operator = self.request.get('operator')

        result = ""
        try:
            result = f[operator](x, y)
        except ValueError:
            result = "Error: Incorrect Number"
        except ZeroDivisionError:
            result = "Error: Division by zero"
        except KeyError:
            pass

        buttons = "".join(["<input type='submit' name='operator' value='"
                           + o + "'>" for o in sorted(f.keys())])
        self.response.out.write("""<html>
            <body>
            <form action='/' method='get' autocomplete='off'>
            <input type='text' name='x' value='%s'/><br/>
            <input type='text' name='y'/><br/>
            %s
            </form>
            </body>
            </html>""" % (result, buttons))

class UganiHandler(BaseHandler):

    def get(self):

        return self.render_template("ugani.html")

    def post(self):
        stevilo=self.request.get("stevilka")

        stevilo = int(stevilo)
        odg = ""
        ugani = 43
        pravilno = "Bravo, uganili ste skrito stevilko :D"
        nepravilno = ":(  Vpisana stevilka ni prava"


        if stevilo == ugani:
            odg = pravilno

        else:
            odg = nepravilno



        spremenljivke = {
            "stevilo": stevilo,
            "skrito": ugani,
            "odgovor": odg,
            "pravilno": pravilno,
            "nepravilno": nepravilno
            }
        return self.render_template("ugani.html", params=spremenljivke)

class DnaHandler(BaseHandler):
    def get(self):

        return self.render_template("dna.html")

    def post(self):

        dna = self.request.get("dna")

        #Lasje
        crni = dna.find("CCAGCAATCGC")
        rjavi = dna.find("GCCAGTGCCG")
        oranzni = dna.find("TTAGCTATCGC")

        #Obraz
        kvadraten = dna.find("GCCACGG")
        okrogel = dna.find("ACCACAA")
        ovalen = dna.find("AGGCCTCA")

        #Oci
        modre  = dna.find("TTGTGGTGGC")
        zelene = dna.find("GGGAGGTGGC")
        rjave = dna.find("AAGTAGTGAC")

        #Spol
        moski = dna.find("TGCAGGAACTTC")
        zenska = dna.find("TGAAGGACCTTC")

        #Rasa
        belec = dna.find("AAAACCTCA")
        crnec = dna.find("CGACTACAG")
        azijec = dna.find("CGCGGGCCG")

        if moski >=0:
            spol = "moski"
        elif zenska >=0:
            spol = "zenska"
        else:
            spol = "ni DNA zapisa"

        if belec >=0:
            rasa = "belec"
        elif crnec >=0:
            rasa = "crnec"
        elif azijec >=0:
            rasa = "azijec"
        else:
            rasa = "ni DNA zapisa"

        if modre >=0:
            oci = "modre"
        elif rjave >=0:
            oci = "rjave"
        elif zelene >=0:
            oci = "zelene"
        else:
            oci = " ni DNA zapisa"

        if crni >=0:
            lasje = "crni"
        elif rjavi >=0:
            lasje="rjavi"
        elif oranzni >=0:
            lasje = "oranzni"
        else:
            lasje = "ni DNA zapisa"

        if kvadraten >=0:
            obraz = "kvadraten"
        elif okrogel >=0:
            obraz = "okrogel"
        elif ovalen >=0:
            obraz = "ovalen"
        else:
            obraz = "ni DNA zapisa"

        lastnosti = []

        lastnosti.append(spol)
        lastnosti.append(rasa)
        lastnosti.append(oci)
        lastnosti.append(lasje)
        lastnosti.append(obraz)

        params = {
            "spol": spol,
            "rasa": rasa,
            "oci": oci,
            "lasje": lasje,
            "obraz": obraz,
            }

        return self.render_template("dna.html", params=params)

class GuestbookHandler(BaseHandler):
    def get(self):

        output = Vnos.query().fetch()

        params = {"output": output,
                  }
        return self.render_template("guestbook.html", params=params)

    def post(self):

        vnos = Vnos(ime = self.request.get("ime"), priimek = self.request.get("priimek"),
                    email = self.request.get("email"), sporocilo = self.request.get("sporocilo"),)
        vnos.put()

        return self.redirect("/projekti/guestbook")

class BlogHandler(BaseHandler):
    def get(self):

        return self.render_template("blog.html")

class KontaktHandler(BaseHandler):
    def get(self):

        return self.render_template("kontakt.html")

class RegistracijaHandler(BaseHandler):
    def get(self):
       return self.render_template("registracija.html")

    def post(self):
       ime = self.request.get("ime")
       priimek = self.request.get("priimek")
       email = self.request.get("email")
       geslo = self.request.get("geslo")
       ponovno_geslo = self.request.get("ponovno_geslo")

       if geslo == ponovno_geslo:
            Uporabnik.ustvari(ime=ime, priimek=priimek, email=email, original_geslo=geslo,)
            return self.redirect_to("main")

class LoginHandler(BaseHandler):
    def get(self):
        return self.render_template("login.html")

    def post(self):
        email = self.request.get("email")
        geslo = self.request.get("geslo")

        uporabnik = Uporabnik.query(Uporabnik.email == email).get()

        if Uporabnik.preveri_geslo(original_geslo=geslo, uporabnik=uporabnik):
            self.ustvari_cookie(uporabnik=uporabnik)
            return self.redirect_to("main")
        else:
            return self.write("Cista jeba")

app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler, name="main"),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/projekti', ProjektiHandler),
    webapp2.Route('/projekti/cas', CasHandler),
    webapp2.Route('/projekti/loto', LotoHandler),
    webapp2.Route('/projekti/kalkulator', KalkulatorHandler),
    webapp2.Route('/projekti/ugani', UganiHandler),
    webapp2.Route('/projekti/dna', DnaHandler),
    webapp2.Route('/projekti/guestbook', GuestbookHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/kontakt', KontaktHandler),
    webapp2.Route('/registracija', RegistracijaHandler),
    webapp2.Route('/login', LoginHandler),

], debug=True)