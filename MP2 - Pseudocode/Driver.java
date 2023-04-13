//Driver Pseudocode

import java.util.Scanner;
import java.util.concurrent.Semaphore;

public class Driver(){
	//Class wide variables
	static int[] nbg = null;
	static Semaphore s = null;
	
	void parseInput(){
		//Get input from user
		Scanner scan = new Scanner(System.in);
		String input = scan.nextLine();
		scan.close();
		
		//Parse input to int[]
		nbg = new int[3];
		String[] temp = input.split(" "); //Split by space
		try{
			for(int i = 0; i < 3; i++)
				nbg[i] = Integer.parseInt(temp[i]);
		}catch(NumberFormatException ex){}
	}
	
	public Driver(){
		//Get and parse input
		parseInput();
		
		//Prepare fittingroom macro parameters
		long timeLimit = 3000; //Time limit per color (non-preemptive)
		long fittingLimit = 5000; //Max fitting time of person
		FttingRoom fittingRoom = new FittingRoom(nbg, timeLimit, fittingLimit);
		
		//Run fitting room.
		try{
			fittingRoom.start();
			fittingRoom.join();
		}catch(InterruptedException ex){}
	}
	
	public static void main(String[] args){
		new Driver();
	}
}