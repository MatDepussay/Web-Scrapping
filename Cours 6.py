from requests import get
import re
from pydantic import BaseModel
from dataclasses import dataclass
from pathlib import Path

def recuperer_page(
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        URL = "https://fr.wikipedia.org/wiki/STOXX_Europe_50"
) -> str:
    """Récupération de la page wikipedia du STOXX Europe 50."""
    requete = get(URL, headers={"User-Agent": user_agent})
    if requete.ok:
        return requete.text
    else:
        raise ValueError("Erreur lors de la récupération de la page")

def extraire_donnees(page: str) -> str:
    """Extraction des données de la première table de la page HTML."""
    modif_table = re.compile("<table.*?</table>")
    resultat, *_ = modif_table.findall(page)(page.replace("\n", ""))
    return resultat 


def extraction_lignes(table: str) -> list[str]:
    """Extraction des lignes de la table HTML."""
    modif_lignes = re.compile("<tr.*?</tr>")
    _, *resultat = modif_lignes.findall(table) #TODO : vérifier que la première ligne est toujours un header
    return resultat



class Entree(BaseModel): 
    nom: str
    symbole: str
    url : str
    pays: str
    secteur: str



def extraction_entree(code_ligne: str) -> Entree:
    """Extrait le contenu d'une ligne de la table"""
    motif_lignes = re.compile("<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>")
    symbole, deuxieme, troisieme, secteur = motif_lignes.findall(code_ligne)
    motif_deuxieme = re.compile('href=\"(.*?)\.*>(.*?)</a>')
    url, nom = motif_deuxieme.findall(deuxieme)
    motif_troisieme = re.compile('>(.*?)</a>')
    *_, pays = motif_troisieme.findall(troisieme)

    return Entree(nom=nom, symbole=symbole, url=url, pays=pays, secteur=secteur)



def serialise(nom_fichier: str, entrees: list[Entree]):
    chemin = Path(".").resolve() / nom_fichier
    if chemin.exists():
        raise ValueError("Le fichier existe déja !")
    else:
       chemin.write_text(str([entree.model_dump() for entree in entrees]), encoding="utf-8")


def main():
    """Fonction orchestrant le scrapping"""
    code_page= recuperer_page()  
    code_table= extraire_donnees(code_page)
    lignes = extraction_lignes(code_table)
    entrees= [extraction_entree(code_ligne) for code_ligne in lignes]
    serialise(nom_fichier="test.json", entrees=entrees)



if __name__ == "__main__":
    main()