/** Timers pour interruptions régulières **/
#include <SimpleTimer.h>
SimpleTimer timerAsservPWM;
SimpleTimer timerPasAPas;

/** constantes pour les codeuses **/
const byte pinSignal1 = 2;// pin d'interruption 0 pour le premier signal
const byte pinSignal2 = 3;// pin d'interruption 1 pour le second signal

/** constantes pour le moteur à courant continu **/
const byte pinDIR = 4;                   // pin de direction du moteur à courant continu
const byte pinPWM = 5;                   // pin de PWM du moteur à courant continu
const int frequence_asserv = 150;        // fréquence de mise à jour du PWM, en Hz
const float nb_ticks_1mm = 4.837070254;  //constante de conversion

/** constantes pour le moteur pas à pas **/
const byte pinSENS  = 6;    // pin de sens du moteur pas à pas
const byte pinCLOCK = 7;    // pin d'impulsion du moteur pas à pas
const byte pinENABLE = 8;   // pin d'activation du moteur pas à pas
const int frequence_PasAPas = 650;     // fréquence d'envoi des impulsions au pas à pas, en Hz
const float nb_pas_1mm = 100.352113; //constante de conversion

/** constantes pour les distributeurs **/
const byte pinBaisseVerin = 9;
const byte pinLeveVerin = 10;

/** constantes pour la lecture des photodiodes **/
const byte pinlecture = 11;

/** variables globales, partagées par plusieurs fonctions **/
long ticks = 0;          // ticks mesurés par l'encodeur et pris en compte par l'asservissement 
long consigne_ticks = 0; // consigne reçue de position du moteur à courant continu, en ticks
//constantes d'asservissement pid
boolean asserv_enable = false;
float kp = 50.0;         // Coefficient proportionnel
float ki = 0.0;         // Coefficient intégrateur
float kd = 0.0;         // Coefficient dérivateur
byte bridage_pwm = 150;   // Valeur de bridage du PWM
int pas = 0;            // position du moteur pas à pas depuis le dernier recalage, valeur en pas
int consigne_pas = 0;   // consigne reçue de position du moteur pas à pas, en pas

//***  niveaux de prescaler  ***//
//int mode = 0b00000001; float prescaler = 64.;// 62kHz
int mode = 0b00000010; float prescaler = 8.;// 7.8kHz
  
/** Routine d'initialisation **/
void setup() {
    //overclock du timer (nécessaire pour le pas à pas)
    TCCR0B = TCCR0B & 0b11111000 | mode;
  
    //serie
    Serial.begin(9600);
    
    //interruptions externes (réception des ticks de la codeuse)
    attachInterrupt(0, update_ticks, CHANGE); // sur arduino duemilanove, pin2 = pin d'interruption 0
    attachInterrupt(1, update_ticks, CHANGE); //                       et pin3 = pin d'interruption 1
    
    //initialisation des états des broches
    pinMode(pinPWM,  OUTPUT);
    pinMode(pinDIR,  OUTPUT);
    pinMode(pinSENS, OUTPUT);
    pinMode(pinCLOCK, OUTPUT);
    pinMode(pinENABLE, OUTPUT);
    pinMode(pinBaisseVerin, OUTPUT);
    pinMode(pinLeveVerin, OUTPUT);
    
    pinMode(pinlecture, INPUT);
    
    //immobilisation initiale du moteur
    analogWrite(pinPWM, 0);
    
    // Interruptions pour calcul du PID et asservissement
    timerAsservPWM.setInterval(1000./(frequence_asserv/prescaler), asservissementPWM);
    // pour les impulsions du pas à pas (la fréquence est doublée pour générer les fronts)
    timerPasAPas.setInterval(1000./(2*frequence_PasAPas/prescaler), gestionPasAPas);
    
    Serial.print("init\n");
}

/** lecture (blocante) d'une ligne sur la série **/
String readLine()
{
  String inString = "";
  while (Serial.available() == 0)
  {
    // On continue à évaluer les interruptions timer
    timerAsservPWM.run();
    timerPasAPas.run();
  }
  char inChar = Serial.read();
  while (inChar != '\n' and inChar != '\r') // attente d'une fin de ligne
  {
    // On continue à évaluer les interruptions timer
    timerAsservPWM.run();
    timerPasAPas.run();
    if (Serial.available() > 0) {
      inString += (char)inChar; 
      inChar = Serial.read();
    }
  }
  //acquittement de la trame
  Serial.println("_");
  return inString;
}

/** Boucle principale (protocole série) **/
void loop(){
  String msg = readLine();
   
  ////// PROTOCOLE FINAL //////////
  //identification de la carte
  if (msg == "?") {
    Serial.println("#");
  }
  
  //reset des pas
  else if (msg == "reset_pap") {
    consigne_pas = 0;
    pas = 0;
  }
  
  //consigne au moteur pas à pas
  else if (msg == "go_pap") {
    consigne_pas = (readLine().toInt() / 1000.0) * nb_pas_1mm;
  }
  
  //consigne au moteur à courant continu
  else if (msg == "go_mot") {
    consigne_ticks = (readLine().toInt() / 1000.0) * nb_ticks_1mm;
  }
  
  //changement de l'origine de la codeuse
  else if (msg == "set_mot") {
    float pos = (readLine().toInt() / 1000.0) * nb_ticks_1mm;
    ticks = pos;
    consigne_ticks = pos;
  }
  
  //activation de l'asservissement
  else if (msg == "asserv_on") {
    digitalWrite(pinLeveVerin, HIGH);
    delay(2000 * prescaler);
    digitalWrite(pinLeveVerin, LOW);
    asserv_enable = true;
  }
  
  //désactivation de l'asservissement
  else if (msg == "asserv_off") {
    asserv_enable = false;
    digitalWrite(pinLeveVerin, HIGH);
    delay(2000 * prescaler);
    digitalWrite(pinLeveVerin, LOW);
  }
  
  //déplacement en un point
  else if (msg == "aller_a") {
    consigne_pas = (readLine().toInt() / 1000.0) * nb_pas_1mm;
    consigne_ticks = (readLine().toInt() / 1000.0) * nb_ticks_1mm;
  }
  
  //acquittement d'arrivée
  else if (msg == "acq?") {
    if(abs(ticks - consigne_ticks) < 3 && pas == consigne_pas)
      Serial.println("1");
    else
      Serial.println("0");
  }
  
  //poinçonnage
  else if (msg == "poincon_bas") {
    digitalWrite(pinBaisseVerin, HIGH);
  }
  else if (msg == "poincon_haut") {
    digitalWrite(pinBaisseVerin, LOW);
    digitalWrite(pinLeveVerin, HIGH);
  }
  else if (msg == "poincon_libre") {
    digitalWrite(pinLeveVerin, LOW);
  }
    
  //lit les pistes et renvoit le nombre de trous lus
  else if (msg == "lecture") {
    lire_photodiodes();
  }
}

void update_ticks()
{
  //sauvegarde des états précédents des 2 signaux de la codeuse
  static int lastS1 = 0;
  static int lastS2 = 0;
  
  //sauvegarde du sens de parcourt de la roue codeuse
  static int sens = 0;
  
  //récupération de l'état des signaux de la codeuse
  int currentS1 = digitalRead(pinSignal1);
  int currentS2 = digitalRead(pinSignal2);
  
  //détermination du sens de rotation de la roue codeuse grace aux états des 2 signaux
  if (currentS1 != lastS1 or currentS2 != lastS2)
  {
    //incrémentation des ticks en fonction du sens de parcours
    if(lastS1 xor currentS2)
      sens = 1;
    else
      sens = -1;
  }
  
  //états précédents
  lastS1 = currentS1;
  lastS2 = currentS2;
  
  ticks += sens;
}
 
/** Calcul du nouveau PWM avec asservissement PID **/
void asservissementPWM()
{
  if (asserv_enable)
  {
    static long somme_erreur = 0;// pour l'intégrateur
    static long erreur_precedente = 0;  // pour le dérivateur
    
    // Calcul des erreurs
    long erreur = consigne_ticks - ticks;
    somme_erreur += erreur;
    long delta_erreur = erreur-erreur_precedente;
    erreur_precedente = erreur;

    // PID : calcul de la commande
    long pwm = kp*erreur + ki*somme_erreur + kd*delta_erreur;
 
    // Normalisation du PWM
    if(pwm < -bridage_pwm)
        pwm = -bridage_pwm;
    else if(pwm > bridage_pwm)
        pwm = bridage_pwm;
        
        
    if(abs(pwm) < kp+5)
      //évite de forcer inutilement
      analogWrite(pinPWM, 0);
      
    else
    {
      //Contrôle du moteur
      if(pwm < 0)
      {
          digitalWrite(pinDIR, HIGH);
          analogWrite(pinPWM, -pwm);
      }
      else
      {
          digitalWrite(pinDIR, LOW);
          analogWrite(pinPWM, pwm);
      }
    }
  }
  else
    analogWrite(pinPWM, 0);
}

/** Gestion de la broche Clock du moteur pas à pas **/
void gestionPasAPas()
{
  static boolean frontMontant = false;
  if (frontMontant)
    _frontMontantPAP();
  else
    _frontDescendantPAP();
  frontMontant = !frontMontant;
}

/** Envoit ou non une impulsion au moteur pas à pas **/
void _frontMontantPAP()
{
  int erreur = consigne_pas - pas;
  if (erreur < 0)
  {
      digitalWrite(pinENABLE, HIGH); //activation du moteur
      digitalWrite(pinSENS, LOW);
      digitalWrite(pinCLOCK, HIGH);
      pas--;
  }
  else if (erreur > 0)
  {
      digitalWrite(pinENABLE, HIGH); //activation du moteur
      digitalWrite(pinSENS, HIGH);
      digitalWrite(pinCLOCK, HIGH);
      pas++;
  }
  else
  {
      digitalWrite(pinENABLE, LOW); //desactivation du moteur (évite de vibrer)
  }
}

/** Remise à zéro du niveau logique (pour générer le créneau) **/
void _frontDescendantPAP()
{
  digitalWrite(pinCLOCK, LOW);
}

/** Renvoit l'état des photodiodes lues une par une **/
void lire_photodiodes()
{
  unsigned long resultat = 0;
  
  for(byte d=26; d>=0; d--)
  {
    //TODO: inscription de l'identifiant sur le port (5 bits)
    
    //attente de la stabilisation du signal (~3ms)
    delay(3 * prescaler);
    
    //lecture et sauvegarde de l'état d'une diode
    if (digitalRead(pinlecture) == HIGH)
      resultat |= 0b1;
    resultat = resultat << 1;
  }
  
  //communication des états des diodes en un seul entier
  Serial.println(resultat >> 1);
}
