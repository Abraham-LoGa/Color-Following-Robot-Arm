#include <C_S.h>   // Incluimos librerías para trabajar sobre el pic
#use rs232(baud=9600, xmit=pin_c6, rcv=pin_c7, bits=8)  // Llamamos librería para comunicación puerto serial
char dato;  // Variable que recibirá el paquete de datos
void mSa(){  // Función para el movimiento del servo Motor
   output_high(pin_B2);  // Habilitamos el pin
   delay_us(1000);   // Delay para giro de Servo dentro del rango de datasheet
   output_low(pin_B2);  // Deshabilitamos
   delay_us(18950);   // Delay de 2ms
}
void mSb(){
   output_high(pin_B2);
   delay_us(1200);
   output_low(pin_B2);
   delay_us(18950);
}
void mSc(){
   output_high(pin_B2);
   delay_us(1400);
   output_low(pin_B2);
   delay_us(18950);
}
void mSd(){
   output_high(pin_B2);
   delay_us(1800);
   output_low(pin_B2);
   delay_us(18950);
}
void mSe(){
   output_high(pin_B2);
   delay_us(2000);
   output_low(pin_B2);
   delay_us(18950);
}
void mSf(){
   output_high(pin_B3);
   delay_us(1000);
   output_low(pin_B3);
   delay_us(18950);
}
void mSg(){
   output_high(pin_B3);
   delay_us(1200);
   output_low(pin_B3);
   delay_us(18950);
}
void mSh(){
   output_high(pin_B3);
   delay_us(1500);
   output_low(pin_B3);
   delay_us(18950);
}
void mSi(){
   output_high(pin_B3);
   delay_us(1700);
   output_low(pin_B3);
   delay_us(18950);
}
void mSj(){
   output_high(pin_B3);
   delay_us(2000);
   output_low(pin_B3);
   delay_us(18950);
}
void main()
{
   while(TRUE)  // Bucle para realizar el programa de manera continua
   {
      //getc();
      dato=getc();  // Recibimos el dato enviado del programa python
      
        // Condicionales para el eje en X
      if(dato=='a'){  // Condicional para "dato", si corresponde a dicha igualdad hará siguiente actividad
         mSa();  // Gira el servo respecto a la función
      }
      if(dato=='b'){
         mSb();
      }
      
      if(dato=='c'){
         mSc();
      }
      if(dato=='d'){
         mSd();
      }
      if(dato=='e'){
         mSe();
      }
      
        // Condicionales para el eje en y
      if(dato=='f'){
         mSf();
      }
      if(dato=='g'){
         mSg();
      }
      
      if(dato=='h'){
         mSh();
      }
      if(dato=='i'){
         mSi();
      }
      if(dato=='j'){
         mSj();
      }
   }

}


