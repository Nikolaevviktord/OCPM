/* 
   OCPM robotics contest
   Senior group - task 1
   Graph
   
   code by vdn
*/



/* 
   *************************************
   **            CONSTANTS            **
   *************************************
*/

const byte L_DIR = 4, L_POW = 5;
const byte R_DIR = 7, R_POW = 6;
const byte R_LINE = A1;
const byte L_LINE = A0;

const int gray = 700;
float L_coef = 0.35;
float R_coef = 0.326;
const float M_coef = (L_coef + R_coef) / 2;



/* 
   *************************************
   **              SETUP              **
   *************************************
*/

void setup() {
  pinMode(L_DIR, OUTPUT);
  pinMode(L_POW, OUTPUT);
  pinMode(R_DIR, OUTPUT);
  pinMode(R_POW, OUTPUT);
  
  pinMode(L_LINE, INPUT);
  pinMode(R_LINE, INPUT);

  Serial.begin(9600);

  int coord = barcode();

  zigzag_to_n_cross(1);
  get_path(coord / 10 - 1, coord % 10 - 1);
  faststop();
}



/* 
   *************************************
   **      LINE SENSOR FUNCTIONS      **
   *************************************
*/

int left_line() {
  return analogRead(L_LINE);
} 

int right_line() {
  return analogRead(R_LINE);
}

bool l_line() {
  return left_line() > gray;
}

bool r_line() {
  return right_line() > gray;
}



/* 
   **************************************
   **         MOVING FUNCTIONS         **
   **************************************
*/

void setMotors(int L, int R) {
  digitalWrite(L_DIR, L < 0);
  digitalWrite(R_DIR, R < 0);
  analogWrite(L_POW, abs(L) * L_coef);
  analogWrite(R_POW, abs(R) * R_coef);
}

void faststop() {
  for (int _ = 0; _ < 5; _++) {
    setMotors(255, 255);
    delay(20);
    setMotors(-255, -255);
    delay(20);
  } setMotors(0, 0);
}

void go_zigzag_to_cross() {
  while (1) {
    bool l = l_line(), r = r_line();
    if (l && r) {
      setMotors(255, 255);
    } else if (l && !r) {
      setMotors(200, -255);
    } else if (!l && r) {
      setMotors(-255, 200);
    } else {
      return;
    }
  }
}

void zigzag_to_n_cross(int n) {
  while (n--) {
    go_zigzag_to_cross();
    setMotors(255, 255);
    delay(100);
  } setMotors(255, 255);
  delay(150 / M_coef);
  while (!l_line() || !r_line()) {
    if (!l_line()) {
      setMotors(-255, 255);
    } else {
      setMotors(255, -255);
    }
  }
}

void turn_left() {
  while (l_line()) { setMotors(-255, 255); }
  while (r_line()) { setMotors(-255, 255); }
  while (!r_line()) { setMotors(-255, 255); }
  setMotors(255, -255);
  delay(200);
}

void turn_right() {
  while (r_line()) { setMotors(255, -255); }
  while (l_line()) { setMotors(255, -255); }
  while (!l_line()) { setMotors(255, -255); }
  setMotors(-255, 255);
  delay(200);
}



/* 
   *************************************
   **         BARCODE READING         **
   *************************************
*/

byte barcode() {
  unsigned long times[15];
  byte index = 0;
  bool last = 1;

  unsigned long start = millis();
  unsigned long end = start + 4000;

  while (millis() < end) {
    bool l = l_line(), r = r_line();
    if (l && r) {
      if (!last) {
        times[index++] = millis();
        last = 1;
      } setMotors(255, 255);
    } else if (!l && !r) {
      if (last) {
        times[index++] = millis();
        last = 0;
      } setMotors(255, 255);
    } else if (l && !r) {
      setMotors(200, -255);
    } else if (!l && r) {
      setMotors(-255, 200);
    }
  }

  faststop();

  bool mask[8];
  int one_line = (times[2] - times[0]) / 2;
  last = 0;

  byte t_ind = 3, m_ind = 0;
  while (t_ind < index) {
    for (byte i = 0; i < round(((double)times[t_ind] - (double)times[t_ind - 1]) / one_line); ++i) {
      mask[m_ind++] = last;
      last ^= 1;
    } ++t_ind;
  }

  for (byte i = m_ind; i < 8; ++i) mask[i] = last;

  byte res = 0;
  byte m = 1;

  for (byte i = 1; i < 8; ++i) {
    res += (!mask[i]) * m;
    m *= 2;
  }

  return res;
}



/* 
   *************************************
   **     RESULT OF ./dijkstra.py     **
   *************************************
*/

// insert code here



/* 
   *************************************
   **       EMPTY LOOP FUNCTION       **
   *************************************
*/

void loop() {

}
