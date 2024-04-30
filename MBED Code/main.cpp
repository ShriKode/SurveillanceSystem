// Including Libraries
#include "mbed.h"
#include <stdio.h> 
#include "rtos.h" // Threading
#include <mpr121.h> // Touch Keypad
#include "Speaker.h" // Speaker API
#include <string>

//Mutex locks
Mutex sonar_lock;
// Global variables used in different threads

volatile bool securityOn = 1; // Security Mode ; default is one
volatile bool securityBreached = 0; // Intruder detection
//capacitive touch sensor global variables
int currentPasscode[4] = {0, 0, 0, 0};  // Store the current passcode
volatile int buffer[4] = {-1, -1, -1, -1}; // Stores the passcode user entered
volatile int b_size = 0; // Length of passcode entered
volatile bool alternator = true; // Variable to handle touch keypad interrupt pattern
volatile bool receivePasscode = false; // Variable to show state of passcode entry

// face detection
volatile bool verified_image = false;

// Pushbuttons to tell device what use plans to do
DigitalIn activateSecurity(p29);
DigitalIn resetPasscode(p30);
DigitalIn enterPasscode(p12);

// Initializing capacitive touch keypad
I2C i2c(p9, p10);
Mpr121 keypad(&i2c, Mpr121::ADD_VSS);
InterruptIn interrupt(p23);

// Initializing sonar
DigitalOut trigger(p6);
DigitalIn echo(p7);
volatile int d = 0;
volatile int correction = 0;
Timer timer;

// Speaker setup for alarm
Speaker mySpeaker(p22);

// Initialize threads
Thread th_sonar;
Thread th_speaker;
Thread th_image;

// Initializing serial communication with pc, to be changed to pi eventually
Serial raspberryPi(USBTX,USBRX);

// States of machine
DigitalOut myled(LED1); // used to indicate active main thread, just blinks on start
DigitalOut securityled(LED2); // Indicates whether security mode is on or off
DigitalOut imageled(LED4);
DigitalOut timerled(LED3);



// Functions

// Action to take when user is close by
void camera(char code) {
    raspberryPi.putc(code);
    //pc.printf("Someone is here\n");
    return;
}

// Reset to a new passcode
void setNewPasscode() {
    while (b_size != 4); // Waiting for user to enter complete password
    for (int i = 0; i < 4; i++) {
        //pc.printf("%d ",buffer[i]); // Prints out the entered password, can be edited later
        ;
    }
    //pc.printf("\n");
    // Sets the passcode
    for (int i = 0; i < 4; i++) {
        currentPasscode[i] = buffer[i];
    }
    b_size = 0; // Reset buffer size to 0
}

// Receive input and check if it matches passcode
bool passcodeCompare() {
    while (b_size != 4);
    for (int i = 0; i < 4; i++) {
        //pc.printf("%d ",buffer[i]);;
        
    }
    //pc.printf("\n");
    bool passcodeCorrect = true; 
    // Compares input to passcode
    for (int i = 0; i < 4; ++i) {
        if (buffer[i] != currentPasscode[i]) {
            passcodeCorrect = false;
            break;
        }
    }
    b_size = 0;
    return passcodeCorrect;
}


// Interrupts

// Key hit/release interrupt routine for touch keypad
void fallInterrupt() {
    int key_code = 0;
    int i = 0;
    int value = keypad.read(0x00);
    value += keypad.read(0x01) << 8;
    i = 0;
    for (i = 0; i < 12; i++) {
        if (((value >> i) & 0x01) == 1) key_code = i;
    }

    if (receivePasscode && b_size < 4 && alternator){
        buffer[b_size++] = key_code;
    }
    alternator = !alternator;
}


// Threads
void image_data() {
    //int count = 0;
    while(1) {
        sonar_lock.lock();
        if (raspberryPi.readable()) {
            char c = raspberryPi.getc();
            if (c == '1') {
                verified_image = true;
                imageled = 1;
                //count = 5;
            } else {
               verified_image= false;
               imageled = 0;
            }
        }
        sonar_lock.unlock();
        Thread::wait(100);
    }
}

void sonar_thread() {
    int consecutiveNonZero = 0;
    while (1) {
        sonar_lock.lock();
        trigger = 1;
        timer.reset();
        wait_us(10.0);
        trigger = 0;
        //wait for echo high
        timerled = 1;
        while (echo==0) {};
        timerled = 0;
        //echo high, so start timer
        timer.start();
        //wait for echo low
        while (echo==1) {};
        //stop timer and read value
        timer.stop();
        //subtract software overhead timer delay and scale to cm
        d = (timer.read_us()-correction)/58.0;
        sonar_lock.unlock();
        //pc.printf(" %d cm and time: %d\n\r",d, timer.read_us()); // Debugging code by printing distance to terminal
        //wait so that any echo(s) return before sending another ping

        if (d != 0 && d < 500) {
                if (consecutiveNonZero < 5) {
                    consecutiveNonZero++; // Increment consecutive non-zero count
                }
                
        } else {
            if (consecutiveNonZero > 0) {
                consecutiveNonZero--;
            }
           
            
        }
        // Check if five consecutive non-zero distances occurred
        if (consecutiveNonZero == 5) {
            // Call the function to turn LED on
            if (securityOn) {
                camera('1');
            }
            // Reset the counter after invoking the function
            //consecutiveNonZero = 0;
        } else if(consecutiveNonZero == 0) {
            camera('0');
        }
        
        Thread::wait(200);
        //sonarled = !sonarled;
    }
}


void speaker_thread(){
    // loops forever playing two notes on speaker
    while(1) {
        while(securityBreached) {
        //pc.printf("Speaker should run now!");
        mySpeaker.PlayNote(969.0,0.5,0.5);
        mySpeaker.PlayNote(800.0,0.5,0.5);
        Thread::wait(5);
        }
    Thread::wait(1000);
    }
}


int main() {

    // Initialize interrupts for touch keypad
    interrupt.fall(&fallInterrupt);
    interrupt.mode(PullUp);
    wait(0.1);

    // Initialize all pushbuttons
    activateSecurity.mode(PullDown);
    wait(0.1);
    resetPasscode.mode(PullDown);
    wait(0.1);
    enterPasscode.mode(PullDown);
    wait(0.1);

    // Setting up the sonar timer
    timer.reset();
    timer.start();
    while (echo == 2);
    timer.stop();
    correction = timer.read_us();
   //pc.printf("Approx software overhead timer delay is %d ", correction);

    // Start threads
    th_sonar.start(&sonar_thread);
    th_speaker.start(&speaker_thread);
    th_image.start(&image_data);


    // Since security is on by default
    securityled = 1;

    while(1) {
        sonar_lock.lock();
        if (securityOn) {
        // Security Mode is ON
            if (enterPasscode) { // Third button pressed
                if (verified_image) {
                    receivePasscode = true;
                    if (passcodeCompare()) {
                        
                        securityBreached = 0;
                        securityOn = false;
                        securityled = 0;
                        //imageled = 0;
                        
                        
                    } else {
                        securityBreached = 1;
                    }
                    receivePasscode = false;
                } else {
                    securityBreached = 1;
                }
                
            } else {
                //blink led
                myled = !myled; // Indicates wait mode where security is on but pb3 is not pressed
                wait(0.5);
                            
            }
        } else {
            if (resetPasscode) { // First button pressed
                receivePasscode = true;
                setNewPasscode();
                receivePasscode = false;
            } else if (activateSecurity) { // Second button pressed
                securityOn = true;
                securityled = 1;
            }
        }
    sonar_lock.unlock();
    Thread::wait(100);
    }
}
