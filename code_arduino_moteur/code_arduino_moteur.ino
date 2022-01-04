//Author : yohan lanier
//Date : Mars 2021
//Part of a one year project at Ecole des PontsParisTech
//Team : Lise Dousset, Alaric Blanqué, Julien Hamelin, Yohan Lanier


//***************************************************************************************************************
//This code allows us to control our mini-extruder through the serial monitor using the following commands
//        +"s" stops the stepper motor
//        +"u" rotates the stepper motor such as the mobile part goes upward
//        +"d" rotates the stepper motor such as the mobile part goes downward
//        +"h" rotates the stepper motor with a high rotation rate
//        +"a" rotates the stepper motor with an average rotation rate
//        +"l" rotates the stepper motor with a low rotation rate
// With our driver settings, we need 400 steps to complete a full rotation of the rotor.
//The delay of the high speed rate is 1ms --> w=2.5 rotation per sec
//The delay of the average speed rate is 2ms --> w=1.25 rotation per sec
//The delay of the low speed rate is 5ms --> w=0.5 rotation per sec
//Beware that these are theorical speeds assuming that the signal is transmitted to the motor without any delay

//We use a microswitch in order to stop the piston when its stroke is over
//***************************************************************************************************************

//***************************************************************************************************************
//Initialisation
//***************************************************************************************************************

//***************************************************************************************************************
//stepper pins
#define PUL 7
#define DIR 6
#define ENA 5


//***************************************************************************************************************
//Microswitch pin
#define MS 4


//***************************************************************************************************************
//delay values
const float delayHighSpeed = 1;//ms
const float delayAverageSpeed = 2;//ms
const float delayLowSpeed = 5;//ms
float delay_ = delayLowSpeed;//This value will take one of the above value depending on the speed the user wants

//***************************************************************************************************************
//varius variables
int counter = 0;//This variable will allow us to control how many revolution we do to make the piston go upward when the switch is activated
bool init_ = true;//Usefull to initialize the driver at the first iterations
int letter;
unsigned long currentTime = 0;
unsigned long previousTime = 0;




//***************************************************************************************************************
//set up
//***************************************************************************************************************

void setup() {
  //initialize serial communications at a 9600 baud rate
  Serial.begin(115200);
  //Driver pins
  pinMode(PUL, OUTPUT);//setting the PUL as an output
  pinMode(DIR, OUTPUT);//setting the DIR as an output
  pinMode(ENA, OUTPUT);//setting the ENA as an output
  //MicroSwitch Pin
  pinMode(MS, INPUT);//setting the microswich as input
}

//***************************************************************************************************************
//Defining functions
//***************************************************************************************************************

//***************************************************************************************************************
//Stepper control
void makeOneStep(float t_delay_) {
  if (currentTime - previousTime > t_delay_) {
    previousTime = currentTime;
    digitalWrite(PUL, HIGH); //One pulse on the PUL born = one step
    digitalWrite(PUL, LOW);
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
  }
  return command;
}

//***************************************************************************************************************
//Speed control
void checkWhatIsSpeed(String t_command) {
  //Low speed
  if (t_command == "l") {
    digitalWrite(ENA, LOW); //Enables stepper
    delay_ = delayLowSpeed;//Setting the delay variable such as the rotation of rate of the stepper is "high"
  }
  //Average speed
  else if (t_command == "a") {
    digitalWrite(ENA, LOW); //Enables stepper
    delay_ = delayAverageSpeed;//Setting the delay variable such as the rotation of rate of the stepper is "high"
  }
  //High speed
  else if (t_command == "h") {
    digitalWrite(ENA, LOW); //Enables stepper
    delay_ = delayHighSpeed;//Setting the delay variable such as the rotation of rate of the stepper is "high"
  }
}

//***************************************************************************************************************
//Direction control
void checkWhatIsDirection(String t_command) {
  if (t_command == "u") {
    digitalWrite(DIR, LOW); //Sets the rotation of the stepper such as the mobile part goes upward
  }
  if (t_command == "d") {
    digitalWrite(DIR, HIGH); //Sets the rotation of the stepper such as the mobile part goes downward
  }
}

void checkForStop(String t_command) {
  if (t_command == "s") {
    digitalWrite(ENA, HIGH); //disables stepper
  }
}

//***************************************************************************************************************
//Initialisation
void initialization(bool& t_init) {
  if (t_init == true) {
    digitalWrite(ENA, LOW); //Enable stepper
    digitalWrite(DIR, LOW); //Going downward
    t_init = false;//No more init
  }
}

//***************************************************************************************************************
//Dealing with the end of the stroke
bool checkEndOfStroke(int t_val) {
  if (t_val == LOW)//If the switch is activated
  {
    return true;//then it means stroke is over
  }
  else {
    return false;//the stroke isn't over
  }
}

void makePistonGoUpAfterEndOfStroke() {
  digitalWrite(DIR, LOW);//Piston goes upward
  counter = 1;// we begin to count the steps
  while (counter != 1600) { //We want to do 4 entire revolutions with the stepper and each revolution is 400 steps
    digitalWrite(PUL, HIGH); //One pulse on the PUL born = one step
    digitalWrite(PUL, LOW);
    delay(2);
    counter += 1; //adding one step to the counter
  }
  //When we have done 4 revolutions
  digitalWrite(ENA, HIGH); //stops the stepper
  counter = 0;//Counter is back to zero and we can re-use the extruder !
}



//***************************************************************************************************************
//loop
//***************************************************************************************************************

void loop() {
  currentTime = millis();
  //*****************************************************************************************************************
  //Initialization
  initialization(init_);

  //*****************************************************************************************************************
  //Checking if the stroke is over
  if (checkEndOfStroke(digitalRead(MS))) {
    makePistonGoUpAfterEndOfStroke();
  }
  else {
    //*****************************************************************************************************************
    //reading the serial monitor
    String command = readSerialMonitor(letter);

    //*****************************************************************************************************************
    //Checking for setting changes
    checkWhatIsSpeed(command);
    checkWhatIsDirection(command);
    checkForStop(command);

    //*****************************************************************************************************************
    //Making one step
    makeOneStep(delay_);
  }
}
