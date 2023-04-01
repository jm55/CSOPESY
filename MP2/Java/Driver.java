/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */


import java.util.Scanner;
import java.util.concurrent.Semaphore;
import java.util.ArrayList;

public class Driver {
    static int[] nbg = null;
    static Semaphore s = null;

    /**
     * Read and parse inputs as an int[].
     * 
     * Sets input to nbg[] as:
     * n = nbg[0] - number of rooms
     * b = nbg[1] - number of blue persons
     * g = nbg[2] - number of green persons
     */
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
        
        System.out.println("Inputs: n=" + nbg[0] +", b=" + nbg[1] + ", g=" + nbg[2]);
    }

    /**
     * Does, well, drive the program.
     */
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
        s = new Semaphore(nbg[0]);
        String[] colors = {"Blue","Green"};
        long timeLimit = 5000; //ms
        FittingRoom fittingRoom = new FittingRoom(nbg[0], timeLimit, colors);

        //Build holders for data
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

        fittingRoom.start();
        System.out.println("Fitting Room Alive: " + fittingRoom.isAlive());

        BluePersons.addAll(GreenPersons);
        for(int b = 0; b < BluePersons.size(); b++)
            BluePersons.get(b).start();

        try{
            for(int b = 0; b < BluePersons.size(); b++)
                BluePersons.get(b).join();
            fittingRoom.join();
        }catch(InterruptedException ex){
            System.out.println("Encountered error while joining thread(s).\n" + ex.getLocalizedMessage());
        }

        System.out.println("Fitting Room Closed!");
    }
    public static void main(String[] args){
        new Driver();
    }
}