/**
 * CSOPESY - Process Scheduling
 * 
 * de Veyra, Escalona, Naval, Villavicencio
 */


import java.util.Scanner;
import java.util.concurrent.Semaphore;

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
        //Build FittingRoom
        long timeLimit = 3000; //ms
        long fittingLimit = 5000;
        FittingRoom fittingRoom = new FittingRoom(nbg, timeLimit, fittingLimit);

        fittingRoom.start();
        
        try{
            fittingRoom.join();
        }catch(InterruptedException ex){
            System.out.println(ex.getLocalizedMessage());
        }finally{
            System.exit(0);
        }
    }
    public static void main(String[] args){
        new Driver();
    }
}