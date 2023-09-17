import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import scipy as sp

# ==============================================================
# ----------------EXERCICE 1 – Relevé de Température------------
# ==============================================================

tableau_temp = np.load("temperatures.npy")
temperatures_reelles = tableau_temp[0:72, 0]
volt_mesures = tableau_temp[0:72, 1]
temperatures_mesures = (volt_mesures * 10) - 10
temperatures_filtres = sp.signal.medfilt(temperatures_mesures)


def affiche_2courbes(t1, t2):
  plt.figure()
  plt.plot(t1, label="Températures réelles")
  plt.plot(t2, label="Températures mesurées")
  plt.title("Comparaison des températures réelles et mesurées")
  plt.legend()
  plt.show()


def affiche_3courbes(t1, t2, t3):
  plt.figure()
  plt.plot(t1, label="Températures réelles")
  plt.plot(t2, label="Températures mesurées")
  plt.plot(t3, label="Températures filtrées")
  plt.title("Comparaison des températures réelles, mesurées et filtrées")
  plt.legend()
  plt.show()


def RMSE(tab1, tab2):
  return np.sqrt(np.mean((tab1 - tab2)**2))


def histogramme(tab1, tab2, titre):
  erreur = tab1 - tab2
  plt.hist(erreur, bins=20)
  plt.title(titre)
  plt.xlabel("Erreur")
  plt.ylabel("Fréquence")
  plt.show()


# ==============================================================
# ------EXERCICE 2 – Remplacer une couleur dans une image-------
# ==============================================================


def Exo2():
  # Chargement de l'image et normalisation des valeurs de pixels entre 0 et 1
  citroen = plt.imread('citroen.jpg') / 255.0
  plt.title('Image originale (RGB)')
  plt.imshow(citroen)
  plt.show()

  # Création d'un tableau d'image HSV vide avec la même forme que l'image originale
  hsv_image = np.zeros(citroen.shape, dtype='float64')

  # Conversion de l'espace de couleur RGB vers HSV pixel par pixel
  for x in range(citroen.shape[0]):
    for y in range(citroen.shape[1]):
      R, G, B = citroen[x, y]

      Cmin = min(R, G, B)
      Cmax = max(R, G, B)
      delta = Cmax - Cmin

      if delta == 0:
        H = 0
      elif Cmax == R:
        H = (1 / 6) * (((G - B) / delta) % 6)
      elif Cmax == G:
        H = (1 / 6) * (((B - R) / delta) + 2)
      elif Cmax == B:
        H = (1 / 6) * (((R - G) / delta) + 4)

      if Cmax == 0:
        S = 0
      else:
        S = delta / Cmax

      V = Cmax

      # Stockage des valeurs H, S et V dans le tableau d'image HSV
      hsv_image[x, y] = (H, S, V)

  # Affichage de l'image HSV convertie
  plt.imshow(hsv_image)
  plt.title('Image convertie (HSV)')
  plt.show()

  # Affichage des canaux H, S et V séparément avec des barres de couleur
  fig, axes = plt.subplots(1, 3, figsize=(12, 4))

  h_img = axes[0].imshow(hsv_image[:, :, 0], cmap='hsv')
  axes[0].set_title('Canal H')
  plt.colorbar(h_img, ax=axes[0])

  s_img = axes[1].imshow(hsv_image[:, :, 1], cmap='gray')
  axes[1].set_title('Canal S')
  plt.colorbar(s_img, ax=axes[1])

  v_img = axes[2].imshow(hsv_image[:, :, 2], cmap='gray')
  axes[2].set_title('Canal V')
  plt.colorbar(v_img, ax=axes[2])
  plt.show()

  # Définition des seuils pour les canaux H, S et V
  h_seuil = (0.4, 0.6)
  s_seuil = (0.38, 1.0)
  v_seuil = (0.3, 1.0)

  # Création d'un masque basé sur les seuils définis
  masque = ((hsv_image[:, :, 0] >= h_seuil[0]) &
            (hsv_image[:, :, 0] <= h_seuil[1]) &
            (hsv_image[:, :, 1] >= s_seuil[0]) &
            (hsv_image[:, :, 1] <= s_seuil[1]) &
            (hsv_image[:, :, 2] >= v_seuil[0]) &
            (hsv_image[:, :, 2] <= v_seuil[1]))

  # La Carrosserie (masque)
  citroen_carrosserie = np.copy(hsv_image)
  citroen_carrosserie[~masque] = 0
  citroen_carrosserie = clr.hsv_to_rgb(citroen_carrosserie)
  plt.imshow(citroen_carrosserie)
  plt.title('La Carrosserie en coleur origine')
  plt.show()

  # Application du masque sur l'image HSV
  citroen_masquee = np.copy(hsv_image)

  # Augmentation progressive de la teinte vers le rouge pour les pixels masqués
  citroen_masquee[masque, 0] = 0  # Réglage de la valeur H à 0 (rouge)

  # Conversion de l'image masquée vers l'espace de couleur RGB
  rgb_image = clr.hsv_to_rgb(citroen_masquee)

  # Affichage de l'image modifiée
  plt.imshow(rgb_image)
  plt.title('Image modifiée (RGB)')
  plt.savefig('citroen_rouge.jpg')
  plt.show()


def main():

  #-------------EXERCICE 1--------------
  #print(tableau_temp)
  #print(temperatures_reeles)

  #--Question 1--
  #affiche_2courbes(temperatures_reelles, temperatures_mesures)

  #--Question 2--
  #histogramme(temperatures_reelles, temperatures_mesures, "Histogramme des erreurs entre températures réelles et mesurées")

  #--Question 3--
  #print("le RMSE entre temperatures reelles et temperatures mesures est :",RMSE(temperatures_reelles, temperatures_mesures))

  #--Question 5--
  #print("le RMSE entre temperatures mesures et temperatures filtres est :",RMSE(temperatures_mesures,temperatures_filtres ))
  #affiche_3courbes(temperatures_reelles, temperatures_mesures,temperatures_filtres)
  #histogramme(temperatures_mesures, temperatures_filtres, "Histogramme des erreurs entre températures mesurées et filtres")

  #-------------EXERCICE 2--------------
  Exo2()
  pass


if __name__ == '__main__':
  main()
