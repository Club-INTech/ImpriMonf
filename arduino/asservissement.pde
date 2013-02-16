#include <SimpleTimer.h>
SimpleTimer timer;       // Timer pour interruptions régulières

/** moteur **/
const int pinPWM = 5;    // pin de PWM du moteur
const int pinDIR = 6;    // pin de direction du moteur

/** codeuses **/
const int pinSignal1 = 2;// pin d'interruption 0 pour le premier signal
const int pinSignal2 = 3;// pin d'interruption 1 pour le second signal
int ticks = 0;           //ticks mesurés
int sens = 0;            //sens de parcourt de la roue codeuse

//états des 2 canaux de la codeuse
int currentS1 = 0;
int currentS2 = 0;
int lastS1 = 0;
int lastS2 = 0;
 
/**  asservissement **/
int consigne_ticks = 0;     // consigne de position en ticks
int somme_erreur = 0;       // pour l'intégrateur
int erreur_precedente = 0;  // pour le dérivateur
int frequence_asserv = 150; // en Hz

float kp = 0.8;             // Coefficient proportionnel
float kd = 0.1;             // Coefficient dérivateur
float ki = 0.0;             // Coefficient intégrateur

/** Routine d'initialisation **/
void setup() {
    //serie
    Serial.begin(9600);
    
    //interruptions externes (réception des ticks de la codeuse)
    attachInterrupt(0, update_ticks, CHANGE); // sur arduino duemilanove, pin2 = pin d'interruption 0
    attachInterrupt(1, update_ticks, CHANGE); //                       et pin3 = pin d'interruption 1
    
    //initialisation PWM et DIR
    pinMode(pinPWM, OUTPUT);
    pinMode(pinDIR, OUTPUT);
    
    //immobilisation initiale du moteur
    Serial.print("init\n");
    analogWrite(pinPWM, 0);
    delay(3000);
 
    timer.setInterval(1000/frequence_asserv, asservissement);  // Interruption pour calcul du PID et asservissement
}

/** lecture (blocante) d'une ligne sur la série **/
String readLine()
{
  String inString = "";
  while (Serial.available() == 0)
  {
    timer.run(); // On continue à évaluer les interruptions timer
  }
  char inChar = Serial.read();
  while (inChar != '\n' and inChar != '\r') // attente d'une fin de ligne
  {
    timer.run(); // On continue à évaluer les interruptions timer
    if (Serial.available() > 0) {
      inString += (char)inChar; 
      inChar = Serial.read();
    }
  }
  return inString;
}

/** Boucle principale (protocole série) **/
void loop(){
  String msg = readLine();
  
  //ping
  if (msg == "?") {
    Serial.println("#");
  }
  
  //modification des constantes d'asservissement
  //en millième ! Il faut entrer 1300 pour spécifier 1.300
  else if (msg == "kp") {
    kp = readLine().toInt()/1000.;
  }
  else if (msg == "ki") {
    ki = readLine().toInt()/1000.;
  }
  else if (msg == "kd") {
    kd = readLine().toInt()/1000.;
  }
  
  //affichage des constantes d'asservissement
  else if (msg == "?pid") {
    Serial.print("kp : ");
    Serial.print(kp);
    Serial.print(", ki : ");
    Serial.print(ki);
    Serial.print(", kd : ");
    Serial.print(kd);
    Serial.print("\n");
  }
}

void update_ticks()
{
  //récupération de l'état des signaux de la codeuse
  int currentS1 = digitalRead(pinSignal1);
  int currentS2 = digitalRead(pinSignal2); 
  
  //détermination du sens de rotation de la roue codeuse grace aux états des 2 signaux
  if (currentS1 != lastS1 or currentS2 != lastS2)
  {
    if(lastS1 xor currentS2)
      sens = 1;
    else
      sens = -1;
  }
  
  //états précédents
  lastS1 = currentS1;
  lastS2 = currentS2;
  
  //incrémentation des ticks
  ticks += sens;
}
 
/** Calcul du nouveau PWD avec asservissement PID **/
void asservissement()
{
    // Calcul des erreurs
    int erreur = consigne_ticks - ticks;
    somme_erreur += erreur;
    int delta_erreur = erreur-erreur_precedente;
    erreur_precedente = erreur;
 
    // PID : calcul de la commande
    int pwd = (int) (kp*erreur + ki*somme_erreur + kd*delta_erreur);
 
    // Normalisation et contrôle du moteur
    if(pwd < -255)
        pwd = -255;
    else if(pwd > 255)
        pwd = 255;
    
    Serial.print(ticks);
    Serial.print("\t");
    Serial.print(pwd);
    Serial.print("\n");
    
    if(pwd < 0)
    {
        digitalWrite(pinDIR, HIGH);
        analogWrite(pinPWM, -pwd);
    }
    else
    {
        digitalWrite(pinDIR, LOW);
        analogWrite(pinPWM, pwd);
    }
}
