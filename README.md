# mini-extrudeur

Development of an Arduino controlled mini-extruder to test various materials at different rates of extrusion. A force measurement device and a data logger were also specially designed. This repository stores various code files :

- Arduino scripts which controls the stepper motor and the cell force (two different arduino Uno boards were used)
- Python scripts used to create GUI (one for the stepper control and one for the data logger)


## The Team of the **3D extrusion of local material** project @Ecole des Ponts ParisTech


- [Lise Dousset](https://github.com/Lise-Dousset)
- [Julien Hamelin](https://github.com/JulienHamelin)
- [Alaric Blanque](https://github.com/alaricblanque)
- [Yohan Lanier](https://github.com/yohan-lanier)

## See also 

- [How we build the prototype](https://www.instructables.com/Geopolymer-Mini-Extruder/)
- [How we build the force measurement device and the data logger](https://www.instructables.com/Force-Measurement-With-Arduino-and-Data-Logger-GUI/)


## Note 

The file *rx_threading.py* has been coded by [DRSEE](https://github.com/DRSEE/GUI_PyDataLogger). We have simply re-used it here because it is a really nice script and it perfectly fitted our needs. 

-----------------------------------------------------------------------------------------------------------------------------------------------------------
Github repo pour le code et les explications de notre prototype dans le cadre du projet "Extrusion 3D de matériaux locaux" @Ecole des Ponts ParisTech

Ce dépot contient : 

    *Le code de contrôle du moteur pap du mini-extrudeur
    *Le code d'acquisition des mesures de forces d'extrusion
    *Les codes python d'interface graphique pour la commande du moteur et pour l'acquisition des données
    *Le code python avec lequel nous avons réalisé l'évaluation numérique des pertes de charges dans l'extrudeur
    

Requierements pour les codes : 

* Arduino : 

      *Librairie HX711-master pour le contrôle de l'ampli utilisé pour la cellule de force
   
* Python : 

      *pyserial pour la communication avec le port série
      *tkinter (pourvu avec l'installation conda, à installer sinon)
      *rx_threading.py (fichier donné dans le dossier de ce repo)
   
Le fichier *rx_threading.py* a été codé par DRSEE (https://github.com/DRSEE/GUI_PyDataLogger) et est purement repris ici car très bien fait. Il sert à gérer les ouvertures et fermetures du port série, le choix du baudrate, à lire les données venant du port série, gérer les exceptions etc...
