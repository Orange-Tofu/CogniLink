// This code is another attempt to merge EEG filter with Spike Recorder
// Not tested yet. High chance of failure BE CAUTIOUS Before using.



#define EKG A0                       // we are reading from AnalogIn 0
#define BUFFER_SIZE 100              // sampling buffer size
#define SIZE_OF_COMMAND_BUFFER 30    // command buffer size
#define LENGTH_OF_MESSAGE_IMPULS 100 // length of message impuls in ms
// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

int buffersize = BUFFER_SIZE;
int head = 0; // head index for sampling circular buffer
int tail = 0; // tail index for sampling circular buffer
byte writeByte;
char commandBuffer[SIZE_OF_COMMAND_BUFFER]; // receiving command buffer
byte reading[BUFFER_SIZE];                  // Sampling buffer

int messageImpulsPin = 5;
int messageImpulseTimer = 0;

#define SAMPLE_RATE 256
#define BAUD_RATE 115200
#define INPUT_PIN A0

////This sets up serial communication values can 9600, 14400, 19200, 28800, 31250, 38400, 57600, and 115200, also 300, 600, 1200, 2400, 4800, but that's too slow for us
/// Interrupt number - very important in combination with bit rate to get accurate data
int interrupt_Number = 198; // Output Compare Registers  value = (16*10^6) / (Fs*8) - 1  set to 1999 for 1000 Hz sampling, set to 3999 for 500 Hz sampling, set to 7999 for 250Hz sampling, 199 for 10000 Hz Sampling
int numberOfChannels = 1;   // current number of channels sampling
int tempSample = 0;
int commandMode = 0; // flag for command mode. Don't send data when in command mode

void setup()
{
    Serial.begin(BAUD_RATE); // Serial communication baud rate (alt. 115200)
    delay(300);              // whait for init of serial
    Serial.println("StartUp!");
    Serial.setTimeout(2);
    pinMode(messageImpulsPin, OUTPUT);

    // TIMER SETUP- the timer interrupt allows preceise timed measurements of the reed switch
    // for mor info about configuration of arduino timers see http://arduino.cc/playground/Code/Timer1
    cli(); // stop interrupts

    // Make ADC sample faster. Change ADC clock
    // Change prescaler division factor to 16
    sbi(ADCSRA, ADPS2); // 1
    cbi(ADCSRA, ADPS1); // 0
    cbi(ADCSRA, ADPS0); // 0

    // set timer1 interrupt at 10kHz
    TCCR1A = 0;               // set entire TCCR1A register to 0
    TCCR1B = 0;               // same for TCCR1B
    TCNT1 = 0;                // initialize counter value to 0;
    OCR1A = interrupt_Number; // Output Compare Registers
    // turn on CTC mode
    TCCR1B |= (1 << WGM12);
    // Set CS11 bit for 8 prescaler
    TCCR1B |= (1 << CS11);
    // enable timer compare interrupt
    TIMSK1 |= (1 << OCIE1A);

    sei(); // allow interrupts
    // END TIMER SETUP
}

ISR(TIMER1_COMPA_vect)
{
    // Interrupt at the timing frequency you set above to measure to measure AnalogIn, and filling the buffers

    if (messageImpulseTimer > 0)
    {
        messageImpulseTimer--;
        if (messageImpulseTimer == 0)
        {
            digitalWrite(messageImpulsPin, LOW);
        }
    }

    if (commandMode != 1)
    {

        // Put samples in sampling buffer "reading". Since Arduino Mega has 10bit ADC we will split every sample to 2 bytes
        // First byte will contain 3 most significant bits and second byte will contain 7 least significat bits.
        // First bit in all byte will not be used for data but for marking begining of the frame of data (array of samples from N channels)
        // Only first byte in frame will have most significant bit set to 1

        // Sample first channel and put it into buffer
        tempSample = analogRead(INPUT_PIN);
        reading[head] = (tempSample >> 7) | 0x80; // Mark begining of the frame by setting MSB to 1
        head = head + 1;
        if (head == BUFFER_SIZE)
        {
            head = 0;
        }
        reading[head] = tempSample & 0x7F;
        head = head + 1;
        if (head == BUFFER_SIZE)
        {
            head = 0;
        }
    }
}

float EEGFilter(float input) {
	float output = input;
	{
		static float z1, z2; // filter section state
		float x = output - -0.95391350*z1 - 0.25311356*z2;
		output = 0.00735282*x + 0.01470564*z1 + 0.00735282*z2;
		z2 = z1;
		z1 = x;
	}
	{
		static float z1, z2; // filter section state
		float x = output - -1.20596630*z1 - 0.60558332*z2;
		output = 1.00000000*x + 2.00000000*z1 + 1.00000000*z2;
		z2 = z1;
		z1 = x;
	}
	{
		static float z1, z2; // filter section state
		float x = output - -1.97690645*z1 - 0.97706395*z2;
		output = 1.00000000*x + -2.00000000*z1 + 1.00000000*z2;
		z2 = z1;
		z1 = x;
	}
	{
		static float z1, z2; // filter section state
		float x = output - -1.99071687*z1 - 0.99086813*z2;
		output = 1.00000000*x + -2.00000000*z1 + 1.00000000*z2;
		z2 = z1;
		z1 = x;
	}
	return output;
}

void loop()
{

    while (head != tail && commandMode != 1) // While there are data in sampling buffer whaiting
    {
        // Calculate elapsed time
        static unsigned long past = 0;
        unsigned long present = micros();
        unsigned long interval = present - past;
        past = present;

        // Run timer
        static long timer = 0;
        timer -= interval;

        // Sample
        if (timer < 0)
        {
            timer += 1000000 / SAMPLE_RATE;
            float sensor_value = analogRead(INPUT_PIN);
            float signal = EEGFilter(sensor_value);
            Serial.println(signal);
        }
    }
}
