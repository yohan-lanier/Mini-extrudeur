//Author : yohan lanier
//Date : Mars 2021
//Part of a one year project at Ecole des PontsParisTech
//Team : Lise Dousset, Alaric Blanqué, Julien Hamelin, Yohan Lanier
/**
 * This codes allows us to acquire data through a load cell durig material extrusion
 * The data acquisition is made using python (pyserial)
 * A GUI made with tkinter allows us to make the acquisition in a convenient way
 */

//***************************************************************************************************************
//Librairies
//***************************************************************************************************************
#include <HX711.h>

//***************************************************************************************************************
//Initialisation
//***************************************************************************************************************
int letter;

//***************************************************************************************************************
//Load cell parameters
#define calibrationFactor 640 //This value is obtained with a specific protocol --> see the corresponding section in our written work
#define DOUT  3
#define CLK  2
HX711 loadCell;
bool firstMeasure = true;
bool ongoingDataAcquisition = false;
unsigned long currentTime = 0;
unsigned long t0 = 0;
unsigned long previousDataAcqTime = 0;

//***************************************************************************************************************
//Load cell functions
void startOrStopDataAcquisition(String t_command) {
  if (t_command == "on") {
    ongoingDataAcquisition = true;
  }
  else if (t_command == "off") {
    ongoingDataAcquisition = false;
    firstMeasure = true;
  }
}

void makeAMeasure() {
  if (firstMeasure == true) {
    t0 = millis();//defining the initial time of measure
    Serial.println("Starting load cell data acquisition. Force unit is Newton. Time unit is second");
    Serial.print("time");
    Serial.print(";");
    Serial.print("Extrusion Force");
    Serial.print(";");
    Serial.println();
    Serial.print((currentTime - t0) * 0.001, 2);
    Serial.print(";");
    Serial.print(loadCell.get_units(), 1);
    Serial.print(";");
    Serial.println();
    firstMeasure = false;
  }
  else {
    if (currentTime - previousDataAcqTime > 10) {
      previousDataAcqTime = currentTime;
      Serial.print((currentTime - t0) * 0.001, 2);
      Serial.print(";");
      Serial.print((loadCell.get_units())/(1.4595*0.9827) + 0.6944/0.9827 + 12.885/0.9827, 1);
      Serial.print(";");
      Serial.println();
    }
  }
}


//***************************************************************************************************************
//Reading the serial monitor
String readSerialMonitor(int t_letter) {
  String command;
  while (Serial.available() > 0)//Check if there is some data in the monitor
  {
    t_letter = Serial.read();
    command += char(t_letter);
    delay(1);
  }
  return command;
}

//***************************************************************************************************************
//set up
//***************************************************************************************************************

void setup() {
  //Load cell
  Serial.begin(115200);
  loadCell.begin(DOUT, CLK);
  loadCell.set_scale(calibrationFactor);//This value is obtained using the SparkFun_HX711_Calibration sketch
  loadCell.tare(); //Assuming there is no weight on the load cell at start-up, rester the scale to 0
  //loadCell.set_offset(-0.6944);//
}

//***************************************************************************************************************
//loop
//***************************************************************************************************************


void loop() {
  
  currentTime = millis();
  //*****************************************************************************************************************
  //reading the serial monitor
  String command = readSerialMonitor(letter);

  
  //*****************************************************************************************************************
  //Data acquisition
  startOrStopDataAcquisition(command);
  if (ongoingDataAcquisition) {
    makeAMeasure();
  }
}
