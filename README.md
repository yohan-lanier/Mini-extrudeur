# mini-extrudeur
Github repo pour le code et les explications de notre prototype dans le cadre du projet "Extrusion 3D de matériaux locaux" @Ecole des Ponts ParisTech

Ce dépot contient : 

    *Le code de contrôle du moteur pap du mini-extrudeur
    *Le code d'acquisition des mesures de forces d'extrusion
    *Les codes python d'interface graphique pour la commande du moteur et pour l'acquisition des données
    *Le code python avec lequel nous avons réalisé l'évaluation numérique des pertes de charges dans l'extrudeur
    
Un wiki est aussi disponible pour plus d'explications et de détails sur l'avancement du projet. Le wiki contient également une liste du matériel à prendre avec soit pour utiliser le prototype ainsi qu'un mode d'emploi.

Requierements pour les codes : 

* Arduino : 

      *Librairie HX711-master pour le contrôle de l'ampli utilisé pour la cellule de force
   
* Python : 

      *pyserial pour la communication avec le port série
      *tkinter (pourvu avec l'installation conda, à installer sinon)
      *rx_threading.py (fichier donné dans le dossier de ce repo)
   
Le fichier *rx_threading.py* a été codé par DRSEE (https://github.com/DRSEE/GUI_PyDataLogger) et est purement repris ici car très bien fait. Il sert à gérer les ouvertures et fermetures du port série, le choix du baudrate, à lire les données venant du port série, gérer les exceptions etc...
