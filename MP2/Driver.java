import java.util.Scanner;
import java.util.concurrent.Semaphore;

import java.util.ArrayList;

public class Driver {
    static int[] nbg = null;
    public void parseInput(){
        Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();
        scan.close();

        nbg = new int[3];
        String[] temp = input.split(" ");
        try{
            for(int i = 0; i < 3; i++)
                nbg[i] = Integer.parseInt(temp[i]);
        }catch(NumberFormatException ex){
            System.out.println("Error parsing inputs!\nExiting...");
            System.exit(1);
        }
        
        System.out.print("Inputs: n=" + nbg[0] +", b=" + nbg[1] + ", g=" + nbg[2]);
    }
    public Driver(){
        //Get input
        parseInput();
        /**
         * Contents of nbg:
         * nbg[0] = n - number of rooms
         * nbg[1] = b - number of blue persons
         * nbg[2] = g - number of green persons
         */

        //Build semaphores
        Semaphore s = new Semaphore(nbg[0]);
        FittingRoom fittingRoom = new FittingRoom(nbg[0], 10000);

        int idCounter = 1;
        ArrayList<Person> BluePersons = new ArrayList<Person>();
        ArrayList<Person> GreenPersons = new ArrayList<Person>();

        for(int b = 0; b < nbg[1]; b++){
            BluePersons.add(new Person(idCounter, "Blue", s, fittingRoom));
            idCounter++;
        }
        for(int g = 0; g < nbg[2]; g++){
            GreenPersons.add(new Person(idCounter, "Green", s, fittingRoom));
            idCounter++;
        }

        /**
         * @TODO: 
         * 1. What order/arrangement should it be? 
         *      How about rand(0-1) where 0-0.5 is "Blue" and >0.5-1.0 is "Green"
         */
    }
    public static void main(String[] args){
        new Driver();
    }
}